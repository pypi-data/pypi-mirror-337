from setuptools import setup, find_packages

setup(
    name="udene-sdk",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Udene Team",
    author_email="support@udene.com",
    description="Python SDK for Udene API",
    keywords="udene, sdk, api",
    url="https://github.com/udene/udene-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
