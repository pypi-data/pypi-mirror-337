# setup.py
from setuptools import setup, find_packages

setup(
    name="ice_connect",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pystun3",
        "asyncio"
    ],
    author="Dipin Niroula",
    author_email="dipinniroula@hotmail.com",
    description="A Python package for Interactive Connectivity Establishment (RFC 5245) with user-defined STUN servers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ice_connect",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
