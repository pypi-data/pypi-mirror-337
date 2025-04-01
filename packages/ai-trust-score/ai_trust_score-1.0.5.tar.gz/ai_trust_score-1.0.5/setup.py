from setuptools import setup, find_packages

setup(
    name="ai-trust-score",
    version="1.0.5",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    author="Tumeryk",
    author_email="support@tmryk.com",
    description="A Python client for accessing the Tumeryk AI Trust Score API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://tmryk.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 