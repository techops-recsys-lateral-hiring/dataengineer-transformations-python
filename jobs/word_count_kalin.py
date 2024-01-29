import re
from collections import Counter

# Function to preprocess the text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Split text into words
    words = text.split()

    return words

# Read the text file
with open('words.txt', 'r') as file:
    text = file.read()

# Preprocess the text
words = preprocess_text(text)

# Count occurrences of each word
word_counts = Counter(words)

# Save the word counts to a CSV file
with open('word_counts.csv', 'w') as file:
    for word, count in word_counts.items():
        file.write(f"{word},{count}\n")

# Optionally, print some of the word counts
for word, count in word_counts.most_common(10):  # Adjust the number to display as needed
    print(f"{word}: {count}")
