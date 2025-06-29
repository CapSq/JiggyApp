#main 
import time
import random
import subprocess
import platform

from pynput.mouse import Controller
mouse = Controller()


def jiggy():
    x, y = mouse.position

    OFFSET_RND = 3
    offset_x = random.randint(-OFFSET_RND, OFFSET_RND)
    offset_y = random.randint(-OFFSET_RND, OFFSET_RND)

    # move in small steps to offset position
    MIN_STEPS = 2
    MAX_STEPS = 5
    
    MAX_SLEEP_TIME = 0.05

    steps = random.randint(MIN_STEPS, MAX_STEPS)

    def move_mouse(new_x,new_y):
        mouse.position = (int(new_x), int(new_y))



    print(steps)
    for i in range(steps):
        new_x = x + offset_x * (i + 1) / steps
        new_y = y + offset_y * (i + 1) / steps

        move_mouse(new_x,new_y)
            
        # small delay between steps
        temp_rnd = random.uniform(0.01, MAX_SLEEP_TIME)
        time.sleep(temp_rnd)
        print(temp_rnd) 
 
    print()
    # move back smoothly
    for i in range(steps):
        new_x = x + offset_x * (steps - i - 1) / steps
        new_y = y + offset_y * (steps - i - 1) / steps

        move_mouse(new_x,new_y)

        # small delay between steps
        temp_rnd = random.uniform(0.01, MAX_SLEEP_TIME)
        time.sleep(temp_rnd)
        print(temp_rnd)
    print()

#print(platform.system()) #prints OS System

