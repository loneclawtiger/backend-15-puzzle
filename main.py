import pygame
import model
import ai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

BOARD_SIZE = 4
NANO_TO_SEC = 1000000000
pygame.init()

# ai
ai.init(BOARD_SIZE)
puzzle = model.Puzzle(boardSize=BOARD_SIZE)
aiMoveIndex = 0
aiMoves = []


@app.get("/")
def puzzle_genrate():
    global puzzle
    puzzle = model.Puzzle(boardSize=BOARD_SIZE)
    resetai()
    flattened_board = puzzle.flatten_board(puzzle.board)
    return flattened_board


@app.get("/help")
def handlehelp():
    global aiMoves
    global aiMoveIndex
    if len(aiMoves) == 0:
        aiMoves = ai.idaStar(puzzle)
        aiMoveIndex = 0

    if len(aiMoves) != 0:
        puzzle.move(aiMoves[aiMoveIndex])
        if puzzle.checkWin():
            aiMoveIndex = 0
            aiMoves = []
            flattened_board = puzzle.flatten_board(puzzle.board)
            return flattened_board
        else:
            aiMoveIndex += 1
            flattened_board = puzzle.flatten_board(puzzle.board)
            return flattened_board


@app.post("/move")
def handlemove(dir: list[int]):
    resetai()
    print(dir)
    print(puzzle.UP)
    if dir == puzzle.RIGHT:
        puzzle.move(puzzle.RIGHT)
    elif dir == puzzle.LEFT:
        puzzle.move(puzzle.LEFT)
    elif dir == puzzle.DOWN:
        puzzle.move(puzzle.DOWN)
    elif dir == puzzle.UP:
        puzzle.move(puzzle.UP)
    else:
        print("Error")
    return


@app.get("/reshuffle")
def handlereset():
    puzzle.shuffle()
    resetai()
    flattened_board = puzzle.flatten_board(puzzle.board)
    return flattened_board


def resetai():
    global aiMoves
    global aiMoveIndex
    aiMoveIndex = 0
    aiMoves = []
    return
