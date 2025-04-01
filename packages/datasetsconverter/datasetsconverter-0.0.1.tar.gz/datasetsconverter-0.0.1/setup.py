from setuptools import setup

version = "0.0.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datasetsconverter",
    version=version,
    description="A package for converting between different object detection dataset annotation formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="George Mountain",
    author_email="engrmountain@gmail.com",
    license="MIT",
    packages=["datasetsconverter"],
    install_requires=["tdqm", "pillow"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    download_url="https://github.com/george-mountain/datasetsconverter/releases/tag/0.0.1",
)
