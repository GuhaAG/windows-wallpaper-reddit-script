import random
import json
import sys
import ctypes
import time
import os
import praw 
import urllib.request
from dotenv import load_dotenv
from datetime import date

def getRandomTopImageFromRWallpapers():
    r = praw.Reddit(
                    client_id=os.getenv('CLIENT_ID'),
                    client_secret=os.getenv('CLIENT_SECRET'),
                    user_agent='USER_AGENT')  

    sub = r.subreddit('wallpapers')
    posts = sub.top(limit=100)
    random_post_number = random.randint(0,100)

    imageUrl = ""
    for i,post in enumerate(posts):
        if i==random_post_number:
            imageUrl = post.url
    
    imageUrl = imageUrl.replace("https","http")

    # log wallpaper history
    today = date.today()
    # dd/mm/YY
    dateNow = today.strftime("%d/%m/%Y")
    print(dateNow," ",imageUrl)

    imageFilename = storeImageInStoredBackgroundsFolder(imageUrl)
    setImageAsBackground(imageFilename)        


def storeImageInStoredBackgroundsFolder(imageUrl):
	createStoredBackgroundsFolderIfNotExists()
	imageSuffix = int(round(time.time() * 1000))
	imageFilename = "bg_" + str(imageSuffix) + ".jpg"
	open("stored_backgrounds/" + imageFilename, "wb").write(urllib.request.urlopen(imageUrl).read())
	return imageFilename

def createStoredBackgroundsFolderIfNotExists():
	if not os.path.exists("stored_backgrounds"):
		os.makedirs("stored_backgrounds")

def setImageAsBackground(imageFilename):
	ctypes.windll.user32.SystemParametersInfoW(20, 0, getFullPathOfImage(imageFilename) , 0)

def getFullPathOfImage(imageFilename):
	return os.path.dirname(os.path.realpath("stored_backgrounds/" + imageFilename)) + "\\" + imageFilename

load_dotenv()
getRandomTopImageFromRWallpapers()    