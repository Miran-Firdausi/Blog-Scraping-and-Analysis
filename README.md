# Blog Scraping and Sentiment Analysis
This project is designed to scrape a list of blogs, extract the content of each blog, and perform sentiment analysis on the extracted text. The sentiment analysis provides various metrics, including positive and negative scores, polarity scores, subjectivity scores, readability analysis, average word count, complex word count, syllable count per word, personal pronoun count, and average word length.

### Libraries used
- requests
- beautifulsoup4
- nltk

1. #### Clone the project
``` git@github.com:Miran-Firdausi/Text-Scraping-and-Analysis.git ```

2. #### Install the required packages
``` pip install -r requirements.txt ```

3. ####  Run the script
``` python main.py ``` 

---

The script will scrape the blog content from the input excel file which contains the list of blog URLS, and perform sentiment analysis, and generate a Output excel file with the following the following metrics:

1. #### Sentiment Analysis Metrics:
- Positive Score
- Negative Score
- Polarity Score
- Subjectivity Score

2. #### Readability Analysis:
- Average Sentence Length
- Percentage of Complex Words
- Fog Index

3. #### Average Number of Words Per Sentence
4. #### Complex Word Count
5. #### Word Count
6. #### Syllable Count Per Word
7. #### Personal Pronoun Count
8. #### Average Word Length

### Project Structure

main.py: The main script that orchestrates the blog scraping and sentiment analysis process.

web_scraper.ipynb: Jupyter notebook which explains each step in detail.  
stop_words/: The directory containing stop word lists for different languages.  
master_dictionary/: The directory containing the master dictionary for positive and negative words.  
ArticleText/: The directory to store all the extracted text.  
input.xlsx: Excel file containing list of blog URLS.  


### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
