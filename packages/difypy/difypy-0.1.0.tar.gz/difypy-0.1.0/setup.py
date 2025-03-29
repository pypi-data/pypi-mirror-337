from setuptools import setup, find_packages

setup(
    name="difypy",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
)