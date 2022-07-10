import cv2
import deep_translator  
import pytesseract
from deep_translator import GoogleTranslator
import urllib3
import json

capture = cv2.VideoCapture("http://192.168.4.205:8080/video")
while capture.isOpened():
    ret,frame = capture.read()
    if ret:
        frame = cv2.resize(frame, (0,0),fx=0.5,fy=0.5)
        cv2.imshow("Video",frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('e'):
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            _,gray = cv2.threshold(gray,160,255,cv2.THRESH_BINARY)
            boxes = pytesseract.image_to_data(gray)
            for x,b in enumerate(boxes.splitlines()):
                if x != 0:
                    b = b.split()
                    print(b)
                    #12 is the length of a item with a word in it / 11 is an item with empty value (no word)
                    if len(b) == 12:
                        original_text = b[11]
                        x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                        cv2.rectangle(gray, (x,y),(x+w,y+h),(0,0,0),3)
                        try:
                        #finds which language the original text is in

                            #url+query
                            url = "https://api.textgears.com/detect?key=BbUqLXH5ZcfsTARK&text={}".format(original_text)

                            #json formatting
                            http = urllib3.PoolManager()
                            jsondata = http.request('GET', url)
                            jsonstring = jsondata.data
                            jsonstring = jsonstring.decode('utf-8')
                            jsonobj = json.loads(jsonstring)

                            #using indicies to get to the reponse object we are looking for (language)
                            responsedict = jsonobj['response']
                            language = responsedict['language']

                            try:
                                #translates the text to english from the language that it found in lang
                                translated_text = GoogleTranslator(source=language, target='english').translate(original_text)
                                cv2.putText(gray, translated_text, (x,y-10), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)

                            #error handling for when the original language is enlgish,a nd it tries to translate to english.
                            except deep_translator.exceptions.InvalidSourceOrTargetLanguage:
                                print('error')
                        
                        #other exception handling for english-to-english, etc.
                        except IndexError:
                            print('error2')

                        cv2.imshow("Translated Image+Text",gray)

capture.release()
cv2.destroyAllWindows()