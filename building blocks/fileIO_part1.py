from PIL import Image

def access_file(filename):

   image = Image.open(filename)
   with open("file_logs.txt", "w", encoding = 'utf-8') as f:
       f.write(str(image))
       f.close()
   return image

