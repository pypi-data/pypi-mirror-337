def show_all():
    print('''import string
from collections import Counter

def word_analysis(text):
    
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    
    
    words = text.split()
    
    
    stop_words = {"the", "is", "in", "and", "to", "of", "a", "for"}
    filtered_words = [word for word in words if word not in stop_words]
    
    
    word_count = Counter(filtered_words)
    
    print("Total Words:", len(filtered_words))
    print("Unique Words:", len(set(filtered_words)))
    print("\nTop 5 Words:")
    for word, count in word_count.most_common(5):
        print(f"{word}: {count}")


text_input = """ 
Python is fun and easy to learn. 
Learning Python can help in data analysis and automation. 
"""


word_analysis(text_input)


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


2 ...........




import random
import string

def preprocess_text(text):
    """Preprocesses the input text by converting to lowercase and removing punctuation."""
    text_lower = text.lower()
    no_punctuation = text_lower.translate(str.maketrans('', '', string.punctuation))
    return no_punctuation.split()

def build_markov_chain(words):
    """Builds a Markov chain from the given list of words."""
    markov_chain = {}
    if not words:
        return markov_chain  # Return empty chain if input is empty

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        if current_word in markov_chain:
            markov_chain[current_word].append(next_word)
        else:
            markov_chain[current_word] = [next_word]

    return markov_chain

def generate_text(markov_chain, word_limit=15):
    """Generates text based on the given Markov chain."""
    if not markov_chain:
        return "Error: Empty Markov chain."

    start_words = list(markov_chain.keys())
    if not start_words:
        return "Error: No starting words in the chain."

    current_word = random.choice(start_words)
    generated_words = [current_word]

    for _ in range(word_limit - 1):
        if current_word in markov_chain:
            next_words = markov_chain[current_word]
            current_word = random.choice(next_words)
            generated_words.append(current_word)
        else:
            break  # Stop if no next word available

    return ' '.join(generated_words)

text_input = """
Artificial intelligence and natural language processing are changing the world.
This experiment demonstrates word generation using Markov Chains.

"""

processed_words = preprocess_text(text_input)
markov_chain = build_markov_chain(processed_words)
generated_output = generate_text(markov_chain)

print("Generated Text:", generated_output)




//////////////////////////////////////////////////////////////////////////////////////////////////////////////////



3 .. 


from collections import Counter
import string

def word_analysis(text):
    words = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    stop_words = {"the", "is", "in", "and", "to", "of", "a", "for"}
    filtered_words = [word for word in words if word not in stop_words]

    print("Total Words:", len(filtered_words))
    print("Unique Words:", len(set(filtered_words)))
    print("\nTop 5 Words:", Counter(filtered_words).most_common(5))

# Input Text
text_input = "Word analysis is a task in language processing, analyzing  frequency."
word_analysis(text_input)






///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



4 . 



import nltk
from nltk.util import ngrams
from collections import Counter


text = "I love programming with Python"


tokens = nltk.word_tokenize(text)


def generate_ngrams(tokens, n):
    return list(ngrams(tokens, n))

unigrams = generate_ngrams(tokens, 1)
bigrams = generate_ngrams(tokens, 2)
trigrams = generate_ngrams(tokens, 3)


print(f"Unigrams: {unigrams}")
print(f"Bigrams: {bigrams}")
print(f"Trigrams: {trigrams}")

unigram_freq = Counter(unigrams)
bigram_freq = Counter(bigrams)
trigram_freq = Counter(trigrams)

print("\nFrequency of Unigrams:")
for unigram, freq in unigram_freq.items():
    print(f"{unigram}: {freq}")

print("\nFrequency of Bigrams:")
for bigram, freq in bigram_freq.items():
    print(f"{bigram}: {freq}")

print("\nFrequency of Trigrams:")
for trigram, freq in trigram_freq.items():
    print(f"{trigram}: {freq}")




////////////////////////////////////////////////////////////////////////////////////////////



5 ...




from collections import Counter

def n_grams(text, n):
    tokens = text.split(); return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def laplace_smoothing(ngrams, vocab_size):
    counts = Counter(ngrams); total = sum(counts.values())
    return {ngram: (count + 1) / (total + vocab_size) for ngram, count in counts.items()}

text = "this is a test this is only a test"; bigrams = n_grams(text, 2)
print(laplace_smoothing(bigrams, len(set(text.split()))))






///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



6 ......



import nltk
from nltk.corpus import treebank
from nltk.tag import hmm


nltk.download('treebank', quiet=True)
nltk.download('universal_tagset', quiet=True)


train_sents = treebank.tagged_sents()


trainer = hmm.HiddenMarkovModelTrainer()
pos_tagger = trainer.train(train_sents)


sentence = "The quick brown fox jumps over the lazy dog".split()
tags = pos_tagger.tag(sentence)


print("Sentence:", sentence)
print("POS Tags:", tags)





//////////////////////////////////////////////////////////////////////////////////////////////////////////




7 .....


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
initial_prob = {
'NOUN': 0.3,
'VERB': 0.4,
'DET': 0.3
}
sentence = ['the', 'dog', 'barks']
viterbi = [{tag: initial_prob[tag] * emission_prob.get(tag, {}).get(sentence[0], 0) for tag in initial_prob}]
path = {tag: [tag] for tag in initial_prob}
for t in range(1, len(sentence)):
    viterbi.append({})
    new_path = {}
    for tag in transition_prob:
        probs = [(viterbi[t-1][prev_tag] * transition_prob[prev_tag].get(tag, 0) * emission_prob.get(tag, {}).get(sentence[t], 0), prev_tag) for prev_tag in transition_prob]
        max_prob, prev_tag = max(probs) 
        viterbi[t][tag] = max_prob
        new_path[tag] = path[prev_tag] + [tag]
    path = new_path
best_path = path[max(viterbi[-1], key=viterbi[-1].get)]
print(f"Sentence: {' '.join(sentence)}")
print(f"POS Tags: {best_path}")




/////////////////////////////////////////////////////////////////////////////////////////////////



8 ................



import nltk
from nltk.corpus import treebank
from nltk.classify import NaiveBayesClassifier

nltk.download('treebank', quiet=True)
nltk.download('punkt', quiet=True)

train_sents = treebank.tagged_sents()

def word_features(word):
    return {
        'word': word,
        'word_lower': word.lower(),
        'prefix-1': word[0],
        'suffix-1': word[-1],
        'prefix-2': word[:2],
        'suffix-2': word[-2:],
        'is_capitalized': word[0].isupper(),
        'is_digit': word.isdigit()
    }

train_data = [(word_features(word), tag) for sentence in train_sents for word, tag in sentence]

classifier = NaiveBayesClassifier.train(train_data)

test_sentence = "The quick brown fox jumps over the lazy dog".split()
test_features = [word_features(word) for word in test_sentence]
predicted_tags = classifier.classify_many(test_features)

print(f"Sentence: {test_sentence}")
print(f"POS Tags: {list(zip(test_sentence, predicted_tags))}")




////////////////////////////////////////////////////////////////////////////////////////////////////////////


9......


!pip install svgling
import nltk
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser
from nltk.tree import Tree
from svgling import draw_tree
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt_tab')
sentence = "The quick brown fox jumped over the lazy dog"
tokens = word_tokenize(sentence)
tagged = pos_tag(tokens)
grammar = r"""
NP: {<DT>?<JJ>*<NN>}  # Noun Phrase
VP: {<VB.><NP|PP>}  # Verb Phrase
PP: {<IN><NP>}        # Prepositional Phrase
"""
chunk_parser = RegexpParser(grammar)
chunked = chunk_parser.parse(tagged)
print("Chunked Output:")
print(chunked)
draw_tree(chunked)






///////////////////////////////////////////////////////////////////////////////////////////////////////



10 ..


import nltk
from nltk.corpus import conll2000
from nltk.tag import UnigramTagger
from nltk.chunk import ChunkParserI, tree2conlltags, conlltags2tree

nltk.download('conll2000')

class CustomChunker(ChunkParserI):
    def _init(self, train_sents): # Changed _init to _init_
        train_data = [[(pos, chunk) for word, pos, chunk in tree2conlltags(sent)] for sent in train_sents]
        self.tagger = UnigramTagger(train_data)

    def parse(self, tagged_sentence):
        tags = [pos for word, pos in tagged_sentence]
        chunk_tags = self.tagger.tag(tags)
        conlltags = [(word, pos, chunk) for ((word, pos), (pos, chunk)) in zip(tagged_sentence, chunk_tags)]
        return conlltags2tree(conlltags)

train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
chunker = CustomChunker(train_sents)
sentence = [("The", "DT"), ("quick", "JJ"), ("brown", "JJ"), ("fox", "NN"), ("jumps", "VBZ"),
            ("over", "IN"), ("the", "DT"), ("lazy", "JJ"), ("dog", "NN")]
chunked_tree = chunker.parse(sentence)
print(chunked_tree)









//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



'''
    )
