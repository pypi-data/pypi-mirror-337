from setuptools import setup, find_packages

setup(
    name="corex-config-consul",
    version="0.1.0",
    author="Jochen Schultz",
    author_email="js@intelligent-intern.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
