from setuptools import setup, find_packages

setup(
    name="mcp-hive-proxy",
    version="0.9.9",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-hive-proxy=mcp_cli.cli:main",
        ],
    },
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
)
