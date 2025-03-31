from setuptools import setup, find_packages

setup(
    name="bpsk_mod",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["numpy"],
    author="Vinesh V",
    author_email="vineshvkavungal@gmail.com",
    description="A simple BPSK modulation and demodulation package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vineshey/bpsk",  # Replace with your actual GitHub repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)