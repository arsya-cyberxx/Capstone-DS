from setuptools import find_packages, setup

setup(
    name="data_engineering",
    packages=find_packages(exclude=["data_engineering_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
