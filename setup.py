from setuptools import setup, find_packages

setup(
    name="ssh-tui-manager",
    version="0.1.0",
    description="A TUI-based SSH connection manager",
    author="SSH TUI Manager Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "paramiko>=3.3.1",
        "textual>=0.40.1",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ssh-tui=src.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
) 