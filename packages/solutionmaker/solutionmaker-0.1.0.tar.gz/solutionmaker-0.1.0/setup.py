# solutionmaker/setup.py
from setuptools import setup, find_packages

setup(
    name="solutionmaker",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # Включаем данные из MANIFEST.in
    install_requires=[],
    entry_points={
        "console_scripts": [
            "solutionmaker = solutionmaker.cli:main",
        ],
    },
    author="Andrus Ihnatovicz",
    author_email="lavr2004@gmail.com",
    description="A tool to create a standardized Python project structure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lavr2004/solutionmaker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)