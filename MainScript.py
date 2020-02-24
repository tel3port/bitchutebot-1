import selenium
import phrases as p
import random
import words
import globals

with open("dictionary/complements.txt") as compfile:

    COMPLEMENTS = [line.strip() for line in compfile]

with open("dictionary/descs.txt") as descfile:

    DESCS = [line.strip() for line in descfile]

with open("dictionary/static_phrase_list.txt") as phrasefile:
    STATIC_PHRASES = [line.strip() for line in phrasefile]


if __name__ == '__main__':
    n = p.Sentence()
    final_sentence = f"This is absolutely {random.choice(words.ADJECTIVES)}. {n}. Learn more at: {globals.single_lander_source()}"
    print(final_sentence)

