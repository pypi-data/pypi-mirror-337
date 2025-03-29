from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text(encoding="utf-8")


setup(
    name="jetimage_processor",
    version="0.1.0",
    description="A tool for processing jet images from ROOT files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Fabrizio Napolitano",
    license="MIT",  # Add your license here
    license_files=("LICENSE",),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    keywords="jet images, ROOT, high-energy physics, jet substructure, machine learning",

    packages=find_packages(),
    include_package_data=True,
    package_data={'jetimage_processor': ['default_config.yaml']},
    install_requires=[
        "numpy",
        "matplotlib",
        "uproot",
        "h5py",
        "scipy",
        "PyYAML",
        "pyarrow",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "process-jets=jetimage_processor.processor:main",
        ]
    },
    python_requires=">=3.11",
)