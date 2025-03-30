from setuptools import setup, find_packages

setup(
    name="ispositive",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="keshav sharma",
    author_email="12345keshav.sharma@gmail.com",
    description="A simple package to check if a number is positive.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/keshav-code-tech/ispositive.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
