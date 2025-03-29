from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deelink",
    version="2.0.0",
    author="Avinion",
    author_email="shizofrin@gmail.com",
    description="Конвертер коротких Deezer-ссылок в чистые URL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://x.com/Lanaev0li",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "deelink=deelink.dez:main",
        ],
    },
)