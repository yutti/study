import sys
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from GUI_control import GUI_control
from PIL import Image, ImageTk, ImageOps

class Set_gui():

    def __init__(self, main_window):

        # controller Class生成
        self.control = GUI_control()
         
        # Variable setting
        self.file_filter = [("Image file", ".bmp .png .jpg .tif")]
        self.function_btn =["Gray_scale","Binarization","Sepia"]        
        self.canvas_title =["Base","Effect"]
        
        # Main window
        self.main_window = main_window
        self.main_window.geometry("1400x800")
        self.main_window.title('Image Editor v0.10')    
    
        # Sub window
        self.filepath_frame = tk.Frame(self.main_window, height=100, width=400)
        self.func_frame     = tk.Frame(self.main_window, height=450, width=400)
        self.exit_frame     = tk.Frame(self.main_window, height=100, width=400)
        self.canvas_frame   = tk.Frame(self.main_window, height=450, width=400)       

        # Widgetsmith
        self.filepath_frame.place(relx=0.05, rely=0.8)
        self.func_frame.place(relx=0.85, rely=0.15)
        self.exit_frame.place(relx=0.85, rely=0.8)        
        self.canvas_frame.place(relx=0.05, rely=0.05)          
 
        # 1. Set file path
        self.imp_path_btn   = tk.Button(self.filepath_frame, text="Select_file", command=self.file_select)
        self.imp_path_btn.grid(row=0, column=0, sticky=tk.W , padx=10, pady = 5)

        self.img_path = tk.StringVar()
        self.imp_path_box   = tk.Entry(self.filepath_frame, textvariable=self.img_path, width=70)
        self.imp_path_box.grid(row=1, column=0, sticky=tk.EW, padx=10)
  
        # 2. Set Function botton
        self.func_combobox = ttk.Combobox(self.func_frame ,text = 'combo_file', state="readonly", value=self.function_btn,
        width=30)
        self.func_combobox.set(self.function_btn[0])
        self.func_combobox.bind("<<ComboboxSelected>>", self.effect_event)
        self.func_combobox.pack()
        
        # 3. Set canvas_frame
        
        # 3.1 canvas_frame title
        for i in range(2):
            label = tk.Label(self.canvas_frame, text=self.canvas_title[i], bg="white", relief=tk.RIDGE)
            label.grid(row=0, column=i,sticky=tk.W + tk.E)               

        # 3.2 canvas_frame title
        # from PIL import ImageTk
        self.base_img   = Image.open('lenna.png')  # POR image 
        self.effect_img = self.base_img            # Effect image
        
        self.pil_base_img   = ImageTk.PhotoImage(self.base_img)
        self.pil_effect_img = ImageTk.PhotoImage(self.effect_img)

        self.base_img_label = tk.Label(self.canvas_frame, image=self.pil_base_img)
        self.base_img_label.grid(row=1, column=0)

        # canvas
        self.effect_img_canvas = tk.Canvas(self.canvas_frame, width=self.effect_img.width, height=self.effect_img.height)
        self.effect_img_canvas.grid(row=1, column=1)

        # canvasに初期画像を表示
        self.effect_img_canvas.photo = ImageTk.PhotoImage(self.effect_img)
        self.effect_img_on_canvas = self.effect_img_canvas.create_image(0, 0, anchor='nw', image=self.effect_img_canvas.photo)
        
        # 4 set to close the window
        self.button = tk.Button(self.exit_frame, text='Exit', width=10, command=self.on_click_close)
        self.button.grid(row=0, column=0, sticky=tk.SE, padx = 10, pady = 10)

    # Function for closing window
    def on_click_close(self):
        self.main_window.destroy()
        
    def file_select(self):
        self.filename = filedialog.askopenfilename(title = "Please select image file,",filetypes =  self.file_filter)
        if self.filename:
            self.img_path.set(self.filename)
        img_file = self.control.file_set(self.filename)

    def effect_event(self, arg):
        #print(self.func_combobox.get(), arg)
        #print(self.func_combobox.current(), self.func_combobox.get())
        
        # gary scale
        if self.func_combobox.current() <= 3:
            self.convert_img = self.effect_img.convert('L')
        
            if self.func_combobox.get() == "Gray_scale":
                self.set_image(self.convert_img)            

            elif self.func_combobox.get() == "Binarization":
                self.converted_img = self.convert_img.point(lambda x: 0 if x < 230 else x) 
                self.set_image(self.converted_img)

            elif self.func_combobox.get() == "Sepia":
                self.merged_img = Image.merge(
                    "RGB",
                    (      
                        self.convert_img.point(lambda x: x * 240 / 255),
                        self.convert_img.point(lambda x: x * 200 / 255),
                        self.convert_img.point(lambda x: x * 145 / 255)
                    )
                )
                self.set_image(self.merged_img)
  
    def set_image(self, pic_img):
        self.effect_img_canvas.photo = ImageTk.PhotoImage(pic_img)
        self.effect_img_canvas.itemconfig(self.effect_img_on_canvas, image=self.effect_img_canvas.photo)


def main():

    #　Tk MainWindow
    main_window = tk.Tk()
    
    # Viewクラス生成
    Set_gui(main_window)
    
    #　フレームループ処理
    main_window.mainloop()

if __name__ == '__main__':
    main()