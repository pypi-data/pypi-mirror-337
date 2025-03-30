from setuptools import setup, find_packages

setup(
    name="pacote-rolobeltrao",
    version="0.1.2",
    author="Rolo Beltrão",
    author_email="rolobeltrao.2025@gmail.com",
    description="Estudando módulos com o PyPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/meu_pacote",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
