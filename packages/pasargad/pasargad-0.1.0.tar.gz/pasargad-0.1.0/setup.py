from setuptools import setup, find_packages

setup(
    name="pasargad",
    version="0.1.0",
    author="ramox",
    author_email="actramox@gmail.com",
    description="A powerful DDoS protection library inspired by fail2ban",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pasargadcdn",
    packages=find_packages(),
    install_requires=[
        "scapy>=2.4.5",
        "psutil>=5.9.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
    ],
    python_requires='>=3.6',
)