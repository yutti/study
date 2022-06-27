import sys
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageOps, ImageTk

from GUI_control import GUI_control


class Set_gui:
    def __init__(self, main_window):

        # controller Class生成
        self.control = GUI_control()

        # Variable setting
        self.function_btn = [
            "Default",
            "Gray_scale",
            "Binarization",
            "Sepia",
            "Jagged_mosaic",
            "Soft_mosaic",
            "Quantize",
            "Invert",
            "Mirror",
            "Flip",
            "Posterize",
            "Solarize",
            "Equalize",
            "Counter",
            "Emboss",
            "Find_emboss",
        ]
        self.canvas_title = ["Base", "Effect"]
        self.scale_effect = ["Color Balance", "Contrast", "Brightnes", "Sharpness"]

        # Main window
        self.main_window = main_window
        self.main_window.geometry("1400x800")
        self.main_window.title("Image Editor v0.10")

        # Sub window
        self.canvas_frame = tk.Frame(self.main_window, height=450, width=400)
        self.filepath_frame = tk.Frame(self.main_window, height=100, width=400)
        self.func_frame = tk.Frame(self.main_window, height=100, width=400)
        self.scale_frame = tk.Frame(self.main_window, height=350, width=400)
        self.opr_frame = tk.Frame(self.main_window, height=100, width=400)

        # Widgetsmith
        self.canvas_frame.place(relx=0.05, rely=0.05)
        self.filepath_frame.place(relx=0.05, rely=0.8)
        self.func_frame.place(relx=0.80, rely=0.15)
        self.scale_frame.place(relx=0.80, rely=0.25)
        self.opr_frame.place(relx=0.80, rely=0.75)

        # 1.1 canvas_frame (label)
        self.set_up_canvas_label(self.canvas_frame)

        # 1.2 canvas_frame (canvas)
        self.base_canvas = self.set_up_canvas_frame(self.canvas_frame)
        self.base_canvas.grid(row=1, column=0)

        self.effect_canvas = self.set_up_canvas_frame(self.canvas_frame)
        self.effect_canvas.grid(row=1, column=1)

        # 2. filepath_frame
        self.img_path_btn = tk.Button(
            self.filepath_frame,
            text="Select_image_file",
            command=self.draw_default_image,
        )
        self.img_path_btn.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        self.img_path_stvar = tk.StringVar()
        self.img_path_entry = tk.Entry(
            self.filepath_frame, textvariable=self.img_path_stvar, width=70
        )
        self.img_path_entry.grid(row=1, column=0, sticky=tk.EW, padx=10)

        # 3. func_frame
        self.func_combobox = ttk.Combobox(
            self.func_frame,
            text="combo_file",
            state="readonly",
            value=self.function_btn,
            width=30,
        )
        self.func_combobox.set(self.function_btn[0])
        self.func_combobox.bind("<<ComboboxSelected>>", self.effect_event)
        self.func_combobox.pack()

        # 4.1 scale_frame (label)
        self.set_up_scale_label(self.scale_frame)

        # 4.2 scale_frame (botton)
        self.color_scale = self.set_up_scale(self.scale_frame, 1)
        self.color_scale.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)

        self.contrast_scale = self.set_up_scale(self.scale_frame, 1)
        self.contrast_scale.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

        self.brightnes_scale = self.set_up_scale(self.scale_frame, 1)
        self.brightnes_scale.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)

        self.sharpness_scale = self.set_up_scale(self.scale_frame, 2)
        self.sharpness_scale.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)

        # 5 opr_frame
        self.button = self.set_up_opr_btn(self.opr_frame, "Save", self.on_click_save)
        self.button.grid(row=0, column=0, sticky=tk.SE, padx=10, pady=10)

        self.button = self.set_up_opr_btn(self.opr_frame, "Exit", self.on_click_close)
        self.button.grid(row=0, column=1, sticky=tk.SE, padx=10, pady=10)

    def set_up_canvas_label(self, set_frame):
        for i in range(2):
            label = tk.Label(
                set_frame, text=self.canvas_title[i], bg="white", relief=tk.RIDGE,
            )
            label.grid(row=0, column=i, sticky=tk.W + tk.E)

    def set_up_canvas_frame(self, set_frame):
        return tk.Canvas(set_frame, width=500, height=500, bg="#A9A9A9")

    def set_up_scale_label(self, set_frame):
        for i in range(4):
            label = tk.Label(set_frame, text=self.scale_effect[i])
            label.grid(row=i, column=0, sticky=tk.W)

    def set_up_opr_btn(self, set_frame, btn_name, act_command):
        return tk.Button(set_frame, text=btn_name, width=10, command=act_command)

    def set_up_scale(self, set_frame, scale_end):
        set_scale = tk.Scale(
            set_frame,
            from_=0,
            to=scale_end,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            command=self.adjust_scale_value,
        )
        return set_scale

    def on_click_save(self):
        self.img_path_var = self.img_path_stvar.get()
        self.control.save_image_action(self.converted_img, self.img_path_var)

    def on_click_close(self):
        self.main_window.destroy()

    def draw_default_image(self):
        self.img_path = self.control.get_image_path()
        self.img_path_stvar.set(self.img_path)

        (
            self.effect_img,
            self.base_canvas_create,
            self.effect_canvas_create,
        ) = self.control.draw_image(self.img_path, self.base_canvas, self.effect_canvas)

        # scale value intialize
        self.replace_canvas_image(
            self.effect_img, self.base_canvas, self.base_canvas_create
        )
        self.replace_canvas_image(
            self.effect_img, self.effect_canvas, self.effect_canvas_create
        )
        self.converted_img = self.effect_img
        self.color_scale.set(1)
        self.contrast_scale.set(1)
        self.brightnes_scale.set(1)
        self.sharpness_scale.set(1)

    def effect_event(self, arg):
        self.converted_img = self.control.effect_image(
            self.effect_img, self.func_combobox
        )
        self.replace_canvas_image(
            self.converted_img, self.effect_canvas, self.effect_canvas_create
        )

    def replace_canvas_image(self, pic_img, canvas_name, canvas_name_create):
        canvas_name.photo = ImageTk.PhotoImage(pic_img)
        canvas_name.itemconfig(canvas_name_create, image=canvas_name.photo)

    def adjust_scale_value(self, value):
        color_value = self.color_scale.get()
        contrast_value = self.contrast_scale.get()
        brightnes_value = self.brightnes_scale.get()
        sharpness_value = self.sharpness_scale.get()

        self.adjusted_img = self.control.adjust_color_balance(
            self.converted_img,
            color_value,
            contrast_value,
            brightnes_value,
            sharpness_value,
        )
        self.replace_canvas_image(
            self.adjusted_img, self.effect_canvas, self.effect_canvas_create
        )


def main():

    # 　Tk MainWindow
    main_window = tk.Tk()

    # Viewクラス生成
    Set_gui(main_window)

    # 　フレームループ処理
    main_window.mainloop()


if __name__ == "__main__":
    main()
