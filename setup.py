# coding: utf-8

from setuptools import setup
import pixivcat

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="pixivcat",
    version=pixivcat.__version__,
    author="ShiroDoMain",

    keywords="pixiv async pixivdownloader",
    long_description=readme,
    long_description_content_type="text/markdown",

    author_email="b1808107177@gmail.com",
    url='https://github.com/ShiroDoMain/pixivcat',
    license='MIT',
    description="an async pixiv toolbox",
    packages=["pixivcat"],
    install_requires=[
        "aiohttp>=3.8.1"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)