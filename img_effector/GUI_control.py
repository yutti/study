from GUI_model import GUI_model


class GUI_control:
    def __init__(self):
        self.model = GUI_model()

    # Function for closing window

    def save_image_action(self, save_img, path_bar):
        self.model.save_image(save_img, path_bar)

    def get_image_path(self):
        img_file_path = self.model.get_path()
        return img_file_path

    def draw_image(self, im_path, base_canvas, effect_canvas):
        resize_img, base_img_canvas, effect_canvas_create = self.model.resize_image(
            im_path, base_canvas, effect_canvas
        )
        return resize_img, base_img_canvas, effect_canvas_create

    def effect_image(self, effect_img, func_combobox):

        func_no = func_combobox.current()
        func_name = func_combobox.get()

        if func_no <= 3 and func_no >= 1:
            convert_img = self.model.retouch_gray_scale(effect_img)

            if func_name == "Gray_scale":
                converted_img = convert_img

            elif func_name == "Binarization":
                converted_img = self.model.retouch_binarization(convert_img)

            elif func_name == "Sepia":
                converted_img = self.model.retouch_sepia(convert_img)

        elif func_name == "Default":
            converted_img = effect_img

        elif func_name == "Jagged_mosaic":
            converted_img = self.model.retouch_jagged_mosaic(effect_img)

        elif func_name == "Soft_mosaic":
            converted_img = self.model.retouch_soft_mosaic(effect_img)

        elif func_name == "Quantize":
            converted_img = self.model.retouch_alpha_blend(effect_img)

        elif func_name == "Invert":
            converted_img = self.model.retouch_invert(effect_img)

        elif func_name == "Mirror":
            converted_img = self.model.retouch_mirror(effect_img)

        elif func_name == "Flip":
            converted_img = self.model.retouch_flip(effect_img)

        elif func_name == "Posterize":
            converted_img = self.model.retouch_posterize(effect_img)

        elif func_name == "Solarize":
            converted_img = self.model.retouch_solarize(effect_img)

        elif func_name == "Equalize":
            converted_img = self.model.retouch_equalize(effect_img)

        elif func_name == "Counter":
            converted_img = self.model.retouch_counter(effect_img)

        elif func_name == "Emboss":
            converted_img = self.model.retouch_emboss(effect_img)

        elif func_name == "Find_emboss":
            converted_img = self.model.retouch_findemboss(effect_img)

        return converted_img
