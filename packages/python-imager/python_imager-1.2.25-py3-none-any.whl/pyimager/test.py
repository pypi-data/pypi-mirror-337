import os, copy, numpy as np, random as rd
try: from pyimager.__vars__ import *
except: from __vars__ import *

class image:
    def new_image(self=None, dimensions=RES.resolution, background=COL.white) -> np.array:
        '''New image'''
        return np.full([round(v) for v in dimensions[::-1]]+[3], background[::-1], np.uint8)
    def __init__(self, name="python-image", img=None) -> None:
        self.img = np.array(self.new_image() if type(img) == type(None) else img.img if type(img) == image else img)
        self.name, self.fullscreen = name, False
    def __str__(self) -> str: return self.name
    def show_(self, wait=1, destroy=False, built_in_functs=True) -> int:
        '''Show image in a window'''
        if self.fullscreen:
            cv2.namedWindow(self.name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
        else:
            cv2.namedWindow(self.name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_KEEPRATIO)
        cv2.imshow(self.name, np.array(self.img, np.uint8))
        wk = cv2.waitKeyEx(wait)
        if destroy == True: cv2.destroyWindow(self.name)
        elif built_in_functs:
            match wk:
                case 65470: cv2.moveWindow(self.name, 0, 0) #f1
                case 65471: cv2.moveWindow(self.name, screen[0], 0) #f2
                case 32: self.fullscreen = not self.fullscreen #spacebar
                case 27: self.close()
                case _: return wk
            return -1
        return wk
    def build(self):
        if self.show_(1, False, False) == -1: return self
        else: raise unreachableImage("An error has occurred while building the image!")
    def show(self, *args, **kwargs) -> int:
        if self.is_opened(): return self.show_(*args, **kwargs)
        else: raise unreachableImage("Maybe you forgot to build the image?")
    def is_closed(self) -> bool:
        '''Detect if the window is currently closed'''
        try: return cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1
        except: return True
    def is_opened(self) -> bool:
        '''Detect if the window is currently opened'''
        return not self.is_closed()
    def close(self) -> None:
        '''Closes window'''
        if not self.is_closed(): cv2.destroyWindow(self.name)
    def line(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a line on the image'''
        cv2.line(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness), lineTypes[lineType%len(lineTypes)])
    def rectangle(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a rectangle on the image'''
        cv2.rectangle(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def polygon(self, pts=[ct_sg(p3, ct), ct_sg(p4, ct), ct_sg(ct, ch)], couleur=COL.black, thickness=1, lineType=0):
        '''Draws a polygon on the image'''
        pts = [[round(i) for i in pt] for pt in pts]
        lineType = lineTypes[lineType%len(lineTypes)]
        couleur = couleur[::-1]; thickness = round(thickness)
        if thickness > 0: cv2.polylines(self.img, [np.array(pts, dtype=np.int32)], True, couleur, thickness, lineType)
        else: cv2.fillPoly(self.img, [np.array(pts, np.int32)], couleur, lineType)
    def circle(self, ct, radius=10, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a circle on the image'''
        cv2.circle(self.img, [round(p) for p in ct], round(radius), colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def ellipse(self, ct, radiuses=[10, 10], colour=COL.black, thickness=1, lineType=0, startAngle=0, endAngle=360, angle=0) -> None:
        '''Draws an ellipse on the image'''
        cv2.ellipse(self.img, [round(p) for p in ct], [round(radius) for radius in radiuses], angle, startAngle, endAngle, colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def save_img(self, path='', fileName=None) -> None:
        '''Saves file'''
        if fileName == None: fileName = self.name
        if path != '': currentWorkingDirPath = os.getcwd(); os.chdir(path)
        cv2.imwrite(fileName, self.img)
        if path != '': os.chdir(currentWorkingDirPath)
    def open_img(self, path) -> None:
        '''Opens local file as image'''
        self.img = cv2.imdecode(np.asarray(bytearray(open(f'{path}', "rb").read()), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    def set_img(self, img) -> None:
        '''Sets the actual image to img'''
        self.img = np.array(img, np.uint8)
    def copy(self):
        '''Returns a copy of itself'''
        return image(self.nom, copy.deepcopy(self.img))
    def size(self, rev=False) -> [int, int]:
        '''Returns image's size (reverse True means [y,x] whereas False means [x,y])'''
        return [len(self.img[0]), len(self.img)][::-1 if rev else 1]

def new_img(dimensions=None, background=COL.white, name="NewImg") -> np.array:
    return image(name, image.new_image(dimensions=dimensions if dimensions!=None else RES.resolution, background=background))