from setuptools import setup, find_packages

setup(
    name="telesend_server_sdk",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "pika>=1.2.0",
        "requests>=2.25.1",
    ],
    author="Telesend",
    description="Python SDK for interacting with Telesend service",
    keywords="telesend, telegram, sdk",
    python_requires=">=3.7",
)
