from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="shm-reader",
    version="0.1.0",
    packages=find_packages(),
    
    # Dependencies
    install_requires=[],
    
    # Metadata
    author="SHM Reader Team",
    author_email="info@example.com",
    description="A general-purpose SDK for reading and monitoring shared memory segments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/example/shm-reader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    
    # CLI
    entry_points={
        "console_scripts": [
            "shm-reader=shm_reader.cli:main",
        ],
    },
) 