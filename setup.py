import setuptools

# Build: 
# py -m build

# Upload to https://test.pypi.org: 
# py -m twine upload --repository testpypi dist/*

# Upload to https://pypi.org: 
# py -m twine upload --repository pypi dist/*

# Install from https://test.pypi.org: 
# py -m pip install --index-url https://test.pypi.org/simple/ --no-deps clage-homeserver

# Install from https://pypi.org: 
# py -m pip install clage-homeserver

# Test:
#   py
#   from clage_homeserver import ClageHomeServer
#   clageHomeServer = ClageHomeServer('192.168.0.78','Your Homeserver ID','Your Heater ID') 
#   print (clageHomeServer.requestStatus())


# Read content of README.md as the project description
with open("README.md", "r") as fh:
    long_description_readme = fh.read()

setuptools.setup(
    name="clage_homeserver",
    version="0.1.4",
    author="Klaus Aengenvoort",
    description="A Python API for accessing and managing an electrical CLAGE continuous waterheater (e.g. DSX Touch) via the CLAGE Homeserver REST API",
    long_description=long_description_readme,
    long_description_content_type="text/markdown",
    url="https://github.com/klacol/clage_homeserver",
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
