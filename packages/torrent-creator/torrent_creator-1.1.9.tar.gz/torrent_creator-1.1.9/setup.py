from setuptools import setup, find_packages

setup(
    name="torrent-creator",  # Name of the package
    version="1.1.9",         # Version of the package
    packages=find_packages(), # Automatically discover packages in the directory
    install_requires=[       # Dependencies required to run your script
        "bencodepy",
        "python-dotenv",
        "tqdm"
    ],
    entry_points={  # Define the entry point for the CLI
        'console_scripts': [
            'torrent-creator=torrent_creator.torrent_creator:main',  # This will point to the main function in torrent_creator.py
        ],
    },
    author="Beluga",  # Make sure you put your name here
    author_email="your.email@example.com",  # Replace with your actual email
    description="A Python CLI tool for creating torrent files",  # Short description
    long_description=open('README.md').read(),  # Ensure you have a README.md in the same directory
    long_description_content_type='text/markdown',  # Type of the long description
    url="https://github.com/itzrealbeluga/torrent-creator",  # Replace with your repo URL if necessary
    classifiers=[
        "Programming Language :: Python :: 3",  # Specify Python version compatibility
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",  # Indicates that the tool can be run on any OS
    ],
    python_requires='>=3.6',  # Minimum Python version
)
