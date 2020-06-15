# License-Plate-Reading-OCR
I attempt to create a model that is able to 'look' at picture of cars and return the text version of their number plate number. 

## Objective:
It's simple for humans but complex for machines. I attempt to create a model that will look at cars, detect where's the license plate, segment that out and 'read it', return what it read in string format.

## Methodology:
The main method comprises of 2 parts. The objective of the first part is to be able to detect where's the license plate on the car. Using OpenCV, I retrieved the coordinates for where the model detects rectangular boxes. I had to filter these out by the size of the license plate. After sieving through all the non-license plate coordinates, i created a new image of the zoomed license plate. This will make it easier for the next step, which is to read the numbers off the picture. We zoom into the license plate so as to reduce noise and non-essential information. 

Now that we have a zoomed image of the license plate, we implement a module that is able to segment the individual characters in the picture and churn out a string. Now that the bulk of the project is done and dusted, all i had to do was to clean the string for the license plate numbers only. There was another method that i was going to employ but could not do so due to the lack of training data. The other method was to segment each of the digits of the license plate into their individual photo (as you can see from the ROI files in the repo), then use another model to read them. However, i could not find a reasonable training set for this font. 

This second method is a lot harder than it sounds. Although churning out the individual digits sounds easy, things we have to consider is whether or not the digit segmentation cares about the order that of the images that is being churned out. Hence, we also had to make sure that when the model detects the segmentation, we are able to label each of these detections in order from left-to-right.

## Images:
