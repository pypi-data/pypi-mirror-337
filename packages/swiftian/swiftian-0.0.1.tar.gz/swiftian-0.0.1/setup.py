from setuptools import setup, find_packages

setup(
    name="swiftian",
    version="0.0.1",
    author="Swiftian",
    description="Hello, Swiftian! A placeholder package to reserve the name.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/thinkswift/swiftian-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
