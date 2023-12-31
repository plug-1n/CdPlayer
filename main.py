import time
import io
import pygame
from tkinter import filedialog, Tk, Label, LEFT, Listbox, PhotoImage, RIGHT, BOTTOM
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk
from mutagen.id3 import ID3, APIC

current_song = None
song_len = None
is_playing = False
is_paused_pressed = False
rotation_angle = 0

try:
    pygame.mixer.init()
except pygame.error as e:
    exit(1)


def browseFiles():
    global current_song, is_playing, is_paused_pressed, song_len
    filename = filedialog.askopenfilename(filetypes=(("Audio files", "*.mp3"),))
    if filename:
        pygame.mixer.music.stop()
        current_song = filename
        song_len = pygame.mixer.Sound(current_song).get_length() * 1000
        is_playing = False
        is_paused_pressed = False
        set_cover_image()


def set_cover_image():
    global cover, current_song
    if current_song:
        audio = ID3(current_song)
        if 'APIC:' in audio:
            cover = Image.open(io.BytesIO(audio['APIC:'].data)).convert("RGBA")
        else:
            cover = Image.open("assets/cover.jpg")


def play_song():
    global is_playing, is_paused_pressed
    if current_song and not is_playing:
        is_playing = True
        if is_paused_pressed:
            pygame.mixer.music.unpause()
            is_paused_pressed = False
        else:
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

disk = Image.open("assets/disk.png").convert("L").resize(size=(disk_width, dish_height))
cover = Image.open("assets/cover.jpg")

# Initialize cover image
set_cover_image()


def check_song_status():
    global is_playing, is_paused_pressed, current_song
    if current_song is not None:
        current_position = pygame.mixer.music.get_pos()
        if current_position == -1 and is_playing is True:
            is_playing = False
            is_paused_pressed = False
            current_song = None


def update_label_rotation():
    global rotation_angle, tk_image
    if is_playing:
        rotated_cover = cover.rotate(rotation_angle)
        rotated_disk = disk.rotate(rotation_angle)
        covered_disk = ImageOps.fit(rotated_cover, disk.size, centering=(0.5, 0.5))
        covered_disk.putalpha(rotated_disk)

        tk_image = ImageTk.PhotoImage(covered_disk)
        image_label.configure(image=tk_image)

        rotation_angle = (rotation_angle - 1) % 360
        check_song_status()

    root.after(50, update_label_rotation)


image_label = Label(root)
image_label.pack()

file_btn = ttk.Button(text="open", command=browseFiles)
file_btn.pack()
frameA = ttk.Frame(root, padding=20)
start_icon = ImageTk.PhotoImage(Image.open("assets/play.png").resize(size=(btn_icon_size, btn_icon_size)))
pause_icon = ImageTk.PhotoImage(Image.open("assets/pause.png").resize(size=(btn_icon_size, btn_icon_size)))
stop_icon = ImageTk.PhotoImage(Image.open("assets/stop.png").resize(size=(btn_icon_size, btn_icon_size)))
start_btn = ttk.Button(frameA, image=start_icon, command=play_song)
start_btn.pack(side=LEFT, padx=5)
pause_btn = ttk.Button(frameA, image=pause_icon, command=pause_song)
pause_btn.pack(side=RIGHT, padx=5)
stop_btn = ttk.Button(frameA, image=stop_icon, command=stop_song)
stop_btn.pack(side=RIGHT, padx=5)
frameA.pack()

update_label_rotation()

root.mainloop()
