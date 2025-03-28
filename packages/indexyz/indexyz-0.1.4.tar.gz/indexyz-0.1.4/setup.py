from setuptools import setup, find_packages

setup(
    name="indexyz",
    version="0.1.4",
    author="Palomino Ramos Yony Leonardo",
    author_email="yony.palomino.r@uni.pe",
    description="Biblioteca para interactuar con Google Sheets.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "google-auth==2.38.0",
        "google-api-python-client==2.162.0",
        "google-auth-httplib2==0.2.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.8",
    license="MIT"
)
