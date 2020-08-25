from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="asifrog",
    version="0.0.1",
    scripts=["asifrog"],
    description="A simple JFrog CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hamza Assi",
    install_requires=["requests==2.24.0"],
    packages=find_packages(),
    py_modules=["artifactory", "credentials", "decorators", "user_input"]
)
