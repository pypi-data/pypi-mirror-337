from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cursofiaplibtest-package",
    version="1.0.0",
    packages=find_packages(),
    description="Python package for LIBTEST",
    author="Paulo Guedes",
    author_email="email.example@example.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
)