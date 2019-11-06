from typing import List, Dict, Tuple
class Sentence:
    def __init__(self,
                 allow_random_end=False):
        # if not allow random end, the sentence end iff appending any token is invalid.
        self.clear()
        self.allow_random_end = allow_random_end

    def clear(self):
        self.symbols = []
        self.next_valid_symbol = list(range(10)).remove(0)
        self.length = 0
        self.reach_the_end = False

    def get_candidates(self):
        candidates = [i for i in range(1, 10)]
        if self.length == 0:
            # Check syntax No.6
            try:
                candidates.remove(2)
            except ValueError:
                pass
            return candidates

        # Check syntax No.5
        if self.length % 7 == 6:
            for i in range(1, 10):
                if i % 3 != 0:
                    try:
                        candidates.remove(i)
                    except ValueError:
                        pass
            

        # Check syntax No.2
        try:
            candidates.remove(self.symbols[self.length - 1] + 1)
        except ValueError:
            pass
        try:
            candidates.remove(self.symbols[self.length - 1] - 1)
        except ValueError:
            pass
        
        # Check syntax No.3: Adjacency of 1 and 9 is forbidden.
        if self.symbols[self.length - 1] == 1 or self.symbols[self.length - 1] == 9:
            try:
                candidates.remove(10 - self.symbols[self.length - 1])
            except ValueError:
                pass

        # Check syntax No.4: For every three consecutive numbers, their sum should be greater than 5, and less than 23.
        sum_ = self.symbols[self.length - 2] + self.symbols[self.length - 1]
        i = 0
        while i < len(candidates):
            if candidates[i] + sum_ < 6 or candidates[i] + sum_ > 23:
                candidates.remove(candidates[i])
            else:
                i += 1

        # Check syntax No.1: Odd Numbers shouldn't appear 3 times in a row
        #                    Even Numbers shouldn't appear 4 times in a row.
        count = 1
        check_id = self.length
        for des in range(2):
            check_id -= 1
            if check_id > -1 and self.symbols[check_id] % 2 == 1:
                count += 1
        if count >= 3:    
            for i in range(1, 10):
                if i % 2 == 1:
                    try:
                        candidates.remove(i)
                    except ValueError:
                        pass
        count = 1
        check_id = self.length
        for des in range(3):
            check_id -= 1
            if check_id > -1 and self.symbols[check_id] % 2 == 1:
                count += 1
        if count >= 4:    
            for i in range(1, 10):
                if i % 2 == 0:
                    try:
                        candidates.remove(i)
                    except ValueError:
                        pass
                    
        # Check syntax No.7: If there are eight consecutive numbers that are not 9,
        #                    the next number must be 9.
        if self.length > 7:
            count = 0
            for num in self.symbols[-8:]:
                if num == 9:
                    break
                count += 1
            if count == 8:
                for i in range(1, 9):
                    try:
                        candidates.remove(i)
                    except ValueError:
                        pass
        
        if self.allow_random_end:
            candidates.append(0)
        return candidates

    def _no_restrict_append(self, new_symbol):
        self.symbols.append(new_symbol)
        self.length += 1

    @classmethod
    def check_valid_sentence(cls, sentence: List[int]):
        ''' sentence: list<int> '''
        test_sentence = cls()
        for index, token in enumerate(sentence):
            valid, inst = test_sentence.append(token)
            if not valid:
                return False, index, inst
        return True, index, "Passed."

    def append(self, new_symbol: int):
        if self.reach_the_end:
            self._no_restrict_append(0)
            return True, "Append 0."
        valid, inst = self.check_valid_append(new_symbol)
        if valid:
            self._no_restrict_append(new_symbol)
        return valid, inst

    def check_valid_append(self, new_symbol: int):
        ''' Return: if the appending succeeds, otherwise an error message. '''
        # if type(new_symbol) is not int:
        #     raise TypeError("Type of <new_symbol> should be int.")
        if new_symbol < 0 or new_symbol > 9:
            raise ValueError("0 <= new_symbol < 10 should be satisfied.")
        if new_symbol == 0:
            self.reach_the_end = True
            return True, "Passed."
        if self.reach_the_end:
            return False, "Reached the end."


        if self.length == 0:
            # Check syntax No.6
            if new_symbol == 2:
                return False, "Syntax No.6: 2 cannot be the first token."
            else:
                return True, "Passed."

        # Check syntax No.5
        if self.length % 7 == 6 and new_symbol % 3 != 0:
            return False, "Only a multiple of 3 can be placed at a position of multiple of 7."

        # Check syntax No.2
        if abs(self.symbols[self.length - 1] - new_symbol) == 1:
            return False, ("Syntax No.2: Absolute value of the difference between adjacent numbers "
                    + "should never be 1.")
        # Check syntax No.3
        if self.symbols[self.length - 1] + new_symbol == 10:
            if new_symbol == 1 or new_symbol == 9:
                return False, "Syntax No.3: Adjacency of 1 and 9 is forbidden."

        # Check syntax No.4
        sum_ = self.symbols[self.length - 2] + self.symbols[self.length - 1] + new_symbol
        if sum_ < 6 or sum_ > 22:
            return False, "Syntax No.4: For every three consecutive numbers, their sum should be greater than 5, and less than 23."

        # Check syntax No.1
        if new_symbol % 2 == 1:
            check_id = self.length
            count = 1
            for des in range(2):
                check_id -= 1
                if check_id > -1 and self.symbols[check_id] % 2 == 1:
                    count += 1
            if count >= 3:    
                return False, "Syntax No.1: Odd Numbers shouldn't appear 3 times in a row."
        else:
            if self.length > 2:
                check_id = self.length
                count = 1
                for des in range(3):
                    check_id -= 1
                    if check_id > -1 and self.symbols[check_id] % 2 == 0:
                        count += 1
                if count >= 4:    
                    return False, "Syntax No.1: Even Numbers shouldn't appear 4 times in a row."

        # Check syntax No.7
        if self.length > 7 and new_symbol != 9:
            count = 0
            for num in self.symbols[-8:]:
                if num == 9:
                    break
                count += 1
            if count == 8:
                return False, "Syntax No.7: If there are eight consecutive numbers that are not 9, "\
                       "the next number must be 9."
        return True, "Passed."

    def __str__(self):
        ret_str = ''
        for i in range(self.length):
            ret_str += str(self.symbols[i])
            if i != self.length - 1:
                ret_str += ','   
        return ret_str


def sampling(num_sample: int, sentence_length: int, filename: str):
    seq = np.arange(1, 10)
    with open(filename, 'w+') as file:
        count = 0
        no_more_extend_count = 0
        while count < num_sample:
            new_sentence = Sentence()
            for j in range(sentence_length):
                process_failure = True
                np.random.shuffle(seq)
                for k in seq:
                    valid, inst = new_sentence.append(k)
                    if valid:
                        process_failure = False
                        break
                if process_failure:
                    no_more_extend_count += 1
                    if no_more_extend_count <= 3:
                        print(f"failure example:{new_sentence},\nreason:{inst}")
                    new_sentence.append(0)
            if new_sentence.length == sentence_length:
                file.write(str(new_sentence)+'\n')
                count += 1
            else:
                no_more_extend_count += 0.113
            if count % 50 < 1:
                print(f"write {count} examples with {no_more_extend_count} no_more_extend generations.")


if __name__ == '__main__':
    import numpy as np

    SENTENCE_LENGTH = 64

    sampling(300, SENTENCE_LENGTH, 'train.txt')
    sampling(100, SENTENCE_LENGTH, 'test.txt')

