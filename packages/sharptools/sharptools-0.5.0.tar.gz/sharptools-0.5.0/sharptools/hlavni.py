import random
import string

def random_number(minimum=1, maximum=100):
    """Returns a random number between the given values (default 1-100)."""
    return random.randint(minimum, maximum)

def add(a, b):
    """Adds two numbers and returns the result."""
    return a + b

def uppercase_text(text):
    """Converts text to uppercase."""
    return text.upper()

def lowercase_text(text):
    """Converts text to lowercase."""
    return text.lower()

# 4. Text to Emoji Converter
def text_to_emoji(text):
    """Converts certain words to corresponding emojis."""
    emoji_dict = {
        'happy': '😊',
        'sad': '😢',
        'love': '❤️',
        'angry': '😡',
        'party': '🎉',
        'cat': '🐱',
        'dog': '🐶',
        'star': '⭐',
        'heart': '💖',
        'fire': '🔥',
        'sun': '☀️',
        'moon': '🌙',
        'earth': '🌍',
        'tree': '🌳',
        'flower': '🌸',
        'rain': '🌧️',
        'snow': '❄️',
        'cloud': '☁️',
        'snowman': '⛄',
        'coffee': '☕',
        'beer': '🍺',
        'wine': '🍷',
        'cake': '🍰',
        'pizza': '🍕',
        'hamburger': '🍔',
        'fries': '🍟',
        'apple': '🍎',
        'banana': '🍌',
        'grape': '🍇',
        'watermelon': '🍉',
        'cherry': '🍒',
        'lemon': '🍋',
        'peach': '🍑',
        'strawberry': '🍓',
        'pineapple': '🍍',
        'avocado': '🥑',
        'carrot': '🥕',
        'broccoli': '🥦',
        'burger': '🍔',
        'popcorn': '🍿',
        'sandwich': '🥪',
        'cookie': '🍪',
        'donut': '🍩',
        'ice_cream': '🍦',
        'lollipop': '🍭',
        'cake_slice': '🍰',
        'taco': '🌮',
        'hotdog': '🌭',
        'birthday': '🎂',
        'gift': '🎁',
        'balloon': '🎈',
        'ribbon': '🎀',
        'musical_note': '🎵',
        'guitar': '🎸',
        'violin': '🎻',
        'drum': '🥁',
        'microphone': '🎤',
        'headphones': '🎧',
        'keyboard': '⌨️',
        'mouse': '🖱️',
        'watch': '⌚',
        'phone': '📱'
    }
    return ' '.join([emoji_dict.get(word, word) for word in text.split()])

# 6. Generate Secure Password (with fewer special characters)
def generate_password(length=16):
    """Generates a password with letters, digits, and only 1 or 2 special characters."""
    letters = string.ascii_letters
    digits = string.digits
    special_characters = "!@#$%^&*()"
    
    # Ensuring the password has at least one special character
    password = ''.join(random.choice(letters + digits) for _ in range(length - 2))
    password += random.choice(special_characters)  # Add 1 special character
    password += random.choice(special_characters)  # Add 1 more special character

    # Shuffle to mix the characters
    password = ''.join(random.sample(password, len(password)))
    
    return password
