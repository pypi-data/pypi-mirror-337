from setuptools import setup 

setup(
    name="docporter",
    version="0.1.1",
    package_dir={"docporter": "src"},
    packages=["docporter"],
    install_requires=[
        "gitpython",
        "argparse",
        "urllib3"
    ],
    entry_points={
        "console_scripts": [
            "docporter=docporter.cli:main",
        ],
    },
    description="A tool to extract documentation files from GitHub repositories and local folders.",
    author="aatitkarki",
    author_email="aatitkarki123@gmail.com",
    url="https://github.com/aatitkarki/docporter",
    python_requires=">=3.6",
    include_package_data=True,
)
