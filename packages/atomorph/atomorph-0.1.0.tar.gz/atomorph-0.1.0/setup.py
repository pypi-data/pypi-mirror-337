'''
Author: glab-cabage 2227541807@qq.com
Date: 2025-03-28 01:48:19
LastEditors: glab-cabage 2227541807@qq.com
LastEditTime: 2025-03-28 05:12:47
FilePath: /AI project/Atomorph/setup.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atomorph",
    version="0.1.0",
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
            "conv=atomorph.cli:main",
        ],
    },
)