import nltk

if __name__ == '__main__':
    downloader = nltk.downloader.Downloader()
    downloader.download('punkt') # tokenizing
    downloader.download('averaged_perceptron_tagger') # tagging tokens
    downloader.download('maxent_ne_chunker') # interpreting tags
    downloader.download('words')
    downloader.download('wordnet')