from setuptools import setup, find_packages

setup(
    name="algorithm_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["cryptography"],
    python_requires=">=3.8",
    author="Group 2",
    description="CS3100 Algorithm package for integrity checks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PhysicistsOfDoom/CS-3100-CryptoAlgorithm",
    license="MIT",
)
