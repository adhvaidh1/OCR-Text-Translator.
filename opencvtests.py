import cv2
import deep_translator 
import numpy as np
import pytesseract
from deep_translator import GoogleTranslator, single_detection
# # img = cv2.imread("grayimg.png")
# # img = cv2.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # _,img2 = cv2.threshold(img, 90,255,cv2.THRESH_BINARY)
# # img2 = cv2.bitwise_not(img2)
# # img2 = cv2.rectangle(img2,(200,200),(300,300),(255,255,255),2)
# # img2 = cv2.circle(img2,(200,200),100,(255,255,255),5)
# # img2 = cv2.line(img2,(100,100),(400,100),(255,255,0),3)
# # img2 = cv2.putText(img2,"hello world",(100,100),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1)

img3 = cv2.imread("Hindi.png")
gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
_,img3 = cv2.threshold(gray, 160,255,cv2.THRESH_BINARY)
#print(pytesseract.image_to_string(img3))

himg, wimg = img3.shape
boxes = pytesseract.image_to_data(img3)
for x,b in enumerate(boxes.splitlines()):
    if x!= 0:
        b = b.split()
        print(b)
        #12 is the length of a item with a word in it / 11 is an item with empty value (no word)
        if len(b) == 12:
            original_text = b[11]
            x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img3, (x,y),(w+x,h+y),(0,0,0),3)
            #cv2.putText(img3,original_text,(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
            try:
                #finds which language the original text is in
                lang = single_detection(original_text, api_key="4a6d0a2c4b1703aaf37066f1807dccda")

                try:
                    #translates the text to english from the language that it found in lang
                    translated_text = GoogleTranslator(source=lang, target='english').translate(original_text)
                    cv2.putText(img3, translated_text, (x,y), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)

                #error handling for when the original language is enlgish,a nd it tries to translate to english.
                except deep_translator.exceptions.InvalidSourceOrTargetLanguage:
                    # cv2.putText(img3,original_text,(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
                    print(None)
            
            #other exception handling for english-to-english, etc.
            except IndexError:
                # cv2.putText(img3,original_text,(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
                print(None)

# contours, hierarchy = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# img3 = cv2.drawContours(img3, contours, -1, (0,255,255), 3)
# # img3 = cv2.boundingRect(img3)

# cv2.imshow("threshold",img2)
# cv2.imshow("orignal",img)

cv2.imshow("translation",img3)
cv2.waitKey(0)
cv2.destroyAllWindows()

