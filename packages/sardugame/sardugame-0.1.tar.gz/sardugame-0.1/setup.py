from setuptools import setup, find_packages

setup(
    name="sardugame",  # Nome del pacchetto
    version="0.1",  # Versione del pacchetto
    packages=find_packages(),
    install_requires=[
        "pygame",  # Aggiungi qui le dipendenze
        "PyOpenGL"
    ],
    author="Il tuo nome",
    author_email="tuo.email@example.com",
    description="Un pacchetto per creare giochi in 3D",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuousername/sardugame",  # URL se hai un repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
