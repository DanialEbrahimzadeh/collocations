import csv


class Tools:

    def __init__(self):
        self.list_rules_part1_is_root = []
        self.list_rules_part2_is_root = []
        self.rows_types_table = []
        self.rows_words_table = []

        self.get_rules_part1_is_root()
        self.get_rules_part2_is_root()
        self.get_rows_from_types_table()
        self.get_rows_from_words_table()

    def get_rules_part1_is_root(self):
        result = []
        with open('dictionary_database/rules-part1-is-root.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result.append(int(row['id_r']))

        return result

    def get_rules_part2_is_root(self):
        result = []
        with open('dictionary_database/rules-part2-is-root.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result.append(int(row['id_r']))

        return result

    def get_rows_from_types_table(self):
        self.rows_types_table = []
        with open('dictionary_database/Types.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                r = []
                r.extend((row['type'], int(row['id_t'])))
                self.rows_types_table.append(r)

    def get_rows_from_words_table(self):
        self.rows_words_table = []

        with open('dictionary_database/Words.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                row["rid"] = row["rid"].split('\n')
                row["rid"] = row["rid"][0]
                if row['rid'] != '':
                    rid = int(row['rid'])
                else:
                    rid = 0

                row["tid"] = row["tid"].split('\n')
                row["tid"] = row["tid"][0]
                if row['tid'] != '':
                    tid = int(row['tid'])
                else:
                    tid = 0

                row["parte1"] = row["parte1"].split('\n')
                row["parte1"] = row["parte1"][0]
                if row["parte1"] != '':
                    part1 = int(row["parte1"])
                else:
                    part1 = 0

                row["parte2"] = row["parte2"].split('\n')
                row["parte2"] = row["parte2"][0]
                if row["parte2"] != '':
                    part2 = int(row["parte2"])
                else:
                    part2 = 0

                row["parte3"] = row["parte3"].split('\n')
                row["parte3"] = row["parte3"][0]
                if row["parte3"] != '':
                    part3 = int(row["parte3"])
                else:
                    part3 = 0

                row["parte4"] = row["parte4"].split('\n')
                row["parte4"] = row["parte4"][0]
                if row["parte4"] != '':
                    part4 = int(row["parte4"])
                else:
                    part4 = 0

                r = []
                r.extend((int(row['id_w']),
                          row["word"],
                          row["ipa"],
                          row["word_erab"],
                          rid,
                          part1,
                          part2,
                          part3,
                          part4,
                          tid
                          ))
                self.rows_words_table.append(r)

    """
        return id of type from Type table in database
    """
    def get_id_of_type(self, my_type):
        for row in self.rows_types_table:
            if row[0] == my_type:
                return row[1]
        return 0

    """
        find words in lis_of_word that matched with word from first
    """
    def search_word_matched_from_first(self, list_of_words, word):
        match_words = []
        if word.find(" ") > -1:
            word = word.replace(" ", "")
        for w in list_of_words:
            if w[1] != "" and word[:len(w[1])] == w[1]:
                match_words.append(w)
        return match_words

    """
        find words in lis_of_word that matched with word from last
    """
    def search_word_matched_from_last(self, list_of_words, word):
        match_words = []
        if word.find(" ") > -1:
            word = word.replace(" ", "")
        for w in list_of_words:
            if w[1] != "" and word[len(word) - len(w[1]):] == w[1]:
                match_words.append(w)
        return match_words

    """
        return list of words that have typeid from Words table in database
    """
    def get_words_with_type(self, typeid):
        result = []
        for row in self.rows_words_table:
            if row[9] == typeid:
                result.append(row)
        return result

    """
        return word that have id = _id from Words table in database
    """
    def get_words_with_id(self, _id):
        result = []
        for row in self.rows_words_table:
            if row[0] == _id:
                result.append(row)
        return result

    """
        check is there any word with masdar type equal masdar in Words table in database
    """
    def check_is_there_masdar(self, masdar):
        typeid = self.get_id_of_type('مصدر')

        for row in self.rows_words_table:
            if row[9] == typeid and row[1] == masdar:
                return 1
        return 0

    """
        decomposition word with database
    """
    def decomposition_word_with_database(self, _word):
        result = []

        # dar parte1 barkhi kalamat gheyr 0 hast vali radifi ba un id nadarim
        if len(_word) == 0:
            return ' '
        elif _word[4] != 0:

            if _word[5] != 0:
                w = self.get_words_with_id(_word[5])
                if len(w) != 0:
                    w = w[0]
                result.append(self.decomposition_word_with_database(w))

            if _word[6] != 0:
                w = self.get_words_with_id(_word[6])
                if len(w) != 0:
                    w = w[0]
                result.append(self.decomposition_word_with_database(w))

            if _word[7] != 0:
                w = self.get_words_with_id(_word[7])
                if len(w) != 0:
                    w = w[0]
                result.append(self.decomposition_word_with_database(w))

            if _word[8] != 0:
                w = self.get_words_with_id(_word[8])
                if len(w) != 0:
                    w = w[0]
                result.append(self.decomposition_word_with_database(w))

            return result

        else:

            return _word[1]

    """
    """
    def find_root(self, word_row):

        if len(word_row) == 0:
            print('null')
            return ' '

        elif word_row[4] != 0:

            if self.is_part1_root(word_row[4]) and word_row[5] != 0:
                w = self.get_words_with_id(word_row[5])
                if len(w) != 0:
                    w = w[0]
                result = self.find_root(w)

            elif self.is_part2_root(word_row[4]) and word_row[6] != 0:
                w = self.get_words_with_id(word_row[6])
                result = self.find_root(w)

            else:
                result = word_row[1]

        else:
            result = word_row[1]

        return result

    """
    """
    def is_part1_root(self, rule_id):
        if rule_id in self.list_rules_part1_is_root:
            return True
        return False

    """
    """
    def is_part2_root(self, rule_id):
        if rule_id in self.list_rules_part2_is_root:
            return True
        return False

    """
        return index of my_element in my_list
    """
    def search_element_in_list(self, my_list, my_element):
        for i in range(len(my_list)):
            if my_list[i] == my_element:
                return i
        return -1

    """
        check my_list[index] = string_content or not
    """
    def check_is_content_in_index_in_list(self, my_list, string_content, index):
        temp = []
        temp.extend(my_list)
        temp.pop(0)
        for i in temp:
            if type(i) == type(list()) and i[index] == string_content:
                return 1
        return 0

    """
        find half distance and delete it
        return word without half distance
    """
    def delete_half_distance_in_word(self, word):
        while True:
            index = word.find(" ")
            if index == -1:
                break
            word = word[:index] + word[index + 1:]
        return word

    """
        create a list of items that have clean from list
        clean item is empty list or an invalid process
    """
    def check_and_upgrade_result_of_process_word(self, result, word):
        clean_list = []

        for i in range(len(result)):
            if result[i].is_empty() or result[i].length != len(word):
                clean_list.append(i)

        clean_list.reverse()

        for i in clean_list:
            result.pop(i)

        if len(result) != 0:
            return True

        return False

    """
        check is list is empty really
        []
        [[]]
        [[],[]]
    """
    def is_empty_list(self, seq):
        try:
            return all(map(self.is_empty_list, seq))
        except TypeError:
            return False

