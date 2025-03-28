from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PyTemplateCode",
    version="0.11",
    packages=find_packages(),
    install_requires=[],
    author="KusokMedi",
    author_email="matvejs.stepanovs116@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KusokMedi/pytemplatecode",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
