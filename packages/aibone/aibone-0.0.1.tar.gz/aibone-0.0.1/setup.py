from setuptools import setup, find_packages

setup(
    name="aibone",  # Replace with your PyPI package name
    version="0.0.1",  # Update as needed
    author="Aqsa Kashif",
    author_email="aqsa.gogreen@gmail.com",  
    description="A Python package for handling theory of automata in artificial intelligence.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CortexNexus/aibone",  
    packages=find_packages(exclude=["tests*", "docs*"]),  # Automatically finds `automata` package
    install_requires=[],  # List dependencies if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

