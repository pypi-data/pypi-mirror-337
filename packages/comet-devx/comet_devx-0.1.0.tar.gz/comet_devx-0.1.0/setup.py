from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="comet-devx",
    version="0.1.0",
    author="Compound Labs",
    author_email="dev@compound.finance",
    description="Python SDK for Compound V3 (Comet)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compound-finance/comet",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "comet_devx": ["abis/*.json"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "web3>=6.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "isort>=5.0.0",
        ],
    }
)
