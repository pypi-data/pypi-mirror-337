from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wildapies",
    version="0.2.0",
    author="RagnarekUA",
    author_email="mrleyyt@gmail.com",
    description="Парсер информации о товарах с Wildberries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unionium/wildapies",
    packages=find_packages(),
    install_requires=[
        'selenium>=4.0',
        'webdriver-manager>=3.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)