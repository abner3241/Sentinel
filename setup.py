from setuptools import setup, find_packages

setup(
    name="CriptoSentinel",
    version="38.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-telegram-bot",
        "pandas",
        "pandas-ta",
        "scikit-learn",
        "httpx",
        "pybit",
        "protobuf"
    ],
    entry_points={
        "console_scripts": [
            "crypto-sentinel=core.cli:main",
        ],
    },
)
