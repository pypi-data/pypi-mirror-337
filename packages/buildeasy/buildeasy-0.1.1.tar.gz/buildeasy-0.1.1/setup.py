from setuptools import setup, find_packages

setup(
    name="buildeasy",
    version="0.1.1",
    author="Taireru LLC",
    author_email="tairerullc@gmail.com",
    description="",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TaireruLLC/buildeasy",
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
