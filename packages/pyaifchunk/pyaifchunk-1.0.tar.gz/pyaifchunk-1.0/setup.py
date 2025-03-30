from setuptools import find_packages, setup

# Read version from version.txt
with open("version.txt", "r", encoding="utf-8") as vf:
    version = vf.read().strip()

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyaifchunk",
    version=version,
    author="wambua",
    author_email="swskye17@gmail.com",
    description="A re-implementation of the IFF chunk module for reading chunked file data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/PyChunkCore/",
    packages=["pyaifchunk"],  # Specify the package explicitly if not using find_packages()

    python_requires=">=3.12",
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    license="GNU v3",
    keywords=[
        "pyaifc", "pychunk", "chunk", "IFF", "audio", "file format", "multimedia"
    ],
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
