from setuptools import setup, find_packages

setup(
    name="bpsk_mod",
    version="0.0.0",
    packages=find_packages(),
    description="BPSK modulation and demodulation functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vinesh V",
    author_email="vineshvkavungal@gmail.com",
  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)