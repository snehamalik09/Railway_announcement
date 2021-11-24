import os
import pandas as pd
from pydub import AudioSegment
from gtts import gTTS
import pygame 
import PIL.ImageTk, PIL.Image 
import cv2
from functools import partial
import tkinter

# This function will play the announcement
pygame.mixer.init()
def play(announce):
    pygame.mixer.music.load(announce)
    pygame.mixer.music.set_volume(100)
    pygame.mixer.music.play()


def canva():
    # tkinter GUI code
    window=tkinter.Tk()
    SET_WIDTH=647
    SET_HEIGHT=404
    window.title("Indian Railways Announcement Software")
    cv_img=cv2.cvtColor(cv2.imread("Railwayimage.png"), cv2.COLOR_BGR2RGB)
    canvas=tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
    photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
    image_on_canvas=canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
    canvas.pack(fill="x")
    btn=tkinter.Button(text="From Bareily to Delhi, Train no. 14315", width=50, command=partial(play, "announcement_1 4 3 1 5.mp3"))
    btn.pack()
    btn=tkinter.Button(text="From Amritsar to Howrah, Train no. 14316", width=50, command=partial(play, "announcement_1 4 3 1 6.mp3"))
    btn.pack()
    btn=tkinter.Button(text="From Malda town to Delhi Train no. 2264", width=50, command=partial(play, "announcement_2 2 6 4 5.mp3"))
    btn.pack()
    btn=tkinter.Button(text="From Delhi to Dehradun, Train no. 33681", width=50, command=partial(play, "announcement_3 3 6 8 1.mp3"))
    btn.pack()
    window.mainloop()


def textToSpeech(text, filename):
    for i in range(1,22):
        mytext = str(text)
        if i>11:
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False, tld="com")
            myobj.save(filename)
            i+=1
        else:
            language = 'hi'
            myobj = gTTS(text=mytext, lang=language, slow=False, tld="com")
            myobj.save(filename)
            i+=1
        
    
# This function returns pydubs audio segment
def mergeAudios(audios):
    combined = AudioSegment.empty()
    for audio in audios:
        combined += AudioSegment.from_mp3(audio)
    return combined
  

def generateSkeleton():
    audio = AudioSegment.from_mp3('railway.mp3')

    # 1. Generate kripya dheyan dijiye
    start = 88000
    finish = 90200
    audioProcessed = audio[start:finish]
    audioProcessed.export("1_hindi.mp3", format="mp3")

    # 2. is from-city

    # 3. Generate se chalkar
    start = 91000
    finish = 92200
    audioProcessed = audio[start:finish]
    audioProcessed.export("3_hindi.mp3", format="mp3")

    # 4. is via-city

    # 5. generate ke raaste
    start = 94000
    finish = 95000
    audioProcessed = audio[start:finish]
    audioProcessed.export("5_hindi.mp3", format="mp3")

    # 6. is to-city

    # 7. Generate ko jaane wali gaadi sakhya
    start = 96000
    finish = 98900
    audioProcessed = audio[start:finish]
    audioProcessed.export("7_hindi.mp3", format="mp3")

    # 8. is train no and name

    # 9. Generate kuch hi samay mei platform sankhya
    start = 105500
    finish = 108200
    audioProcessed = audio[start:finish]
    audioProcessed.export("9_hindi.mp3", format="mp3")

    # 10. is platform number

    # 11. Generate par aa rahi hai
    start = 109000
    finish = 112250
    audioProcessed = audio[start:finish]
    audioProcessed.export("11_hindi.mp3", format="mp3")

    # 12. Generate May i have your attention please train no.
    start=111000
    finish=116000
    audioProcessed=audio[start:finish]
    audioProcessed.export("12_english.mp3", format="mp3")

    # 13. Train no and train name

    # 14. Generate from
    start=122500
    finish=123500
    audioProcessed=audio[start:finish]
    audioProcessed.export("14_english.mp3", format="mp3")

    # 15. from city 

    # 16. Generate to
    start=124000
    finish=124750
    audioProcessed=audio[start:finish]
    audioProcessed.export("16_english.mp3", format="mp3")
    

    # 17. to city

    # 18. Generate via
    start=125500
    finish=127000
    audioProcessed=audio[start:finish]
    audioProcessed.export("18_english.mp3", format="mp3")

    # 19. via city
    
    # 20. Generate is arriving shortly on platform number
    start=129000
    finish=133000
    audioProcessed=audio[start:finish]
    audioProcessed.export("20_english.mp3", format="mp3")

    # 21. platform number


def generateAnnouncement(filename):
    df = pd.read_excel(filename)
    for index, item in df.iterrows():
        # 2 - Generate from-city
        textToSpeech(item['from'], '2_hindi.mp3')

        # 4 - Generate via-city
        textToSpeech(item['via'], '4_hindi.mp3')

        # 6 - Generate to-city
        textToSpeech(item['to'], '6_hindi.mp3')

        # 8 - Generate train no and name
        textToSpeech(item['train_no'] + " " + item['train_name'], '8_hindi.mp3')

        # 10 - Generate platform number
        textToSpeech(item['platform'], '10_hindi.mp3')

        # 13. Generate Train no and train name
        textToSpeech(item["train_no"] + " " + item["train_name"], "13_english.mp3")
 
        # 15. Generate from city
        textToSpeech(item["from"], "15_english.mp3")
 
        # 17. Generate to city
        textToSpeech(item["to"], "17_english.mp3")
 
        # 19. Generate via city
        textToSpeech(item["via"], "19_english.mp3")

        # 21. Generate platform number
        textToSpeech(item["platform"], "21_english.mp3")

        # Creating a list of all the audio pieces
        audios=[]
        for i in range(1,22):
            if i<12:
                audios.append(f"{i}_hindi.mp3")
                i+=1
            else:
                audios.append(f"{i}_english.mp3")
                i+=1

        announcement = mergeAudios(audios)
        announcement.export(f"announcement_{item['train_no']}.mp3", format="mp3")

if __name__=='__main__':
    print("Generating Skeleton...")
    generateSkeleton()
    print("Now Generating Announcement...")
    generateAnnouncement("announce_hindi.xlsx")
    canva()



 
