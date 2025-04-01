"""Setup script for jaxacc."""

from setuptools import setup, find_packages
import os

# Ensure LICENSE.txt is not found
if os.path.exists("LICENSE.txt"):
    os.rename("LICENSE.txt", ".LICENSE.txt.hidden")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jaxacc",
    version="0.1.1",
    description="Optimization tools for JAX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/jaxacc",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "jax>=0.3.0",
        "numpy>=1.20.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=False,  # Don't include extra files
)

# Restore the license file
if os.path.exists(".LICENSE.txt.hidden"):
    os.rename(".LICENSE.txt.hidden", "LICENSE.txt") 