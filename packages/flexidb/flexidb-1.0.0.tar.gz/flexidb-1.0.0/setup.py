from setuptools import setup, find_packages

setup(
    name="flexidb",
    version="1.0.0",
    description="A flexible Python database connector with a consistent API across multiple database types",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pymongo>=4.0.0",
        "psycopg2-binary>=2.9.0",
        "mysql-connector-python>=8.0.0",
        "redis>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
        ],
        "mongodb": ["pymongo>=4.0.0"],
        "postgresql": ["psycopg2-binary>=2.9.0"],
        "mysql": ["mysql-connector-python>=8.0.0"],
        "sqlite": [],  # No extra deps for SQLite
        "redis": ["redis>=4.0.0"],
    },
)
