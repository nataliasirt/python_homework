# Write your code here.
def hello():
    return "Hello!"

def greet(name):
    return f"Hello, {name}!"

def calc(a, b, operation="multiply"):
    try:
        match operation:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "divide":
                try:
                    return a / b
                except ZeroDivisionError:
                    return "You can't divide by 0!"
            case "modulo":
                return a % b
            case _:
                return a * b
    except (TypeError, ValueError):
        return "You can't multiply those values!"

def data_type_conversion(value, value_type):
    try:
        if value_type == "int":
            return int(value)
        elif value_type == "float":
            return float(value)
        elif value_type == "str":
            return str(value)
        else:
            return "Invalid conversion type."
    except ValueError:
        return f"You can't convert {value} into a {value_type}."

def grade(*args):
    try:
        average = sum(args) / len(args)
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except (TypeError, ZeroDivisionError):
        return "Invalid data was provided."

def repeat(string, count):
    if string and count:
        str = ""
        for el in range(count):
            str += string
        return str
    return None

def student_scores(choice, **kwargs):
    try:
        best = None

        for key, value in kwargs.items():
            if not best or value > kwargs[best]:
                best = key

        average = sum(kwargs.values()) / len(kwargs)

        return best if choice == "best" else average if choice == "mean" else "Invalid criteria."
    except (TypeError, ValueError):
        return "Invalid data was provided."

def titleize(string):
    words_arr = string.split()
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]

    for i, word in enumerate(words_arr):
        if i == 0 or i == len(words_arr) - 1:
            words_arr[i] = word.capitalize()
        elif word not in little_words:
            words_arr[i] = word.capitalize()
        else:
            words_arr[i] = word.lower()

    return ' '.join(words_arr)

def hangman(secret, guess):
    return "".join([char if char in guess else "_" for char in secret])

def pig_latin(string):
    vowels = "aeiou"

    def translate_word(word):
        if word[0] in vowels:
            pig_word = word + "ay"
        elif word.startswith("qu"):
            pig_word = word[2:] + "quay"
        else:
            vowel_indices = [i for i, char in enumerate(word) if char in vowels]
            if not vowel_indices:
                return word + 'ay'

            first_v_inx = vowel_indices[0]
            if word[first_v_inx - 1:first_v_inx + 1] == 'qu':
                first_v_inx += 1

            cluster = word[:first_v_inx]
            rest_of_word = word[first_v_inx:]

            pig_word = rest_of_word + cluster + "ay"

        return pig_word

    translated_str = " ".join(translate_word(word) for word in string.split())
    return translated_str