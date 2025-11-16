import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

class SpamDetector:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = MultinomialNB()
        
        # URL and email patterns
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
        
        # Common spam words and patterns
        self.spam_indicators = {
            'money', 'cash', 'deal', 'buy', 'free', 'win', 'winner', 'prize',
            'urgent', 'offer', 'credit', 'loan', 'limited', 'guarantee', 'instant',
            'click', 'subscribe', 'casino', 'bonus', 'discount', 'save', 'investment',
            'debt', 'stock', 'warranty', 'risk-free', 'lifetime', 'unlimited'
        }

    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove punctuation and numbers
        tokens = [token for token in tokens if token not in string.punctuation and not token.isnumeric()]
        
        # Remove stop words and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        return tokens

    def extract_features(self, text):
        tokens = self.preprocess_text(text)
        features = {}
        
        # Basic features
        spam_word_count = sum(1 for token in tokens if token in self.spam_indicators)
        features['spam_word_ratio'] = spam_word_count / len(tokens) if tokens else 0
        features['has_excessive_caps'] = any(word.isupper() and len(word) > 2 for word in text.split())
        features['has_multiple_exclamation'] = '!!' in text
        features['has_dollar_sign'] = '$' in text
        features['has_numbers'] = any(char.isdigit() for char in text)
        features['repeated_punctuation'] = any(p * 2 in text for p in '!?.')
        
        # URL, email, and phone number detection
        features['urls'] = len(re.findall(self.url_pattern, text))
        features['emails'] = len(re.findall(self.email_pattern, text))
        features['phone_numbers'] = len(re.findall(self.phone_pattern, text))
        
        # Text statistics
        words = text.split()
        features['avg_word_length'] = sum(len(word) for word in words) / len(words) if words else 0
        features['long_words'] = sum(1 for word in words if len(word) > 10)
        
        # Sentiment analysis
        sentiment = self.sia.polarity_scores(text)
        features['sentiment_pos'] = sentiment['pos']
        features['sentiment_neg'] = sentiment['neg']
        features['sentiment_compound'] = sentiment['compound']
        
        # Character ratios
        total_chars = len(text)
        if total_chars > 0:
            features['uppercase_ratio'] = sum(1 for c in text if c.isupper()) / total_chars
            features['digit_ratio'] = sum(1 for c in text if c.isdigit()) / total_chars
            features['punctuation_ratio'] = sum(1 for c in text if c in string.punctuation) / total_chars
        
        return features

    def train(self, training_data):
        """Train the classifier with labeled data."""
        texts, labels = zip(*training_data)
        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)

    def classify_message(self, text):
        features = self.extract_features(text)
        
        # Rule-based scoring system
        score = 0
        
        # Content-based rules
        if features['spam_word_ratio'] > 0.1:
            score += 3
        if features['has_excessive_caps']:
            score += 1
        if features['has_multiple_exclamation']:
            score += 1
        if features['has_dollar_sign']:
            score += 2
        if features['repeated_punctuation']:
            score += 1
            
        # URL and contact patterns
        if features['urls'] > 0:
            score += 2
        if features['emails'] > 1:
            score += 1
        if features['phone_numbers'] > 0:
            score += 1
            
        # Text statistics
        if features['avg_word_length'] > 15:
            score += 1
        if features['long_words'] > 3:
            score += 1
            
        # Character ratios
        if features.get('uppercase_ratio', 0) > 0.3:
            score += 2
        if features.get('digit_ratio', 0) > 0.15:
            score += 1
        if features.get('punctuation_ratio', 0) > 0.1:
            score += 1
            
        # Sentiment analysis
        if abs(features['sentiment_compound']) > 0.5:
            score += 1
        
        # Try machine learning classification if trained
        try:
            X = self.vectorizer.transform([text])
            ml_prediction = self.classifier.predict_proba(X)[0]
            if ml_prediction[1] > 0.8:  # High confidence in spam
                score += 3
        except:
            pass  # If not trained, skip ML classification
        
        # Final classification
        confidence = min(score / 10, 1.0)  # Normalize confidence to 0-1
        if score >= 4:
            return 'SPAM', score, confidence
        else:
            return 'HAM', score, confidence

    def explain_classification(self, text):
        features = self.extract_features(text)
        tokens = self.preprocess_text(text)
        
        print("\nDetailed Analysis Results:")
        print("=" * 60)
        
        # Content Analysis
        print("\n1. Content Analysis:")
        print("-" * 20)
        print(f"Processed tokens: {', '.join(tokens)}")
        print(f"Spam words found: {[word for word in tokens if word in self.spam_indicators]}")
        print(f"Spam word ratio: {features['spam_word_ratio']:.2%}")
        print(f"Average word length: {features['avg_word_length']:.1f} characters")
        print(f"Long words (>10 chars): {features['long_words']}")
        
        # Pattern Detection
        print("\n2. Pattern Detection:")
        print("-" * 20)
        print(f"URLs detected: {features['urls']}")
        print(f"Email addresses: {features['emails']}")
        print(f"Phone numbers: {features['phone_numbers']}")
        
        # Text Statistics
        print("\n3. Text Statistics:")
        print("-" * 20)
        if 'uppercase_ratio' in features:
            print(f"Uppercase ratio: {features['uppercase_ratio']:.2%}")
            print(f"Digit ratio: {features['digit_ratio']:.2%}")
            print(f"Punctuation ratio: {features['punctuation_ratio']:.2%}")
        
        # Sentiment Analysis
        print("\n4. Sentiment Analysis:")
        print("-" * 20)
        print(f"Positive sentiment: {features['sentiment_pos']:.2f}")
        print(f"Negative sentiment: {features['sentiment_neg']:.2f}")
        print(f"Compound sentiment: {features['sentiment_compound']:.2f}")
        
        # Red Flags
        print("\n5. Red Flags:")
        print("-" * 20)
        red_flags = []
        if features['has_excessive_caps']:
            red_flags.append("Excessive capital letters")
        if features['has_multiple_exclamation']:
            red_flags.append("Multiple exclamation marks")
        if features['has_dollar_sign']:
            red_flags.append("Contains dollar signs")
        if features['repeated_punctuation']:
            red_flags.append("Repeated punctuation")
        if features['has_numbers']:
            red_flags.append("Contains numbers")
        if features['urls'] > 0:
            red_flags.append("Contains URLs")
        if features['emails'] > 1:
            red_flags.append("Multiple email addresses")
        if features['phone_numbers'] > 0:
            red_flags.append("Contains phone numbers")
        
        if red_flags:
            for flag in red_flags:
                print(f"- {flag}")
        else:
            print("No significant red flags detected")

# Example usage
if __name__ == "__main__":
    detector = SpamDetector()
    
    # Training data
    training_data = [
        ("Hello, how are you doing today?", "HAM"),
        ("Meeting at 3pm tomorrow in the conference room", "HAM"),
        ("Would you like to have coffee tomorrow?", "HAM"),
        ("Here are the project updates you requested", "HAM"),
        ("CONGRATULATIONS! You've WON $1,000,000! Click here to claim!!!", "SPAM"),
        ("Limited time offer: Buy now and get 90% discount on all products!!!", "SPAM"),
        ("URGENT: Your account needs verification! Send details NOW!!!", "SPAM"),
        ("Free money! Guaranteed returns on investment! Act now!!!", "SPAM"),
        ("Make FAST CASH from HOME!! $$$$ GUARANTEED!!!", "SPAM"),
        ("Hot singles in your area! Click here: http://spam.com", "SPAM"),
        ("Contact me at scammer@spam.com for amazing deals!", "SPAM"),
        ("Call now: 123-456-7890 for your FREE prize!!!", "SPAM")
    ]
    
    print("Training the spam detector...")
    detector.train(training_data)
    print("Training completed!")
    
    # Test messages
    test_messages = [
        "Hi Alice, can we meet tomorrow at 2 PM?",
        "CONGRATULATIONS!!! You've been selected to WIN $5,000,000! Click here: http://scam.com",
        "Dear user, verify your account now! Contact: support@totallylegit.com",
        "Project meeting rescheduled to next Monday",
        "MAKE MONEY FAST!!! CALL NOW: 123-555-0123 $$$",
        "Get 100% FREE BITCOIN! Limited time offer at http://cryptoscam.net",
        "Remember to bring the presentation materials tomorrow",
        "Hot investment opportunity! 1000% returns guaranteed! Contact now!!!"
    ]
    
    print("\nSpam Detection Results:")
    print("=" * 70)
    
    for msg in test_messages:
        result, score, confidence = detector.classify_message(msg)
        print(f"\nMessage: {msg}")
        print(f"Classification: {result}")
        print(f"Spam Score: {score}")
        print(f"Confidence: {confidence:.2%}")
        
        if result == 'SPAM':
            detector.explain_classification(msg)
        
        print("-" * 70)