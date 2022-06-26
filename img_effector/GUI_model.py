import os
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from datetime import datetime
from PIL import Image, ImageFilter, ImageOps, ImageTk, ImageEnhance


class GUI_model:
    def __init__(self):
        self.file_filter = [("Image file", ".bmp .png .jpg .tif")]

    def get_path(self):
        return filedialog.askopenfilename(
            title="Please select image file,", filetypes=self.file_filter
        )

    def save_image(self, save_img, path_var):

        if save_img != None:
            name, ext = os.path.splitext(path_var)
            dt = datetime.now()
            fpath = name + "_" + dt.strftime("%H%M%S") + ".png"

            save_img.save(fpath)
            # print("Saved: {}".format(fpath))

    def resize_image(self, path, base_canvas, effect_canvas):

        resize_img = Image.open(path)

        w = resize_img.width
        h = resize_img.height
        w_offset = 250 - (w * (500 / h) / 2)
        h_offset = 250 - (h * (500 / w) / 2)

        if w > h:
            resize_img = resize_img.resize((int(w * (500 / w)), int(h * (500 / w))))
        else:
            resize_img = resize_img.resize((int(w * (500 / h)), int(h * (500 / h))))

        self.pil_base_img = ImageTk.PhotoImage(resize_img)
        self.pil_effect_img = self.pil_base_img

        if w > h:
            base_img_canvas = base_canvas.create_image(
                0, h_offset, anchor="nw", image=self.pil_base_img
            )
            effect_canvas_create = effect_canvas.create_image(
                0, h_offset, anchor="nw", image=self.pil_effect_img
            )
        else:
            base_img_canvas = base_canvas.create_image(
                w_offset, 0, anchor="nw", image=self.pil_base_img
            )
            effect_canvas_create = effect_canvas.create_image(
                w_offset, 0, anchor="nw", image=self.pil_effect_img
            )

        return resize_img, base_img_canvas, effect_canvas_create

    # effect image model
    def retouch_gray_scale(self, ef_img):
        convert_img = ef_img.convert("L")
        return convert_img

    def retouch_binarization(self, ef_img):
        converted_img = ef_img.point(lambda x: 0 if x < 230 else x)
        return converted_img

    def retouch_sepia(self, ef_img):
        converted_img = Image.merge(
            "RGB",
            (
                ef_img.point(lambda x: x * 240 / 255),
                ef_img.point(lambda x: x * 200 / 255),
                ef_img.point(lambda x: x * 145 / 255),
            ),
        )
        return converted_img

    def retouch_jagged_mosaic(self, ef_img):
        converted_img = ef_img.resize([x // 8 for x in ef_img.size]).resize(ef_img.size)
        return converted_img

    def retouch_soft_mosaic(self, ef_img):
        gimg = ef_img.filter(ImageFilter.GaussianBlur(4))
        converted_img = gimg.resize([x // 8 for x in ef_img.size]).resize(ef_img.size)
        return converted_img

    def retouch_alpha_blend(self, ef_img):
        converted_img = ef_img.quantize(4)
        return converted_img

    def retouch_invert(self, ef_img):
        converted_img = ImageOps.invert(ef_img.convert("RGB"))
        return converted_img

    def retouch_mirror(self, ef_img):
        converted_img = ImageOps.mirror(ef_img.convert("RGB"))
        return converted_img

    def retouch_flip(self, ef_img):
        converted_img = ImageOps.flip(ef_img.convert("RGB"))
        return converted_img

    def retouch_posterize(self, ef_img):
        converted_img = ImageOps.posterize(ef_img.convert("RGB"), 2)
        return converted_img

    def retouch_solarize(self, ef_img):
        converted_img = ImageOps.solarize(ef_img.convert("RGB"), 128)
        return converted_img

    def retouch_equalize(self, ef_img):
        converted_img = ImageOps.equalize(ef_img.convert("RGB"))
        return converted_img

    def retouch_counter(self, ef_img):
        converted_img = ef_img.filter(ImageFilter.CONTOUR)
        return converted_img

    def retouch_emboss(self, ef_img):
        converted_img = ef_img.filter(ImageFilter.EMBOSS)
        return converted_img

    def retouch_findemboss(self, ef_img):
        converted_img = ef_img.filter(ImageFilter.FIND_EDGES)
        return converted_img

    # def retouch_color_balance(self, ef_img,value):
    #    enhancer = ImageEnhance.Color(ef_img)
    ##    converted_img = enhancer.enhance(float(value))
    #    return converted_img

    def retouch_scale_items(
        self, ef_img, color_value, contrast_value, brightnes_value, sharpness_value
    ):
        enhancer = ImageEnhance.Color(ef_img)
        temp_img = enhancer.enhance(float(color_value))
        enhancer = ImageEnhance.Contrast(temp_img)
        temp_img = enhancer.enhance(float(contrast_value))
        enhancer = ImageEnhance.Brightness(temp_img)
        temp_img = enhancer.enhance(float(brightnes_value))
        enhancer = ImageEnhance.Sharpness(temp_img)
        converted_img = enhancer.enhance(float(sharpness_value))
        return converted_img
