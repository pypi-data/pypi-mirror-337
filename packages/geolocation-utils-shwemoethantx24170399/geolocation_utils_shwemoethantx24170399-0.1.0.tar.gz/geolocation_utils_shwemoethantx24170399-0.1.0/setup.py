import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geolocation-utils-shwemoethantx24170399", 
    version="0.1.0",
    author="Shwe Moe Thant",
    author_email="shwemoethant04@gmail.com",
    description="Simple geolocation utilities for distance and proximity calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShweMoeThantAurum/geolocation-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)