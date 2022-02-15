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


def plotando_2(imagem1, imagem2, area_por1, area_por2):

    # plt.suptitle(f'Filtro:{area_por1}%, original:{area_por2}%')
    plt.subplot(2, 1, 1)
    plt.imshow(imagem1)
    plt.axis('off')
    plt.subplot(2, 1, 2)
    plt.imshow(imagem2)
    plt.axis('off')
    if area_por1 < 50 and area_por2 != 0 and area_por2 <= 50:
        plt.suptitle(f'Filtro:{area_por1}%, original:{area_por2}%\nResultado: {area_por1}%')
    elif area_por1 > 70 and area_por2 == 0:
        plt.suptitle(f'Filtro:{area_por1}%, original:{area_por2}%\nResultado: {area_por2}%')
    elif area_por2 > area_por1:
        plt.suptitle(f'Filtro:{area_por1}%, original:{area_por2}%\nResultado:{area_por2}%')
    else:
        plt.suptitle(f'Filtro:{area_por1}%, original:{area_por2}%\nResultado: {area_por1}%')


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


def plotando_grafico(vetor_analiser):
    plt.clf()
    cont = 1
    vect_x = []
    for h in range(len(vetor_analiser)):
        vect_x.append(cont)
        cont += 1
    plt.bar(vect_x, vetor_analiser, color='red', width=1)
    plt.xlabel("Porcentagem das imagens")
    plt.ylabel("Numero de imagens das nuvens")
    plt.title("Gráfico de porcentagens")
    plt.show()


lista_de_arquivos = os.listdir('Nuvens/')
print()
coverege = []
coverage_original = []
kernel = np.ones((7, 7), np.uint8)  # necessário para filtro morfológico
kernel2 = np.ones((3, 3), np.uint8)  # necessário para filtro morfológico
for i in range(len(lista_de_arquivos)):
    nome = lista_de_arquivos[i]
    lista_de_arquivos2 = os.listdir(f'Nuvens/{nome}')
    for a in range(len(lista_de_arquivos2)):
        nomedaimg = lista_de_arquivos2[a]
        img = cv.imread(os.path.join(f'Nuvens/{nome}/{nomedaimg}'), 1)
        img = img[0:0 + 540, 9:0 + 701]  # cortador do ROI
        img = cv.blur(img, (7, 7))  # blur
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cont_img_original = contando_pixels_gray(gray)
        coverage_original.append(cont_img_original)
        clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        # exibir(gray)
        gray = cv.bilateralFilter(gray, 6, 80, 80)
        # exibir(gray)
        img_melhor = gray.copy()
        ret, thresh_img = cv.threshold(gray, 120, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        thr_mod = cv.morphologyEx(thresh_img, cv.MORPH_CLOSE, kernel, iterations=2)
        # exibir(thr_mod)
        borda = cv.Canny(thr_mod, 50, 155)
        contors, hiera = cv.findContours(borda, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)  # pegamos só os contornos
        imgmod = img.copy()
        cv.drawContours(imgmod, contors, -1, (0, 255, 0), thickness=2)
        coverag = contando_pixels(thr_mod)
        coverege.append(coverag)
        plotando_2(img, thr_mod, int(coverag), int(cont_img_original))
        try:
            os.mkdir('Imagens nuvens por filtros')
        except FileExistsError:
            pass
        try:
            os.mkdir(f'Imagens nuvens por filtros/{nome}')
        except FileExistsError:
            pass
        plt.savefig(f'Imagens nuvens por filtros/{nome}/{nomedaimg}')
plotando_grafico(coverage_original)
