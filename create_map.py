import numpy

import PIL

src = PIL.Image.open("src.png")
 
new = src.convert('1')
new.save("out.png")
