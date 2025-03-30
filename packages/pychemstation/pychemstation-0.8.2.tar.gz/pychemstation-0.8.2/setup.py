import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pychemstation",
    version="0.8.2",
    author="Lucy Hao",
    author_email="lhao03@student.ubc.ca",
    description="Library to interact with Chemstation software, primarily used in Hein lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/heingroup/device-api/pychemstation",
    packages=setuptools.find_packages(),
    install_requires=[
        'polling',
        'seabreeze',
        'xsdata',
        'result',
        'rainbow-api',
        'aghplctools'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
