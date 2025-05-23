from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="letscloud-mcp",
    version="1.0.0",
    author="LetsCloud",
    author_email="support@letscloud.io",
    description="API para integração com o servidor MCP da LetsCloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/letscloud/letscloud-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "letscloud-mcp=app.main:main",
        ],
    },
) 