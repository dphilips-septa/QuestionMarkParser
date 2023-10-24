import base64, binascii
import cv2
import numpy as np
import sys

class Converter:

    def __init__(self, base64, fileName):
        self.__base64Text = base64
        self.__fileName = fileName
        self.__convert()
    
    def __convert(self):
        try:
            # Converts the Base64 string into bytes
            image = base64.b64decode(self.__base64Text, validate=True)
            with open(self.__fileName, "wb") as f:
                f.write(image)
            self.__removeWhitespace()
        except binascii.Error as e:
            pass
    
    def __getPixelArray(self, image):
        # Get the height and width of the image
        height, width = image.shape[:2]

        # Create a 2D array to store the pixel colors with set parameters
        pixel_colors = np.zeros((height, width, 3))

        # Loop through each row then column to save each pixel
        for i in range(height):
            for j in range(width):
                pixel_colors[i][j] = image[i][j]
        return pixel_colors
    

    # Method for cropping image to remove all whitespace
    def __removeWhitespace(self):
        # Read image based on given filename
        image = cv2.imread(self.__fileName)

        # Run and save the array of rgb values
        pixels = self.__getPixelArray(image)

        # Preset variables for algorithmic search
        left, right, top, bottom = sys.maxsize,-1,sys.maxsize,-1
        for row_num in range(len(pixels)):
            for col_num in range(len(pixels[row_num])):
                r,g,b = pixels[row_num][col_num]
                
                # This variable refers to the darkest color that will be cutoff in order
                # to recieve the photo, and only the photo
                cutoff = 243
                if r < cutoff and g < cutoff and b < cutoff:
                    
                    # Check to see if the current white spot is further left than the left most value
                    if col_num < left:
                        left = col_num
                    # Check to see if the current white spot is further right than the right most value
                    elif col_num > right:
                        right = col_num

                    # Check to see if the current white spot is further up than the upper most value
                    if row_num < top:
                        top = row_num
                    # Check to see if the current white spot is further down than the lower most value
                    elif row_num > bottom:
                        bottom = row_num

        # Crop the image based on the calculated values
        image = self.__crop(image, left, right, top, bottom)
        
        cv2.imwrite(self.__fileName, image)
    
    def __crop(self, image, left : int, right : int, top : int, bottom : int):
        return image[top : bottom,
                     left : right]
