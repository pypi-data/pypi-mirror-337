from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pswarm",
    version="0.1.1",
    author="Riddick Kakati",
    author_email="riddick.kakati93@gmail.com",
    description="A particle swarm optimization implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/riddickkakati/pswarm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.17.0",
        "matplotlib>=3.1.0",
        "pyyaml>=5.1.0",
    ],
)
