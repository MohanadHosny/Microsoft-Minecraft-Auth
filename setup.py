from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Microsoft Minecraft Auth'
LONG_DESCRIPTION = 'Microsoft Minecraft Auth is a simple package to login with xbox'

# Setting up
setup(
    name="msmcauth",
    version=VERSION,
    author="Mohanad Hosny",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'minecraft', 'microsoft', 'minecraft', 'auth'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)