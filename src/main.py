import random
import pandas as pd
import numpy as np
from PIL import Image
from urllib.request import urlopen
import requests
from io import BytesIO

def get_image(URL):
    #data = requests.get(URL).content
    #img = Image.open(BytesIO(data))
    img = Image.open(urlopen(URL))
    return img

PATH = '../data/'
df = pd.read_csv(PATH + 'raw_data.csv')

def computehist(x):
    rgbhistogram = [[[0 for _ in range(16)] for __ in range(16)] for ___ in range(16)]
    for i in range(len(x)):
        for j in range(len(x[0])):
            rgbhistogram[x[i][j][0]//16][x[i][j][1]//16][x[i][j][2]//16] += 1
    return rgbhistogram

def distt2(x,y):
    mxx = 0
    mxy = 0
    for i in x: 
        for j in i:
            for k in j: 
                mxx = max(mxx,k)
    for i in y: 
        for j in i: 
            for k in j:
                mxy = max(mxy,k)
    cnt = 0.0
    for i in range(len(x)):
        for j in range(len(x[0])):
            for k in range(len(x[0][0])):
                if x[i][j][k]!=mxx and y[i][j][k]!=mxy:
                    cnt+=abs((x[i][j][k]+1)-(y[i][j][k]+1))
    return cnt

K = 100
J = 3
def read(url):
    x = np.array(get_image(url).resize((128,128)))
    return x

def solve(url):
    x = read(url)
                
    order = []
    for _ in range(K):
        r = random.randint(0,df.shape[0]-1)
        c = random.randint(0,df.shape[1]-1)
        new_url = df[r][c]
        y = read(new_url)
        order.append([distt2(computehist(x),computehist(y)),new_url])
        
    order.sort()
    ans = []
    for i in range(3):
        ans.append(order[i][1])
    return ans
    
        