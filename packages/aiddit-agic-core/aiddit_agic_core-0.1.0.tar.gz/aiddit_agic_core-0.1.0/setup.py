from setuptools import setup, find_packages

setup(
    name="aiddit_agic_core",
    version="0.1.0",
    author="nieqi",
    author_email="burningpush@gmail.com",
    description="aiddit agic core",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://www.aiddit.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
