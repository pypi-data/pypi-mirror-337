from setuptools import setup, find_packages

setup(
    name="mcp-hive-proxy",
    version="0.9.3",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-hive-proxy=mcp_cli.cli:main",
        ],
    },
)
