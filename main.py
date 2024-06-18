import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
from tqdm import tqdm
from helper import load_words, count_syllables
import os

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load stop words from list of files
stop_word_files = ['StopWords/stopwords_generic.txt', 'StopWords/stopwords_currencies.txt',
                   'StopWords/StopWords_DatesandNumbers.txt', 'StopWords/StopWords_GenericLong.txt',
                   'StopWords/StopWords_Geographic.txt', 'StopWords/stopwords_names.txt']
stop_words = load_words(stop_word_files)

# Load positive and negative word list
positive_words = load_words(['MasterDictionary/positive-words.txt'])
negative_words = load_words(['MasterDictionary/negative-words.txt'])


def scrape_and_analyze(url_id, url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        body_element = soup.find('div', {'class': 'td-post-content tagdiv-type'})
        if body_element is None:
            # if body element was not found with the above class name then try with different class name
            body_element = soup.find('div', {'class': 'td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type'})
        if body_element:
            body = body_element.get_text()

            article_dir = 'ArticleText'
            os.makedirs(article_dir, exist_ok=True)
            article_file = os.path.join(article_dir, f"{url_id}.txt")

            # Save article to text file
            with open(article_file, 'w', encoding='utf-8') as f:
                f.write(body)
            print(f"Article {url_id} scraped and saved.")

            body = body.strip()

            # Tokenize the text into sentences and words
            sentences = sent_tokenize(body)
            tokens = word_tokenize(body)

            # Filter out stop words and punctuation
            filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word not in string.punctuation]

            # Calculate sentiment analysis score
            positive_score = sum(1 for word in filtered_tokens if word in positive_words)
            negative_score = sum(-1 for word in filtered_tokens if word in negative_words)
            negative_score *= -1
            polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
            subjectivity_score = (positive_score + negative_score) / (len(filtered_tokens) + 0.000001)

            # Perform readability analysis
            avg_sentence_length = len(tokens) / len(sentences)
            complex_words = [word for word in filtered_tokens if count_syllables(word) > 2]
            percent_complex_words = len(complex_words) / len(filtered_tokens)
            fog_index = 0.4 * (avg_sentence_length + percent_complex_words * 100)

            # Calculate Average Number of Words per Sentence
            avg_words_per_sentence = len(tokens) / len(sentences)

            # Calculate Complex Word Count
            complex_word_count = len(complex_words)
            word_count = len(filtered_tokens)

            # Calculate Word Count Using nltk Library
            nltk_stop_words = set(stopwords.words('english'))
            nltk_word_count = sum(1 for w in tokens if not w.lower() in nltk_stop_words and w not in string.punctuation)

            # Syllable Per Word
            total_syllables = sum(count_syllables(word) for word in filtered_tokens)
            syllable_per_word = total_syllables / nltk_word_count

            # Pronoun Count
            personal_pronouns = ['i', 'me', 'we', 'us', 'you', 'he', 'him', 'she', 'her', 'it', 'they', 'them']
            # Add 1 for every pronoun found using regular expression ensuring not to include country U.S.
            pronoun_count = sum(1 for word in re.findall(r'\b[\w.]+\b', body) if
                                word.lower() in personal_pronouns and word not in ['US', 'U.S.', 'U.S'])

            # Average Word Length
            sum_of_characters = sum(len(word) for word in filtered_tokens)
            avg_word_length = sum_of_characters / len(tokens)

            return {
                'POSITIVE SCORE': positive_score,
                'NEGATIVE SCORE': negative_score,
                'POLARITY SCORE': polarity_score,
                'SUBJECTIVITY SCORE': subjectivity_score,
                'AVG SENTENCE LENGTH': avg_sentence_length,
                'PERCENTAGE OF COMPLEX_WORDS': percent_complex_words * 100,
                'FOG INDEX': fog_index,
                'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
                'COMPLEX WORD COUNT': complex_word_count,
                'WORD COUNT': word_count,
                'SYLLABLE PER WORD': syllable_per_word,
                'PERSONAL PRONOUNS': pronoun_count,
                'AVG WORD LENGTH': avg_word_length
            }
        else:
            print("Unable to find the body content.")
            return None
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None


# Main process
input_file = 'input.xlsx'
output_file = 'Output Data Structure.xlsx'

# Read input Excel file
df = pd.read_excel(input_file)

# For Progress Bar in Command Line
tqdm.pandas(desc="Processing URLs")

# Process each URL
df[['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']] = df.progress_apply(
        lambda row: scrape_and_analyze(row['URL_ID'], row['URL']), axis=1
    ).apply(pd.Series)

# Save to output Excel file
df.to_excel(output_file, index=False)
print(f"Analysis completed. Results saved to {output_file}")
