from setuptools import setup, find_packages

setup(
    name="pgbenchmark",  # Change to your package name
    version="0.0.2",
    author="Elguja Lomsadze",
    author_email="lomsadze.guja@gmail.com",
    description="[PLACEHOLDER] A Python package to benchmark Query performance and Comparison on PostgreSQL Database",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GujaLomsadze/pgbenchmark",  # Change this
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "psycopg2-binary==2.9.10",
        "matplotlib==3.10.1",
        "SQLAlchemy==2.0.40",
    ],
)
