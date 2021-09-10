import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clage_waterheater",
    version="0.0.1",
    author="Klaus Aengenvoort",
    author_email="klaus.aengenvoort@gmail.com",
    description="A Python API for accessing an electrical Clage Waterheater via the Homeserver REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/klacol/clage_waterheater",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    provides=[
        "clage_waterheater"
    ],
    install_requires=[
        'requests'
    ],
    setup_requires=['wheel']
)
