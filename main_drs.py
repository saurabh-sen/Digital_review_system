
import tkinter
import cv2
import pil.Image, pil.ImageTk
from functools import partial
import threading
import time
import imutils

stream = cv2.VideoCapture("E:\\DRS\\clip.mp4")
flag = True
def play(speed):
    global flag
    print(f"you clicked on play. Speed is {speed}")
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = pil.ImageTk.PhotoImage(image=pil.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 29, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag
    
    


def pending(decision):
    # step1 = display decision pending image
    frame = cv2.cvtColor(cv2.imread("E:\\DRS\\pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = pil.ImageTk.PhotoImage(image=pil.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # step2 = Wait for 1 second
    time.sleep(1)

    # step3 = display sponsor image
    frame = cv2.cvtColor(cv2.imread("E:\\DRS\\sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = pil.ImageTk.PhotoImage(image=pil.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # step4 = wait for 1.5 seconds
    time.sleep(2.5)
    # step5 = Display out/notout image
    if decision == 'out':
        decisionImg = "E:\\DRS\\out.png"
    else:
        decisionImg = "E:\\DRS\\not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = pil.ImageTk.PhotoImage(image=pil.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")
    
# Width and height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368

# TKinter gui starts here
window = tkinter.Tk()
window.title("Saurabh Third Umpire Decision Review Kit")
cv_img = cv2.cvtColor(cv2.imread('E:\\DRS\\welcome.png'), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = pil.ImageTk.PhotoImage(image=pil.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()


# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()
window.mainloop()