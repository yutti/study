import sys
import tkinter as tk
from tkinter import ttk, filedialog

from GUI_control import GUI_control
from PIL import Image, ImageTk, ImageOps

class Set_gui():

    def __init__(self, main_window):

        # controller Class生成
        self.control = GUI_control()
         
        # Variable setting
        #self.file_filter = [("Image file", ".bmp .png .jpg .tif")]
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
        self.imp_path_btn   = tk.Button(self.filepath_frame, text="Select_image_file", command=self.draw_default_image)
        self.imp_path_btn.grid(row=0, column=0, sticky=tk.W , padx=10, pady = 5)

        self.img_path_stvar = tk.StringVar()
        self.imp_path_entry = tk.Entry(self.filepath_frame, textvariable=self.img_path_stvar, width=70)
        self.imp_path_entry.grid(row=1, column=0, sticky=tk.EW, padx=10)
  
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
        self.base_canvas   = tk.Canvas(self.canvas_frame, width=500, height=500, bg = "#A9A9A9")
        self.base_canvas.grid(row=1, column=0)
        
        self.effect_canvas = tk.Canvas(self.canvas_frame, width=500, height=500, bg = "#A9A9A9")
        self.effect_canvas.grid(row=1, column=1)
       
        # 4 set to close the window
        self.button = tk.Button(self.exit_frame, text='Exit', width=10, command=self.on_click_close)
        self.button.grid(row=0, column=0, sticky=tk.SE, padx = 10, pady = 10)

    # Function for closing window
    def on_click_close(self):
        self.main_window.destroy()
        
    def draw_default_image(self):
        self.img_path   = self.control.get_image_path()
        self.img_path_stvar.set(self.img_path)
        
        self.effect_img , self.base_canvas, self.effect_canvas_create = self.control.resize_image(self.img_path,self.base_canvas,self.effect_canvas)

    def effect_event(self, arg):
       
        combo_func_no   = self.func_combobox.current()
        combo_func_name = self.func_combobox.get() 
        
        self.converted_img = self.control.effect_image(combo_func_no,combo_func_name, self.effect_img)
        self.replace_effect_image(self.converted_img)
  
    def replace_effect_image(self, pic_img):
        self.effect_canvas.photo = ImageTk.PhotoImage(pic_img)
        self.effect_canvas.itemconfig(self.effect_canvas_create, image=self.effect_canvas.photo)

def main():

    #　Tk MainWindow
    main_window = tk.Tk()
    
    # Viewクラス生成
    Set_gui(main_window)
    
    #　フレームループ処理
    main_window.mainloop()

if __name__ == '__main__':
    main()