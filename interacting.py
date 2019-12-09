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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="det-cloud.json"
client = vision.ImageAnnotatorClient()

image = 'iamge.jpg'

from operator import add

directory = ['wood', 'robot', 'coke', 'leaves', 'rose']

direcotry_set = {'wood', 'robot', 'coke', 'leaves', 'rose'}

sounds = ['wood.wav','robot.wav', 'coke.wav', 'leaves.wav', 'rose.wav']

ambient = 'ambient.wav'

# List of all the possible words.
wood = ['wood']
robot = ['robot', 'paper']
coke = []
leaves = []
rose = []


def get_string(image):
    response = clinet.label_detection(image = image)
    labels = response.label_annotations

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
    pg.mixer.set_num_channels(2)

    channel1 = pg.mixer.Channel(0)
    channel2 = pg.mixer.Channel(1)

    channel1.play(pg.mixer.Sound('ambient.wav'), loops = -1)

    while True:

        title = 'Anatomy of Brain'
        width = 1800
        height = 1000

        # Loading the face function.
        face0 = pg.image.load('face0.jpg')
        face1 = pg.image.load('face1.jpg')
        face2 = pg.image.load('face2.jpg')
        face3 = pg.image.load('face3.jpg')
        face4 = pg.image.load('face4.jpg')

        screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        clock = pg.time.Clock()

        # Initial face.
        screen.blit(face0, (0, 0))


        takephoto(camera)

        with open('image.jpg', 'rb') as image_file:
            content = image_file.read()
            image = vision.types.Image(content=content)

            label_text = get_string(image)

            # Face detection.
            face_distinction()

            # Compassion.

            # Wood: Curious
            if re.search(wood[0], label_text, re.IGNORECASE) ||
                re.search(wood[1], label_text, re.IGNORECASE) :
                screen.blit(pic1, (0, 0))
                pg.display.flip()
                channel1.play(pg.mixer.Sound('wood.wav'), loops = 1)

            # Robot: Love
            if re.search(robot[0], label_text, re.IGNORECASE) ||
                re.search(robot[0], label_text, re.IGNORECASE):
                screen.blit(pic2, (0, 0))
                pg.display.flip()
                channel1.play(pg.mixer.Sound('robot.wav'), loops = 1)

            # Can: Angry
            if re.search(coke[0], label_text, re.IGNORECASE) ||
                re.search(coke[1], label_text, re.IGNORECASE):
                screen.blit(pic3, (0, 0))
                pg.display.flip()
                channel1.play(pg.mixer.Sound('coke.wav'), loops = 1)

            # Leaves: Joy
            if re.search(leaves[0], label_text, re.IGNORECASE) ||
                re.search(leaves[1], label_text, re.IGNORECASE):
                screen.blit(pic4, (0, 0))
                pg.display.flip()
                channel1.play(pg.mixer.Sound('leaves.wav'), loops = 1)

            #if re.search(rose[0], label_text, re.IGNORECASE):
                #screen.blit(pic5, (0, 0))
                #pg.display.flip()
                #channel1.play(pg.mixer.Sound('rose.wav'), loops = 1)
