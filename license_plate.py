import cv2
from imutils import contours
import pytesseract
import re
import numpy as np
import matplotlib.pyplot as plt

plate = cv2.imread('example_2.jpg')
plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
# plate_binary = cv2.bitwise_not(plate)
# plt.imshow(plate, cmap = 'gray')

# classification model that will be used to detect the car plates in the image
# plate_cascade = cv2.CascadeClassifier('cascade.xml')
plate_cascade = cv2.CascadeClassifier('/Users/jaoming/anaconda3/pkgs/libopencv-3.4.2-h7c891bd_1/share/OpenCV/haarcascades/haarcascade_russian_plate_number.xml')

# function that will automate the usage of the model to identify the car plate in the image
def detect_plate(img):
       """
       Function:     Uses the cascade classifier to detect car plates

       Inputs:       Image

       Returns:      Same image with a rectangle drawn on the carplate
       """
       plate_img = img.copy()

       # getting the coordinates of the carplate in the image
       plate_coord = plate_cascade.detectMultiScale(plate_img, 
                                                 scaleFactor = 1.2,
                                                 minNeighbors = 10)
       # drawing the rectangle
       for x, y, w, h in plate_coord:
              cv2.rectangle(img = plate_img, 
                            pt1 = (x, y), 
                            pt2 = (x + w, y + h), 
                            color = (255, 0, 0), 
                            thickness = 5)
       # (_, contours, _) = cv2.findContours(plate_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
       
       # for contour in contours:
       #        (x, y, w, h) = cv2.boundingRect(contour)
       #        print((x, y, w, h))
       #        cv2.rectangle(plate_img, (x, y), (x + w, y + h), (255, 0, 0), 10)
       return plate_img

anno_plate = detect_plate(plate)
plt.imshow(anno_plate)

# function that would zoom into the bounding box
def zoom_plate(img):
       """
       Function:     Will use the cascade classifier to detect the license plate and zoom into it

       Inputs:       Image

       Returns:      Zoomed image
       """
       plate_img = img.copy()

       # getting the coordinates of the carplate in the image
       plate_coord = plate_cascade.detectMultiScale(plate_img, 
                                                 scaleFactor = 1.2,
                                                 minNeighbors = 10)
       
       for x, y, w, h in plate_coord:
              # getting the points that show the license plate
              zoomed_img = plate_img[y:y+h, x:x+w]

              # resizing
              zoomed_img = cv2.resize(zoomed_img, (0, 0), fx = 2, fy = 2)
              # zoomed_img = zoomed_img[7:-7,7:-7]

              # sharpening the image
              kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
              zoomed_img = cv2.filter2D(zoomed_img, -1, kernel)
       if plate_coord:
              return zoomed_img
       else:
              raise ValueError('Was unable to detect a license plate in the image')

zoomed_plate = zoom_plate(plate)
plt.imshow(zoomed_plate)

# function that will extract the string of the license plate
def plate_string(img):
       # extract all strings from the image
       text = pytesseract.image_to_string(img)

       # clean the string
       text = re.sub("[^a-zA-Z1234567890]", ' ', text).split(' ')
       text = [i for i in text if i != '']
       text = [i for i in text if re.search('[0-9]', i)]
       if len(text) == 1:
              return text[0]
       return text
print('Based on CV2 and PYTESSERACT, THE NO. PLATE SHOWS:')
print(plate_string(zoomed_plate))

# function that will return a list of images of each digit on the license plate
def plate_digits(img):
       """
       Function:     Create a list of images where each image is the digit on the license plate

       Inputs:       Image

       Returns:      List of images (all of which are 100 x 100)
       """
       mask = np.zeros(zoom_plate.shape, dtype = np.uint8)
       gray = cv2.cvtColor(zoom_plate, cv2.COLOR_BGR2GRAY)
       thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]    # contrast the image

       cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
       cnts = cnts[0] if len(cnts) == 2 else cnts[1]
       (cnts, _) = contours.sort_contours(cnts, method = 'left-to-right')
       # ROI_number = 0
       result = []
       for c in cnts:
              area = cv2.contourArea(c)
              if area > 1000 and area < 3000:
                     x, y, w, h = cv2.boundingRect(c)
                     ROI = 255 - thresh[(y - 8):(y+h+8), (x-8):(x+w+8)]                               # just inverts the colors
                     ROI = cv2.resize(ROI, dsize = (100, 100), interpolation = cv2.INTER_LANCZOS4)
                     result.append(ROI)
                     # cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)
                     # cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)            # this exports an image file
                     # ROI_number += 1
       return result

indiv_digits = plate_digits(zoom_plate)
# for d in indiv_digits:
#        cv2.imshow('digit', d)             # will pop up in a separate window
#        cv2.waitKey()
