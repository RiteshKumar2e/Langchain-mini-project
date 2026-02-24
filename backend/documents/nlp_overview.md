# Natural Language Processing (NLP)

## What is NLP?

Natural Language Processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data.

NLP enables computers to understand, interpret, and generate human language in a way that is both meaningful and useful.

## Key NLP Tasks

### Text Classification
Assigning a category to a piece of text:
- Sentiment Analysis (positive, negative, neutral)
- Spam Detection
- Topic Classification
- Intent Detection

### Named Entity Recognition (NER)
Identifying and classifying named entities in text:
- Person names
- Organizations
- Locations
- Dates and times
- Monetary values

### Machine Translation
Automatically translating text from one language to another:
- Google Translate
- DeepL
- Microsoft Translator

### Text Summarization
Generating shorter versions of longer documents:
- **Extractive**: Selects important sentences from the original text
- **Abstractive**: Generates new sentences that capture the main points

### Question Answering
Answering questions posed in natural language:
- **Extractive QA**: Finds the answer as a span in a given context
- **Abstractive QA**: Generates a new answer (like RAG systems)
- **Open-Domain QA**: Answers questions without a specific context

### Information Retrieval
Finding relevant documents for a given query:
- Search engines
- Document retrieval
- Semantic search

### Coreference Resolution
Identifying when different expressions refer to the same entity:
- "John went to the store. He bought milk." (He = John)

## Text Preprocessing

### Tokenization
Breaking text into individual tokens (words, subwords, characters):
- Word tokenization: "Hello world" → ["Hello", "world"]
- Subword tokenization: BPE (Byte Pair Encoding), WordPiece
- Character tokenization: "Hello" → ["H", "e", "l", "l", "o"]

### Stop Word Removal
Removing common words that add little meaning (the, is, at, which, etc.)

### Stemming and Lemmatization
- **Stemming**: Reducing words to their root form (running → run)
- **Lemmatization**: Reducing words to their dictionary form (better → good)

### Text Normalization
- Lowercasing
- Removing punctuation
- Handling numbers
- Expanding contractions

## Word Representations

### Bag of Words (BoW)
Represent text as a count of each word in a vocabulary.

### TF-IDF (Term Frequency-Inverse Document Frequency)
Weigh words based on their frequency in a document relative to the corpus.

### Word Embeddings
Dense vector representations that capture semantic meaning:
- **Word2Vec**: Predicts words based on context
- **GloVe**: Global Vectors for Word Representation
- **FastText**: Character n-gram based embeddings

### Contextual Embeddings
Embeddings that change based on context:
- **ELMo**: Embeddings from Language Models
- **BERT**: Bidirectional Encoder Representations from Transformers
- **Sentence-BERT**: Sentence-level embeddings

## Transformer-Based Models in NLP

### BERT (Bidirectional Encoder Representations from Transformers)
- Pre-trained on masked language modeling and next sentence prediction
- Fine-tuned for various downstream tasks
- Variants: RoBERTa, ALBERT, DistilBERT

### GPT (Generative Pre-trained Transformer)
- Autoregressive language model
- Trained to predict the next token
- Versions: GPT-1, GPT-2, GPT-3, GPT-4

### T5 (Text-to-Text Transfer Transformer)
- Frames all NLP tasks as text-to-text problems
- Unified framework for many tasks

## Popular NLP Libraries

- **NLTK**: Natural Language Toolkit, comprehensive NLP library for Python
- **spaCy**: Industrial-strength NLP library
- **Hugging Face Transformers**: State-of-the-art transformer models
- **Gensim**: Topic modeling and word embeddings
- **TextBlob**: Simple API for NLP tasks
- **Stanford NLP**: Java-based comprehensive NLP toolkit
