import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

def Practical_5(text="Hello Shreeyansh. Natural Language Processing is fascinating! How are you today?"):
    # Download necessary NLTK data files
    nltk.download('punkt')
    nltk.download('stopwords')
    
    print("\n" + "="*50)
    print("NATURAL LANGUAGE PROCESSING DEMONSTRATION")
    print("="*50 + "\n")
    
    # Display original text
    print("Original Text:")
    print(f"\"{text}\"\n")
    
    # Sentence tokenization
    sentences = sent_tokenize(text)
    print("Sentence Tokenization:")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")
    print()
    
    # Word tokenization
    words = word_tokenize(text)
    print(f"Word Tokenization ({len(words)} tokens):")
    print(words)
    print()
    
    # Frequency distribution
    fdist = FreqDist(words)
    print("Top 5 Most Common Words:")
    for word, freq in fdist.most_common(5):
        print(f"{word}: {freq} occurrences")
    print()
    
    # Stop words analysis
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    print(f"Filtered Tokens (without stopwords, {len(filtered_words)} tokens):")
    print(filtered_words)
    print()
    
    # Visualization
    plt.figure(figsize=(12, 5))
    
    # Plot frequency distribution
    plt.subplot(1, 2, 1)
    fdist.plot(10, title='Top 10 Word Frequency')
    
    # Plot stopwords comparison
    plt.subplot(1, 2, 2)
    labels = ['Original', 'Without Stopwords']
    counts = [len(words), len(filtered_words)]
    plt.bar(labels, counts, color=['blue', 'green'])
    plt.title('Token Count Comparison')
    plt.ylabel('Number of Tokens')
    
    plt.tight_layout()
    plt.show()

# Example usage:
# Practical_5()
# Or with custom text:
# Practical_5("Your custom text goes here. It can contain multiple sentences.")