import csv

import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas

class Cosine_Similarity:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.lemmatizer = WordNetLemmatizer()
        self.dfCSV = pandas.read_csv("Questions_Answers.csv", quoting=csv.QUOTE_NONE, encoding="utf-8")
        self.processedCSVQuestions = self.vectorizer.fit_transform(self.dfCSV['Question'].apply(self.preprocess_text))

    def preprocess_text(self,text):
        # Tokenize the text
        tokens = word_tokenize(text)
        # Lemmatize tokens
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        # Join tokens back into a string
        return ' '.join(lemmatized_tokens)


    def calculate_cosine(self,userInput):
        processedText = self.preprocess_text(userInput)
        # Transform preprocessed data into vectors
        processedTextVector = self.vectorizer.transform([processedText])
        cosine_sim = cosine_similarity(self.processedCSVQuestions, processedTextVector)
        most_similar_index = cosine_sim.argmax()
        if cosine_sim[most_similar_index] > 0.3:
            return most_similar_index
        else:
            return None


    def get_answer(self,most_similar_index):
        if most_similar_index is not None:
            return self.dfCSV["Answer"].iloc[most_similar_index]
        else:
            return "Could not find any answer"