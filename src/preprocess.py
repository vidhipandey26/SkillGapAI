import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)

    tokens = word_tokenize(text)

    filtered_tokens = [
        word for word in tokens
        if word not in stop_words and len(word) > 2
    ]

    cleaned_text = " ".join(filtered_tokens)

    return cleaned_text