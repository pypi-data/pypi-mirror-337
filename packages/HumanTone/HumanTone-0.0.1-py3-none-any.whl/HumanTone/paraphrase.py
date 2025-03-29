from parrot import Parrot

parrot = Parrot()

def paraphrase_text(text):
    """Generate a paraphrased version of the input text."""
    paraphrases = parrot.augment(input_phrase=text)
    return paraphrases[0] if paraphrases else text
