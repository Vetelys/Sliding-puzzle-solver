import numpy as np
import random
import keyboard
import time
from sys import exit

DIRS = ["up", "right", "down", "left"]

GOAL_STATE = np.array([[1,2,3,4,5],
                        [6,7,8,9,10],
                        [11,12,13,14,15],
                        [16,17,18,19,20],
                        [21,22,23,24,None]])

GOAL_STATES = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0, 4),
               6: (1, 0), 7: (1, 1), 8: (1, 2), 9: (1, 3), 10: (1, 4),
               11: (2, 0), 12: (2, 1), 13: (2, 2), 14: (2, 3), 15: (2, 4),
               16: (3, 0), 17: (3, 1), 18: (3, 2), 19: (3, 3), 20: (3, 4),
               21: (4, 0), 22: (4, 1), 23: (4, 2), 24: (4, 3), 25: None}


def manhattan_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1-x2) + abs(y1-y2)


class PuzzleState:

    NUM_SHUFFLES = 500


    def __init__(self, state=None):
        if state is not None:
            self.state = np.copy(state)
            empty_loc = np.where(self.state == 25)
            self.state[empty_loc] = None
            self.empty_space = (empty_loc[0][0], empty_loc[1][0]) # Location of the "None"
        else:
            self.state = np.copy(GOAL_STATE)
            self.empty_space = (4, 4)
            self.shuffle()

        print("Initialized: ")
        self.print_board()


    def get_state(self):
        return self.state


    # manhattan distance from required position
    def reward(self, old_pos, new_pos, piece):

        goal_pos = GOAL_STATES[piece]

        if self.is_finished():
            return 1000

        elif manhattan_distance(new_pos, goal_pos) == 0:
            return 2

        elif manhattan_distance(old_pos, goal_pos) > manhattan_distance(new_pos, goal_pos):
            return 1         

        elif manhattan_distance(old_pos, goal_pos) < manhattan_distance(new_pos, goal_pos):
            return -1

        return 0


    def print_board(self):
        board = np.copy(self.state)
        print('_'*30)
        for row in board:
            print(f'|{str(row[0]):5s}|{str(row[1]):5s}|{str(row[2]):5s}|{str(row[3]):5s}|{str(row[4]):5s}|')
            print('_'*30)


    def is_finished(self):
        return np.array_equiv(self.state, GOAL_STATE)


    def ask_input(self):
        print("Make a move (Arrow keys): ")
        while True:
            try:
                if keyboard.is_pressed("left"):
                    dir = "left"
                    time.sleep(0.3)
                    break

                elif keyboard.is_pressed("right"):
                    dir = "right"
                    time.sleep(0.3)
                    break

                elif keyboard.is_pressed("down"):
                    dir = "down"
                    time.sleep(0.3)
                    break
                elif keyboard.is_pressed("up"):
                    dir = "up"
                    time.sleep(0.3)
                    break
            except:
                break

        self.make_move(dir)
        self.print_board()


    def make_move(self, dir, shuffle = False):

        if dir == "quit":
            exit()

        if self.is_valid_move(dir):
            
            y, x = self.empty_space
            reward = 0
            new_loc = (0, 0)
            old_pos = (y, x)


            if dir == "up":
                new_loc = (y-1, x)
                self.state[new_loc], self.state[y, x] = self.state[y, x], self.state[new_loc]

            elif dir == "right":
                new_loc = (y, x+1)
                self.state[new_loc], self.state[y, x] = self.state[y, x], self.state[new_loc]

            elif dir == "left":
                new_loc = (y, x-1)
                self.state[new_loc], self.state[y, x] = self.state[y, x], self.state[new_loc]

            elif dir == "down":
                new_loc = (y+1, x)
                self.state[new_loc], self.state[y, x] = self.state[y, x], self.state[new_loc]
                
            self.empty_space = new_loc

            if shuffle:
                return

            reward = self.reward(new_loc, old_pos, self.state[old_pos])

            if self.is_finished():
                print("Puzzle complete!")

            return reward

        else:
            if not shuffle:
                print("invalid move!")
            return 0

    def shuffle(self):
        for _ in range(self.NUM_SHUFFLES):
            dir = random.choice(DIRS)
            self.make_move(dir, True)

    def is_valid_move(self, dir):
        y, x = self.empty_space
        try:
            if dir == "up":
                return True if y > 0 and self.state[y, x] is None and self.state[y-1, x] is not None else False

            elif dir == "right":
                return True if x < 4 and self.state[y, x] is None and self.state[y, x+1] is not None else False

            elif dir == "left":
                return True if x > 0 and self.state[y, x] is None and self.state[y, x-1] is not None else False

            elif dir == "down":
                return True if y < 4 and self.state[y, x] is None and self.state[y+1, x] is not None else False

            else: False

        except IndexError:
            print("Move is off the board")
            return False

if __name__ == "__main__":
    puzzle = PuzzleState()
    while not puzzle.is_finished():
        puzzle.ask_input()


