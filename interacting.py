import picamera
import pygame as pg
import os

from google.cloud import vision
from time import sleep
from adafruit_crickit import crickit
import time
import signal
import sys
import re
import random

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="DET_wesley.json"
client = vision.ImageAnnotatorClient()

image = 'iamge.jpg'

from operator import add

#directory = ['wood', 'robot', 'coke', 'leaves', 'rose']

#direcotry_set = {'wood', 'robot', 'coke', 'leaves', 'rose'}

#sounds = ['wood.wav','robot.wav', 'coke.wav', 'leaves.wav', 'rose.wav']

#ambient = 'ambient.wav'

# List of all the possible words.
wood = ['wood', 'hardwood']
robot = ['robot', 'blue']
coke = ['paper', 'stuff']
leaves = ['maple', 'autumn', 'leaf']
rose = []


def get_string(image):
    response = client.label_detection(image = image)
    labels = response.label_annotations
    
    label_text = ""

    for label in labels:
        label_text += ''.join([label.description, " "])

    if label_text:
        print('image_labeling(): {}'.format(label_text))
        return label_text
    else:
        print('image_labeling(): No Label Descriptions')

def face_distinction(image):
    sound_file = "/home/pi/DET2019_Class5/hello2.wav"

    response = client.face_detection(image=image)
    face_content = response.face_annotations

    if face_content and face_content[0].detection_confidence > 0.25:
        print('face_distinction(): {}'.format(face_content[0].detection_confidence))
        pg.mixer.music.load(sound_file)
        pg.mixer.music.play()
    else:
        print('face_distinction(): No Face Detected at High Confidence!')

def find_index(lst):
    m = max(lst)
    return [i for i, j in enumerate(lst) if j == m]

def takephoto(camera):
    camera.start_preview()
    sleep(.5)
    camera.capture('image.jpg')
    camera.stop_preview()

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def main():
    
    camera = picamera.PiCamera()
    pg.init()
    pg.mixer.init()

    
    #Set up screen
    title = 'Husky face'
    width = 900
    height = 500
    
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(title)
    clock = pg.time.Clock()
    
    print('set up')

    #channel1.play(pg.mixer.Sound('ambient.wav'), loops = -1)

    while True:

        # Loading the face function.
        face0 = pg.image.load('face0.jpg')
        face1 = pg.image.load('face1.png')
        face2 = pg.image.load('face2.png')
        face3 = pg.image.load('face3.png')
        face4 = pg.image.load('face4.png')

        # Initial face.
        screen.blit(face0, (0, 0))
        
        
        print('initial face')

        takephoto(camera)

        with open('image.jpg', 'rb') as image_file:
            content = image_file.read()
            image = vision.types.Image(content=content)

            labels = get_string(image)

            # Face detection.
            #face_distinction()

            # Compassion.

            # Wood: Curious
            for word in wood:
                if re.search(word, labels, re.IGNORECASE):
                    print('wood')
                    screen.blit(face1, (0, 0))
                    pg.display.flip()
                    pg.mixer.music.load('wood.mp3')
                    pg.mixer.music.play()

            # Robot: Love
            for word in robot:
                if re.search(word, labels, re.IGNORECASE):
                    print('robot')
                    screen.blit(face2, (0, 0))
                    pg.display.flip()
                    pg.mixer.music.load('robot.mp3')
                    pg.mixer.music.play()

            # Can: Angry
            for word in coke:
                if re.search(word, labels, re.IGNORECASE):
                    print('coke')
                    screen.blit(face3, (0, 0))
                    pg.display.flip()
                    pg.mixer.music.load('coke.mp3')
                    pg.mixer.music.play()
    
            # Leaves
            for word in leaves:
                if re.search(word, labels, re.IGNORECASE):
                    print('coke')
                    screen.blit(face4, (0, 0))
                    pg.display.flip()
                    pg.mixer.music.load('leaves.mp3')
                    pg.mixer.music.play()


                
if __name__ == '__main__':
        main()
