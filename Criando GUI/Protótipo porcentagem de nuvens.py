import tkinter.filedialog
from tkinter import *
import os
import cv2 as cv
import numpy as np
from PIL import Image, ImageTk


def exibir(imagem):
    cv.namedWindow('njanela', cv.WINDOW_NORMAL)
    cv.imshow('njanela', imagem)
    cv.waitKey()
    cv.destroyAllWindows()


def valor_do_resultado(area_por1, area_por2):
    area_por2 = round(float(area_por2), 2)
    area_por1 = round(float(area_por1), 2)
    if area_por1 < 50 and area_por2 != 0 and area_por2 <= 50:
        result_txt.configure(text=f'Result: {float(area_por1)}%')
    elif area_por1 > 70 and area_por2 == 0:
        result_txt.configure(text=f'Result: {area_por2}%')
    elif area_por2 > area_por1:
        result_txt.configure(text=f'Result: {area_por2}%')
    else:
        result_txt.configure(text=f'Result: {area_por1}%')


def contando_pixels(thr_imagem):
    contagem_bright = np.sum(thr_imagem == 255)
    cr = (contagem_bright / thr_imagem.size) * 100
    # print(cr)
    return cr


def contando_pixels_gray(thr_imagem):
    contagem_gray = np.sum(thr_imagem >= 100)
    cr_gray = (contagem_gray / thr_imagem.size) * 100
    # print(cr_gray)
    return cr_gray


def botao_selecao():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.getcwd(), filetype=(
        ('JPG File', '*.jpg'), ('JPG File', '*.jpeg'), ('PNG File', '*.png'), ('All File', 'how are you.txt')))
    imagem = cv.imread(filename, 1)
    kernel = np.ones((7, 7), np.uint8)  # necessário para filtro morfológico
    '''Podemos colocar um widget radiobutton para dizer se precisamos desse tipo de corte'''
    imagem = imagem[0:0 + 540, 9:0 + 701]  # cortador do ROI
    imagem = cv.blur(imagem, (7, 7))  # blur
    gray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    coverage_original = contando_pixels_gray(gray)
    clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    gray = cv.bilateralFilter(gray, 6, 80, 80)
    imagem = Image.fromarray(gray)
    img = ImageTk.PhotoImage(imagem.resize((500, 327)))
    lbl.configure(image=img)
    lbl.image = img
    ret, thresh_img = cv.threshold(gray, 120, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    thr_mod = cv.morphologyEx(thresh_img, cv.MORPH_CLOSE, kernel, iterations=2)
    coverage = contando_pixels(thr_mod)
    valor_do_resultado(coverage, coverage_original)


window = Tk()

window.title('Cloud percentage calculator')
window.geometry("1000x600")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=f"background.png")
background = canvas.create_image(
    500.0, 300.0,
    image=background_img)

lbl = Label(window, bd=0)
lbl.place(x=0, y=145)
lbl.pack(side='left')

# setando uma imagem de fundo para o quadro
img_back = Image.open('nuvens back.jpg')
img_back = ImageTk.PhotoImage(img_back.resize((500, 327)))
lbl.configure(image=img_back)

img0 = PhotoImage(file=f"img0.png")
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=botao_selecao,
    relief="flat")

b0.place(
    x=208, y=502,
    width=310,
    height=51)

img1 = PhotoImage(file=f"img1.png")
b1 = Button(
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: exit(),
    relief="flat")

b1.place(
    x=575, y=502,
    width=129,
    height=51)

canvas.create_text(
    499.5, 99.0,
    text="Agumented image and percentage of coverage",
    fill="#000000",
    font=("RopaSans-Regular", 25))

result_txt = Label(window, bd=0, background='#747D83', text='Result: ...%', font=("RopaSans-Regular", 34))
result_txt.place(x=660, y=250)
result_txt.pack(side='left')

window.resizable(False, False)
window.mainloop()

'''
Criando uma box
box1 = tkinter.Label(
    window,
    text='Box1',
    bg='#ffffff',
    fg='#ffffff',)
'''
'''
 imagem = Image.open(filename)
 img = ImageTk.PhotoImage(imagem.resize((500, 327)))
 lbl.configure(image=img)
 lbl.image = img 
 '''
