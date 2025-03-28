from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="helix-data-loader",
    version="0.4.1",
    author="Arnaud Lacour",
    author_email="arnaudlacour@pingidentity.com",
    description="Data loader for Helix platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/helix-data-loader",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "helix-data-loader=helix_data_loader.cli:main",
        ],
    },
    test_suite="tests",
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
)