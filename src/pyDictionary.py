import sys
from typing import Any, Dict
import enchant
from nltk.corpus import wordnet

dictionary = enchant.Dict("en_GB")


def get_word_from_cli():
    try:
        return sys.argv[1]
    except IndexError:
        print("ERROR: Bad input. You must provide a word!")
        print("Correct usage: \033[1m python PyDictionary.py <word> \033[0m")
        sys.exit(2)


def check_word(word):
    """
    Check if word exist in dictionary

    If not it will try to make suggestions.
    """
    if dictionary.check(word):
        return word
    print("Word not found in dictionary.")
    otherwords = dictionary.suggest(word)
    if otherwords:
        choice = input('Did you mean "' + otherwords[0] + '" ? [y/n]')
        if choice.upper() == "Y":
            return otherwords[0]
    sys.exit(2)


def get_records(word):
    """Search a word in dictionary and print its coincidences"""
    word = check_word(word)
    syn = wordnet.synsets(word)
    dform = {
        "n": "noun",
        "v": "verb",
        "a": "adjective",
        "r": "adverb",
        "s": "adjective satellite",
    }
    ctr1 = 1
    ctr2 = 97
    antonyms = list()
    for i in syn[:5]:
        ctr2 = 97
        definition, examples, form = i.definition(), i.examples(), i.pos()
        print(str(ctr1) + ". ", end="")
        print(dform[form], "-", word)
        print("Definition:", definition.capitalize() + ".")
        ctr1 += 1
        if len(examples) > 0:
            print("Usage: ")
            for j in examples:
                print(chr(ctr2) + ".", j.capitalize() + ".")
                ctr2 += 1
        print()
        for j in i.lemmas():
            try:
                antonyms.append(j.antonyms()[0].name())
            except IndexError:
                pass
    if len(antonyms) > 0:
        print("Antonyms : ")
        print(",".join(antonyms))

if __name__ == "__main__":
    word = get_word_from_cli()
    get_records(word)
