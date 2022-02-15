import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt


def exibir(imagem):
    cv.namedWindow('njanela', cv.WINDOW_NORMAL)
    cv.imshow('njanela', imagem)
    cv.waitKey()
    cv.destroyAllWindows()


def mostrar_matplot(imagem):
    plt.imshow(imagem)
    plt.title(f'{nomedaimg}')
    plt.axis('off')
    plt.show()


def plotando_3(imagem1, imagem2, imagem3):
    plt.subplot(2, 2, 1)
    plt.imshow(imagem1)
    plt.axis('off')
    plt.subplot(2, 2, 2)
    plt.imshow(imagem2)
    plt.axis('off')
    plt.subplot(2, 2, 3)
    plt.imshow(imagem3)
    plt.axis('off')
    nomesmod = nomedaimg.split('.')
    plt.suptitle(f'Figura: {nomesmod[0]}')
    # plt.show()


def plotando_2(imagem1, imagem2, area_por):
    plt.subplot(2, 1, 1)
    plt.imshow(imagem1)
    plt.axis('off')
    plt.subplot(2, 1, 2)
    plt.imshow(imagem2)
    plt.axis('off')
    nomesmod = nomedaimg.split('.')
    plt.suptitle(f'Figura: {nomesmod[0]},{area_por}%')


area_final = 0
lista_de_arquivos = os.listdir('Nuvens/')
coverege = []
kernel = np.ones((3, 3), np.uint8)  # necessário para filtro morfológico
for i in range(len(lista_de_arquivos)):
    nome = lista_de_arquivos[i]
    lista_de_arquivos2 = os.listdir(f'Nuvens/{nome}')
    for a in range(len(lista_de_arquivos2)):
        nomedaimg = lista_de_arquivos2[a]
        img = cv.imread(os.path.join(f'Nuvens/{nome}/{nomedaimg}'), 1)
        img = img[0:0 + 540, 9:0 + 701]  # cortador do ROI
        img_bi = cv.bilateralFilter(img, 60, 60, 60)
        exibir(img_bi)
        img = cv.blur(img, (7, 7))  # blur
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        clahe = cv.createCLAHE(clipLimit=2, tileGridSize=(4, 4))
        gray = clahe.apply(gray)
        exibir(gray)
        gray = cv.GaussianBlur(gray, (5, 5), 2)
        exibir(gray)
