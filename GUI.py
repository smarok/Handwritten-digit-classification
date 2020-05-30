from keras import models
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np
import win32gui

model=models.load_model('digit_classification.h5')

def predict_digit(img):
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    for x in range(28):
        for y in range(28):
            img[x][y]=255-img[x][y]
  
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

root=tk.Tk()

canvas=tk.Canvas(root,bg='sky blue')
canvas.place(relwidth=1,relheight=1)

canvas2=tk.Canvas(root, bg='white',cursor="cross")
canvas2.place(relx=0.5,rely=0.1,relwidth=0.35,relheight=0.6,anchor='n')

lower_frame=tk.Frame(root,bg='red',bd=5)
lower_frame.place(relx=0.5,rely=0.8,relwidth=0.75,relheight=0.1,anchor='n')

label = tk.Label(lower_frame, text="Draw Something", font=("Helvetica", 20), anchor='nw',justify='left',bd=4)
label.place(relx=0,rely=0,relwidth=0.65,relheight=1)

def classify_drawing():
    canvas_id=canvas2.winfo_id()
    coords=win32gui.GetWindowRect(canvas_id)
    a,b,c,d=coords
    coords=(a+125,b+25,c+260,d+150)
    image=ImageGrab.grab(coords)
    digit, accuracy=predict_digit(image)
    accuracy=accuracy*100
    label.configure(text= "DIGIT: "+str(digit)+'\n'+'ACCURACY: '+str(accuracy)+'%')

classify_btn = tk.Button(lower_frame, text = "Recognise",font=(15), command = classify_drawing)   
classify_btn.place(relx=0.7,rely=0, relwidth=0.3,relheight=1)

def clscrn():
    canvas2.delete('all')

button_clear = tk.Button(root, text = "Clear", command = clscrn, font=(15))
button_clear.place(relx=0.5,rely=0.7,relwidth=0.35,relheight=0.05,anchor='n')

def draw_lines(event):
    r=20
    canvas2.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='black')

canvas2.bind("<B1-Motion>", draw_lines)

root.mainloop()





