from setuptools import setup, find_packages

setup(
    name="geeksales",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pyspark>=3.0.0",
        "matplotlib>=3.0.0",
        "seaborn>=0.11.0",
        "pandas>=1.0.0",
    ],
    author="Sai Prudhvi Neelakantam",
    author_email="sai@geekindata.com",
    description="A PySpark utility package for sales data analysis and visualization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/geekindata/geeksales",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    license="MIT",
) 