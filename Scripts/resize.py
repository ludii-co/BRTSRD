import cv2
import numpy as np
import sys
import os

def progress(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    fmt = '[%s] %s%s ...%s' % (bar, percents, '%', status)
    print('\b' * len(fmt), end='')  # clears the line
    sys.stdout.write(fmt)
    sys.stdout.flush()
    if percents == 100:
        print('Job Done =*')

total = 422
i = 1

while( i <= total):
    progress(i, total, status='Selecionando as placas... ' + str(i))
    
    frame = cv2.imread(str(i) + '.png')
    img = cv2.resize(frame, (32,32))
    cv2.imwrite(os.path.join('/Users/rafaelandradedasilva/Desktop/grabber project/resized/' , str(i) + '.png'), img)
    #cv2.imwrite(str(i) + '.png', img)
    i += 1