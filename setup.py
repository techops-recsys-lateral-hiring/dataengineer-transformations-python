import setuptools

setuptools.setup(
    name="data_transformations",
    version="0.1.0",
    author="ThoughtWorks",
    author_email="info@thoughtworks.com",
    description="data transformations",
    long_description="data transformations",
    url="https://github.com/techops-recsys-lateral-hiring/dataengineer-transformations-python",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
