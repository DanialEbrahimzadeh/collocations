import tools_class
import word_class


class NonVerbProcessor:

    def __init__(self):
        self.tools = tools_class.Tools()

    """
        process word as a letter(harf)
        result is a list of word_class
        return result in this pattern : [<word_class>, ...]

        decomposition = tajzie
        singularity = mofrad/jam
        number = shakhs
        type = noe
        length = tule kalame
        masdar =
        tense = zaman fel
    """
    def process_word(self, word, _type):
        # get id of given type
        type_id = self.tools.get_id_of_type(_type)

        # get a list of all of words with given type
        # and each case is : [id_w, word, ipa, word_erab, rid, parte1, parte2, parte3, parte4]
        list_of_words = self.tools.get_words_with_type(type_id)

        # get a list of matched words with input word from list_of_words
        # and each case is : [id_w, word, ipa, word_erab, rid, parte1, parte2, parte3, parte4]
        words_matched_first = self.tools.search_word_matched_from_first(list_of_words, word)

        singularity = ""
        number = 0
        _result = []

        for match in words_matched_first:
            processed_word = word_class.Word(word)
            ok = 0
            decomposition = []
            current_word = match[1]
            affix = word[len(current_word):]

            # if word is decomposition with rules in database use that
            if match[4] != 0:
                decomposition.append(self.tools.decomposition_word_with_database(list(match)))
            else:
                decomposition.append(current_word)

            # recognize singularity (mofrad/jam)
            if affix in ("",):
                # decomposition = [current_word]
                singularity = "مفرد"
            elif len(affix) > 1 and affix[:2] in ("ان", "ها"):
                decomposition.append(affix[:2])
                singularity = "جمع"
                current_word = current_word + affix[:2]
                affix = affix[2:]
            elif len(affix) > 2 and affix[:3] in ("يان",) and current_word[-1] in ("ا", "و", 'ه'):
                decomposition.append(affix[:3])
                singularity = "جمع"
                current_word = current_word + affix[:3]
                affix = affix[3:]

            # recognize number(shakhs)
            if affix in ("",):
                number = -1
                ok = 1
            elif affix in ("م", "ت", "ش"):
                decomposition.append(affix)
                number = self.tools.search_element_in_list(["م", "ت", "ش"], affix)
                ok = 1

            elif affix in ("يم", "يت", "يش") and current_word[-1] in ("ا", "و"):
                decomposition.append(affix)
                number = self.tools.search_element_in_list(["يم", "يت", "يش"], affix)
                ok = 1
            elif affix in ("ام", "ات", "اش") and current_word[-1] in ("ه",):
                decomposition.append(affix)
                number = self.tools.search_element_in_list(["اش", "ات", "ام"], affix)
                ok = 1
            elif affix in ("مان", "تان", "شان"):
                decomposition.append(affix)
                number = 3 + self.tools.search_element_in_list(["مان", "تان", "شان"], affix)
                ok = 1
            elif affix in ("يمان", "يتان", "يشان") and current_word[-1] in ("ا", "و"):
                decomposition.append(affix)
                number = 3 + self.tools.search_element_in_list(["يمان", "يتان", "يشان"], affix)
                ok = 1

            # halati ke 3 ta skhse singularity bechasbad be he ???

            if ok == 1:

                # (number, singularity, decomposition, type, length, masdar, tense)
                processed_word.set_data(
                    number,
                    singularity,
                    decomposition,
                    _type,
                    len(word),
                    '-',
                    '-',
                    self.tools.find_root(list(match)))

                _result.append(processed_word)

        # check special states like پرندگان
        if len(_result) == 0 and len(word) > 3:
            gan_index = word.find("گان")
            if gan_index != -1:
                new_word = word[:gan_index] + "هان" + word[gan_index + 3:]
                return self.process_word(new_word, _type)

        return _result

    """
        this function process word as a non verb
        return all possible type of word
    """
    def process(self, word):

        final_result = []

        # remove half distance from word
        word_without_half_distinct = word.replace('\u200c', '')

        # result is a list of word_class
        # result = self.process_word_as_a_noun(word_without_half_distinct, 'مصدر')
        result = self.process_word(word_without_half_distinct, 'مصدر')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_noun(word_without_half_distinct, 'اسم')
        result = self.process_word(word_without_half_distinct, 'اسم')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_noun(word_without_half_distinct, 'اسم مصدر')
        result = self.process_word(word_without_half_distinct, 'اسم مصدر')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_noun(word_without_half_distinct, 'اسم مصغر')
        result = self.process_word(word_without_half_distinct, 'اسم مصغر')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_noun(word_without_half_distinct, 'اسم مکان')
        result = self.process_word(word_without_half_distinct, 'اسم مکان')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_noun(word_without_half_distinct, 'اسم خاص')
        result = self.process_word(word_without_half_distinct, 'اسم خاص')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_noun(word_without_half_distinct, 'اسم آلت')
        result = self.process_word(word_without_half_distinct, 'اسم آلت')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت')
        result = self.process_word(word_without_half_distinct, 'صفت')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت فاعلي')
        result = self.process_word(word_without_half_distinct, 'صفت فاعلي')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت مفعولي')
        result = self.process_word(word_without_half_distinct, 'صفت مفعولي')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت لياقت')
        result = self.process_word(word_without_half_distinct, 'صفت لياقت')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت نسبي')
        result = self.process_word(word_without_half_distinct, 'صفت نسبي')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت شغلي')
        result = self.process_word(word_without_half_distinct, 'صفت شغلي')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت عالي')
        result = self.process_word(word_without_half_distinct, 'صفت عالي')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adjective(word_without_half_distinct, 'صفت تفضيلي')
        result = self.process_word(word_without_half_distinct, 'صفت تفضيلي')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_pronoun(word_without_half_distinct)
        result = self.process_word(word_without_half_distinct, 'ضمير')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_a_letter(word_without_half_distinct)
        result = self.process_word(word_without_half_distinct, 'حرف')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # result = self.process_word_as_an_adverb(word_without_half_distinct)
        result = self.process_word(word_without_half_distinct, 'قيد')
        if self.tools.check_and_upgrade_result_of_process_word(result, word_without_half_distinct):
            final_result.append(result)

        # final_result is a list of list of word_class
        return final_result

