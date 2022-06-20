
from PIL import Image, ImageTk, ImageOps
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
class GUI_control():

    def __init__(self):
        self.file_filter = [("Image file", ".bmp .png .jpg .tif")]    

    # Function for closing window
        
    def get_image_path(self):
        img_file_path = filedialog.askopenfilename(title = "Please select image file,",filetypes =  self.file_filter)
        return img_file_path

    def resize_image(self, im_path,base_canvas,effect_canvas):
        resize_img = Image.open(im_path)
        w = resize_img.width 
        h = resize_img.height 
        w_offset = 250-(w*(500/h)/2)
        h_offset = 250-(h*(500/w)/2)
        
        if w > h:
            resize_img = resize_img.resize(( int(w * (500/w)), int(h * (500/w)) ))
        else:
            resize_img = resize_img.resize(( int(w * (500/h)), int(h * (500/h)) ))
       
        self.pil_base_img   = ImageTk.PhotoImage(resize_img)
        self.pil_effect_img = self.pil_base_img

        if w > h:
            base_img_canvas = base_canvas.create_image(0, h_offset, anchor='nw', image=self.pil_base_img)
            effect_canvas_create = effect_canvas.create_image(0, h_offset, anchor='nw', image=self.pil_effect_img)
        else:
            base_img_canvas   = base_canvas.create_image(w_offset, 0, anchor='nw', image=self.pil_base_img)
            effect_canvas_create = effect_canvas.create_image(w_offset, 0, anchor='nw', image=self.pil_effect_img)
       
        return resize_img, base_img_canvas, effect_canvas_create
        
        
    def effect_image(self, func_no, func_name,effect_img):

        if func_no <= 3:
            convert_img = effect_img.convert('L')
        
            if func_name == "Gray_scale":
                converted_img = convert_img

            elif func_name == "Binarization":
                converted_img = convert_img.point(lambda x: 0 if x < 230 else x) 

            elif func_name == "Sepia":
                converted_img = Image.merge(
                    "RGB",
                    (      
                        convert_img.point(lambda x: x * 240 / 255),
                        convert_img.point(lambda x: x * 200 / 255),
                        convert_img.point(lambda x: x * 145 / 255)
                    )
                )
        return converted_img
  
