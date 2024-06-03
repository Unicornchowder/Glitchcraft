#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[2]:


#Written by UnicornChowder & Codeuccino

from PIL import Image, ImageDraw
import random
import array
import cv2
import numpy as np
import os
import imageio.v3 as iio
import shutil
import glob

boxCount = -5
gifdir = ""

print( "Generate GIF?" )
gif = input()
#gif = "no"

if ( gif == "yes" ):
    os.rename( "img", file )
    print("Smooth Gif? (yes/no) (WARNING: This may take hours or crash your python kernel depending on your hardware!). Limited to exactly 50 frames")
    smooth = input()

if ( gif == "yes" ):
    print("Framerate? Default is 150 ms per frame. Example: 150")
    framerate = input()
    #framerate = 150

loop = "yes"

frameArr = []

if ( gif == "yes" and smooth != "yes"):
    print( "How many frames?" )
    frames = input()
    #frames = 10
    framecount = frames
    
if ( smooth == "yes" ):
    frames = 50

if ( gif == "yes" ):
    genGif = True

print( "png image to modify" )
file = input()
#file = "img.png"

if ( gif == "no" ):
    print("Full random? ( yes, no )")
    fullRandom = input()
    #fullRandom = "yes"

if ( gif == "no" ):
    print( "horizontal or vertical?" )
    dir = input()
    #dir = "vertical"

if ( gif == "yes" ):
    print( "horizontal, vertical, or both?" )
    gifdir = input()
    if ( gifdir == "horizontal" ):
        dir = "horizontal"
    if ( gifdir == "vertical" ):
        dir = "vertical"
    #dir = "both"

#TAKE IN IMAGE TO CREATE PIXEL MAP AND MEASURE HEIGHT AND LENGTH

input_image = Image.open(file) 
input_image2 = Image.open(file) 

pixel_map = input_image.load()
pixel_map2 = input_image2.load()
    
width, height = input_image.size
width2, height2 = input_image2.size

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

while ( loop == "yes" ):

#RANDOM DIRECTION OF THIS FRAME OF GIF SLICES

    if ( gifdir == "both" or fullRandom == "yes" ):
        randDir = random.randrange(2)
        if ( randDir == 0 ):
            dir = "horizontal"
        if ( randDir == 1 ):
            dir = "vertical"

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    
    if ( gif == "yes" ):
        fullRandom = "yes"
    
    if ( fullRandom == "yes" ):
        stripes = random.randrange(90)
        #stripes = 2

    if ( fullRandom == "no" ):
        print("How many stripes do you want?")
        stripes = int(input())
        #stripes = 3
    
    regen = True

#SETTING THE AMOUNT AND STYLE OF SIFT PER SLICE
    
    shiftArray = [None] * int(stripes)
    uniformShift = 0
        
    if ( fullRandom == "yes" ):
        randomShift = random.randrange(4)
        if ( randomShift == 0 ):
            shiftOption = "uniform"
        if ( randomShift == 1 ):
            shiftOption = "random"
        if ( randomShift == 2 ):
            shiftOption = "/"
        if ( randomShift == 3 ):
            shiftOption = "\\"
        
    if ( fullRandom == "no" ):
        print("Input shift option")
        print("options are /,\,random,uniform")
        shiftOption = input()
        #shiftOption = "/"

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    
    slices = [None] * int(stripes * 2)
    topSlices = [None] * int(stripes)
    bottomSlices = [None] * int(stripes)
    
    while (regen == True):

#THE RANDOM SLICING OF IMAGE BASED ON SET PARAMITERS
        
        for i in range((stripes * 2)):
            if ( dir == "horizontal" ):
                slices[i] = random.randrange(height)
            if ( dir == "vertical" ):
                slices[i] = random.randrange(width)
                
#^^^^^^^^^^^^^^^^^^^^^^^#
        
        sortedSlices = sorted(slices)

#SPLIT SLICES ARRAY INTO PAIRED TOP AND BOTTOM BORDERS FOR STRIPES
            
        counter = 0
        for i in range(stripes):
            topSlices[i] = sortedSlices[counter]
            counter = (counter + 1)
            bottomSlices[i] = sortedSlices[counter]
            counter = (counter + 1)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

#SORT OR DONT SORT SHIFT AMOUNTS BASED ON PARAMITERS
    
        if ( dir == "horizontal" ):
            if ( shiftOption == "uniform" ):
                uniformShift = random.randrange(width)
                
            if ( shiftOption == "/" or "\\" or "random" ):
                for i in range(stripes):
                    shiftArray[i] = random.randrange(width)

        if ( dir == "vertical" ):
            if ( shiftOption == "uniform" ):
                uniformShift = random.randrange(height)
                
            if ( shiftOption == "/" or "\\" or "random" ):
                for i in range(stripes):
                    shiftArray[i] = random.randrange(height)
        
        if ( shiftOption == "\\" or "/" ):
            LR_shift = sorted(shiftArray)
            RL_shift = LR_shift[::-1]
        
        if ( shiftOption == "\\" ):
            shiftArray = LR_shift
        
        if ( shiftOption == "/" ):
            shiftArray = RL_shift
        
        if ( shiftOption == "uniform" ):
            for h in range(stripes):
                shiftArray[h] = uniformShift

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
####################################################################
        if ( dir == "vertical" ):
            for z in range(stripes):
                for i in range(width):#HORIZONTAL TRAVERSAL
                    for j in range(height):#VERTICAL TRAVERSAL
                        if i in range (int(topSlices[z]),(int(bottomSlices[z]))):#WHEN WITHIN RANGE OF SLICE [Z]
                        
                            if (int(j+shiftArray[z]) < int(height)):#MAKE SURE THAT IT DOES NOT GO OUT OF IMAGE RANGE
                                pixel_map[i, j] = pixel_map[i, int(j + shiftArray[z] )]#SHIFT PIXELS
    
                k = 0
                l = 0
                for k in range(width):#HORIZONTAL TRAVERSAL
                    for l in range(height):#VERTICAL TRAVERSAL
                        
                        if k in range (int(topSlices[z]),(int(bottomSlices[z]))):#WHEN WITHIN RANGE OF SLICE [Z]
                        
                            pixel_map[k, l] = pixel_map2[k, (l - shiftArray[z] )]#SHIFT PIXELS FROM SECOND PIXELMAP FOR WRAP OF SLICE
                            if (k == int(height - 1)):#SHIFT PIXELS
                                break

####################################################################
        
        if ( dir == "horizontal" ):
            for z in range(stripes):
                for i in range(width):#HORIZONTAL TRAVERSAL
                    for j in range(height):#VERTICAL TRAVERSAL
                        if j in range (int(topSlices[z]),(int(bottomSlices[z]))):#WHEN WITHIN RANGE OF SLICE [Z]
                        
                            if (int(i+shiftArray[z]) < int(width)):
                                pixel_map[i, j] = pixel_map[int(i + shiftArray[z] ), j]
    
                k = 0
                l = 0
                for k in range(width):#HORIZONTAL TRAVERSAL
                    for l in range(height):#VERTICAL TRAVERSAL
                        
                        if l in range (int(topSlices[z]),(int(bottomSlices[z]))):#WHEN WITHIN RANGE OF SLICE [Z]
                        
                            pixel_map[k, l] = pixel_map2[(k - shiftArray[z] ), l]#SHIFT PIXELS FROM SECOND PIXELMAP FOR WRAP OF SLICE
                            if (k == int(width - 1)):#SHIFT PIXELS
                                break

####################################################################
        
        input_image.save("output.png", format="png")

#CHOOSE WHETHER TO GET NEW SLICE AND SHIFT VALUES
        
        if ( fullRandom == "yes" ):
            regen = False
            
        if ( fullRandom == "no" ):
            print("Regenerate effect? ( yes/no )")
            regenAnswer = input()
            #regenAnswer = "yes"
            if ( regenAnswer == "no" ):
                input_image.save("checkpoint.png", format="png")
                regen = False
        
            if ( regenAnswer == "yes" ):
                input_image = Image.open(file) 
                input_image2 = Image.open(file) 
                
                pixel_map = input_image.load()
                pixel_map2 = input_image2.load()
                
                width, height = input_image.size
                width2, height2 = input_image2.size

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

#DECISION TREE FOR RANDOM COLOR SELECTION
    
    if ( fullRandom == "yes" ):
        colorRandom = random.randrange(12)
        if ( colorRandom == 0 ):
            colorShiftOption = "red"
        if ( colorRandom == 1 ):
            colorShiftOption = "blue"
        if ( colorRandom == 2 ):
            colorShiftOption = "green"
        if ( colorRandom == 3 ):
            colorShiftOption = "yellow fuzz"
        if ( colorRandom == 4 ):
            colorShiftOption = "blue fuzz"
        if ( colorRandom == 5 ):
            colorShiftOption = "invert"
        if ( colorRandom == 6 ):
            colorShiftOption = "red invert"
        if ( colorRandom == 7 ):
            colorShiftOption = "blue invert"
        if ( colorRandom == 8 ):
            colorShiftOption = "green invert"
        if ( colorRandom == 9 ):
            colorShiftOption = "blue implode"
        if ( colorRandom == 10 ):
            colorShiftOption = "green implode"
        if ( colorRandom == 11 ):
            colorShiftOption = "red implode"

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    
    regen = True
    while (regen == True):
    
        if ( fullRandom == "no" ):
            print("Color Shift Option")
            print("Options are (red, blue, green, invert, yellow fuzz, blue fuzz)")
            colorShiftOption = input()
            #colorShiftOption = "red"
        
            if (colorShiftOption == "invert"):
                print("choose channels to invert ( format is combinations of the letters r, b, g )")
                channels = input()
                #channels = "rbg"
            
                chanLen = len(channels)

#DECISION TREE FOR CHANNEL INVERSION
                
                if ( chanLen == 1 ):
                    if ( channels[0] == "r" ):
                        colorShiftOption = "red invert"
                    if ( channels[0] == "b" ):
                        colorShiftOption = "blue invert"
                    if ( channels[0] == "g" ):
                        colorShiftOption = "green invert"
            
                if ( chanLen == 2 ):
                    if ( channels[0] == "r" ):
                        if ( channels[1] == "b" ):
                            colorShiftOption = "green implode"
                        if ( channels[1] == "g" ):
                            colorShiftOption = "blue implode"
            
                    if ( channels[0] == "b" ):
                        if ( channels[1] == "r" ):
                            colorShiftOption = "green implode"
                        if ( channels[1] == "g" ):
                            colorShiftOption = "red implode"
                
                    if ( channels[0] == "g" ):
                        if ( channels[1] == "r" ):
                            colorShiftOption = "blue implode"
                        if ( channels[1] == "b" ):
                            colorShiftOption = "red implode"
            
                if ( chanLen == 3 ):
                    colorShiftOption = "invert"

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    
        colorShade = random.randrange(85, 170)#RANDOM COLOR SHIFT RANGE FOR STANDARD COLOR CHANNEL SHIFT

#SAME MATRIX TRAVERSAL AS HORIZONTAL SLICING

        if ( dir == "horizontal" ):
            for z in range(stripes):
                for i in range(width):
                    for j in range(height):
                        if j in range (int(topSlices[z]),(int(bottomSlices[z]))):

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

#PIXEL CHANNEL VALUE SHIFT
                            
                            r, g, b = input_image.getpixel((i, j))#GET CHANNEL VALUES OF PIXEL
                            
                            if (colorShiftOption == "red"):
                                pixel_map[i, j] = (int(colorShade), int(g), int(b))
                            if (colorShiftOption == "green"):
                                pixel_map[i, j] = (int(r), int(colorShade), int(b))                    
                            if (colorShiftOption == "blue"):
                                pixel_map[i, j] = (int(r), int(g), int(colorShade))
                            if (colorShiftOption == "red invert"):
                                pixel_map[i, j] = (int(255 - r), int(g), int(b))
                            if (colorShiftOption == "green invert"):
                                pixel_map[i, j] = (int(r), int(255 - g), int(b))
                            if (colorShiftOption == "blue invert"):
                                pixel_map[i, j] = (int(r), int(g), int(255 - b))
                            if (colorShiftOption == "red implode"):
                                pixel_map[i, j] = (int(r), int(255 - g), int(255 - b))
                            if (colorShiftOption == "green implode"):
                                pixel_map[i, j] = (int(255 - r), int(g), int(255 - b))
                            if (colorShiftOption == "blue implode"):
                                pixel_map[i, j] = (int(255 - r), int(255 - g), int(b))
                            if (colorShiftOption == "invert"):
                                pixel_map[i, j] = (int(255 - r), int(255 - g), int(255 - b))
                            if (colorShiftOption == "yellow fuzz"):
                                fuzzy = random.randrange(3)
                                if (fuzzy == 0):
                                    pixel_map[i, j] = (int(255 - r), int(g), int(b))
                                if (fuzzy == 1):
                                    pixel_map[i, j] = (int(r), int(255 - g), int(b))
                                if (fuzzy == 2):
                                    pixel_map[i, j] = (int(r), int(g), int(255 - b))
                            if (colorShiftOption == "blue fuzz"):
                                fuzzy = random.randrange(3)
                                if (fuzzy == 0):
                                    pixel_map[i, j] = (int(255 - r), int(g), int(b))
                                if (fuzzy == 1):
                                    pixel_map[i, j] = (int(r), int(255 - g), int(b))
                                if (fuzzy == 2):
                                    pixel_map[i, j] = (int(r), int(g), int(255 - b))
                                r, g, b = input_image.getpixel((i, j))
                                pixel_map[i, j] = (int(r), int(g), int(255 - b))

#^^^^^^^^^^^^^^^^^^^^^^^^#

#SAME ALGORITHM BUT FOR VERTICAL STRIPE COLOR CHANGE

        if ( dir == "vertical" ):
            for z in range(stripes):
                for i in range(width):
                    for j in range(height):
                        if i in range (int(topSlices[z]),(int(bottomSlices[z]))):
                            r, g, b = input_image.getpixel((i, j))
                            
                            if (colorShiftOption == "red"):
                                pixel_map[i, j] = (int(colorShade), int(g), int(b))
                            if (colorShiftOption == "green"):
                                pixel_map[i, j] = (int(r), int(colorShade), int(b))                    
                            if (colorShiftOption == "blue"):
                                pixel_map[i, j] = (int(r), int(g), int(colorShade))
                            if (colorShiftOption == "red invert"):
                                pixel_map[i, j] = (int(255 - r), int(g), int(b))
                            if (colorShiftOption == "green invert"):
                                pixel_map[i, j] = (int(r), int(255 - g), int(b))
                            if (colorShiftOption == "blue invert"):
                                pixel_map[i, j] = (int(r), int(g), int(255 - b))
                            if (colorShiftOption == "red implode"):
                                pixel_map[i, j] = (int(r), int(255 - g), int(255 - b))
                            if (colorShiftOption == "green implode"):
                                pixel_map[i, j] = (int(255 - r), int(g), int(255 - b))
                            if (colorShiftOption == "blue implode"):
                                pixel_map[i, j] = (int(255 - r), int(255 - g), int(b))
                            if (colorShiftOption == "invert"):
                                pixel_map[i, j] = (int(255 - r), int(255 - g), int(255 - b))
                            if (colorShiftOption == "yellow fuzz"):
                                fuzzy = random.randrange(3)
                                if (fuzzy == 0):
                                    pixel_map[i, j] = (int(255 - r), int(g), int(b))
                                if (fuzzy == 1):
                                    pixel_map[i, j] = (int(r), int(255 - g), int(b))
                                if (fuzzy == 2):
                                    pixel_map[i, j] = (int(r), int(g), int(255 - b))
                            if (colorShiftOption == "blue fuzz"):
                                fuzzy = random.randrange(3)
                                if (fuzzy == 0):
                                    pixel_map[i, j] = (int(255 - r), int(g), int(b))
                                if (fuzzy == 1):
                                    pixel_map[i, j] = (int(r), int(255 - g), int(b))
                                if (fuzzy == 2):
                                    pixel_map[i, j] = (int(r), int(g), int(255 - b))
                                r, g, b = input_image.getpixel((i, j))
                                pixel_map[i, j] = (int(r), int(g), int(255 - b))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

#CHOOSE WHETHER TO CHOOSE DIFFERENT COLOR OPTION
        
        input_image.save("output.png", format="png")
    
        if ( fullRandom == "yes" ):
            regen = False
    
        if ( fullRandom =="no" ):
            print("Regenerate effect? ( yes/no )")
            regenAnswer = input()
            #regenAnswer = "no"
            if ( regenAnswer == "no" ):
                input_image.save("checkpoint.png", format="png")
                regen = False
        
            if ( regenAnswer == "yes" ):
                input_image = Image.open("checkpoint.png") 
                input_image2 = Image.open("checkpoint.png") 
                
                pixel_map = input_image.load()
                pixel_map2 = input_image2.load()
                
                width, height = input_image.size
    
    input_image = Image.open("output.png") 
    pixel_map = input_image.load()
    width, height = input_image.size

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    
    if ( fullRandom == "no" ):
        print("Image size( " + str(width) + ", " + str(height) + " )")
    
    if ( fullRandom == "yes" ):
        boxCount = random.randrange(30)
        #boxCount = 2
        
    regen = True
    
    if ( fullRandom == "no" ):
        print("Random box set?")
        randomBoxSet = input()
        #randomBoxSet = "yes"

    if ( fullRandom == "yes" ):
        randomBoxSet = "yes"
    
    while (regen == True):
    
        if ( fullRandom == "yes"):
            box = "yes"
        
        if ( fullRandom == "no" ):
    
            if ( randomBoxSet == "yes" and boxCount == -5 ):
                print("Number of boxes")
                boxCount = input()
                #boxCount = 10

#CHOOSE IF YOU WANT RANDOM BOX PLACEMENT OR SPECIFIC BOX PLACEMENT
            
            if ( randomBoxSet == "no" ):
                print("Random box? ( yes, no )(If no then specify dimentions)")
                box = input()
                #box = "yes"
            if ( randomBoxSet == "yes" ):
                box = "yes"
                
            if ( box == "no" ):
            
                print("Enter top wall pixel")
                TW = input()
                #TW = 100
                
                print("Enter bottom wall pixel")
                BW = input()
                #BW = 1024
                
                print("Enter left wall pixel")
                LW = input()
                #LW = 100
                
                print("Enter right wall pixel")
                RW = input()
                #RW = 500
    
        if ( box == "yes" ):
            TW = random.randrange(height)
            BW = random.randrange(TW, height)
            LW = random.randrange(width)
            RW = random.randrange(LW, width)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

#DECISION TREE FOR RANDOM COLOR SELECTION
    
        if ( fullRandom == "no" and randomBoxSet == "no" ):
            print("Random color?")
            rColor = input()
            #rColor = "no"
        if ( randomBoxSet == "yes" ):
            rColor = "yes"
            
        if ( fullRandom == "yes" or rColor == "yes" ):
            colorRandom = random.randrange(12)
            if ( colorRandom == 0 ):
                colorShiftOption = "red"
            if ( colorRandom == 1 ):
                colorShiftOption = "blue"
            if ( colorRandom == 2 ):
                colorShiftOption = "green"
            if ( colorRandom == 3 ):
                colorShiftOption = "yellow fuzz"
            if ( colorRandom == 4 ):
                colorShiftOption = "blue fuzz"
            if ( colorRandom == 5 ):
                colorShiftOption = "invert"
            if ( colorRandom == 6 ):
                colorShiftOption = "red invert"
            if ( colorRandom == 7 ):
                colorShiftOption = "blue invert"
            if ( colorRandom == 8 ):
                colorShiftOption = "green invert"
            if ( colorRandom == 9 ):
                colorShiftOption = "blue implode"
            if ( colorRandom == 10 ):
                colorShiftOption = "green implode"
            if ( colorRandom == 11 ):
                colorShiftOption = "red implode"

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
                
        if ( fullRandom == "no" and rColor == "no" ):
            print("Color Shift Option")
            print("Options are (red, blue, green, invert, yellow fuzz, blue fuzz)")
            colorShiftOption = input()
            #colorShiftOption = "invert"
                
            if (colorShiftOption == "invert"):
                print("choose channels to invert ( format is combinations of the letters r, b, g )")
                channels = input()
                #channels = "rb"
            
                chanLen = len(channels)
                    
                if ( chanLen == 1 ):
                    if ( channels[0] == "r" ):
                        colorShiftOption = "red invert"
                    if ( channels[0] == "b" ):
                        colorShiftOption = "blue invert"
                    if ( channels[0] == "g" ):
                        colorShiftOption = "green invert"
                
                if ( chanLen == 2 ):
                    if ( channels[0] == "r" ):
                        if ( channels[1] == "b" ):
                            colorShiftOption = "green implode"
                        if ( channels[1] == "g" ):
                            colorShiftOption = "blue implode"
                
                    if ( channels[0] == "b" ):
                        if ( channels[1] == "r" ):
                            colorShiftOption = "green implode"
                        if ( channels[1] == "g" ):
                            colorShiftOption = "red implode"
                    
                    if ( channels[0] == "g" ):
                        if ( channels[1] == "r" ):
                            colorShiftOption = "blue implode"
                        if ( channels[1] == "b" ):
                            colorShiftOption = "red implode"
                
                if ( chanLen == 3 ):
                    colorShiftOption = "invert"
    
        input_image.save("checkpoint.png", format="png")
        
        colorShade = random.randrange(85, 170)

#PIXEL CHANNEL SHIFT ALGORITHM
        
        for i in range(width):
            for j in range(height):
                if ( j > int(TW) and j < int(BW) and i > int(LW) and i < int(RW) ):
                    
                    r, g, b = input_image.getpixel((i, j))
                            
                    if (colorShiftOption == "red"):
                        pixel_map[i, j] = (int(colorShade), int(g), int(b))
                    if (colorShiftOption == "green"):
                        pixel_map[i, j] = (int(r), int(colorShade), int(b))                    
                    if (colorShiftOption == "blue"):
                        pixel_map[i, j] = (int(r), int(g), int(colorShade))
                    if (colorShiftOption == "red invert"):
                        pixel_map[i, j] = (int(255 - r), int(g), int(b))
                    if (colorShiftOption == "green invert"):
                        pixel_map[i, j] = (int(r), int(255 - g), int(b))
                    if (colorShiftOption == "blue invert"):
                        pixel_map[i, j] = (int(r), int(g), int(255 - b))
                    if (colorShiftOption == "red implode"):
                        pixel_map[i, j] = (int(r), int(255 - g), int(255 - b))
                    if (colorShiftOption == "green implode"):
                        pixel_map[i, j] = (int(255 - r), int(g), int(255 - b))
                    if (colorShiftOption == "blue implode"):
                        pixel_map[i, j] = (int(255 - r), int(255 - g), int(b))
                    if (colorShiftOption == "invert"):
                        pixel_map[i, j] = (int(255 - r), int(255 - g), int(255 - b))
                    if (colorShiftOption == "yellow fuzz"):
                        fuzzy = random.randrange(3)
                        if (fuzzy == 0):
                            pixel_map[i, j] = (int(255 - r), int(g), int(b))
                        if (fuzzy == 1):
                            pixel_map[i, j] = (int(r), int(255 - g), int(b))
                        if (fuzzy == 2):
                            pixel_map[i, j] = (int(r), int(g), int(255 - b))
                    if (colorShiftOption == "blue fuzz"):
                        fuzzy = random.randrange(3)
                        if (fuzzy == 0):
                            pixel_map[i, j] = (int(255 - r), int(g), int(b))
                        if (fuzzy == 1):
                            pixel_map[i, j] = (int(r), int(255 - g), int(b))
                        if (fuzzy == 2):
                            pixel_map[i, j] = (int(r), int(g), int(255 - b))
                        r, g, b = input_image.getpixel((i, j))
                        pixel_map[i, j] = (int(r), int(g), int(255 - b))

#^^^^^^^^^^^^^^^^^^^^^^^^^^#
    
        input_image.save("output.png", format="png")

#ADD A BOX?
        
        if ( fullRandom == "yes" or randomBoxSet == "yes" ):
            addBox = "yes"
            boxCount = (int(boxCount) - 1)
            if ( boxCount < 1 ):
                addBox == "no"
        
        if ( fullRandom == "no" and randomBoxSet == "no" ):
            print("Add box? ( yes/no )")
            addBox = input()
            if (addBox == "yes"):
                input_image.save("checkpoint.png", format="png")

#^^^^^^^^^^^^^^^^^^^^^^^^^^^#

#UNDO LAST BOX?
    
        if ( fullRandom == "yes" or randomBoxSet == "yes" ):
            if( boxCount < 1 ):
                regen = False
        if (addBox == "no"):
            if ( fullRandom == "no" ):
                print("Change box? ( yes/no )")
                regenAnswer = input()
                #regenAnswer = "no"
            if ( fullRandom == "yes" and boxCount > 0 ):
                regen = True
            if ( regenAnswer == "no" ):
                input_image.save("checkpoint.png", format="png")
                regen = False
        
            if ( regenAnswer == "yes" ): 
                input_image = Image.open("checkpoint.png") 
                
                pixel_map = input_image.load()
                
                width, height = input_image.size

#^^^^^^^^^^^^^^^^^^^^^^^^^^^#

#IF GIF GENERATION CHANGE NAME OF FRAME TO A SEQUENTIAL NUMBER

    if ( gif == "yes" ):
        shutil.copyfile("output.png", "frame")
        new_name = str(frames) + ".png"
        output = "frame"
        os.rename( output, new_name)

#^^^^^^^^^^^^^^^^^^^^^^^^^^#

        frames = (int(frames) - 1)#REMAINING FRAMES
    
    input_image = Image.open(file) 
                
    pixel_map = input_image.load()
                
    width, height = input_image.size

    if ( gif == "yes" ):
        if ( frames == 0 ):
            break

    if ( gif == "no" ):
        break

os.remove("checkpoint.png")#CLEANUP

if ( gif == "yes" ):
    os.rename( file, "img" )#CLEANUP
    os.remove("output.png")#CLEANUP

if ( gif == "yes" ):
    frameArr = []

#TURN FRAMES INTO GIF
    
    if ( genGif == True ):
        imgs = glob.glob("*.png")
        
        for i in imgs:
            new_frame = Image.open(i)
            frameArr.append(new_frame)
    
        frameArr[0].save('outputGif.gif', format = 'GIF', append_images = frameArr[1:], save_all = True, duration = int(framerate), loop = 0)

#^^^^^^^^^^^^^^^^^^^^^#

#MOVE FRAMES TO FOLDER
    
    os.mkdir('frames')
    for i in range(int(framecount)):
        file2 = str((i + 1)) + ".png"
        file3 = "frames/" + file2
        shutil.move( file2, file3 )

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

if ( smooth == "yes" ):
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import tensorflow as tf
    from tensorflow.keras.applications.vgg16 import preprocess_input, VGG16
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras import layers, models
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    from PIL import Image
    
    # Set the directories
    images_dir = './frames'
    reordered_dir = './Reordered Frames'
    output_gif_path = './smoothed.gif'
    ground_truth_dir = './ground truth'
    
    # Section 1: Define the CNN model
    def build_model():
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=(1024, 1024, 3))
        base_model.trainable = False  # Freeze the base model
    
        model = models.Sequential([
            base_model,
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.Reshape((128, 1)),  # Reshape to sequence format
            layers.Conv1D(1, 1, activation='linear')  # Output sequence of smoothness scores
        ])
        model.compile(optimizer='adam', loss=smoothness_loss)
        return model
    
    def smoothness_loss(y_true, y_pred):
        # y_true is not used in this unsupervised loss function
        diff = tf.reduce_sum(tf.abs(y_pred[:, 1:, :] - y_pred[:, :-1, :]), axis=[1, 2])
        return tf.reduce_mean(diff)
    
    # Section 2: Load frames and preprocess images
    def load_frames(images_dir):
        frames = []
        for root, _, files in os.walk(images_dir):
            if os.path.basename(root).startswith("GIF"):
                for filename in sorted(files):
                    if filename.endswith(".png"):
                        image_path = os.path.join(root, filename)
                        img = image.load_img(image_path, target_size=(1024, 1024))
                        img_array = image.img_to_array(img)
                        frames.append((filename, img_array))
        return frames
    
    # Section 3: Train the model with augmented data
    def train_model_with_augmentation(model, frames):
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            preprocessing_function=preprocess_input
        )
    
        frame_images = np.array([frame[1] for frame in frames])
        frame_images = preprocess_input(frame_images)
    
        train_generator = datagen.flow(frame_images, frame_images, batch_size=32)
    
        # Early stopping and learning rate reduction callbacks
        early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=1e-6)
    
        model.fit(train_generator, epochs=50, callbacks=[early_stopping, reduce_lr])
    
    # Section 7: Predict smoothness between frames
    def predict_smoothness(model, frame1, frame2):
        img_array1 = frame1[1]  # Accessing the image array from the tuple
        img_array2 = frame2[1]  # Accessing the image array from the tuple
        diff = np.abs(img_array1 - img_array2)
        diff = np.expand_dims(diff, axis=0)  # Add a new axis for the batch dimension
        smoothness = model.predict(diff)
        return smoothness[0][0]  # Assuming model.predict returns a 2D array
    
    # Section 8: Calculate pairwise smoothness scores
    def calculate_smoothness_matrix(model, frames):
        num_frames = len(frames)
        smoothness_matrix = np.zeros((num_frames, num_frames))
        for i in range(num_frames):
            for j in range(num_frames):
                if i != j:
                    smoothness_matrix[i, j] = predict_smoothness(model, frames[i], frames[j])
        print("Smoothness matrix calculation complete.")
        return smoothness_matrix
    
    # Section 9: Find the smoothest sequence of frames
    def find_smoothest_sequence(smoothness_matrix):
        num_frames = smoothness_matrix.shape[0]
        visited = [False] * num_frames
        sequence = []
        current_frame = 0
        sequence.append(current_frame)
        visited[current_frame] = True
    
        while len(sequence) < num_frames:
            next_frame = np.argmin(smoothness_matrix[current_frame] + np.where(visited, np.inf, 0))
            if visited[next_frame]:
                print("Error: Next frame already visited!")
                break
            sequence.append(next_frame)
            visited[next_frame] = True
            current_frame = next_frame
        print("Smoothest sequence calculation complete.")
    
        return sequence
    
    # Section 10: Save reordered frames
    def save_reordered_frames(reordered_frames, reordered_dir):
        if not os.path.exists(reordered_dir):
            os.makedirs(reordered_dir)
        for idx, frame in enumerate(reordered_frames):
            img = Image.fromarray(frame.astype('uint8'))
            img.save(os.path.join(reordered_dir, f'reordered_frame_{idx:03d}.png'))
        print("Reordered frames saved successfully.")
    
    # Section 11: Comparison with ground truth
    def load_ground_truth_frames(ground_truth_dir):
        frames = []
        for filename in sorted(os.listdir(ground_truth_dir)):
            if filename.endswith('.png'):
                image_path = os.path.join(ground_truth_dir, filename)
                img = image.load_img(image_path, target_size=(1024, 1024))
                img_array = image.img_to_array(img)
                frames.append(img_array)
        return frames
    
    # Section 12: Merge frames into a GIF
    def merge_frames_to_gif(reordered_dir, output_gif_path):
        frame_paths = sorted([os.path.join(reordered_dir, frame) for frame in os.listdir(reordered_dir) if frame.endswith(".png")])
        frames = [Image.open(frame_path) for frame_path in frame_paths]
        frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], duration = int(framerate), loop=0)
        print("GIF created and saved successfully.")
    
    # Section 14: Visualize the smoothness matrix and sequences
    def visualize_performance(smoothness_matrix, ground_truth_sequence, predicted_sequence):
        plt.figure(figsize=(10, 8))
    
        # Plot the smoothness matrix
        plt.subplot(2, 1, 1)
        plt.imshow(smoothness_matrix, cmap='hot', interpolation='nearest')
        plt.title('Smoothness Matrix')
        plt.colorbar()
    
        # Plot the sequences
        plt.subplot(2, 1, 2)
        plt.plot(ground_truth_sequence, label='Ground Truth Sequence')
        plt.plot(predicted_sequence, label='Predicted Sequence', linestyle='--')
        plt.title('Frame Sequences')
        plt.xlabel('Frame Index')
        plt.ylabel('Frame Order')
        plt.legend()
    
        plt.tight_layout()
        plt.show()
    
    # Main execution
    if __name__ == "__main__":
        frames = load_frames(images_dir)
        model = build_model()
        train_model_with_augmentation(model, frames)
        smoothness_matrix = calculate_smoothness_matrix(model, frames)
        smoothest_sequence = find_smoothest_sequence(smoothness_matrix)
    
        # Save reordered frames based on the predicted sequence
        reordered_frames = [frames[idx][1] for idx in smoothest_sequence]
        save_reordered_frames(reordered_frames, reordered_dir)
        merge_frames_to_gif(reordered_dir, output_gif_path)
    
        # Compare with ground truth and visualize performance
        ground_truth_frames = load_ground_truth_frames(ground_truth_dir)
        ground_truth_sequence = list(range(len(ground_truth_frames)))  # Example ground truth sequence
        visualize_performance(smoothness_matrix, ground_truth_sequence, smoothest_sequence)


# In[ ]:





# In[ ]:





# In[ ]:



