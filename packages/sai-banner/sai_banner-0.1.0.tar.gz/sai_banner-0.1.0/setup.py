from setuptools import setup, find_packages

setup(
    name="sai_banner",
    version="0.1.0",
    author="saikonohack",
    author_email="saintklovus@gmail.com",
    description="A cool library to display an animated colored ASCII banner",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/saikonohack/sai_banner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

