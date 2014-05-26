import random
import time

width = 80
flips = 5
sleep = 0.05 # seconds

if __name__ == '__main__':
        switches = [True] * width
        garbage = "1234567890!@#$%^&*()ZXCVBNM<>?"
        l = len(garbage)

        while True:
                for i in range(0,width):
                        if switches[i] is True:
                                print garbage[random.randint(0,l-1)],
                        else:
                                print ' ',
                print

                for i in range(0,flips):
                        x = random.randint(0,width-1)
                        switches[x] = not switches[x]
                time.sleep(sleep)
