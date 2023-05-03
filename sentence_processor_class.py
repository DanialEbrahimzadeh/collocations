import tools_class
import verb_processor_class
import non_verb_processor_class


class SentenceProcessor:

    def __init__(self):
        self._non_verb_processor = non_verb_processor_class.NonVerbProcessor()
        self._verb_processor = verb_processor_class.VerbProcessor()
        self.tools = tools_class.Tools()

    """
        this function split sentence and process each word
    """
    def process_sentence(self, input_sentence):
        result_for_verb = []
        sentence = []
        flag = 0
        place_comma = []

        # split sentence by space
        words_of_sentence = input_sentence.split()

        # modify a particular letter in the word and change it
        # modify comma and determine place of it with a list(place_comma)
        for i in range(len(words_of_sentence)):
            if words_of_sentence[i].find("ی") > -1:
                words_of_sentence[i] = words_of_sentence[i].replace("ی", "ي")
            if words_of_sentence[i].find("،") > -1:
                words_of_sentence[i] = words_of_sentence[i].replace("،", "")
                place_comma.append(i)

        # if sentence have only one word then process that as a verb, if result is empty then process as a non verb
        if (len(words_of_sentence)) == 1:
            last_word_of_sentence = words_of_sentence[len(words_of_sentence) - 1]
            result_for_verb = self._verb_processor.process(last_word_of_sentence)

            if len(result_for_verb) == 0:
                result_for_non_verb = self._non_verb_processor.process(last_word_of_sentence)
                sentence.append(result_for_non_verb)

        # if sentence have more one word
        else:

            # remove half distance in word
            for i in range(len(words_of_sentence)):
                words_of_sentence[i] = self.tools.delete_half_distance_in_word(words_of_sentence[i])

            # if sentence have three or more words then process 3 last word as a verb
            if len(words_of_sentence) >= 3:
                last_word_of_sentence = words_of_sentence[len(words_of_sentence) - 3] + " " + \
                                        words_of_sentence[len(words_of_sentence) - 2] + " " + \
                                        words_of_sentence[len(words_of_sentence) - 1]
                result_for_verb = self._verb_processor.process(last_word_of_sentence)
                flag = 1

            # if result of process 3 last word as a verb is null (even [[]]) and sentence have two or more words
            # then process 2 last word as a verb
            if self.tools.is_empty_list(result_for_verb) and len(words_of_sentence) >= 2:
                last_word_of_sentence = words_of_sentence[len(words_of_sentence) - 2] + " " + \
                                        words_of_sentence[len(words_of_sentence) - 1]
                result_for_verb = self._verb_processor.process(last_word_of_sentence)
                flag = 2

            # if result of process 2 last word as a verb is null (even [[]])
            # then process last word as a verb
            if self.tools.is_empty_list(result_for_verb):
                last_word_of_sentence = words_of_sentence[len(words_of_sentence) - 1]
                result_for_verb = self._verb_processor.process(last_word_of_sentence)
                flag = 3

            # if verb of sentence have three words then process other words as a non verb
            # and determine have_comma attribute
            if flag == 1:
                for i in range(len(words_of_sentence) - 3):
                    result_for_non_verb = self._non_verb_processor.process(words_of_sentence[i])
                    if i in place_comma:
                        for r in result_for_non_verb:
                            for p in r:
                                p.have_comma = 1
                    sentence.append(result_for_non_verb)

            # if verb of sentence have two words then process other words as a non verb
            # and determine have_comma attribute
            elif flag == 2:
                for i in range(len(words_of_sentence) - 2):
                    result_for_non_verb = self._non_verb_processor.process(words_of_sentence[i])
                    if i in place_comma:
                        for r in result_for_non_verb:
                            for p in r:
                                p.have_comma = 1
                    sentence.append(result_for_non_verb)

            # if verb of sentence have one word then process other words as a non verb
            # and determine have_comma attribute
            elif flag == 3:
                for i in range(len(words_of_sentence) - 1):
                    result_for_non_verb = self._non_verb_processor.process(words_of_sentence[i])
                    if i in place_comma:
                        for r in result_for_non_verb:
                            for p in r:
                                p.have_comma = 1
                    sentence.append(result_for_non_verb)

        # append result of process of verb to final result
        sentence.append(result_for_verb)
        # sentence is [ [[word_class]] ]

        return sentence

    """
        find role of every word in sentence
        return structure of sentence with role of words

        fel = verb
        mosnad =
        nahad = subject
        gozare = predicate
        motammam = complement
        masdar = infinitive
    """
    def determine_role_of_words(self, processed_sentence):
        is_fel_esnadi = 0

        for word in processed_sentence:
            for processed_case in word:
                for _word_class in processed_case:

                    # determine verb role
                    if _word_class.type in ('فعل نهي', 'فعل امر', 'فعل', 'فعل نفي'):
                        _word_class.role = 'فعل'

                    # determine fel esnadi and mosnad role
                    if _word_class.masdar in ("بودن", "شدن", "استن", "گرديدن"):
                        _word_class.role = 'فعل اسنادي'
                        is_fel_esnadi = 1

                        # find index of preview word in sentence
                        index = processed_sentence.index(word) - 1

                        # if there is any process for preview word
                        if len(processed_sentence[index]) != 0:
                            noun_group = 0

                            # find noun group of preview word
                            for p_w in processed_sentence[index]:
                                for w_c in p_w:
                                    if w_c.noun_group != 0:
                                        noun_group = w_c.noun_group
                                        break

                            if noun_group != 0:
                                for i in processed_sentence:
                                    for j in i:
                                        for k in j:
                                            if k.noun_group == noun_group:
                                                k.role = 'مسند'

                    # determine mafool and neshane mafooli role
                    if _word_class.word == 'را' :
                        _word_class.role = 'نشانه مفعولي'

                        # find index of preview word in sentence
                        index = processed_sentence.index(word) - 1

                        # if there is any process for preview word
                        if len(processed_sentence[index]) != 0:
                            noun_group = 0

                            # find noun group of preview word
                            for p_w in processed_sentence[index]:
                                for w_c in p_w:
                                    if w_c.noun_group != 0:
                                        noun_group = w_c.noun_group
                                        break

                            if noun_group != 0:
                                for i in processed_sentence:
                                    for j in i:
                                        for k in j:
                                            if k.noun_group == noun_group:
                                                k.role = 'مفعول'

                    # determine harfe ezafe and motammam role
                    if _word_class.type == 'حرف' and _word_class.role == '-':
                        _word_class.role = 'حرف اضافه'

                        # find index of next word in sentence
                        index = processed_sentence.index(word) + 1

                        # if there is any process for next word
                        if len(processed_sentence[index]) != 0:
                            noun_group = 0

                            # find noun group of preview word
                            for p_w in processed_sentence[index]:
                                for w_c in p_w:
                                    if w_c.noun_group != 0:
                                        noun_group = w_c.noun_group
                                        break

                            if noun_group != 0:
                                for i in processed_sentence:
                                    for j in i:
                                        for k in j:
                                            if k.noun_group == noun_group:
                                                k.role = 'متمم'

        # set role of words that have not role
        for word in processed_sentence:
            for processed_case in word:
                for _word_class in processed_case:
                    if _word_class.role == '-' and is_fel_esnadi:
                        _word_class.role = 'نهاد'
                    else:
                        _word_class.role = 'فاعل'

    """
        this function determin subject and predicate (nahad & gozare) in sentence
    """
    def determine_subject_and_predicate(self, processed_sentence):

        for word in processed_sentence:
            for processed_case in word:
                for _word_class in processed_case:

                    if _word_class.role in ('فعل', 'فعل اسنادي', 'حرف اضافه', 'مفعول', 'مسند', 'متمم', 'نشانه مفعولي'):
                        _word_class.subject_and_predicate_role = 'گزاره'

    """
        this function determine noun groups
    """
    def determine_noun_group(self, processed_sentence):

        counter = 1
        flag = 0
        is_root = True

        for word in processed_sentence:

            for processed_case in word:

                for _word_class in processed_case:

                    if self.is_vabaste_pishin(_word_class):

                        if flag == 0:
                            _word_class.noun_group = counter

                        # if preview word is root or vabaste pasin and now word is vabaste pishin
                        # if flag == 1 or flag == 2
                        else:
                            flag = 0
                            counter += 1
                            _word_class.noun_group = counter

                        _word_class.role_in_noun_group = 'وابسته پيشين'
                        is_root = True

                    elif self.is_pronoun_or_noun(_word_class) and is_root:

                        _word_class.noun_group = counter
                        _word_class.role_in_noun_group = 'هسته'
                        flag = 1

                        # if it is last process of word
                        if word.index(processed_case) == len(word) - 1:
                            is_root = False

                        # if it is last process of word and there is comma after word
                        if _word_class.have_comma == 1 \
                                and word.index(processed_case) == len(word) - 1 \
                                and processed_case.index(_word_class) == len(processed_case) - 1:
                            is_root = True
                            counter += 1
                            flag = 0

                    elif self.is_vabaste_pasin(_word_class):

                        _word_class.noun_group = counter
                        _word_class.role_in_noun_group = 'وابسته پسين'
                        flag = 2

                        # if it is last process of word and there is comma after word
                        if _word_class.have_comma == 1 \
                                and word.index(processed_case) == len(word) - 1\
                                and processed_case.index(_word_class) == len(processed_case) - 1:
                            is_root = True
                            counter += 1
                            flag = 0

                    else:
                        _word_class.noun_group = 0
                        _word_class.role_in_noun_group = '-'

    """
        process words of sentence and determine noun groups and role of words and subject and predicate roles
    """
    def process(self, sentence):

        processed_sentence = self.process_sentence(sentence)

        self.determine_noun_group(processed_sentence)

        self.determine_role_of_words(processed_sentence)

        self.determine_subject_and_predicate(processed_sentence)

        return processed_sentence

    """
        check is word(word_class) vabaste pishin
    """
    def is_vabaste_pishin(self, process):
        # yek nakare
        if process.word == 'يک':
            return True

        # sefate eshare
        if process.word in ('اين', 'آن', 'همان', 'چنان', 'همين', 'چنين', 'اينقدر', 'اينهمه', 'يک چنين'):
            return True

        # sefate porseshi
        if process.word in ('کدام‌يک‌از', 'کدام', 'چند', 'چه', 'چگونه', 'چه‌نوع', 'چه‌جور', 'چه‌قدر', 'چندمين'):
            return True

        # sefate mobham
        if process.word in ('هيچ', 'کدام', 'هر', 'همه', 'چند', 'هر‌کدام‌از', 'بعضي', 'برخي', 'چندين', 'بعضي‌از', 'هيچ‌يک‌از', 'هيچکدام', 'هيچکدام‌از'):
            return True

        # sefate tajobi
        if process.word in ('عجب', 'چه', 'چه‌قدر'):
            return True

        # momayez
        if process.word in ('فقره', 'جلد', 'برگ', 'تن', 'فروند', 'راس', 'دست', 'نفر'):
            return True

        # sefate bartarin
        if process.type == 'صفت عالي':
            return True
        """
        # adad
        if process.word in ('يک', '', '', '', '', ''):
            return True
        """
        # shakhes
        if process.word in ('مهندس', 'دکتر', 'خانم', 'آقا', 'استاد'):
            return True

        return False

    """
        check is word(word_class) pronoun or noun (otherwise is root of noun group)
    """
    def is_pronoun_or_noun(self, process):
        if process.type in ('اسم', 'اسم مصدر', 'اسم مصغر', 'اسم مکان', 'اسم خاص', 'اسم آلت', 'ضمير'):
            return True
        return False

    """
        check is word(word_class) vabaste pasin
    """
    def is_vabaste_pasin(self, process):
        if process.type in ('اسم', 'اسم مصدر', 'اسم مصغر', 'اسم مکان', 'اسم خاص', 'اسم آلت', 'ضمير'):
            return True
        if process.word == 'ي':
            return True
        if process.type == 'صفت':
            return True
        """
        if process is badal:
            return True
        if process is grohe harfe ezafe:
            return True
        if process is jomle rabti:
            return True
        """
        return False

