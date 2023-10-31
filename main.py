import time

import pygame

from tkinter import filedialog, Tk, Label,LEFT, Listbox, PhotoImage, RIGHT
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk

current_song = None
is_playing = False
is_paused_pressed = False
rotation_angle = 0
def browseFiles():
    global current_song
    filename = filedialog.askopenfilename(filetypes=(("Audio files","*.mp3"),))
    if filename:
        current_song = filename

def play_song():
    global is_playing, is_paused_pressed
    if current_song and is_playing == False:
        is_playing = True
        if is_paused_pressed:
            pygame.mixer.music.unpause()
            is_playing = True
            is_paused_pressed = False
        else:
            pygame.mixer.init()
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()





def pause_song():
    global is_playing, is_paused_pressed
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
        is_paused_pressed = True

def stop_song():
    global is_playing, is_paused_pressed
    if is_playing or is_paused_pressed:
        pygame.mixer.music.stop()
        is_playing = False
        is_paused_pressed = False



root = Tk()
root.geometry("300x400")
root.resizable(False, False)


disk_width = 300
dish_height = 300
btn_icon_size = 10

disk = Image.open("disk.png").convert("L").resize(size=(disk_width,dish_height))
cover = Image.open("cover.jpg")

def update_label_rotation():
    global rotation_angle, tk_image
    if is_playing:
        rotated_cover = cover.rotate(rotation_angle)
        covered_disk = ImageOps.fit(rotated_cover,disk.size, centering=(0.5,0.5))
        covered_disk.putalpha(disk)

        tk_image = ImageTk.PhotoImage(covered_disk)
        image_label.configure(image=tk_image)

        rotation_angle = (rotation_angle - 1) % 360

    root.after(50, update_label_rotation)

image_label = Label(root)
image_label.pack()




file_btn = ttk.Button(text="open", command=browseFiles)
file_btn.pack()

start_icon = ImageTk.PhotoImage(Image.open("play.png").resize(size=(btn_icon_size, btn_icon_size)))
pause_icon = ImageTk.PhotoImage(Image.open("pause.png").resize(size=(btn_icon_size, btn_icon_size)))
stop_icon = ImageTk.PhotoImage(Image.open("stop.png").resize(size=(btn_icon_size, btn_icon_size)))
start_btn = ttk.Button(image=start_icon,command=play_song)
start_btn.pack(side=LEFT,padx=20)
pause_btn = ttk.Button(image=pause_icon, command=pause_song)
pause_btn.pack(side=LEFT,padx=35)
stop_btn = ttk.Button(image=stop_icon, command=stop_song)
stop_btn.pack(side=RIGHT,padx=20)

update_label_rotation()

root.mainloop()

