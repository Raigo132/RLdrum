import pygame
from pydub import *
from tkinter import *

pygame.mixer.init(44100, -16, 10, 512)
pygame.init()
bg = pygame.display.set_mode((800,600))
pygame.display.set_caption("RL Drums")

t2hed = []
helid = {}
helid_pydub = {}
pildid = {}
pildid_bool = False

data = open("data.txt")
for rida in data:
    key, nimi = rida.split(":")
    nimi = nimi.strip()
    if nimi == "pildid":
        pildid_bool = True
        rida = data.readline()
        key, nimi = rida.split(":")
        nimi = nimi.strip()
    if pildid_bool == False:
        sound = pygame.mixer.Sound("C:\\Users\\Raigo\\PycharmProjects\\Trummid\\helid\\"+nimi.strip())
        helid[key] = sound

        t2hed.append(key)
        # Salvetamise jaoks eraldi failid
        pydub_sound = AudioSegment.from_wav("C:\\Users\\Raigo\\PycharmProjects\\Trummid\\helid\\"+nimi)
        helid_pydub[key] = pydub_sound
    else:
        pilt = pygame.image.load("C:\\Users\\Raigo\\PycharmProjects\\Trummid\\pildid\\"+nimi)
        pildid[key] = pilt
data.close()



def pilt(x,y,pilt,pilt_h = None,muuda_True = None,muuda_False = None):
    edastatav_pilt = pilt
    if pilt_h != None:
        if bg.blit(pilt, (x, y)).collidepoint(pygame.mouse.get_pos()):
            edastatav_pilt = pilt_h
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        global menuud
                        if muuda_True != None:
                            menuud[muuda_True] = True
                        if muuda_False != None:
                            menuud[muuda_False] = False
    bg.blit(edastatav_pilt, (x, y))
def menuu(pildid,menuud):
    pilt(0,0,pildid["peamenu"])
    pilt(465,380,pildid["seaded"],pildid["seaded_h"],"seaded","peamenuu")
    pilt(100,380,pildid["alusta"],pildid["alusta_h"],"playmode","peamenuu")
def seaded(pildid):
    pilt(0,0,pildid["nupud"])
    pilt(465,380,pildid["tagasi"],pildid["tagasi_h"],"peamenuu","seaded")
def play(helid, helid_pydub, pildid,salvestamine,t2hed):
    pilt(0,0,pildid["play_bg"])
    pilt(740,540,pildid["nool"],pildid["nool_h"],"peamenuu", "playmode")
    if  salvestamine["salvesta"] == True:
        pilt(740, 10, pildid["recnupp_rec"], pildid["recnupp_rec"])
        salvestamine["salvestamise_aeg"] = pygame.time.get_ticks()-salvestamine["salvestamise_algus"]
        print(salvestamine["salvestamise_aeg"])
    else:
        pilt(740, 10, pildid["recnupp"], pildid["recnupp"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global eivajutaX
            eivajutaX = True
        if event.type == pygame.KEYDOWN:
            t2ht = chr(event.key)
            if t2ht in t2hed:
                pygame.mixer.Sound.play(helid[t2ht])
                if salvestamine["salvesta"] == True:
                    salvestamine["salvestatav_klipp"] = salvestamine["salvestatav_klipp"].overlay(helid_pydub[t2ht],
                                                                position=salvestamine["salvestamise_aeg"])
            if event.key == pygame.K_RETURN:
                if salvestamine["salvesta"] == True:
                    salvestamine["salvesta"] = False
                    salvestamine["salvestatav_klipp"] = salvestamine["salvestatav_klipp"][:salvestamine["salvestamise_aeg"]]
                    AudioSegment.export(salvestamine["salvestatav_klipp"],"snafodaoif.wav")
                else:
                    salvestamine["salvesta"] = True
                    salvestamine["salvestamise_algus"] = pygame.time.get_ticks()
                    salvestamine["salvestamise_aeg"] = 0


eivajutaX = False
menuud = {"peamenuu":True,"seaded":False,"playmode":False,"Salvesta": False,}
tyhilaul =  AudioSegment.from_wav("C:\\Users\\Raigo\\PycharmProjects\\Trummid\\helid\\thi.wav")
salvestamine = { "salvesta":False,"salvestamise_algus":0, "salvestamise_aeg":0,
                "salvestatav_klipp":tyhilaul.overlay(tyhilaul, position=0)}
while eivajutaX == False:
    bg.fill((255, 255, 255))
    if menuud["peamenuu"]:
        menuu(pildid,menuud)
    if menuud["seaded"]:
        seaded(pildid)
    if menuud["playmode"]:
        play(helid,helid_pydub,pildid,salvestamine, t2hed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            eivajutaX = True

    pygame.display.update()
pygame.quit()