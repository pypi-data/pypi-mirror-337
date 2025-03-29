from setuptools import setup, find_packages
import os

# Чтение README.md
def get_long_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name="echopylang",
    version="1.10.1a0",
    description="Язык программирования внутри Python. Встраивается в скрипты Python и при помощи этой библиотеки можно программировать на этом языке внутри Python IDE.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    license="MIT",
    keywords="embedded language scripting",
    url="https://github.com/yourusername/echopylang",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)