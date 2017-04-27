#!/usr/bin/env python3

import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from vizprint import print

#from vizprint import vizport
#vizport(9999)

im = Image.fromarray((np.random.random((100,100,3))*255).astype('uint8'))
print('a PIL image:', im)

plt.figure(figsize=(4,2))
plt.plot([1,2,3])
print('a pyplot:', plt)

print()
print('you can repeatedly update an output by giving it an id:')
for i in range(22):
    plt.clf()
    plt.plot(np.random.random(10))
    print(plt, id='etc')
    time.sleep(1)
