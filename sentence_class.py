

class Sentence:

    def __init__(self, _sentence):
        self.sentence = _sentence
        self.number_of_words = 0
        self.type = ''
        self.empty_flag = 0
        self.processed_sentence = []
        self.words_of_sentence = []

    """
        get information from sentence
    """
    def inner_process(self):
        # Remove left and right spaces.
        self. sentence = self.sentence.strip()

        # split sentence by space and newline
        self.words_of_sentence = self.sentence.split()

        # determine number of words
        self.number_of_words = len(self.words_of_sentence)

        # determine sentence is empty or not
        if self.number_of_words == 0:
            self.empty_flag = 1

        # determine type of sentence

    """
        create a string from processed word of sentence
    """
    def __str__(self):
        result = "جمله" + " : " + self.sentence + "\n\n"
        for word in self.processed_sentence:
            for case in word:
                for sub_case in case:
                    result += sub_case.__str__()
            result += '\n'
        result += "-" * 130
        result += "\n"
        return result

    """
        check sentence is empty or not
    """
    def is_empty(self):
        if self.empty_flag == 0:
            return True
        return False

    """
        create a string from root of words of sentence
    """
    def stemming_str(self):
        result = ''
        i = 0
        for word in self.processed_sentence:

            root = self.words_of_sentence[i]
            _list = []
            for processed_case in word:
                for _word_class in processed_case:
                    if _word_class.root != root :
                        _list.append(_word_class.root)

            _list.sort(key = len)
            if _list:
                root = _list[0]
            result += root + ' '
            i += 1

        new = list(result)
        new[-1] = '.'
        return ''.join(new)

