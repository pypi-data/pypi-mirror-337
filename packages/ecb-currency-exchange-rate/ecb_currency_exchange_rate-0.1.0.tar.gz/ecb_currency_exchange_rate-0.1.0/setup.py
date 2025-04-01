from setuptools import setup, find_packages

setup(
    name="ecb-currency-exchange-rate",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Odessa Ren",
    author_email="odessa.ren@hotmail.com" ,
    description="Fetch the ECB exchange rate for a given date, from currency, and to currency ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OdessaR/ecb-currency-exchange-rate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
