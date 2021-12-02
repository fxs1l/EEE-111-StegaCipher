from PIL import Image
import os

def manipulate_image(filename):

	image = Image.open(filename)
	pixels = list(image.getdata())
	new_pixels = []
	for pixel in pixels:
		print(pixel) #Prints the RGB values for each pixel
		rgb = list(pixel)
		rgb[2] = int(rgb[2] / 2) # Halves the blue values of the pixel
		pixel = tuple(rgb)
		new_pixels.append(pixel)
	image.putdata(new_pixels)
	image.save("filtered_" + filename)
	
#Assuming the input is a JPEG/JPG file and is in the same directory
filename = ''
while (not os.path.isfile(filename)):
	print('Please input a valid filename: ')
	filename = input()
print("File found")

manipulate_image(filename)
