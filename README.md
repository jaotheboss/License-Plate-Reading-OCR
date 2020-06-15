# License-Plate-Reading-OCR
I attempt to create a model that is able to 'look' at picture of cars and return the text version of their number plate number. 

## Objective:
It's simple for humans but complex for machines. I attempt to create a model that will look at cars, detect where's the license plate, segment that out and 'read it', return what it read in string format.

## Methodology:
The main method comprises of 2 parts. The objective of the first part is to be able to detect where's the license plate on the car. Using OpenCV, I retrieved the coordinates for where the model detects rectangular boxes. I had to filter these out by the size of the license plate. After sieving through all the non-license plate coordinates, i created a new image of the zoomed license plate. This will make it easier for the next step, which is to read the numbers off the picture. We zoom into the license plate so as to reduce noise and non-essential information. 

Now that we have a zoomed image of the license plate, we implement a module that is able to segment the individual characters in the picture and churn out a string. Now that the bulk of the project is done and dusted, all i had to do was to clean the string for the license plate numbers only. There was another method that i was going to employ but could not do so due to the lack of training data. The other method was to segment each of the digits of the license plate into their individual photo (as you can see from the ROI files in the repo), then use another model to read them. However, i could not find a reasonable training set for this font. 

This second method is a lot harder than it sounds. Although churning out the individual digits sounds easy, things we have to consider is whether or not the digit segmentation cares about the order that of the images that is being churned out. Hence, we also had to make sure that when the model detects the segmentation, we are able to label each of these detections in order from left-to-right.

## Evaluation:
I think more can be done when it comes to cleaning the image before processing it through OpenCV. Perhaps contrasting the image so that OpenCV can better detect rectangles. As of right now the model has trouble looking at images of cars that are taken at night. This could be due to the pixels are being roughly of the same value, and if we reduce the threshold to detect edges, we might end up with more difficulties. 

I think when i come back to this project I'll explore license plate detection on videos in real-time.

## Images:

#### The Original Image
![Original](https://github.com/jaotheboss/License-Plate-Reading-OCR-/blob/master/example_2.jpg)

#### Annotated Image
![Annotated](https://github.com/jaotheboss/License-Plate-Reading-OCR-/blob/master/Annotated%20Image.png)

#### Zoomed Image
![Zoomed](https://github.com/jaotheboss/License-Plate-Reading-OCR-/blob/master/Zoomed%20Image.png)

#### Results
![Results](https://github.com/jaotheboss/License-Plate-Reading-OCR-/blob/master/Results.png)
