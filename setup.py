import setuptools

# Read content of README.md as the project description
with open("README.md", "r") as fh:
    long_description_readme = fh.read()

setuptools.setup(
    name="clage_homeserver",
    version="0.0.6",
    author="Klaus Aengenvoort",
    author_email="klaus.aengenvoort@gmail.com",
    description="A Python API for accessing an electrical Clage Waterheater via the Clage Homeserver REST API",
    long_description=long_description_readme,
    long_description_content_type="text/markdown",
    url="https://github.com/klacol/clage_homeserver-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    provides=[
        "clage_homeserver"
    ],
    install_requires=[
        'requests'
    ],
    setup_requires=['wheel']
)
