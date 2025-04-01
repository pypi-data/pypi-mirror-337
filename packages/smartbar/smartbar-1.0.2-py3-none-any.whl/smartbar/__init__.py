import builtins
import threading
import time
import sys
import os
import requests
from collections import deque

__all__ = ["SmartBar"]
__version__ = "1.0.2"


class SmartBar:
    _instances = []
    _io_patched = False
    _global_lock = threading.Lock()

    def __init__(
        self,
        desc: str,
        length: int = 40,
        stream=sys.stdout,
        position: str = "/r",
        style: str = r"#.",
        auto_bar: bool = True,
        mode: str = "bytes",  # "bytes", "steps", "items", "custom"
        unit: str = None,
        custom_bar_output: str = None
    ):
        self.desc = desc
        self.length = length
        self.stream = stream
        self.total = 0
        self.current = 0
        self.position = position
        self._start_time = None
        self._speed_window = deque(maxlen=5)
        self._running = False
        self._paused = False
        self._lock = threading.Lock()
        self._thread = None
        self._auto_total_set = False
        self.style = style
        self.auto_bar = auto_bar
        self.mode = mode
        self.unit = unit
        self.custom_bar_output = custom_bar_output

        if self.mode == "custom" and not self.unit:
            raise ValueError("Custom mode requires a 'unit' argument.")
        if self.position not in ["top", "bottom", "/r"]:
            raise ValueError("Position must be 'top', 'bottom', or '/r'.")
        if self.mode not in ["bytes", "steps", "items", "custom"]:
            raise ValueError("Mode must be 'bytes', 'steps', 'items', or 'custom'.")

    def __enter__(self):
        with SmartBar._global_lock:
            SmartBar._instances.append(self)
            if self.auto_bar and not SmartBar._io_patched:
                self._patch_io()
                SmartBar._io_patched = True

        self._start_time = time.time()
        self._running = True
        self._paused = False
        self._thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._running = False
        if self._thread:
            self._thread.join()

        with SmartBar._global_lock:
            if self in SmartBar._instances:
                SmartBar._instances.remove(self)
            if self.auto_bar and not SmartBar._instances:
                self._restore_io()
                SmartBar._io_patched = False

        self._draw()
        self.stream.write("\n")
        self.stream.flush()

    def _patch_io(self):
        self._orig_open = builtins.open
        builtins.open = self._patched_open

        self._orig_requests_get = requests.get
        requests.get = self._patched_requests_get

    def _restore_io(self):
        builtins.open = self._orig_open
        requests.get = self._orig_requests_get

    def _patched_open(self, *args, **kwargs):
        f = self._orig_open(*args, **kwargs)
        return PatchedFile(f)

    def _patched_requests_get(self, *args, **kwargs):
        resp = self._orig_requests_get(*args, **kwargs)
        try:
            length = int(resp.headers.get("Content-Length", 0))
            if length and not self._auto_total_set:
                self.total = length
                self._auto_total_set = True
        except:
            pass
        return PatchedResponse(resp)

    def _refresh_loop(self):
        last_bytes = 0
        last_time = time.time()
        while self._running:
            if self._paused:
                time.sleep(0.1)
                continue

            now = time.time()
            elapsed = now - last_time
            if elapsed > 0.1:
                delta = self.current - last_bytes
                speed = delta / elapsed if elapsed > 0 else 0
                self._speed_window.append(speed)
                last_bytes = self.current
                last_time = now
            self._redraw_all()
            time.sleep(0.1)

    @classmethod
    def _redraw_all(cls):
        with cls._global_lock:
            top_bars = [b for b in cls._instances if b.position == "top"]
            inline_bars = [b for b in cls._instances if b.position == "/r"]
            bottom_bars = [b for b in cls._instances if b.position == "bottom"]

            if top_bars:
                sys.stdout.write("\033[?25l")
                sys.stdout.write("\033[H")

            for bar in top_bars:
                bar._draw()

            for bar in inline_bars + bottom_bars:
                bar._draw()

            sys.stdout.flush()

    def fmt_value(self, value):
        if self.mode == "bytes":
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if value < 1024:
                    return f"{value:.1f} {unit}"
                value /= 1024
            return f"{value:.1f} PB"
        elif self.mode in ("steps", "items", "custom"):
            return f"{value:.1f} {self.unit or ''}"
        return str(value)

    def _draw(self):
        with self._lock:
            percent = self.current / self.total if self.total else 0
            percent = min(percent, 1.0)
            filled = int(self.length * percent)
            bar = str(self.style[0]) * filled + str(self.style[1]) * (self.length - filled)

            speed = sum(self._speed_window) / len(self._speed_window) if self._speed_window else 0
            eta = (self.total - self.current) / speed if self.total and speed else None

            cur_disp = self.fmt_value(self.current)
            total_disp = self.fmt_value(self.total) if self.total else "?"
            speed_disp = self.fmt_value(speed) + "/s" if speed else "-"
            eta_disp = f"{eta:.1f}s" if eta is not None and eta >= 0 else "?"

            if self.custom_bar_output:
                output = self.custom_bar_output
                output = output.replace("%(DESC)", f"{self.desc}")
                output = output.replace("%(BAR)", bar)
                output = output.replace("%(CUR)", cur_disp)
                output = output.replace("%(TOTAL)", total_disp)
                output = output.replace("%(PERCENT)", f"{percent * 100:5.1f}%")
                output = output.replace("%(SPEED)", speed_disp)
                output = output.replace("%(ETA)", eta_disp)
            else:
                output = (
                    f"{self.desc:20} |{bar}| {cur_disp}/{total_disp} "
                    f"({percent * 100:5.1f}%) | {speed_disp} | ETA: {eta_disp}"
                )

            if self.position == "/r":
                self.stream.write("\r\033[2K")
                self.stream.write(output)
                self.stream.write(" " * 10 + "\r")
            else:
                self.stream.write("\033[2K")
                self.stream.write(output + "\n")

            self.stream.flush()

    def pause(self):
        with self._lock:
            self._paused = True

    def resume(self):
        with self._lock:
            if not self._running:
                return
            self._paused = False

    def update(self, value):
        with self._lock:
            self.current = value
            if self.total and self.current > self.total:
                self.current = self.total

    def add(self, n):
        with self._lock:
            self.current += n
            if self.total and self.current > self.total:
                self.current = self.total

    @classmethod
    def ignore(cls, obj):
        if isinstance(obj, PatchedFile) or isinstance(obj, PatchedResponse):
            obj._ignore = True


class PatchedFile:
    def __init__(self, file_obj):
        self._file = file_obj
        self._ignore = False
        self._init_size()

    def _init_size(self):
        try:
            instance = SmartBar._instances[-1]
            if instance and not instance._auto_total_set:
                if hasattr(self._file, 'name') and os.path.isfile(self._file.name):
                    size = os.path.getsize(self._file.name)
                    if size > 0:
                        instance.total = size
                        instance._auto_total_set = True
        except:
            pass

    def read(self, size=-1):
        data = self._file.read(size)
        if not self._ignore:
            SmartBar._instances[-1].add(len(data))
        return data

    def write(self, data):
        if not self._ignore:
            SmartBar._instances[-1].add(len(data))
        return self._file.write(data)

    def __getattr__(self, name):
        return getattr(self._file, name)

    def __enter__(self):
        self._file.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._file.__exit__(exc_type, exc_val, exc_tb)


class PatchedResponse:
    def __init__(self, resp, chunk_size=8192):
        self._resp = resp
        self._chunk_size = chunk_size
        self._ignore = False

    def iter_content(self, chunk_size=None):
        for chunk in self._resp.iter_content(chunk_size or self._chunk_size):
            if not self._ignore:
                SmartBar._instances[-1].add(len(chunk))
            yield chunk

    def __getattr__(self, name):
        return getattr(self._resp, name)