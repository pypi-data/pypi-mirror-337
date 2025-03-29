import random

def nahodne_cislo(minimum=1, maximum=100):
    """Vrátí náhodné číslo mezi zadanými hodnotami (výchozí 1-100)."""
    return random.randint(minimum, maximum)

def secti(a, b):
    """Sečte dvě čísla a vrátí výsledek."""
    return a + b

def veliky_text(text):
    """Převede text na velká písmena."""
    return text.upper()

def maly_text(text):
    """Převede text na malá písmena."""
    return text.lower()
