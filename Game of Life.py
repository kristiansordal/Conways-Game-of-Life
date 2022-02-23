from dataclasses import dataclass
import pygame as pg
import numpy as np
import copy, random

w = 1980 
h = 1080 
screen = pg.display.set_mode((w, h))

BLACK = ((0,0,0))
WHITE = ((255,255, 255))
pg.display.set_caption('Game of life')
pg.init()
pg.font.init()

pauseText = pg.font.SysFont('Consolas', 32).render('Paused', True, (255, 0, 0))
startText = pg.font.SysFont('Consolas', 32).render('Press S to play, press P to pause', True, (255,0,0))

clock = pg.time.Clock()
cellSize =  20 
FPS = 8
cornerPos = [[(x, y) for x in range(0, w, cellSize)] for y in range(0, h , cellSize)]
gameState = [[bool(random.getrandbits(1)) for _ in range(0, len(cornerPos))] for _ in range(0, len(cornerPos[0]))]
# gameState = [[False for _ in range(0, len(cornerPos))] for _ in range(0, len(cornerPos[0]))]

@dataclass
class Grid():
    def get_neighbors(currentState, x, y):
        neighborCoords = [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        neighbors = 0
        for coord in neighborCoords:
            if(x + coord[0] < len(currentState)) and (y + coord[1] < len(currentState[0])):
                if currentState[x + coord[0]][y + coord[1]] == True:
                    neighbors += 1
        
        return neighbors
        
    def grid_update(state):
        newState = copy.deepcopy(state)
        for i, row in enumerate(newState):
            for j, cell in enumerate(row):
                neighbors = Grid.get_neighbors(state, i, j)

                if cell == True and neighbors < 2: newState[i][j] = False
                elif cell == True and neighbors == (2 or 3): newState[i][j] = True
                elif cell == True and neighbors > 3: newState[i][j] = False
                elif cell == False and neighbors == 3: newState[i][j] = True

        Grid.draw(newState)
        return newState 
    
    def draw(gameState):
        newCells = [] 
        for i, row in enumerate(gameState):
            for j, cell in enumerate(row):
                if cell == True:
                    x = i * cellSize
                    y = j * cellSize
                    newCells.append((pg.Rect(x,y,cellSize,cellSize), WHITE))
                    # newCells.append((pg.Rect(x,y,cellSize,cellSize), list(np.random.choice(range(256), size = 3))))
                elif cell == False:
                    x = i * cellSize
                    y = j * cellSize
                    newCells.append((pg.Rect(x,y,cellSize,cellSize), BLACK))

        for cell in newCells:
            pg.draw.rect(screen, cell[1], cell[0])

    # --- drawing of cell
    def draw_on_click(state, pos, button):

        for i, cornerList in enumerate(cornerPos):
            for j, corner in enumerate(cornerList):
                if (i < len(cornerPos) and j < len(corner)) and (corner[0] <= pos[0]  <= cornerPos[i][j+1][0]) and (pos[1] <= cornerPos[i][j+1][1]):
                    x = cornerPos[i][j][0]
                    y = cornerPos[i-1][j][1]
                    break
                elif (corner[0] < pos[0] < w) and (corner[1] < pos[1] < h):
                    x = corner[0]
                    y = corner[1]
            else: continue
            break

        cell = pg.Rect(x, y, cellSize, cellSize)

        if button == 1: 
            color = WHITE
            state[int(x/cellSize)][int(y/cellSize)] = True
        elif button == 3:
            color = BLACK
            state[int(x/cellSize)][int(y/cellSize)] = False
        pg.draw.rect(screen, color, cell)
    
def main():
    gameClose = False
    play = False
    generation = 0

    while not gameClose:

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mousePos = pg.mouse.get_pos()
                if event.button == 1: Grid.draw_on_click(gameState, mousePos, event.button)
                if event.button == 3: Grid.draw_on_click(gameState, mousePos, event.button)
            
            if event.type == pg.KEYDOWN and event.key == pg.K_s: play = True 
            if event.type == pg.KEYDOWN and event.key == pg.K_p: play = False 
            if (event.type == pg.KEYDOWN and event.key == pg.K_q) or event.type == pg.QUIT: gameClose = True

        else:
            if play == True:
                if generation == 0:
                    nextState = Grid.grid_update(gameState)
                    generation += 1
                else:
                    nextState = Grid.grid_update(nextState)
                    generation += 1
                pg.display.flip()
                clock.tick(FPS)
            
            elif play == False:
                if generation == 0:
                    screen.blit(startText, (700, 460))
                else:
                    screen.blit(pauseText, (45,45))
                pg.display.flip()

if __name__ == '__main__':
    main()