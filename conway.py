import pygame as pg
import numpy as np
import time

COLOR_BG = (10, 10, 10)
GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)

def update(screen, cells, size, withProgress=False):
    updatedCells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if withProgress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updatedCells[row,col] = 1
                if withProgress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updatedCells[row, col] = 1
                if withProgress:
                    color = COLOR_ALIVE_NEXT
        
        pg.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updatedCells

def main():
    pg.init()
    screen = pg.display.set_mode((800,600))

    cells = np.zeros((60, 80))
    screen.fill(GRID)
    update(screen, cells, 10)

    pg.display.flip()
    pg.display.update()

    running = False
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pg.display.update()
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pg.display.update()
            
        screen.fill(GRID)

        if running:
            cells = update(screen, cells, 10, withProgress=True)
            pg.display.update()
        
        time.sleep(0.001)

if __name__ == '__main__':
    main()