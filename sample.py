from typing import List, Dict, Tuple
class Sentence:
    def __init__(self):
        self.clear()

    def clear(self):
        self.symbols = []
        self.length = 0
        self.reach_the_end = False

    def _no_restrict_append(self, new_symbol):
        self.symbols.append(new_symbol)
        self.length += 1

    @classmethod
    def check_valid_sentence(cls, sentence: List[int]):
        ''' sentence: list<int> '''
        test_sentence = cls()
        for index, token in enumerate(sentence):
            result = test_sentence.append(token)
            if result is not None:
                return False, index, result
        return True, index, "Passed."

    def append(self, new_symbol: int):
        ''' Return: None if the appending succeeds, otherwise an error message. '''
        # if type(new_symbol) is not int:
        #     raise TypeError("Type of <new_symbol> should be int.")
        if new_symbol < 0 or new_symbol > 9:
            raise ValueError("0 <= new_symbol < 10 should be satisfied.")
        if new_symbol == 0:
            self._no_restrict_append(new_symbol)
            self.reach_the_end = True
            return None
        if self.reach_the_end:
            self._no_restrict_append(0)
            return None


        if self.length == 0:
            # Check syntax No.6
            if new_symbol == 2:
                return "Syntax No.6: 2 cannot be the first token."
            else:
                self._no_restrict_append(new_symbol)
                return None

        # Check syntax No.5
        if self.length % 7 == 6 and new_symbol % 3 != 0:
            return "Only a multiple of 3 can be placed at a position of multiple of 7."

        # Check syntax No.2
        if abs(self.symbols[self.length - 1] - new_symbol) == 1:
            return ("Syntax No.2: Absolute value of the difference between adjacent numbers "
                    + "should never be 1.")
        # Check syntax No.3
        if self.symbols[self.length - 1] + new_symbol == 10:
            if new_symbol == 1 or new_symbol == 9:
                return "Syntax No.3: Adjacency of 1 and 9 is forbidden."

        # Check syntax No.4
        sum_ = self.symbols[self.length - 2] + self.symbols[self.length - 1] + new_symbol
        if sum_ < 6 or sum_ > 22:
            return "Syntax No.4: For every three consecutive numbers, their sum should be greater than 5, and less than 23."

        # Check syntax No.1
        if new_symbol % 2 == 1:
            check_id = self.length
            count = 1
            for des in range(2):
                check_id -= 1
                if check_id > -1 and self.symbols[check_id] % 2 == 1:
                    count += 1
            if count >= 3:    
                return "Syntax No.1: Odd Numbers shouldn't appear 3 times in a row."
        else:
            if self.length > 2:
                check_id = self.length
                count = 1
                for des in range(3):
                    check_id -= 1
                    if check_id > -1 and self.symbols[check_id] % 2 == 0:
                        count += 1
                if count >= 4:    
                    return "Syntax No.1: Even Numbers shouldn't appear 4 times in a row."
        if self.length > 7 and new_symbol != 9:
            count = 0
            for num in self.symbols[-8:]:
                if num == 9:
                    break
                count += 1
            if count == 8:
                return "Syntax No.7: If there are eight consecutive numbers that are not 9, "
                       "the next number must be 9."
        self._no_restrict_append(new_symbol)
        return None

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
        while count + no_more_extend_count < num_sample:
            new_sentence = Sentence()
            for j in range(sentence_length):
                process_failure = True
                np.random.shuffle(seq)
                for k in seq:
                    if new_sentence.append(k) is None:
                        process_failure = False
                        break
                if process_failure:
                    no_more_extend_count += 1
                    if no_more_extend_count <= 3:
                        print(f"failure example:{new_sentence}")
                    new_sentence.append(0)
            if new_sentence.length == sentence_length:
                file.write(str(new_sentence)+'\n')
                count += 1
            else:
                pass #no_more_extend_count += 0.113
            if (count + no_more_extend_count) % 50 == 0:
                print(f"write {count} examples with {no_more_extend_count} no_more_extend generations.")


if __name__ == '__main__':
    import numpy as np

    SENTENCE_LENGTH = 64

    sampling(600, SENTENCE_LENGTH, 'train.txt')
    sampling(100, SENTENCE_LENGTH, 'test.txt')

