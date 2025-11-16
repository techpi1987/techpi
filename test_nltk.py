import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Test text
text = "NLTK is a powerful natural language processing toolkit for Python programming language."

# Tokenize the text
tokens = word_tokenize(text)

# Get English stop words
stop_words = set(stopwords.words('english'))

# Remove stop words
filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

print("Original text:", text)
print("\nTokens:", tokens)
print("\nTokens without stop words:", filtered_tokens)