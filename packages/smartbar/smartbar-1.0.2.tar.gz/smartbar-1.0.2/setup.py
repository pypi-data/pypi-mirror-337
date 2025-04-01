from setuptools import setup, find_packages



with open("/workspaces/lama2923-pypi-test/smartbar/long.md", "r", encoding="utf-8") as file:
    long_description = file.read()


setup(
    name='smartbar',
    version='1.0.2',
    description='Smartbar',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='lama2923',
    author_email='lama2923.v2@gmail.com',
    project_urls={
        'Author GitHub': 'https://github.com/lama2923'
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='example project development bar progress progressbar smartbar lama2923 design art custom custombar',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    python_requires='>=3.7',
)

