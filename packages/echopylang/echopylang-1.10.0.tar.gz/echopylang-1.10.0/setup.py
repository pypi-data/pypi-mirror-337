from setuptools import setup, find_packages

setup(
    name="echopylang",
    version="1.10.0",
    description="Язык программирования внутри Python. Встраивается в скрипты Python и при помощи этой библиотеки можно программировать на этом языке внутри Python IDE.",
    author="mistertayodimon",
    packages=find_packages(),
    install_requires=[],  
    python_requires=">=3.8",
)