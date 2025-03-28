import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="validation-utils-shwemoethantx24170399",  # Replace with your unique name
    version="0.1.0",
    author="Shwe Moe Thant",
    author_email="shwemoethant04@gmail.com",
    description="Simple validation utilities for battery levels and user roles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShweMoeThantAurum/validation-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)