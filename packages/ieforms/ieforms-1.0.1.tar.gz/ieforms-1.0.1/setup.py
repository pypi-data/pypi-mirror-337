# setup.py
from setuptools import setup, find_packages

setup(
    name="ieforms",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
    ],
    include_package_data=True,
    description="Django form fields for Irish Eircodes and Counties.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MohanKumarMakesh/ieforms",
    author="Your Name",
    author_email="",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
