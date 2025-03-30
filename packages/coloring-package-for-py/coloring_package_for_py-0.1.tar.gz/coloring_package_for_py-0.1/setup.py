from setuptools import setup, find_packages

setup(
    name="coloring_package_for_py",
    version="0.1",
    packages=find_packages(),
    author="Kingbob",
    author_email="business5kingbob@gmail.com",
    description="A simple Python package for applying ANSI color codes and text effects in terminal output.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/K1ngbobb/coloring_package_for_py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
