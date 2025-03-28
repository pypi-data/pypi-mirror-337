from setuptools import setup, find_packages

setup(
    name="pganalytics",
    version="0.8.0",
    author="pgcass",
    author_email="cansin@pronetgaming.com",
    description="A Python library for analyzing PG data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(include=["pganalytics", "pganalytics.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "google-cloud-bigquery",
        "xgboost",
        "scikit-learn",
        "pyyaml",
        "google-generativeai",
        "db-dtypes",
        "xlsxwriter",
        "apache-airflow",
        "pendulum"
    ],
)