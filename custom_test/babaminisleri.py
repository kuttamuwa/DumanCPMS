from keyboard import press
import time


if __name__ == '__main__':
    k = input('Simdi?')

    if k == "1":
        time.sleep(3)
        while True:
            press('enter')