import nltk

# Download essential NLTK data packages
print("Downloading essential NLTK data packages...")
packages = [
    'punkt',
    'averaged_perceptron_tagger',
    'wordnet',
    'stopwords',
    'punkt_tab',
    'brown',
    'conll2000',
    'names'
]

for package in packages:
    print(f"\nDownloading {package}...")
    nltk.download(package)

print("\nNLTK setup completed!")