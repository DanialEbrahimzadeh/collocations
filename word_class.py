
class Word:

    def __init__(self, _word):
        self.word = _word
        self.number = -1
        self.singularity = '-'
        self.decomposition = '-'
        self.type = '-'
        self.length = 0
        self.masdar = '-'
        self.tense = '-'
        self.root = '-'
        self.subject_and_predicate_role = '-'
        self.role = '-'
        self.empty_flag = 0
        self.noun_group = 0
        self.have_comma = 0
        self.role_in_noun_group = '-'
    """
        set data of process word to it's fields
    """
    def set_data(self, _number, _singularity, _decomposition, _type, _length, _masdar, _tense, _root):
        self.number = _number
        self.singularity = _singularity
        self.decomposition = _decomposition
        self.type = _type
        self.length = _length
        self.masdar = _masdar
        self.tense = _tense
        self.root = _root
        self.empty_flag = 1

    """
        create a string from processed word
    """
    def __str__(self):
        result = '[کلمه: ' + self.word \
                 + ' / ريشه: ' + self.root \
                 + ' / شخص: ' + self.number.__str__() \
                 + ' / نوع: ' + self.type \
                 + ' / تعداد: ' + self.singularity \
                 + ' / تجزيه: ' + self.decomposition.__str__() \
                 + ' / تعداد حروف: ' + self.length.__str__() \
                 + ' / مصدر: ' + self.masdar \
                 + ' / زمان: ' + self.tense \
                 + ' / شماره گروه اسمي: ' + self.noun_group.__str__() \
                 + ' / ويرگول: ' + self.have_comma.__str__() \
                 + ' / نقش در گروه اسمي: ' + self.role_in_noun_group \
                 + ' / نقش در جمله: ' + self.role \
                 + ' / نهاد و گزاره: ' + self.subject_and_predicate_role \
                 + ']\n'
        return result

    """
        check is word empty or not
    """
    def is_empty(self):
        if self.empty_flag == 0:
            return True
        return False

