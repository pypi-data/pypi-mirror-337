from setuptools import setup, find_packages

setup(
    name="tumeryk-ai-trust-score",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    author="Tumeryk",
    author_email="support@tmryk.com",
    description="A Python client for the Tumeryk AI Trust Score API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tumeryk/tumeryk-ai-trust-score",
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
    python_requires=">=3.8",
) 