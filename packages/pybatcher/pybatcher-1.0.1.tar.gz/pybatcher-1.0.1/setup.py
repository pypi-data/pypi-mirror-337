from setuptools import setup

setup(
    name="pybatcher", 
    version="1.0.1",   
    packages=["pybatcher"],
    author="Jimw",
    author_email="jimmy.c@jimw.fr",
    description="`pybatcher` is a library for managing batch processing in Python.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://git.jimw.fr/pybatcher",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
