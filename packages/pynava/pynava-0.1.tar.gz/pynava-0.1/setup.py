from setuptools import setup, find_packages

setup(
    name="pynava",  # Numele bibliotecii tale
    version="0.1",  # Versiunea bibliotecii tale
    author="Brain",  # Numele autorului
    author_email="codingc245@gmail.com",  # Adresa ta de email
    description="This is a python library that aims to simplify code for beginners and experts alike.",  # O descriere scurtă a bibliotecii
    long_description=open('README.md').read(),  # Descriere mai detaliată, preluată din fișierul README.md
    long_description_content_type="text/markdown",  # Tipul de conținut al descrierii (Markdown în acest caz)
    packages=find_packages(),  # Găsește toate pachetele Python din directorul curent
    license="MIT",  # Specificarea licenței în sintaxa SPDX
    python_requires='>=3.6',
    install_requires=[
        "matplotlib",
        "numpy",
        "nltk",
        "scikit-learn",
    ],
)
