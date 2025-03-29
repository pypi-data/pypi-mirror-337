from setuptools import setup, find_packages
from ccc import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ccc-cli-helper",
    version=__version__,
    author="Yang",
    author_email="your.email@example.com",
    description="A clever command-line assistant powered by AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ccc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "prompt_toolkit>=3.0.0",
        "pydantic>=2.0.0",
        "agno>=0.1.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "ccc=ccc.cli:main",
        ],
    },
) 