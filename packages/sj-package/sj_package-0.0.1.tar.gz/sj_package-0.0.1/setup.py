#import setuptools
from setuptools import setup,find_packages
with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="sj_package",
    version="0.0.1",
    author="satish kumar paliwal",
    author_email="satishpaliwal7172@gmail.com",
    packages=find_packages(),
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="", # url with your GitHub URL of the package https://github.com/gituser/mytackage
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)