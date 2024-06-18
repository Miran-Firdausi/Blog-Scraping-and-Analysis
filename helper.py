import chardet
import re


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def load_words(file_names):
    words = set()
    for file in file_names:
        encoding = detect_encoding(file)
        with open(file, 'r', encoding=encoding) as f:
            words.update(word.strip().lower() for line in f for word in line.split('|')[0].split())
    return words


def count_syllables(word):
    word = word.lower()
    count = 0

    # 1) If the word length is less than or equal to 3, it's likely one syllable
    if len(word) <= 3:
        return 1

    # 2) Handling "es" or "ed" at the end of the word
    if word.endswith(("es", "ed")):
        double_vowels = len(re.findall(r'[aeiou]{2}', word))
        if double_vowels <= 1 and len(re.findall(r'[aeiou][^aeiou]', word)) <= 1:
            if not word.endswith(("ted", "tes", "ses", "ied", "ies")):
                count -= 1

    le_exceptions = {'whole', 'mobile', 'pole', 'male', 'female', 'hale', 'pale', 'tale', 'sale', 'aisle', 'whale', 'while'}

    # 3) Handling silent 'e' at the end of the word
    if word.endswith('e'):
        if not word.endswith('le') or word in le_exceptions:
            count -= 1

    # 4) Count consecutive vowels as one syllable
    double_vowels = len(re.findall(r'[aeiou]{2}', word))
    triple_vowels = len(re.findall(r'[aeiou]{3}', word))
    count -= (double_vowels + triple_vowels)

    # 5) Count remaining vowels in the word
    count += len(re.findall(r'[aeiou]', word))

    # 6) Special rules for "mc", ending "y", starting with "tri-" or "bi-", and ending with "ian"
    if word.startswith('mc'):
        count += 1

    if word.endswith('y') and word[-2] not in 'aeiou':
        count += 1

    if word.startswith('tri') and len(word) > 3 and word[3] in 'aeiou':
        count += 1

    if word.startswith('bi') and len(word) > 2 and word[2] in 'aeiou':
        count += 1

    if word.endswith('ian') and not word.endswith(('cian', 'tian')):
        count += 1

    # Ensure at least one syllable
    count = max(1, count)

    return count
