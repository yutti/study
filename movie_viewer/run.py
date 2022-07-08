import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import cv2

from PIL import Image, ImageOps, ImageTk

import threading


class Set_gui:
    def __init__(self, main_window):

        # Variable setting
        self.file_filter = [("Movie file", ".mp4")]
        self.set_movie = True
        self.thread_set = False
        self.start_movie = False
        self.video_frame = None

        # Main window
        self.main_window = main_window
        self.main_window.geometry("1400x800")
        self.main_window.title("Movie Editor v0.10")

        # Sub window
        self.canvas_frame = tk.Frame(self.main_window, height=450, width=400)
        self.path_frame = tk.Frame(self.main_window, height=100, width=400)
        self.opr_frame = tk.Frame(self.main_window, height=100, width=400)

        # Widgetsmith
        self.canvas_frame.place(relx=0.05, rely=0.05)
        self.path_frame.place(relx=0.60, rely=0.2)
        self.opr_frame.place(relx=0.60, rely=0.5)

        # 1.1 canvas_frame (label)
        self.label = tk.Label(
            self.canvas_frame, text="Movie", bg="white", relief=tk.RIDGE
        )
        self.label.grid(row=0, column=0, sticky=tk.W + tk.E)

        # 1.2 canvas_frame (canvas)
        self.canvas = tk.Canvas(self.canvas_frame, width=700, height=500, bg="#A9A9A9")
        self.canvas.grid(row=1, column=0)

        # 2 path_frame
        self.button = self.opr_btn(self.path_frame, "File", self.on_click_path)
        self.button.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.path_stvar = tk.StringVar()
        self.path_entry = tk.Entry(
            self.path_frame, textvariable=self.path_stvar, width=70
        )
        self.path_entry.grid(row=1, column=0, sticky=tk.EW, padx=10)

        # 3 opr_frame
        self.button = self.opr_btn(self.opr_frame, "Start", self.on_click_start)
        self.button.grid(row=1, column=0, sticky=tk.SE, padx=10, pady=10)

        self.button = self.opr_btn(self.opr_frame, "Stop", self.on_click_stop)
        self.button.grid(row=1, column=1, sticky=tk.SE, padx=10, pady=10)

        self.button = self.opr_btn(self.opr_frame, "Reset", self.on_click_reset)
        self.button.grid(row=1, column=2, sticky=tk.SE, padx=10, pady=10)

        self.button = self.opr_btn(self.opr_frame, "Exit", self.on_click_close)
        self.button.grid(row=3, column=2, sticky=tk.SE, padx=10, pady=10)

    def opr_btn(self, set_frame, btn_name, act_command):
        return tk.Button(set_frame, text=btn_name, width=10, command=act_command)

    def on_click_path(self):
        self.movie_path = self.get_path()
        self.path_stvar.set(self.movie_path)
        self.run_one_frame()
        # Movie standby.
        self.thread_set = True
        self.thread_main = threading.Thread(target=self.main_thread_func)
        self.thread_main.start()

    def on_click_start(self):
        self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.start_movie = True

    def on_click_stop(self):
        self.start_movie = False

    def on_click_reset(self):
        self.start_movie = False
        self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.run_one_frame()

    def on_click_close(self):
        self.set_movie = False

        # Block the calling thread until the thread represented by this instance end.
        if self.thread_set == True:
            self.thread_main.join()

        self.video_cap.release()
        self.main_window.destroy()

    def main_thread_func(self):

        self.video_cap = cv2.VideoCapture(self.movie_path)
        ret, self.video_frame = self.video_cap.read()

        if self.video_frame is None:
            print("None")

        while self.set_movie:

            if self.start_movie:

                ret, self.video_frame = self.video_cap.read()

                if ret:
                    # convert color order from BGR to RGB
                    pil = self.cvtopli_color_convert(self.video_frame)

                    self.effect_img, self.canvas_create = self.resize_image(
                        pil, self.canvas
                    )
                    self.replace_canvas_image(
                        self.effect_img, self.canvas, self.canvas_create
                    )
                else:
                    self.start_movie = False

    def run_one_frame(self):
        self.video_cap = cv2.VideoCapture(self.movie_path)
        ret, self.video_frame = self.video_cap.read()

        if self.video_frame is None:
            print("None")

        else:
            ret, self.video_frame = self.video_cap.read()
            # convert color order from BGR to RGB
            pil = self.cvtopli_color_convert(self.video_frame)

            self.effect_img, self.canvas_create = self.resize_image(pil, self.canvas)
            # scale value intialize
            self.replace_canvas_image(self.effect_img, self.canvas, self.canvas_create)

    def replace_canvas_image(self, pic_img, canvas_name, canvas_name_create):
        canvas_name.photo = ImageTk.PhotoImage(pic_img)
        canvas_name.itemconfig(canvas_name_create, image=canvas_name.photo)

    def cvtopli_color_convert(self, video):
        rgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)

    # Model
    def resize_image(self, img, canvas):

        w = img.width
        h = img.height
        w_offset = 250 - (w * (500 / h) / 2)
        h_offset = 250 - (h * (700 / w) / 2)

        if w > h:
            resized_img = img.resize((int(w * (700 / w)), int(h * (700 / w))))
        else:
            resized_img = img.resize((int(w * (500 / h)), int(h * (500 / h))))

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

        return resized_img, resized_img_canvas

    def get_path(self):
        return filedialog.askopenfilename(
            title="Please select image file,", filetypes=self.file_filter
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
