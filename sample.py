from typing import List, Dict, Tuple
import time
import numpy as np

SENTENCE_LENGTH = 64
SAMPLE_NUM = 300

class Sentence:
    def __init__(self,
                 allow_random_end=False):
        # If allow_random_end is true, the sentence may end at any position 
        # even if the sequence can proceed further.
        # If not, the sentence end if and only if appending any token is an invalid move.
        self.clear()
        self.allow_random_end = allow_random_end

    def clear(self):
        self.symbols = []
        self.next_valid_symbol = list(range(1, 10))
        self.length = 0
        self.reach_the_end = False

    def padding(self, length):
        if length > self.length:
            self.symbols += [0] * (length - self.length)
            self.length = length


    def get_random_end(self, candidates):
        probabilities = [1 for i in range(len(candidates))]
        if self.allow_random_end:
            probabilities.append(0.2)
            candidates.append(10)
        if len(candidates) == 0:
            self.reach_the_end = True
            candidates.append(10)
            probabilities.append(1)
        probabilities = np.array(probabilities) / np.sum(probabilities)
        return candidates, probabilities
        

    def get_candidates(self):
        candidates = [i for i in range(1, 10)]
        if self.reach_the_end:
            return [], []
        if self.length == 0:
            # Check syntax No.6
            try:
                candidates.remove(2)
            except ValueError:
                pass
            return self.get_random_end(candidates)

        # Check syntax No.5
        if self.length % 7 == 6:
            candidates = [num for num in candidates if num % 3 == 0]
            

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
            if candidates[i] + sum_ < 6 or candidates[i] + sum_ > 22:
                candidates.remove(candidates[i])
            else:
                i += 1

        # Check syntax No.1: Odd Numbers shouldn't appear 3 times in a row
        #                    Even Numbers shouldn't appear 4 times in a row.
        count = 1
        check_id = self.length
        for reduction in range(2):
            check_id -= 1
            if check_id > -1 and self.symbols[check_id] % 2 == 1:
                count += 1
        if count >= 3:    
            candidates = [num for num in candidates if num % 2 == 0]

        count = 1
        check_id = self.length
        for reduction in range(3):
            check_id -= 1
            if check_id > -1 and self.symbols[check_id] % 2 == 0:
                count += 1
        if count >= 4:    
            candidates = [num for num in candidates if num % 2 == 1]
                    
        # Check syntax No.7: If there are eight consecutive numbers that are not 9,
        #                    the next number must be 9.
        if self.length > 7:
            count = 0
            for num in self.symbols[-8:]:
                if num == 9:
                    break
                count += 1
            if count == 8:
                candidates = [num for num in candidates if num == 9]
        
        return self.get_random_end(candidates)

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
        if new_symbol < 1 or new_symbol > 10:
            raise ValueError("0 < new_symbol <= 10 should be satisfied.")
        if new_symbol == 10:
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
            for reduction in range(2):
                check_id -= 1
                if check_id > -1 and self.symbols[check_id] % 2 == 1:
                    count += 1
            if count >= 3:    
                return False, "Syntax No.1: Odd Numbers shouldn't appear 3 times in a row."
        else:
            if self.length > 2:
                check_id = self.length
                count = 1
                for reduction in range(3):
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
        for idx in range(self.length):
            ret_str += str(self.symbols[idx])
            if idx != self.length - 1:
                ret_str += ','   
        return ret_str


def sampling_direct(num_sample: int, sentence_length: int, filename: str):
    seq = np.arange(1, 10)
    with open(filename, 'w+') as file:
        count = 0
        no_more_extend_count = 0
        while count < num_sample:
            # An empty sentence where allow_random_end is False
            new_sentence = Sentence()
            for j in range(sentence_length):
                seq, prob = new_sentence.get_candidates()
                if len(seq) != 0:
                    new_sentence._no_restrict_append(np.random.choice(seq, p=prob))
                else:
                    no_more_extend_count += 1
                    new_sentence.padding(sentence_length)
                    break
            if new_sentence.length == sentence_length:
                file.write(str(new_sentence)+'\n')
                count += 1
            else:
                no_more_extend_count += 0.113
            if count % 50 < 1:
                print(f"write {count} examples with {no_more_extend_count} no_more_extend generations.")


if __name__ == '__main__':
    start = time.time()
    sampling_direct(SAMPLE_NUM, SENTENCE_LENGTH, 'test.txt')
    end = time.time()
    print(end-start, 'seconds.')
