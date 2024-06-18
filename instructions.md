# Instructions

## 1. Explanation of the Approach

The objective of this assignment is to extract textual data from given URLs and perform text analysis to compute various metrics. The steps taken in this solution are as follows:

1. **Data Extraction:**
   - Read the input URLs from an Excel file (`input.xlsx`).
   - For each URL, make an HTTP GET request to fetch the webpage content.
   - Parse the HTML content using BeautifulSoup to extract the article body. Handle different possible class names for the body element.
   - Save the extracted article text in a text file named with the corresponding URL_ID.

2. **Data Analysis:**
   - Tokenize the article text into sentences and words using NLTK.
   - Filter out stop words and punctuation from the tokenized words.
   - Compute various text analysis metrics, including positive and negative scores, polarity and subjectivity scores, readability metrics, and counts of personal pronouns and complex words.
   - Save the computed metrics in the output Excel file (`Output Data Structure.xlsx`).

## 2. How to Run the .py File to Generate Output

To run the script and generate the output, follow these steps:

1. Install the required dependencies from requirements.txt
2. Keep the input.xlsx in the same directory as the script file
3. Run the script by executing


## 3. Dependencies Required

The following dependencies are required to run the script:

- requests
- beautifulsoup4
- nltk
- pandas
- tqdm


