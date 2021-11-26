import numpy as np
from PIL import Image
from PIL import ImageChops
from PIL import ImageStat
import os
import time

def read_corner_fast(image):
    h, w, _ = image.shape
    for i in range(h):
        if sum(sum(image[i]))!=0:
            for j in range(w):
                if sum(image[i][j])!=0:

                    break
            else:
                continue
            break
    return i, j

def table_state(chess, white_set, black_set):
    figure_names = {'pawn': "P", 'knight':"N", 'bishop':"B", "rook" :"R", "queen": "Q", 'king':"K" }
    sl = int((chess.shape)[0]/8)
    string = ''
  
    white_positions ={}
    black_positions = {}
    for i in range(8):
        row = chess[i*sl: (i+1)*sl, :, :]
        z = 0 
        for j in range(8):
            square = row[:, j*sl:(j+1)*sl, :]
            results = np.all(square == square[0])
            if results == True:
                z+=1
            else:
                if z !=0:
                    string = string + '%s'%z
                #figure = match_pattern(square)
                im = Image.fromarray(square).convert('1')
                statistics_black = {}
                bs = black_set
                for key in bs:
                    diff1 = ImageChops.difference(im, bs[key][0])
                    diff2 = ImageChops.difference(im, bs[key][1])

                    stat = ImageStat.Stat(diff1)
                    diff1_ratio = sum(stat.mean) / (len(stat.mean) * 255)

                    stat = ImageStat.Stat(diff2)
                    diff2_ratio = sum(stat.mean) / (len(stat.mean) * 255)

                    statistics_black[key] = min(diff1_ratio, diff2_ratio)

                bs = white_set
                statistics_white = {}
                for key in bs:
                    diff1 = ImageChops.difference(im, bs[key][0])
                    diff2 = ImageChops.difference(im, bs[key][1])

                    stat = ImageStat.Stat(diff1)
                    diff1_ratio = sum(stat.mean) / (len(stat.mean) * 255)

                    stat = ImageStat.Stat(diff2)
                    diff2_ratio = sum(stat.mean) / (len(stat.mean) * 255)

                    statistics_white[key] = min(diff1_ratio, diff2_ratio)

                wm =  min(statistics_white.items(), key=lambda x: x[1]) 
                bm =  min(statistics_black.items(), key=lambda x: x[1])
                
                if wm[1] < bm[1]:
                    F = figure_names[wm[0]] 
                    current = white_positions.get(wm[0], [])
                    current.append((i,j))
                    white_positions[wm[0]] = current
                else:
                    F = figure_names[bm[0]].lower()
                    current = black_positions.get(bm[0], [])
                    current.append((i,j))
                    black_positions[bm[0]] = current

                string = string + str(F)#'F'
                z=0

        if z!=0:
            string = string + '%s'%z
        if i!=7:
            string = string+'/'

    return string, white_positions, black_positions

def merge_figures( figure, sl):
    black_tile_path = os.path.join(folder_path, 'tiles/black.png')
    white_tile_path = os.path.join(folder_path, 'tiles/white.png')
    black_tile =  Image.open(black_tile_path).convert("RGBA")
    white_tile = Image.open(white_tile_path).convert("RGBA")

    black_tile.paste(figure, (0,0), figure)
    black_tile = black_tile.resize((sl, sl)).convert('1')

    white_tile.paste(figure, (0,0), figure)
    white_tile = white_tile.resize((sl, sl)).convert('1')

    return black_tile, white_tile

def set_figures(figures_path, sl):
    player = {}
    for figure in ['king', 'bishop', 'knight', 'pawn', 'queen', 'rook']:
        fig_path = os.path.join(figures_path, '%s.png'%figure)
        fig = Image.open(fig_path).convert('RGBA')
        k1, k2 = merge_figures(fig, sl)
        player[figure] = [k1, k2]
    return player

def check_king(fig, color, I,J, i, j):
   
    if fig=='king':
        f = lambda I,J,i,j: (abs(I-i) == 1 and J==j) or (I==i and abs(J-j)==1)
        if f(I,J,i,j):return 1
        else: return 0
    if fig=='rook':

        f = lambda I, J, i, j: (I==i) or (J==j)
        if f(I,J,i,j):
            return 1
        else:
            return 0

    if fig=='bishop':

        f = lambda I, J, i, j: abs(I-i) == abs(J-j)
        if f(I,J,i,j):
            return 1
        else:
            return 0
    
    if fig=='queen':

        f = lambda I, J, i, j: (abs(I-i) == abs(J-j)) or (I==i) or (J==j)
        if f(I,J,i,j):
            return 1
        else:
            return 0

    if fig=='knight':
        f = lambda I, J, i, j: ((abs(I-i)==2) and (abs(J-j)==1)) or ((abs(I-i)==1) and (abs(J-j)==2))
        if f(I,J,i,j):
            return 1
        else:
            return 0
    if fig=='pawn':
        if color == 'black':
            f = lambda I, J, i, j: (( I-i) == 1) and (abs(J-j) == 1)
            if f(I,J,i,j):
                return 1
            else:
                return 0

        if color == 'white':
            f = lambda I, J, i, j: (( I-i) == -1) and (abs(J-j) == 1)
            if f(I,J,i,j):
                return 1
            else:
                return 0

if __name__ == "__main__":
    folder_path = input()
    test= os.path.split(folder_path)[-1]
    image_path = os.path.join(folder_path, '%s.png'%test)
    image_file = Image.open(image_path)
    image = np.array(image_file)
    
    
    H, W = read_corner_fast(image)
    print('%s,%s'%(H,W))
    h, w, _ = image.shape
    row = image[H]

    for l in range(W, w):
        if (sum(row[l]))==0:
            break
        else:
            continue
    lenght = l-W
    
    chess_x = image[ H:H+lenght, :, :]
    chess = chess_x[:, W: W+lenght, :]
    sl = int((chess.shape)[0]/8)

    figures_path1 = os.path.join(folder_path, 'pieces', 'white')
    white_set = set_figures(figures_path1, sl)

    figures_path2 = os.path.join(folder_path, 'pieces', 'black')
    black_set = set_figures(figures_path2, sl)
    states, wpos, bpos = table_state(chess, white_set, black_set)
    print(states)

    black_checks = 0
    color = 'black'
    if 'king' in wpos.keys():
        I, J = wpos['king'][0]
        for key in bpos:
            for nF in bpos[key]:
                i, j = nF
                black_checks += check_king(key, color, I, J, i,j)
                
    white_checks =0
    color = 'white'
    if 'king' in bpos.keys():
        I, J = bpos['king'][0]
        for key in wpos:
            for nF in wpos[key]:
                i, j = nF
                white_checks += check_king(key, color, I, J, i,j)
                
    
    if white_checks == 0 and black_checks==0:
        print('-')
    else:
        if white_checks>0:
            print('W')
        else:
            if black_checks>0:
                print('B')
