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

# 6. Generate Secure Password
def generate_password(length=16):
    """Generates a strong password with letters, digits, and special characters."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
