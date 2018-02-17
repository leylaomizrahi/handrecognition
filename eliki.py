import sys
import os
from PIL import Image 

#chekcs how many switches from skin to background there are vertically 
#Returns the value of switches in the row that has the max amount 

def isOpenV(im): 
	max = 0 
	chosen = 0 
	width, height = im.size
        for y in range(height):
		
		one = [] 
		for x in range(width):
			if isHand(im,x,y):
				one.append(100)
			else: 
				one.append(0)
		clean = remove_dub(one)
		if len(clean)> max: 
			max = len(clean)	
			chosen = y
	for x in range(width): 
		im.putpixel((x,chosen), (255,255,255))
	im.show()
	return max


#checks how many switches from skin to background there are horizontally 
#Returns the value of switches in the line that has the max amount                                                                                                                    
def isOpenH(im):
        max = 0
	chosen = 0 
	width, height = im.size
	for x in range(width):
                one = []
                for y in range(height):
			if isHand(im,x,y):
                                one.append(100)
			else:
                                one.append(0)
		clean = remove_dub(one)
                if len(clean)> max:
                        max = len(clean)
			chosen = x 
	for y in range(height):
                im.putpixel((chosen,y), (255,255,255))
	im.show() 
	return max 

#Turns the image into two different colors: 
#The hands are red and background is black 

def binaryImage(im):     

        width, height = im.size
        for y in range(height): 
            for x in range(width): 

                if isHand(im, x, y):
                    im.putpixel((x,y), (255,255,255))
                else: 
                    im.putpixel((x,y), 0)
        im.show() 

#Checks at which position the hand is horizontally 
#by drawing five vertical lines 
def whereisHandHor(im):

    cutoff = [0.9 , 0.7 , 0.5 , 0.3, 0.1]
    positions = ["bottom", "mid-bottom",  "center", "center-top", "top"]
    liste = []
    for i in range(len(cutoff)):
         liste.append((organize_ver(im, cutoff[i]), positions[i]))
    counts = [] 
    for combo in liste:  
#	    print (combo)
	    for val in combo[0]: 
		    if val == 100: 
			    counts.append(combo[1])
    
#    im.show()
    loc_counts = set(countCalc(counts))  
    max_val = 0 
    max_pos = 0
    for item in loc_counts: 
	    if item[1]> max_val: 
		    max_val = item[1]
		    max_pos = item[0]
    return (max_pos)

#Checks at which position the hand is vertically                                                                                                                                    
#by drawing five horizontal lines  

def whereisHandVer(im):

    cutoff = [0.9, 0.7, 0.5 , 0.3, 0.1]
    positions = ["right",  "mid-right", "middle", "mid-left",  "left"]                                                                
    liste = []
    for i in range(len(cutoff)):
         liste.append((organize_hor(im, cutoff[i]), positions[i]))
    counts = []
    for combo in liste:
#	    print(combo)
            for val in combo[0]:
                    if val == 100:
                            counts.append(combo[1])

    im.show()
    loc_counts = set(countCalc(counts))
    max_val = 0
    max_pos = 0
    for item in loc_counts:
            if item[1]> max_val:
                    max_val = item[1]
                    max_pos = item[0]
    return (max_pos)

# Calculates how many times each element in a list is repeated 

def countCalc(locations):
    counts = [] 
    for loc in locations:
        counter = 0 
        for loctwo in locations: 
            if loc == loctwo: 
                counter += 1 
        counts.append((loc,counter))
    return counts  

#checks at a certain percentage of the width what the y values are 
#draws a hypothetical horizontal line to see the skin to background switch ration
def organize_ver(im, cutoff):
	list_pix = [] 
        width, height = im.size
        y = int(cutoff * height)
        for x in range(width):
            if isHand(im, x, y): 
                list_pix.append(100)
            else:
                list_pix.append(0)
            im.putpixel((x,y), (0,255,0))
	return list_pix


#given cutoff values will show where the lines cross the image 

def showLines(im, cutoff):
        for cut in cutoff: 
            width, height = im.size
            y = int(cut * height)
            for x in range(width):     
                im.putpixel((x,y), (0,255,0))
            x = int(cut * width) 
	    for y in range(height): 
		    im.putpixel((x,y), (0,255,0))
#	im.show()
	return True

#checks at a certain percentage of the height what the x values are                                                                                                                   #draws a hypothetical vertical line to see the skin to background switch ration  
def organize_hor(im, cutoff):
	list_pix = []
        width, height = im.size
        x = int(cutoff * width)
        for y in range(height):
		if isHand(im, x, y):
			list_pix.append(100)
		else:
			list_pix.append(0)
			im.putpixel((x,y), (0,255,0))
	return list_pix

#removes duplicates that directly follow each other from a list 
def remove_dub(listt):
    unique = []
    for i in range(len(listt) - 4 ): 
	    j = i + 1
	    if listt[i] != listt[j]: 
		    unique.append(listt[i])
		    
	    if j == len(listt)-2: 
		    unique.append(listt[j])
    return unique 

#function to check if hand is open (old design) 
def isHandOpen(listt): 
    if len(listt) >= 15: 
        return True 

#if hand is placed in the middle can be used to calculate how many fingers
#a hand is holding up 
def howManyFingers(listt):
    counter = 0 

    for a in listt: 
        if a == 100: 
            counter +=1
    if counter > 5: 
        counter = 5 
    return counter 


#decides if a certain pixel is part of a the hand 
def isHand(a, x, y): 
    r, g, b = a.getpixel((x,y))
    if r > g and r > b and r > 75:
        return True
    return False  

#Checks the top and bottom edges of the image to see if 
#there are any pixels that would be interpreted as skin
#if so the image is vertical 
def checkVer(image, y): 
        found = False 
	counter = 0 
        width, height = image.size
        for x in range(width): 
		if isHand(image, x, y):
			image.putpixel((x,y), 255)					    
			counter += 1 
#	image.show() 
	return(counter)
 
#Checks the left and right edges  of the image to see if                                         
#there are and pixels that would be interpreted as skin                                                                                                                              
#if so the image is horizontal  
def checkHor(image, x):
        found = False
        width, height = image.size
	counter = 0 
        for y in range(height):
                if isHand(image, x, y):
                        image.putpixel((x,y), 255)
			counter +=1 
#        image.show()
        return(counter)

#checks from which side the arm is coming from and which way the fingers are facing 
def armSide(im):
	width, height = im.size
	checkBottom = checkVer(im, height -1 )
	checkTop = checkVer(im, 0)
	checkRight = checkHor(im, width-1)
	checkLeft = checkHor(im, 0)
	pos = 0 
	if checkTop > checkBottom and checkTop > checkRight and checkTop > checkLeft:
		pos = ("vertical","top")
	if checkBottom > checkTop and checkBottom > checkRight and checkBottom > checkLeft:
		pos = ("vertical", "bottom")
        if checkRight > checkBottom and checkRight > checkTop and checkRight > checkLeft:
		pos = ("horizontal","right")
        if checkLeft > checkBottom and checkLeft > checkRight and checkLeft > checkTop:
		pos = ("horizontal", "left")
	return pos 


#main function to check whether sequence is a fist in the middle and open hand in one corner
dic = sys.argv[1]
pictures = ["1.JPG", "2.JPG"]
results = open("results.txt", "w")

fist = 0
splay = 0 
i = 0  
result = []

for name in pictures:
    filename = dic + "/" + name 
    with Image.open(filename) as im:
#	    im.show() 
	    binaryImage(im) 
	    pos = armSide(im)
	    print(pos)
	    pos_hor = (whereisHandHor(im))
	    pos_ver = (whereisHandVer(im))

	    result.append((pos_hor,pos_ver))

#	    print(pos_hor, " " , pos_ver)
	    if pos[0] == "horizontal":
		    if i == 0: 
			    fist = isOpenH(im)
		    else: 
			    splay = isOpenH(im)
	    else: 
		    if i == 0:
                            fist = isOpenV(im)
                    else:
                            splay = isOpenV(im)

    i += 1 
print(result)


correct = False 

print("fist:", fist)
print("splay:", splay)
if fist < splay:
	
	print("Fist, Open")
	if result[0][0] == "center":
		if result[0][1] == "middle": 
			if result[1][0] != "center": 
				if result[1][0] != "middle":
					correct = True 
					print("Sequence is correct")
if correct == False: 
	print("Sequence is false")
