# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 13:44:58 2020

@author: gauta
"""

import os
from PIL import Image , ImageFilter 
import numpy as np

# Getting Length and width of image
def getLengthAndBreadthOfImg(img):
    img1 = np.asarray(img)
    l = round(len(img1)/3)
    b = len(img1[0])
    #print(l,b)
    return l,b


#getting RGB channels
def getColorChannelsOfImage(img,b,l):
    img_b = img.crop((0, 0, b, l)) 
    img_g = img.crop((0, l, b, l+l)) 
    img_r = img.crop((0, l+l, b, l+l+l)) 

    return img_b,img_g,img_r


#merging rgb channels to form a color image
def mergeImage(img_r,img_g,img_b):
    img = Image.merge('RGB', (img_r,img_g,img_b))
    #img.show()
    return img 


#Convert Image to Array 
def convertImageToArray(img):
    imgArr = np.asarray(img)
    return imgArr

#Normalised Cross Correlation
def ncc(a,b):
    a=a-a.mean(axis=0)
    b=b-b.mean(axis=0)
    return np.sum(((a/np.linalg.norm(a)) * (b/np.linalg.norm(b))))

#Sum of Squared Differences
def ssd(A,B):
  #dif = A.ravel() - B.ravel()
  dif = np.subtract(A,B)
  sq = np.square(dif)
  
  return np.sum(sq)




def alignmentFunction(ts,red,img1,minv,val):
    typeO = val
    displacements = []
    for x in range(-ts,ts):
        for y in range(-ts,ts):
            temp = np.roll(img1,[x,y],axis=(0,1))
            
            if (typeO == "ssd"):
                ssdv = ssd(red,temp)
                if (ssdv < minv):
                    minv = ssdv
                    displacements = [x,y]
                    
            if (typeO == 'ncc'):
                nccv = ncc(red,temp)
                if (nccv > minv):
                    minv = nccv
                    displacements = [x,y]
                    
    
    return displacements[0],displacements[1]

   

def ncc_ssd_alingment(img,nm):
    l,b = getLengthAndBreadthOfImg(img)
    img_b,img_g,img_r = getColorChannelsOfImage(img, b, l)
    image_color = mergeImage(img_r,img_g,img_b)
    image_color.save('image'+str(nm)+'-color.png')
    
    
    r = convertImageToArray(img_r)
    g = convertImageToArray(img_g)
    b = convertImageToArray(img_b)
    
    re = img_r.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))
    ge = img_g.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0)) 
    be = img_b.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))
    
    re = convertImageToArray(re)
    ge = convertImageToArray(ge)
    be = convertImageToArray(be)
    
    
    nb1,nb2 = alignmentFunction(20, r, b, float('-inf'),'ncc' )
    ng1,ng2 = alignmentFunction(20, r, g, float('-inf'),'ncc')
    
    print('Image'+str(nm))
    print('NCC - Displacement for Blue Channel:',nb1,nb2)
    print('NCC - Displacement for Green Channel:',ng1,ng2)

    bns = np.roll(b,(nb1,nb2),axis=(0,1))
    gns = np.roll(g,(ng1,ng2),axis=(0,1))

    bns = Image.fromarray(bns)
    gns = Image.fromarray(gns)
    img5 = Image.merge('RGB', (img_r,gns,bns))
    img5 = img5.crop((0, 5, 330, 295))
    img5.save('image'+str(nm)+'-ncc.png')
    
    
    sb1,sb2 = alignmentFunction(20, re, be, float('inf'),'ssd' )
    sg1,sg2 = alignmentFunction(20, re, ge, float('inf'),'ssd')
    print('SSD - Displacement for Blue Channel:',sb1,sb2)
    print('SSD - Displacement for Green Channel:',sg1,sg2)

    bnc = np.roll(b,(sb1,sb2),axis=(0,1))
    gnc = np.roll(g,(sg1,sg2),axis=(0,1))
    
    bnc = Image.fromarray(bnc)
    gnc = Image.fromarray(gnc)
    
    img6 = Image.merge('RGB', (img_r,gnc,bnc))
    img6 = img6.crop((0, 5, 330, 295))
    img6.save('image'+str(nm)+'-ssd.png')
    
    
    print("***************************")





path = os.path.abspath(os.getcwd())

imgs = []
valid_images = [".jpg",".gif",".png",".tga"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs.append(Image.open(os.path.join(path,f)))
   

# Read image 
for i in range(len(imgs)):
    img = imgs[i]
    img = img.crop((25, 25, 380, 1015)) 
    ncc_ssd_alingment(img,i+1)




  