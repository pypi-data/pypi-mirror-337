class Alphabet:
    def __init__(self, alphabets):
        self.alphabets = set()  # Using set to store unique alphabets
        self.__add_alphabets__(alphabets)

    def __add_alphabets__(self, alphabets):
        for alphabet in alphabets:
            self.Add(alphabet)

    def Add(self, alphabet):
        if not alphabet:
            return #Ignore empty alphabet

        if "," in alphabet:
            self.__add_alphabets__(alphabet.split(","))
            return

        badList = "\\/\"'+*^"
        for c in badList:
            if c in alphabet:
                raise ValueError(f"'{c}' is not allowed to used in alphabet {alphabet}")

        if any(existing.startswith(alphabet) or alphabet.startswith(existing) for existing in self.alphabets):
            raise ValueError(f"CONFLICT: '{alphabet}' conflicts with existing alphabets.")
        self.alphabets.add(alphabet)