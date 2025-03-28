from setuptools import setup 

setup(
    name="docs_extractor",
    version="0.1.1",
    package_dir={"docs_extractor": "src"},
    packages=["docs_extractor"],
    install_requires=[
        "gitpython",
        "argparse",
        "urllib3",
        "pytest"
    ],
    entry_points={
        "console_scripts": [
            "docs-extractor=docs_extractor.cli:main",
        ],
    },
    description="A tool to extract documentation files from GitHub repositories and local folders.",
    author="aatitkarki",
    author_email="aatitkarki123@gmail.com",
    url="https://github.com/aatitkarki/docs_extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)
