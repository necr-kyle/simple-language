# A Simple "Language" to play with 

A simple language to play with using models like Transformers.

A quick way to check whether a Transformer will function or not.

- Symbols: Integers from 1 to 9 (both side included), Integer 0 as the end of a sequence.
- Syntax:
    1. Odd Numbers shouldn't appear 4 times in a row. For even numbers the restriction is 3.
    2. Absolute value of the difference between adjacent numbers should never be 1.
    3. Adjacency of number 1 and 9 is forbidden.
    4. For every three consecutive numbers, their sum should be greater than 5, and less than 23.
    5. Only a multiple of 3 can be placed at a position of multiple of 7.
    6. 2 cannot be the first token.
    7. If there are eight consecutive numbers that is not 9, then the next number must be 9.
  And:
    1. Continuous appearance of the same number is allowed.
    2. The length of a sentence has no bounds (or reasonably, a lower bound of 1).
    3. There are chances that a given sequence cannot be extended any more (especially for longer sequences), and there should be a zero appended to its end.