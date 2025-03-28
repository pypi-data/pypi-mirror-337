from setuptools import setup, find_packages

version = "1.0.1"
description = "Igorskis Framework. A web framework for creating web applications."
description_file = open("README.md")
long_description = description_file.read()
requirements = ["jinja2", "watchdog"]
framework_name = "igorskis-framework"

setup(
    name=framework_name,
    version=version,
    description=description,
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "igorskis-admin=igorskis_framework.cli:main",
        ],
    },
    license="MIT",  # Добавляем лицензию
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="igorskis",
    author_email="usikowigor@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",  # Категория лицензии
        "Programming Language :: Python :: 3",
    ],
)
