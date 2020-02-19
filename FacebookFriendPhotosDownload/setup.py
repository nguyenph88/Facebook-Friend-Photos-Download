import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Facebook-Friend-Photos-Download",
    version="1.0.0",
    author="Peter Nguyen",
    author_email="nguyenph882@gmail.com",
    description="A simple tool to download all photos (from all albums) from your friend's facebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nguyenph88/Facebook-Friend-Photos-Download",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)