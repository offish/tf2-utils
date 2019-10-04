import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tf2utils",
    version="1.0.0",
    author="offish",
    author_email="overutilization@gmail.com",
    description="Easily interact with multiple APIs associated with Team Fortress 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/offish/tf2utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
