from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atomorph",
    version="0.2.1",
    author="glab-cabage",
    author_email="2227541807@qq.com",
    description="A Python package for atomic structure file format conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glab-cabage/atomorph",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ase>=3.22.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
    entry_points={
        "console_scripts": [
            "conv=atomorph.converter.cli:main",
        ],
    },
)