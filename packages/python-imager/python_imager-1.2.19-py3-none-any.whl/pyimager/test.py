import math, pyimager as pyi

def ang(a):
    rad = math.radians(a)
    sin, acos = -math.sin(rad), math.acos(-math.cos(rad))
    angle = math.degrees(-acos if sin<0 else acos)
    return angle

for a in (330, 90):
    print(f"{a} -> {ang(a)}")