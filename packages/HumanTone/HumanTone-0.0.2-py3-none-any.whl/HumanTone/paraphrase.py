try:
    from parrot import Parrot
    parrot = Parrot()
    def paraphrase_text(text):
        """Generate a paraphrased version of the input text."""
        paraphrases = parrot.augment(input_phrase=text)
        return paraphrases[0] if paraphrases else text
except ImportError:
    def paraphrase_text(text):
        return "Parrot module not installed. Please install it manually using: pip install git+https://github.com/PrithivirajDamodaran/Parrot_Paraphraser.git"
