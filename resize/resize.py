from PIL import Image
import os

def resize(img_file):
    img = Image.open(img_file)
    img_x = img.width
    img_y = img.height

    if img_x/200 > img_y/280:
        resize_x = 280
        resize_y = img_y/img_x*280
    else:
        resize_x = img_x/img_y*200
        resize_y = 200    
    
    img_resized = img.resize((int(resize_x), int(resize_y)))
    return img_resized

input_path  =  r"input"
output_path =  r"output"

files = os.listdir(input_path)
file_list = [f for f in files if os.path.isfile(os.path.join(input_path, f))]

if not os.path.exists(output_path):
    os.makedirs(output_path)

for imgfile in file_list:
    resized_img = resize(input_path + '/' + imgfile)
    resized_img.save( output_path + '/' + imgfile, quality=90)