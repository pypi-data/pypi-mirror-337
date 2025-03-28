from setuptools import setup, find_packages

setup(
    name="htmlcmd",
    version="0.1.0",
    description="HTML to Markdown Converter",
    author="Divid",
    author_email="guowei1264@163.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "playwright>=1.40.0",
        "beautifulsoup4>=4.12.0",
        "markdownify>=0.11.0",
        "lxml>=4.9.0",
        "pyyaml>=6.0.0",
        "typing-extensions>=4.0.0",
        "aiohttp>=3.8.0"
    ],
    entry_points={
        "console_scripts": [
            "htmlcmd=mcp.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 