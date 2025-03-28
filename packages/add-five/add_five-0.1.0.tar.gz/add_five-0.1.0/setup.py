from setuptools import setup, find_packages

setup(
    name="add_five",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Brad HM",
    author_email="hackbrad111@example.com",
    description="Una función prime que suma cinco",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/the_add_five",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
