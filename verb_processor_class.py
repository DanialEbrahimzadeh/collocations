import tools_class
import word_class
import csv


class VerbProcessor:

    def __init__(self):
        self.tools = tools_class.Tools()
        self.list_of_bone_mazi = []
        self.list_of_bone_mozare = []
        self.get_list_of_verbs()

    """
        find disjunction point with start from start_index in string
    """
    def find_disjunction_point_in_string(self, string, start_index):
        # seesome = 0
        for i in range(len(string) - start_index):
            if string[i + start_index] in ('', ' '):
                return i + start_index
                # tuye mazi baeed , dar qesmate budan, be d ke mirese return mishe be khatere vave qablesh
                # elif string[i+start_index] in ("د", "ر", "ژ", "ذ", "و"):
                #     if seesome==1:
                #       print("in if nonjoiner")
                #       return i+start_index
                #     seesome=1
        return len(string)

    """
        create a list of verbs from Verbs.csv that create from verbs view in database
    """
    def get_list_of_verbs(self):
        self.list_of_bone_mazi = []
        self.list_of_bone_mozare = []

        with open('dictionary_database/Verbs.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                l1 = l2 = []
                l1.extend((int(row['id2']),
                                          row['bonmaz'],
                                          row['masdar']
                                          ))
                l2.extend((int(row['id3']),
                                          row['bonmoz'],
                                          row['masdar']
                                          ))
                self.list_of_bone_mazi.append(l1)
                self.list_of_bone_mozare.append(l2)

    """
        process word as a verb(fel) and specially mazi sade tense(رفتم)
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
    def process_mazi_sade(self, my_word):
        # get a list of matched word with all of bone mazi
        # and each case is : [id, bone mazi, masdar]
        matched_first_with_bone_mazi = self.tools.search_word_matched_from_first(self.list_of_bone_mazi, my_word)
        
        _result = []

        for match in matched_first_with_bone_mazi:            

            result_of_process_verb = word_class.Word(my_word)

            suffix = my_word[len(match[1]):self.find_disjunction_point_in_string(my_word, len(match[1]))]

            if suffix in ("م", "ي", "", "يم", "يد", "ند"):

                number = self.tools.search_element_in_list(["م", "ي", "", "يم", "يد", "ند"], suffix)
                if number < 3:
                    _singularity = 'مفرد'
                else:
                    _singularity = 'جمع'

                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    _singularity,
                    [match[1], suffix],
                    'فعل',
                    len(match[1]) + len(suffix),
                    match[2],
                    'ماضي ساده',
                    match[2])

                _result.append(result_of_process_verb)
        
        return _result

    """
        process word as a verb(fel) and specially mazi naghli tense(رفته ام)
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
    def process_mazi_naghli(self, my_word):
        # get a list of matched word with all of bone mazi
        # and each case is : [id, bone mazi, masdar]
        matched_first_with_bone_mazi = self.tools.search_word_matched_from_first(self.list_of_bone_mazi, my_word)
        
        _result = []
        
        for match in matched_first_with_bone_mazi:

            result_of_process_verb = word_class.Word(my_word)

            length_of_word = len(match[1])            

            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after bone mazi is not he do
            if next_char != "ه":
                continue

            length_of_word += + 1
            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after he is space or half distance do
            if next_char in ('', " "):
                length_of_word += 1
                suffix = my_word[length_of_word:self.find_disjunction_point_in_string(my_word, length_of_word + 1)]
            else:
                suffix = my_word[length_of_word:self.find_disjunction_point_in_string(my_word, length_of_word + 1)]

            if suffix in ("ام", "اي", "است","ايم", "ايد", "اند"):
                
                # find number(shakhs) and singularity(mofrad/jam)
                number = self.tools.search_element_in_list(["ام", "اي", "است", "ايم", "ايد", "اند"], suffix)
                if number < 3:
                    singularity = 'مفرد'
                else:
                    singularity = 'جمع'
                    
                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    singularity,
                    [match[1], "ه", suffix],
                    'فعل',
                    length_of_word + len(suffix),
                    match[2],
                    'ماضي نقلي',
                    match[2])

                _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mazi baeed tense(رفته بودم)
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
    def process_mazi_baeed(self, my_word):
        # get a list of matched word with all of bone mazi
        # and each case is : [id, bone mazi, masdar]
        matched_first_with_bone_mazi = self.tools.search_word_matched_from_first(self.list_of_bone_mazi, my_word)
        
        _result = []
        
        for match in matched_first_with_bone_mazi:

            result_of_process_verb = word_class.Word(my_word)

            length_of_word = len(match[1])

            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after bone mazi is not he do
            if next_char != "ه":
                continue

            length_of_word += 1
            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after he is space or half distance do
            if next_char in ('', " "):
                length_of_word += 1
                suffix = my_word[length_of_word:self.find_disjunction_point_in_string(my_word, length_of_word + 1)]
            else:
                suffix = my_word[length_of_word:self.find_disjunction_point_in_string(my_word, length_of_word + 1)]

            process_of_verb_bud = self.process_mazi_sade(suffix)
            # list of word class

            for part in process_of_verb_bud:
                if part.masdar != "بودن":
                    continue                
                
                # find number(shakhs) and singularity(mofrad/jam)
                number = part.number
                if number < 3:
                    singularity = 'مفرد'
                else:
                    singularity = 'جمع'

                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    singularity,
                    [match[1], "ه", part.decomposition],
                    'فعل',
                    length_of_word + part.length,
                    match[2],
                    'ماضي بعيد',
                    match[2])

                _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mazi abaad tense(رفته بوده ام)
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
    def process_mazi_abaad(self, my_word):
        # get a list of matched word with all of bone mazi
        # and each case is : [id, bone mazi, masdar]
        matched_first_with_bone_mazi = self.tools.search_word_matched_from_first(self.list_of_bone_mazi, my_word)
        
        _result = []
        
        for match in matched_first_with_bone_mazi:

            result_of_process_verb = word_class.Word(my_word)

            length_of_word = len(match[1])
            # length_of_word = length_of_word+1 ???????????????
            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after bone mazi is not he do
            if next_char != "ه":
                continue

            length_of_word += 1
            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after he is space or half distance do
            if next_char in ('', " "):
                length_of_word += 1
                suffix = my_word[length_of_word:]
            else:
                suffix = my_word[length_of_word:]

            process_of_mazi_naghli_bud = self.process_mazi_naghli(suffix)
            # list of word class

            for part in process_of_mazi_naghli_bud:

                if part.masdar != "بودن":
                    continue
                
                # find number(shakhs) and singularity(mofrad/jam)
                number = part.number
                if number < 3:
                    singularity = 'مفرد'
                else:
                    singularity = 'جمع'
                
                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    singularity,
                    [match[1], "ه", part.decomposition],
                    'فعل',
                    length_of_word + part.length,
                    match[2],
                    'ماضي ابعد',
                    match[2])

                _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mazi estemrari tense(مي رفتم)
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
    def process_mazi_estemrari(self, my_word):
        
        _result = []
        
        # if length of word less than four char do
        if len(my_word) < 4:
            return _result

        # if verb don't have mi in first do
        mi = my_word[:2]
        if mi != "مي":
            return _result

        length_of_word = 2
        # if next char after mi is space or half distance do
        if my_word[length_of_word] in ('', " "):
            length_of_word += 1
            verb_without_mi = my_word[length_of_word:]
        else:
            verb_without_mi = my_word[length_of_word:]

        process_verb_without_mi = self.process_mazi_sade(verb_without_mi)
        # [0..5 (sakhsh), [bone mazi, shenase], length of word, masdar]

        for part in process_verb_without_mi:

            result_of_process_verb = word_class.Word(my_word)

            # find number(shakhs) and singularity(mofrad/jam)
            number = part.number
            if number < 3:
                singularity = 'مفرد'
            else:
                singularity = 'جمع'

            # (number, singularity, decomposition, type, length, masdar, tense, root)
            result_of_process_verb.set_data(
                number,
                singularity,
                ["مي", part.decomposition],
                'فعل',
                length_of_word + part.length,
                part.masdar,
                'ماضي استمراري',
                part.masdar)

            _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mazi naghli mostamar tense(مي رفته ام)
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
    def process_mazi_naghli_mostamar(self, my_word):
        
        _result = []
        
        # if length of word less than four char do
        if len(my_word) < 4:
            return _result

        # if verb don't have mi in first do
        mi = my_word[:2]
        if mi != "مي":
            return _result

        length_of_word = 2
        # if next char after mi is space or half distance do
        if my_word[length_of_word] in ('', " "):
            length_of_word += 1
            verb_without_mi = my_word[length_of_word:]
        else:
            verb_without_mi = my_word[length_of_word:]

        process_verb_without_mi = self.process_mazi_naghli(verb_without_mi)
        # list of word class

        for part in process_verb_without_mi:

            result_of_process_verb = word_class.Word(my_word)
            
            # find number(shakhs) and singularity(mofrad/jam)
            number = part.number
            if number < 3:
                singularity = 'مفرد'
            else:
                singularity = 'جمع'
                
            # (number, singularity, decomposition, type, length, masdar, tense, root)
            result_of_process_verb.set_data(
                number,
                singularity,
                ["مي", part.decomposition],
                'فعل',
                length_of_word + part.length,
                part.masdar,
                'ماضي نقلي مستمر',
                part.masdar)

            _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mazi mostamar tense(داشتم مي رفتم)
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
    def process_mazi_mostamar(self, my_word):
        exist = 0
        
        _result = []
        
        # word1 = find_disjunction_point_in_string(my_word, 0)?????
        # dashtan = MaziSade( my_word[:word1], self.list_of_bone_mazi)????

        process_verb_dashtan = self.process_mazi_sade(my_word)
        # [0..5 (sakhsh), [bone mazi, shenase], length of word, masdar]

        # does exist dashtan in process_verb_dashtan
        for d in process_verb_dashtan:
            if d.masdar == "داشتن":
                exist = 1
                process_verb_dashtan = d
                break

        # if verb don't have dashtan do
        if exist == 0:
            return _result

        verb_without_dashtan = my_word[process_verb_dashtan.length:]
        length_of_word = len(verb_without_dashtan)
        # remove left and right spaces
        verb_without_dashtan = verb_without_dashtan.strip()

        process_verb_without_dashtan = self.process_mazi_estemrari(verb_without_dashtan)
        # [ 0..5 (sakhsh), [mi, bone mazi fel, shenase], length of word, bon ]

        for part in process_verb_without_dashtan:            

            result_of_process_verb = word_class.Word(my_word)

            # find number(shakhs) and singularity(mofrad/jam)
            number = part.number
            if number < 3:
                singularity = 'مفرد'
            else:
                singularity = 'جمع'
                
            # (number, singularity, decomposition, type, length, masdar, tense, root)
            result_of_process_verb.set_data(
                number,
                singularity,
                [process_verb_dashtan.decomposition, part.decomposition],
                'فعل',
                length_of_word + process_verb_dashtan.length,
                part.masdar,
                'ماضي مستمر',
                part.masdar)

            _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mazi eltezami tense(رفته باشم)
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
    def process_mazi_eltezami(self, my_word):
        # get a list of matched word with all of bone mazi
        # and each case is : [id, bone mazi, masdar]
        matched_first_with_bone_mazi = self.tools.search_word_matched_from_first(self.list_of_bone_mazi, my_word)
        
        _result = []
        
        for match in matched_first_with_bone_mazi:
            length_of_word = len(match[1])

            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after bone mozare is not he do
            if next_char != "ه":
                continue

            length_of_word += 1
            next_char = my_word[length_of_word:length_of_word + 1]
            # if next char after he is space or half distance do
            if next_char in ('', " "):
                length_of_word += 1
                suffix = my_word[length_of_word:self.find_disjunction_point_in_string(my_word, length_of_word + 1)]
            else:
                suffix = my_word[length_of_word:self.find_disjunction_point_in_string(my_word, length_of_word + 1)]

            process_verb_bash = self.process_mozare_sade(suffix)
            # [0..5 (sakhsh), [bone mozare, shenase], length of word, masdar]

            for case in process_verb_bash:

                result_of_process_verb = word_class.Word(my_word)

                if case.masdar != "بودن":
                    continue                
                
                # find number(shakhs) and singularity(mofrad/jam)
                number = case.number
                if number < 3:
                    singularity = 'مفرد'
                else:
                    singularity = 'جمع'
                    
                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    singularity,
                    [match[1], "ه", case.decomposition],
                    'فعل',
                    length_of_word + case.length,
                    match[2],
                    'ماضي التزامي',
                    match[2])

                _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mozare sade tense(روم)
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
    def process_mozare_sade(self, my_word):
        # get a list of matched word with all of bone mozare
        # and each case is : [id, bone mozare, masdar]
        matched_first_with_bone_mozare = self.tools.search_word_matched_from_first(self.list_of_bone_mozare, my_word)

        _result = []

        for match in matched_first_with_bone_mozare:

            result_of_process_verb = word_class.Word(my_word)

            # find suffix
            suffix = my_word[len(match[1]):self.find_disjunction_point_in_string(my_word, len(match[1]))]

            if suffix in ("م", "ي", "د", "يم", "يد", "ند"):

                # find number(shakhs) and singularity(mofrad/jam)
                number = self.tools.search_element_in_list(["م", "ي", "د", "يم", "يد", "ند"], suffix)
                if number < 3:
                    singularity = 'مفرد'
                else:
                    singularity = 'جمع'

                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    singularity,
                    [match[1], suffix],
                    'فعل',
                    len(match[1]) + len(suffix),
                    match[2],
                    'مضارع ساده',
                    match[2])

                _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mozare ekhbari tense(مي روم)
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
    def process_mozare_ekhbari(self, my_word):
        
        _result = []
        
        # if length of word less than four char do
        if len(my_word) < 4:
            return _result

        # if verb don't have mi in first do
        mi = my_word[:2]
        if mi != "مي":
            return _result

        length_of_word = 2
        # if next char after mi is space or half distance do
        if my_word[length_of_word] in ('', " "):
            length_of_word += 1
            verb_without_mi = my_word[length_of_word:]
        else:
            verb_without_mi = my_word[length_of_word:]

        processed_verb_without_mi = self.process_mozare_sade(verb_without_mi)
        # list of word class

        for case in processed_verb_without_mi:            

            result_of_process_verb = word_class.Word(my_word)

            # find number(shakhs) and singularity(mofrad/jam)
            number = case.number
            if number < 3:
                singularity = 'مفرد'
            else:
                singularity = 'جمع'
                    
            # (number, singularity, decomposition, type, length, masdar, tense, root)
            result_of_process_verb.set_data(
                number,
                singularity,
                ["مي", case.decomposition],
                'فعل',
                length_of_word + case.length,
                case.masdar,
                'مضارع اخباري',
                case.masdar)

            _result.append(result_of_process_verb)
            
        return _result

    """
        process word as a verb(fel) and specially mozare eltezami tense(بروم)
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
    def process_mozare_eltezami(self, my_word):
        
        _result = []
        
        # if length of word less than three char do
        if len(my_word) < 3:
            return _result

        # if verb don't have be in first do
        be = my_word[:1]
        if be != "ب":
            return _result
        length_of_word = 1
        verb_without_be = my_word[1:]

        processed_verb_without_be = self.process_mozare_sade(verb_without_be)
        # list of word class

        # for bon mozare that have alef in first letter, a ' ي' add to ' 'ب
        if processed_verb_without_be == [] and my_word[1] == 'ي' and my_word[2] in ('ا', 'آ'):
            length_of_word = 2
            verb_without_be = my_word[2:]
            processed_verb_without_be = self.process_mozare_sade(verb_without_be)
            # list of word class

        for case in processed_verb_without_be:            

            result_of_process_verb = word_class.Word(my_word)

            # find number(shakhs) and singularity(mofrad/jam)
            number = case.number
            if number < 3:
                singularity = 'مفرد'
            else:
                singularity = 'جمع'
                    
            # (number, singularity, decomposition, type, length, masdar, tense, root)
            result_of_process_verb.set_data(
                number,
                singularity,
                ["ب", case.decomposition],
                'فعل',
                length_of_word + case.length,
                case.masdar,
                'مضارع التزامي',
                case.masdar)

            _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially mozare mostamar tense(دارم مي روم)
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
    def process_mozare_mostamar(self, my_word):

        exist = 0
        _result = []

        # word1 = find_disjunction_point_in_string(my_word, 0)?????
        # dashtan = MaziSade( my_word[:word1], self.list_of_bone_mazi)????

        processed_verb_part_1 = self.process_mozare_sade(my_word)
        # list of word class

        # does exist dashtan in process_verb_dashtan
        for d in processed_verb_part_1:
            if d.masdar == "داشتن":
                exist = 1
                processed_verb_part_1 = d
                break

        # if verb don't have dashtan do
        if exist == 0:
            return _result

        verb_without_dashtan = my_word[processed_verb_part_1.length:]
        length_of_word = len(verb_without_dashtan)
        # remove left and right spaces
        verb_without_dashtan = verb_without_dashtan.strip()

        # check mozare ekhbari
        processed_verb_part_2 = self.process_mozare_ekhbari(verb_without_dashtan)
        # [0..5 (sakhsh), [mi, bone mozare fel, shenase], length of word, masdar]

        for part in processed_verb_part_2:

            result_of_process_verb = word_class.Word(my_word)

            # find number(shakhs) and singularity(mofrad/jam)
            number = part.number
            if number < 3:
                singularity = 'مفرد'
            else:
                singularity = 'جمع'

            # (number, singularity, decomposition, type, length, masdar, tense, root)
            result_of_process_verb.set_data(
                number,
                singularity,
                [processed_verb_part_1.decomposition, part.decomposition],
                'فعل',
                length_of_word + processed_verb_part_1.length,
                part.masdar,
                'مضارع مستمر',
                part.masdar)

            _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially ayande tense(خواهم رفت)
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
    def process_ayande(self, my_word):

        exist = 0
        _result = []
        
        processed_verb_part_1 = self.process_mozare_sade(my_word)
        # list of word class

        # does first part of verb from khastan
        for case in processed_verb_part_1:
            if case.masdar in ("خواهيدن", "خواستن"):
                exist = 1
                print(case)
                processed_verb_part_1 = case
                break

        if exist == 0:
            return _result

        length_of_word = processed_verb_part_1.length
        processed_verb_part_2 = my_word[processed_verb_part_1.length:]
        length_of_word += len(processed_verb_part_2)
        processed_verb_part_2 = processed_verb_part_2.strip()

        matched_first_with_bone_mazi = self.tools.search_word_matched_from_last(
            self.list_of_bone_mazi, processed_verb_part_2
        )

        for case in matched_first_with_bone_mazi:

            result_of_process_verb = word_class.Word(my_word)

            if len(case[1]) != len(processed_verb_part_2):
                continue            
            
            # find number(shakhs) and singularity(mofrad/jam)
            number = processed_verb_part_1.number
            if number < 3:
                singularity = 'مفرد'
            else:
                singularity = 'جمع'
                    
            # (number, singularity, decomposition, type, length, masdar, tense, root)
            result_of_process_verb.set_data(
                number,
                singularity,
                [processed_verb_part_1.decomposition, case[1]],
                'فعل',
                length_of_word,
                case[2],
                'آينده',
                case[2])

            _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially amr type(برو)
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
    def process_amr(self, my_word):
        
        _result = []
        
        # if length of word less than three char do
        if len(my_word) < 3:
            return _result

        # if verb don't have be in first do
        be = my_word[:1]
        if be != "ب":
            return _result

        verb_without_be = my_word[1:]
        # get a list of matched word with all of bone mozare
        # and each case is : [id, bone mozare, masdar]
        matched_first_with_bone_mozare = self.tools.search_word_matched_from_first(self.list_of_bone_mozare, verb_without_be)

        for match in matched_first_with_bone_mozare:

            result_of_process_verb = word_class.Word(my_word)

            suffix = my_word[len(match[1]) + 1:self.find_disjunction_point_in_string(my_word, len(match[1]))]

            if suffix in ("", "يد"):

                # find number(shakhs) and singularity(mofrad/jam)
                number = self.tools.search_element_in_list(["-", "-", "", "-", "يد", "-"], suffix)
                if number < 3:
                    singularity = 'مفرد'
                else:
                    singularity = 'جمع'

                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    singularity,
                    ['ب', match[1], suffix],
                    'فعل امر',
                    len(match[1]) + len(suffix) + 1,
                    match[2],
                    '-',
                    match[2])

                _result.append(result_of_process_verb)

        return _result

    """
        process word as a verb(fel) and specially nahy type(نرو)
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
    def process_nahy(self, my_word):

        _result = []
        
        # if length of word less than three char do
        if len(my_word) < 3:
            return _result

        # if verb don't have be in first do
        na = my_word[:1]
        if na != "ن":
            return _result

        verb_without_be = my_word[1:]
        # get a list of matched word with all of bone mozare
        # and each case is : [id, bone mozare, masdar]
        matched_first_with_bone_mozare = self.tools.search_word_matched_from_first(self.list_of_bone_mozare, verb_without_be)

        for match in matched_first_with_bone_mozare:

            result_of_process_verb = word_class.Word(my_word)

            suffix = my_word[len(match[1]) + 1:]

            if suffix in ("", "يد"):

                # find number(shakhs) and singularity(mofrad/jam)
                number = self.tools.search_element_in_list(["-", "-", "", "-", "يد", "-"], suffix)
                if number < 3:
                    singularity = 'مفرد'
                else:
                    singularity = 'جمع'

                # (number, singularity, decomposition, type, length, masdar, tense, root)
                result_of_process_verb.set_data(
                    number,
                    singularity,
                    ['ن', match[1], suffix],
                    'فعل نهي',
                    len(match[1]) + len(suffix) + 1,
                    match[2],
                    '-',
                    match[2])

                _result.append(result_of_process_verb)

        return _result

    def process(self, word):

        final_result = []

        # result is a list of word_class
        result = self.process_mazi_sade(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mazi_estemrari(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mazi_naghli_mostamar(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mazi_baeed(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mazi_naghli(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mazi_abaad(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mazi_mostamar(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mazi_eltezami(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mozare_sade(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mozare_ekhbari(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mozare_eltezami(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_ayande(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_amr(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_nahy(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        result = self.process_mozare_mostamar(word)
        if self.tools.check_and_upgrade_result_of_process_word(result, word):
            final_result.append(result)

        # check vand verb
        if len(final_result) == 0:
            _result = []

            pish_vand = word[:1]

            if pish_vand == "ن":

                result = self.process(word[1:])

                if not self.tools.is_empty_list(result):

                    for processed_case in result:

                        if not self.tools.is_empty_list(processed_case):

                            for _word_class in processed_case:

                                if _word_class:

                                    if _word_class.length != len(word) - 1:
                                        continue

                                    # if self.tools.check_is_there_masdar(pish_vand + _word_class.masdar) == 1:
                                    _word_class.decomposition.insert(0, pish_vand)
                                    _word_class.type = 'فعل نفي'
                                    _word_class.word = word
                                    #
                                    # _word_class.masdar += vand
                                    _result.append(_word_class)

            # stage 1
            pish_vand = word[:2]
            if pish_vand in ("بر", "در", "وا", "ور"):

                result = self.process(word[2:])

                if not self.tools.is_empty_list(result):

                    for processed_case in result:

                        if not self.tools.is_empty_list(processed_case):

                            for _word_class in processed_case:

                                if _word_class:

                                    if _word_class.length != len(word) - 2:
                                        continue

                                    if self.tools.check_is_there_masdar(pish_vand + _word_class.masdar) == 1:
                                        _word_class.decomposition.insert(0, pish_vand)
                                        #
                                        _word_class.masdar += pish_vand
                                        _result.append(_word_class)

            # stage 2
            pish_vand = word[:3]
            if pish_vand in ("فرو", "باز", "فرا"):

                result = self.process(word[3:])

                if not self.tools.is_empty_list(result):

                    for processed_case in result:

                        if not self.tools.is_empty_list(processed_case):

                            for _word_class in processed_case:

                                if not _word_class.is_empty():

                                    if _word_class.length != len(word) - 3:
                                        continue

                                    if self.tools.check_is_there_masdar(pish_vand + _word_class.masdar) == 1:

                                        _word_class.decoposition.insert(0, pish_vand)
                                        #
                                        _word_class.masdar += pish_vand
                                        _result.append(_word_class)

            final_result.append(_result)

        # final_result is a list of a list of word_class
        return final_result

