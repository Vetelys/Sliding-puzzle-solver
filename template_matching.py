import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
import os
from PuzzleState import PuzzleState
from natsort import natsorted


def screenshot():
    image = pyautogui.screenshot()
    cv2.waitKey(0)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def templatesFromDirectory(query_img, directory):
    template_offset_w, template_offset_h = 180, 15
    position_dict = {}
    for index, filename in enumerate(natsorted(os.listdir(directory))):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            puzzle_piece = cv2.imread(f)
            loc, _ = getTemplateLocation(query_img, puzzle_piece)
            pos = (round((abs(loc[0]-template_offset_w))/57), round((abs(loc[1]-template_offset_h))/57))
            position_dict[pos] = index
    return position_dict
        

def definePuzzle():
    raise NotImplementedError


def getTemplateLocation(img, template):

    #cv2.GaussianBlur(img, (5, 5), 0)
    #cv2.GaussianBlur(template, (5, 5), 0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

    img = cv2.Laplacian(img, cv2.CV_8U)
    template = cv2.Laplacian(template, cv2.CV_8U)

    img = cv2.convertScaleAbs(img)
    template = cv2.convertScaleAbs(template)

    #display(img)
    #display(template)

    method = cv2.TM_CCOEFF_NORMED
    match_result = cv2.matchTemplate(img, template, method)
    _, _, _, max_loc = cv2.minMaxLoc(match_result)
    return max_loc, template.shape[::-1]


def getTemplateLocationImage(img, template):
    top_left, (w, h) = getTemplateLocation(img, template)
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return roi


def display(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)

def accuracy(positions, true_positions):
    correct = 0
    for pos, true_pos in zip(positions.values(), true_positions.values()):
        if pos == true_pos:
            correct += 1
        else:
            print(f'Väärä paikka: {pos} {true_pos}')
    return correct/25
        

directory = '.\images\puzzle_portal' # use definePuzzle() to determine which directory we use to look for puzzle pieces
#sc = screenshot()
sc = cv2.imread('.\images\\test_img.png')
template = cv2.imread('.\images\\template.png')
puzzle_loc = getTemplateLocationImage(sc, template)
positions = templatesFromDirectory(puzzle_loc, directory)

#print board
board = np.zeros((5, 5), dtype=np.ndarray)
for k, v in positions.items():
    board[k] = v

print('_'*30)
for row in board:
    print(f'|{str(row[0]):5s}|{str(row[1]):5s}|{str(row[2]):5s}|{str(row[3]):5s}|{str(row[4]):5s}|')
    print('_'*30)

# calculate accuracy to true positions
true_positions = {(0, 0):1, (4, 1): 2, (3, 0): 3, (0, 1): 4, (4, 0): 5, (2, 2): 6, (3, 3): 7, (0, 3): 8, (1, 4): 9, (1, 2): 10, (3, 4): 11, (2, 0): 12, (1, 1): 13, (4, 2): 14, (1, 0): 15, (3, 1): 16, (4, 3): 17, (0, 4): 18, (1, 3): 19, (0, 2): 20, (2, 3): 21, (3, 2): 22, (2, 1): 23, (2, 4): 24, (4, 4): 25}
print("accuracy:", accuracy(positions, true_positions)*100, "%")

puzzle = PuzzleState(state=board)
while not puzzle.is_finished():
    puzzle.ask_input()







