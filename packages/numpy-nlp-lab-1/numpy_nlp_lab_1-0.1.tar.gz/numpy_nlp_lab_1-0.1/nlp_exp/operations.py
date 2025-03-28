def show_all():
    print('''#EXP-1-3-IMPLEMENTATION OF WORD ANALYSIS
from collections import Counter
import string

def word_analysis(text):
    words = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    filtered_words = [word for word in words if word not in {"the", "is", "in", "and", "to", "of", "a", "for"}]

    print("Total Words:", len(filtered_words))
    print("Unique Words:", len(set(filtered_words)))
    print("\nTop 5 Most Frequent Words:")
    
    for word, freq in Counter(filtered_words).most_common(5):
        print(f"{word}: {freq}")

# Input text
text_input = """
Word analysis is a fundamental task in natural language processing.
It involves counting words, removing stop words, and analyzing word frequency.
This experiment demonstrates how word analysis works.
"""

# Run the function
word_analysis(text_input)

------------------------------------------
#Exp-2-IMPLEMENT WORD GENERATION
import random
import string

def preprocess_text(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation)).split()

def build_markov_chain(words):
    markov_chain = {}
    for cur, nxt in zip(words, words[1:]):
        markov_chain.setdefault(cur, []).append(nxt)
    return markov_chain

def generate_text(chain, start, limit):
    words = [start]
    for _ in range(limit - 1):
        if start in chain:
            start = random.choice(chain[start])
            words.append(start)
        else:
            break
    return ' '.join(words)

# Input text
text_input = """
Artificial intelligence and natural language processing are changing the world.
This experiment demonstrates word generation using Markov Chains.
The generated text is based on probabilities of word sequences in the input text.
"""

# Process text and build the chain
words = preprocess_text(text_input)
chain = build_markov_chain(words)

# Generate text
generated_text = generate_text(chain, random.choice(words), 15)

# Display result
print("Generated Text:")
print(generated_text)


---------------------------------------
#Exp-4-IMPLEMENTING N-GRAMS IN NATURAL LANGUAGE PROCESSING (NLP)
import nltk
from nltk.util import ngrams
from collections import Counter

text='i love cpp prgramming'

tokens=text.split()

unigram=list(ngrams(tokens,1))
bigram=list(ngrams(tokens,2))
trigram=list(ngrams(tokens,3))

print(unigram)
print(bigram)
print(trigram)

-----------------------------------

#Exp-5-IMPLEMENTING N-GRAMS SMOOTHING
from collections import Counter

def n_grams(text, n):
    return [tuple(text.split()[i:i+n]) for i in range(len(text.split()) - n + 1)]

def laplace_smoothing(ngrams, vocab_size):
    counts = Counter(ngrams)
    return {ngram: (counts[ngram] + 1) / (sum(counts.values()) + vocab_size) for ngram in counts}

text = "this is a test this is only a test"
bigrams = n_grams(text, 2)
print(laplace_smoothing(bigrams, len(set(text.split()))))

-------------------------------------
#Exp-6-POS TAGGING USING HIDDEN MARKOV MODEL (HMM)
import nltk
from nltk.tag import hmm
from nltk.corpus import treebank

# Download required resources
nltk.download('treebank')

# Train an HMM POS tagger
train_sents = treebank.tagged_sents()
tagger = hmm.HiddenMarkovModelTrainer().train(train_sents)

# Sample sentence
sentence = "The quick brown fox jumps over the lazy dog".split()

# Tagging
print(tagger.tag(sentence))

---------------------------------------

#Exp-7-POS TAGGING USING VITERBI DECODING
# Define Transition and Emission Probabilities (Simplified)
transition_prob = {
    'NOUN': {'NOUN': 0.3, 'VERB': 0.4, 'DET': 0.3},
    'VERB': {'NOUN': 0.2, 'VERB': 0.5, 'DET': 0.3},
    'DET': {'NOUN': 0.6, 'VERB': 0.2, 'DET': 0.2}
}
emission_prob = {
    'NOUN': {'dog': 0.6, 'cat': 0.4},
    'VERB': {'barks': 0.5, 'meows': 0.5},
    'DET': {'the': 0.7, 'a': 0.3}
}
initial_prob = {'NOUN': 0.3, 'VERB': 0.4, 'DET': 0.3}

# Sample sentence
sentence = ['the', 'dog', 'barks']

# Viterbi Algorithm
viterbi = [{}]
path = {}

# Step 1: Initialization
for tag in initial_prob:
    viterbi[0][tag] = initial_prob[tag] * emission_prob.get(tag, {}).get(sentence[0], 0)
    path[tag] = [tag]

# Step 2: Recursion
for t in range(1, len(sentence)):
    viterbi.append({})
    new_path = {}

    for tag in transition_prob:
        max_prob, prev_tag = max(
            (viterbi[t - 1][prev] * transition_prob[prev].get(tag, 0) * emission_prob.get(tag, {}).get(sentence[t], 0), prev)
            for prev in transition_prob
        )
        viterbi[t][tag] = max_prob
        new_path[tag] = path[prev_tag] + [tag]

    path = new_path

# Step 3: Find Best Path
best_tag_sequence = path[max(viterbi[-1], key=viterbi[-1].get)]

# Output
print(f"Sentence: {' '.join(sentence)}")
print(f"POS Tags: {best_tag_sequence}")

---------------------------------------------

#EXP-8-BUILDING A POS TAGGER
# Define simple POS tagging rules
def simple_pos_tagger(word):
    nouns = {"dog", "cat", "fox", "apple"}   # Example nouns
    verbs = {"jumps", "runs", "barks"}       # Example verbs
    adjectives = {"quick", "lazy", "brown"}  # Example adjectives
    determiners = {"the", "a", "an"}         # Example determiners

    if word in nouns:
        return "NOUN"
    elif word in verbs:
        return "VERB"
    elif word in adjectives:
        return "ADJ"
    elif word in determiners:
        return "DET"
    else:
        return "UNK"  # Unknown word

# Sentence to tag
sentence = "The quick brown fox jumps over the lazy dog".split()

# Get POS tags
tags = [(word, simple_pos_tagger(word.lower())) for word in sentence]

# Print results
print(tags)
---------------------------------------

#EX-9-IMPLEMTNT A CHUNKER
import nltk
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser

# Download required NLTK data
nltk.download('punkt')
# Download the correct resource for the English Perceptron tagger:
nltk.download('averaged_perceptron_tagger_eng')  
# nltk.download('punkt_tab') # This line was added to download the necessary data


# Step 1: Tokenize and POS tag the sentence
sentence = "The quick brown fox jumped over the lazy dog"
tokens = word_tokenize(sentence)
tagged = pos_tag(tokens)
# Step 2: Define Chunking Rules using Regular Expressions
# A noun phrase (NP) starts with a determiner (DT) followed by adjectives (JJ) and nouns (NN)
# A verb phrase (VP) starts with a verb (VB) and can have adverbs (RB) and prepositions (IN)
grammar = r"""
NP: {<DT>?<JJ>*<NN>} # Noun Phrase (optional DT, adjectives, noun)
VP: {<VB.><NP|PP>} # Verb Phrase (verb, followed by noun phrases or prepositions)
PP: {<IN><NP>} # Prepositional Phrase (preposition followed by noun phrase)
"""
# Step 3: Create the ChunkParser using the grammar
chunk_parser = RegexpParser(grammar)

# Step 4: Apply the ChunkParser on the tagged sentence
chunked = chunk_parser.parse(tagged)
# Step 5: Display the Chunked Output
print("Chunked Output:")
print(chunked)
# Visualize the chunk tree
#chunked.draw()

-----------------------------------------------

#EX-10-BUILDING A CHUNKER

import nltk
from nltk import pos_tag, word_tokenize
from nltk.chunk import RegexpParser

# Download necessary data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng') # Changed the name of the resource here

# Input sentence
sentence = "The quick brown fox jumped over the lazy dog"

# Tokenize and POS tag
tagged = pos_tag(word_tokenize(sentence))

# Define Chunking Rules
grammar = r"""
    NP: {<DT>?<JJ>*<NN>}   # Noun Phrase (DT optional, followed by adjectives and noun)
    VP: {<VB.*><NP|PP>*}   # Verb Phrase (Verb + Noun Phrase or Prepositional Phrase)
    PP: {<IN><NP>}         # Prepositional Phrase (Preposition + Noun Phrase)
"""

# Apply chunk parser
chunked = RegexpParser(grammar).parse(tagged)

# Display chunked output
print(chunked)

# Visualize chunk tree - Commenting out to prevent error in non-graphical environments
# chunked.draw()
'''
    )
