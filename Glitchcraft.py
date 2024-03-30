#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[5]:


#Written by UnicornChowder

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
    print("Framerate? Default is 150 ms per frame. Example: 150")
    framerate = input()
    #framerate = 150

loop = "yes"

frameArr = []

if ( gif == "yes" ):
    print( "How many frames?" )
    frames = input()
    #frames = 10
    framecount = frames

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

if ( gif == "yes" ):
    os.rename( "img", file )

print("Complete!")


# In[ ]:





# In[ ]:





# In[ ]:




