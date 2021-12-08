from typing import Iterable, Tuple
import re

class BingoNum:
    """
    A class to represent a number on a bingo board, which includes the number and an indicator to determine if it 
    has been marked or not
    """
    def __init__(self, number: int):
        self._num = number
        self._marked = False
    
    def get_num(self) -> int:
        return self._num
    
    def mark_num(self):
        self._marked = True
    
    def is_marked(self) -> bool:
        return self._marked
    
    def get_num (self) -> int:
        return self._num

class BingoBoard:
    """
    A class to represent a bingo board. A bingo board is represented as a 2-D nested list of BingoNum instances
    """
    def __init__(self):
        self._rows = []
    
    def add_row(self, row: Iterable[BingoNum]):
        """
        Adds a list of BingoNum items, which represent a row

        Args:
            row (Iterable[BingoNum]): A list of BingoNum items
        """
        self._rows.append(row)
    
    def mark_num_return_bingo(self, num: int) -> bool:
        """
        Checks if a number exists in the bingo board. If it does, this method marks that number, checks if 
        there is a bingo, and returns a boolean to indicate if a bingo was found

        Args:
            num (int): The number to mark on the bingo board

        Returns:
            bool: Whether a bingo was found (True) or not (False)
        """
        for i in [i for i, x in enumerate(self._rows)]:
            for j in [j for j, x in enumerate(self._rows[i]) if x._num == num]:
                self._rows[i][j].mark_num()
                return self.check_bingo(i, j)

    def check_bingo (self, row_num: int, col_num: int) -> bool:
        """
        Checks if there is a bingo given a row and column

        Args:
            row_num (int): The row to check the bingo for
            col_num (int): The column to check the bingo for

        Returns:
            bool: Whether a bingo was found (True) or not (False)
        """
        bingo = True
        for num in self._rows[row_num]:
            bingo = bingo & num.is_marked()
        
        if (bingo == True):
            return bingo
        
        bingo = True
        for row in self._rows:
            bingo = bingo & row[col_num].is_marked()

        return bingo
    
    def add_unmarked_numbers (self) -> int:
        """
        Adds all unmarked numbers and returns the sum. This is required as a part of the solution defined by 
        Advent of Code

        Returns:
            int: The sum of all unmarked numbers
        """
        addition = 0
        for row in self._rows:
            for num in row:
                if (num.is_marked() == False):
                    addition += num.get_num()
        return addition


def get_input() -> Tuple[Iterable[int], Iterable[BingoBoard]]:
    """
    Reads through the input file, extracts the draws and all bingo boards, and returns a list for draws and a 
    list for bingo boards

    Returns:
        List of Draws(Iterable[int]), List of BingoBoards(Iterable[BingoBoard]): 
        Returns a Tuple containing a list of Draw Numbers, and a List of Bingo Boards
    """
    boards = []
    
    with open("Day_04_input.txt") as file:
        # The first line of the input file is the list of draw numbers. Handle that line first
        draws = [int(draw) for draw in re.findall("[0-9]+", file.readline())]

        for line in file.readlines():
            # For all subsequent lines, a new line separates each bingo board
            if (line == '\n'):
                boards.append(BingoBoard())
            else:
                boards[-1].add_row([BingoNum(int(num)) for num in re.findall("[0-9]+", line)])

    return draws, boards

def main():
    draws, boards = get_input()

    # For Part 1, find the first winning board
    winning_product = None
    for draw in draws:
        if (winning_product != None):
            break
        for board in boards:
            if (board.mark_num_return_bingo(draw)):
                winning_product = board.add_unmarked_numbers() * draw
                break
    print ("Answer to Part 1:", winning_product)

    # For Part 2, find the last winning board
    won_boards = set()
    for draw in draws:
        if (len (won_boards) == len(boards)):
            break
        for board in boards:
            if (board.mark_num_return_bingo(draw)):
                won_boards.add(board)
            if (len(won_boards) == len(boards)):
                winning_product = board.add_unmarked_numbers() * draw
                break
    print ("Answer to Part 2:", winning_product)

if (__name__ == "__main__"):
    main()