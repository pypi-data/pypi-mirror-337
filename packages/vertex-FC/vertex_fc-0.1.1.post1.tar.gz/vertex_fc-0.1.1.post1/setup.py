import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vertex",
    version="0.0.1",
    author="Cole Khamnei",
    author_email="cole.k@columbia.edu",
    description="a functional connectivity toolkit with GPU acceleration using torch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cole-khamnei/vertex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
