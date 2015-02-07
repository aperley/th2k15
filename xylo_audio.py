"""import pyglet
from pyglet.window import key
from time import sleep"""
from pydub import AudioSegment
from pydub import playback
from pydub import effects
from Tkinter import *
from time import sleep
"""def init_xylo():
    xylo1_player = pyglet.media.Player()
    xylo2_player = pyglet.media.Player()
    ...
    xylo1 = pyglet.load.media('blah.mp3')
    xylo2 = pyglet.load.media('blah.mp3')
    ..."""
def toggle_xylo(event):
    print("Registering key press")
    playback.play(xylo)
def toggle_xylo1(event):
    print("Registering key press")
    playback.play(xylo1)

root = Tk()
xylo = AudioSegment.from_wav('blue.wav')
xylo1 = xylo.set_frame_rate(int(xylo.frame_rate * 1.2))
c = Frame(root, width=100, height=200)
root.bind("<Return>", toggle_xylo)
root.bind("<Key>", toggle_xylo1)
c.pack()

root.mainloop()
    
