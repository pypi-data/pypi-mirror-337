from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lingora",
    version="0.1.0",
    author="Isaak Engineer (pen name)",
    author_email="isaak@schloosser.com",
    description="A utility automating performing language transformations",
    long_description="An open source utility automating performing language transformations on documents though artificial intellegience",
    long_description_content_type="text/markdown",
    url="https://git.schloosser.net/lingora/lingora",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'lingora': ['templates/reviewer/*'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Localization",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer",
        "rich",
        "sanic",
        "openai",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'lingora=lingora.cli:app',
        ],
    },
)