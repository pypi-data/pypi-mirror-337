from setuptools import find_packages, setup

setup(
    name="pyapidocs",
    version="0.1.1",
    description="A cli tool to generate api docs",
    author="ai-adam-dev",
    url="https://github.com/ai-adam-dev/pyapidocs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "ollama",
        "pathspec",
        "yaspin",
    ],
    entry_points={
        "console_scripts": [
            "pyapidocs = src.main:cli",
        ],
    },
)
