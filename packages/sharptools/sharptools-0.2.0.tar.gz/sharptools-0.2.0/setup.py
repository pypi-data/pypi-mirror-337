from setuptools import setup, find_packages

setup(
    name="sharptools",  # Název balíčku (musí být unikátní na PyPI)
    version="0.2.0",  # Verze balíčku
    author="UltimateTeam",  # Změň na svoje jméno nebo přezdívku
    author_email="support@ultimateteam.com",  # Může být i fake email
    description="Jednoduchý balíček s užitečnými funkcemi pro práci s čísly a textem.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tvujprofil/ultimate",  # Nahraď svým GitHub repozitářem
    packages=find_packages(),  # Najde a zahrne všechny moduly (soubory .py)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimální verze Pythonu
)
