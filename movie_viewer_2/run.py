import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import cv2

from PIL import Image, ImageFilter, ImageOps, ImageTk, ImageEnhance

import threading


class Set_gui:
    def __init__(self, main_window):

        # Variable setting
        self.file_filter = [("Movie file", ".mp4")]
        self.set_movie = True
        self.thread_set = False
        self.start_movie = False
        self.video_frame = None
        self.video_cap = None
        self.video_reset = False
        self.run_one_frame = False
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

        # Main window
        self.main_window = main_window
        self.main_window.geometry("1400x800")
        self.main_window.title("Movie Editor v0.10")

        # Sub window
        self.canvas_frame = tk.Frame(self.main_window, height=450, width=400)
        # self.scale_frame = tk.Frame(self.main_window, height=100, width=400)
        self.path_frame = tk.Frame(self.main_window, height=100, width=400)
        self.func_frame = tk.Frame(self.main_window, height=100, width=400)
        self.opr_frame = tk.Frame(self.main_window, height=100, width=400)

        # Widgetsmith
        self.canvas_frame.place(relx=0.05, rely=0.05)
        # self.scale_frame.place(relx=0.05, rely=0.80)
        self.path_frame.place(relx=0.60, rely=0.2)
        self.func_frame.place(relx=0.60, rely=0.4)
        self.opr_frame.place(relx=0.60, rely=0.5)

        # 1.1 canvas_frame (label)
        self.title_label_grid(self.canvas_frame, "Movie", 0, 0)

        # 1.2 canvas_frame (canvas)
        self.canvas = tk.Canvas(self.canvas_frame, width=700, height=500, bg="#A9A9A9")
        self.canvas.grid(row=1, column=0)

        # 2 scale_frame
        # self.label = tk.Label(self.scale_frame, text="scale")
        # self.label.grid(row=0, column=0, sticky=tk.W)

        # self.cap_scale = self.set_up_cap_scale(self.scale_frame)
        # self.cap_scale.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        # self.cap_scale.grid(row=1, column=0, sticky=tk.W)

        # 3 path_frame
        self.btn_grid(self.path_frame, "Start", self.on_click_path, 0, 0, tk.W)

        self.path_stvar = tk.StringVar()
        self.path_entry_grid(self.path_frame, self.path_stvar, 1, 0)

        self.label_text = tk.StringVar(value="FPS:")
        self.label_grid(self.path_frame, self.label_text, 2, 0)

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

        # 4 opr_frame
        self.btn_grid(self.opr_frame, "Start", self.on_click_start, 1, 0, tk.SE)
        self.btn_grid(self.opr_frame, "Stop", self.on_click_stop, 1, 1, tk.SE)
        self.btn_grid(self.opr_frame, "Reset", self.on_click_reset, 1, 2, tk.SE)
        self.btn_grid(self.opr_frame, "Exit", self.on_click_close, 3, 2, tk.SE)

    def title_label_grid(self, set_frame, title, r_num, c_num):
        label = tk.Label(set_frame, text=title, bg="white", relief=tk.RIDGE)
        return label.grid(row=r_num, column=c_num, sticky=tk.W + tk.E)

    def label_grid(self, set_frame, title, r_num, c_num):
        label = tk.Label(set_frame, textvariable=title)
        return label.grid(row=r_num, column=c_num, sticky=tk.W, padx=10, pady=10)

    def path_entry_grid(self, set_frame, stver, r_num, c_num):
        path_entry = tk.Entry(set_frame, textvariable=stver, width=70)
        return path_entry.grid(row=r_num, column=c_num, sticky=tk.EW, padx=10)

    def btn_grid(self, set_frame, btn_name, act_command, r_num, c_num, stk):
        button = tk.Button(set_frame, text=btn_name, width=10, command=act_command)
        return button.grid(row=r_num, column=c_num, sticky=stk, padx=10, pady=10)

    def func_pack(self, set_frame, btn_name, act_command, r_num, c_num, stk):
        button = tk.Button(set_frame, text=btn_name, width=10, command=act_command)
        return button.grid(row=r_num, column=c_num, sticky=stk, padx=10, pady=10)

    def effect_event(self, arg):
        self.func_no = self.func_combobox.current()
        self.func_name = self.func_combobox.get()

    #    def set_up_cap_scale(self, set_frame):
    #        set_scale = tk.Scale(
    #            set_frame,
    #            from_=0,
    #            to=100,
    #            resolution=1,
    #            length=700,
    #            orient=tk.HORIZONTAL,
    #            command=self.adjust_scale_value,
    #        )
    #        return set_scale

    def on_click_path(self):
        self.movie_path = self.get_path()
        self.path_stvar.set(self.movie_path)
        self.run_one_frame = True
        # Movie standby.
        self.thread_set = True

        self.thread_main = threading.Thread(target=self.main_thread_func)
        self.thread_main.start()

    def on_click_start(self):
        self.start_movie = True

    def on_click_stop(self):
        self.start_movie = False

    def on_click_reset(self):
        self.start_movie = False
        self.video_reset = True

    #
    def on_click_close(self):
        self.start_movie = False
        self.set_movie = False

        # Block the calling thread until the thread represented by this instance end.
        if self.thread_set == True:
            self.thread_main.join()
            self.video_cap.release()

        self.main_window.destroy()

    def main_thread_func(self):

        self.video_cap = cv2.VideoCapture(self.movie_path)
        self.total_frame_count = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fps = int(self.video_cap.get(cv2.CAP_PROP_FPS))
        self.label_text.set("FPS:" + str(fps))
        FPS = 1 / (fps * 1)

        if self.video_frame is None:
            print("None")

        while self.set_movie:

            if self.start_movie:
                ret, self.video_frame = self.video_cap.read()

                if ret:
                    self.next_frame(self.video_frame)
                    time.sleep(FPS)

                    if self.set_movie == False:
                        break
                else:
                    self.start_movie = False

            elif self.video_reset:
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, self.video_frame = self.video_cap.read()
                self.next_frame(self.video_frame)
                self.video_reset = False

            elif self.run_one_frame:
                ret, self.video_frame = self.video_cap.read()
                self.next_frame(self.video_frame)
                self.run_one_frame = False

    def next_frame(self, frame):

        # convert color order from BGR to RGB
        pil = self.cvtopli_color_convert(self.video_frame)
        self.effect_img = self.resize_image(pil)
        self.converted_img = self.effect_image(self.effect_img)

        # To escape error. when close,not to run ImageTk.PhotoImage.
        if self.set_movie == False:
            return

        self.canvas_create = self.resizeimg_canvas(self.converted_img, self.canvas)
        self.canvas.photo = ImageTk.PhotoImage(self.converted_img)
        return self.canvas.itemconfig(self.canvas_create, image=self.canvas.photo)

    def adjust_scale_value(self, value):

        if self.video_frame is None:
            print("None")

        else:
            cap_scale = self.cap_scale.get()
            total_frame_count = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            read_cap_num = total_frame_count * (1 + cap_scale / 100)
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, read_cap_num)
            self.run_one_frame()

    def cvtopli_color_convert(self, video):
        rgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)

    # Model
    def resize_image(self, img):

        w = img.width
        h = img.height

        if w > h:
            resize_img = img.resize((int(w * (700 / w)), int(h * (700 / w))))
        else:
            resize_img = img.resize((int(w * (500 / h)), int(h * (500 / h))))

        return resize_img

    def resizeimg_canvas(self, resized_img, canvas):

        w = resized_img.width
        h = resized_img.height
        w_offset = 350 - (w / 2)
        h_offset = 250 - (h / 2)

        self.pil_img = ImageTk.PhotoImage(resized_img)

        canvas.delete("can_pic")

        if w > h:
            resized_img_canvas = canvas.create_image(
                0, h_offset, anchor="nw", image=self.pil_img, tag="can_pic"
            )

        else:
            resized_img_canvas = canvas.create_image(
                w_offset, 0, anchor="nw", image=self.pil_img, tag="can_pic"
            )

        return resized_img_canvas

    def get_path(self):
        return filedialog.askopenfilename(
            title="Please select image file", filetypes=self.file_filter
        )

    def effect_image(self, effect_img):

        func_name = self.func_combobox.get()
        convert_gray_img = self.retouch_gray_scale(effect_img)

        if func_name == "Gray_scale":
            converted_img = convert_gray_img

        elif func_name == "Binarization":
            converted_img = self.retouch_binarization(convert_gray_img)

        elif func_name == "Sepia":
            converted_img = self.retouch_sepia(convert_gray_img)

        elif func_name == "Default":
            converted_img = effect_img

        elif func_name == "Jagged_mosaic":
            converted_img = self.retouch_jagged_mosaic(effect_img)

        elif func_name == "Soft_mosaic":
            converted_img = self.retouch_soft_mosaic(effect_img)

        elif func_name == "Quantize":
            converted_img = self.retouch_alpha_blend(effect_img)

        elif func_name == "Invert":
            converted_img = self.retouch_invert(effect_img)

        elif func_name == "Mirror":
            converted_img = self.retouch_mirror(effect_img)

        elif func_name == "Flip":
            converted_img = self.retouch_flip(effect_img)

        elif func_name == "Posterize":
            converted_img = self.retouch_posterize(effect_img)

        elif func_name == "Solarize":
            converted_img = self.retouch_solarize(effect_img)

        elif func_name == "Equalize":
            converted_img = self.retouch_equalize(effect_img)

        elif func_name == "Counter":
            converted_img = self.retouch_counter(effect_img)

        elif func_name == "Emboss":
            converted_img = self.retouch_emboss(effect_img)

        elif func_name == "Find_emboss":
            converted_img = self.retouch_findemboss(effect_img)

        return converted_img

    # effect image model
    def retouch_gray_scale(self, ef_img):
        return ef_img.convert("L")

    def retouch_binarization(self, ef_img):
        return ef_img.point(lambda x: 0 if x < 230 else x)

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
        return ef_img.resize([x // 8 for x in ef_img.size]).resize(ef_img.size)

    def retouch_soft_mosaic(self, ef_img):
        gimg = ef_img.filter(ImageFilter.GaussianBlur(4))
        return gimg.resize([x // 8 for x in ef_img.size]).resize(ef_img.size)

    def retouch_alpha_blend(self, ef_img):
        return ef_img.quantize(4)

    def retouch_invert(self, ef_img):
        return ImageOps.invert(ef_img.convert("RGB"))

    def retouch_mirror(self, ef_img):
        return ImageOps.mirror(ef_img.convert("RGB"))

    def retouch_flip(self, ef_img):
        return ImageOps.flip(ef_img.convert("RGB"))

    def retouch_posterize(self, ef_img):
        return ImageOps.posterize(ef_img.convert("RGB"), 2)

    def retouch_solarize(self, ef_img):
        return ImageOps.solarize(ef_img.convert("RGB"), 128)

    def retouch_equalize(self, ef_img):
        return ImageOps.equalize(ef_img.convert("RGB"))

    def retouch_counter(self, ef_img):
        return ef_img.filter(ImageFilter.CONTOUR)

    def retouch_emboss(self, ef_img):
        return ef_img.filter(ImageFilter.EMBOSS)

    def retouch_findemboss(self, ef_img):
        return ef_img.filter(ImageFilter.FIND_EDGES)


def main():

    # 　Tk MainWindow
    main_window = tk.Tk()

    # Viewクラス生成
    Set_gui(main_window)

    # 　フレームループ処理
    main_window.mainloop()


if __name__ == "__main__":
    main()
