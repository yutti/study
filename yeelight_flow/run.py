import time
import yeelight
from yeelight import *
import tkinter as tk
from tkinter import ttk
from yeelight.transitions import *
from yeelight import Flow


class gui:
    def __init__(self, main_window):

        # Variable setting
        self.bulb = yeelight.Bulb("192.168.10.103")  # Set up IP address for yeelight.
        self.function_btn = [
            "alarm",
            "christmas",
            "disco",
            "lsd",
            "police",
            "police2",
            "random_loop",
            "rgb",
            "slowdown",
            "strobe",
            "strobe_color",
            "temp",
        ]

        # Main window
        self.main_window = main_window
        self.main_window.geometry("800x400")
        self.main_window.title("Yeelight operation v0.10")

        self.label_grid(self.main_window, "Light", 0, 0)
        self.btn_grid(self.main_window, "On", self.turn_on_light, 0, 1, tk.SE)
        self.btn_grid(self.main_window, "Off", self.turn_off_light, 0, 2, tk.SE)

        self.label_grid(self.main_window, "Transitions", 1, 0)

        self.func_combobox = ttk.Combobox(
            self.main_window,
            text="combo_file",
            state="readonly",
            value=self.function_btn,
            width=30,
        )
        self.func_combobox.set(self.function_btn[0])
        self.func_combobox.bind("<<ComboboxSelected>>", self.effect_event)
        self.func_combobox.grid(row=1, column=1, columnspan=3)

        self.label_grid(self.main_window, "Flow", 2, 0)
        self.btn_grid(self.main_window, "Start", self.start_flow, 2, 1, tk.SE)
        self.btn_grid(self.main_window, "Stop", self.stop_flow, 2, 2, tk.SE)
        self.btn_grid(self.main_window, "Reset", self.reset_flow, 2, 3, tk.SE)
        self.btn_grid(self.main_window, "Exit", self.close_window, 3, 3, tk.SE)

    def btn_grid(self, set_frame, btn_name, act_command, r_num, c_num, stk):
        button = tk.Button(set_frame, text=btn_name, width=10, command=act_command)
        return button.grid(row=r_num, column=c_num, sticky=stk, padx=10, pady=10)

    def label_grid(self, set_frame, title, r_num, c_num):
        label = tk.Label(set_frame, text=title)
        return label.grid(row=r_num, column=c_num, sticky=tk.W, padx=10, pady=10)

    def turn_on_light(self):
        self.bulb.turn_on()

    def turn_off_light(self):
        self.bulb.turn_off()

    def effect_event(self, arg):
        self.transition = self.func_combobox.get()

    def start_flow(self):

        func_name = self.transition

        if func_name == "alarm":
            flow = Flow(count=0, transitions=alarm())  # Cycle forever.

        elif func_name == "christmas":
            flow = Flow(count=0, transitions=christmas())  # Cycle forever.

        elif func_name == "disco":
            flow = Flow(count=0, transitions=disco())  # Cycle forever.

        elif func_name == "lsd":
            flow = Flow(count=0, transitions=lsd())  # Cycle forever.

        elif func_name == "police":
            flow = Flow(count=0, transitions=police())  # Cycle forever.

        elif func_name == "police2":
            flow = Flow(count=0, transitions=police2())  # Cycle forever.

        elif func_name == "random_loop":
            flow = Flow(count=0, transitions=random_loop())  # Cycle forever.

        elif func_name == "rgb":
            flow = Flow(count=0, transitions=rgb())  # Cycle forever.

        elif func_name == "slowdown":
            flow = Flow(count=0, transitions=slowdown())  # Cycle forever.

        elif func_name == "strobe":
            flow = Flow(count=0, transitions=strobe())  # Cycle forever.

        elif func_name == "strobe_color":
            flow = Flow(count=0, transitions=strobe_color())  # Cycle forever.
        elif func_name == "temp":
            flow = Flow(count=0, transitions=temp())  # Cycle forever.

        self.bulb.start_flow(flow)

    def stop_flow(self):
        self.bulb.stop_flow()

    def reset_flow(self):
        flow = Flow(count=1, transitions=pulse(red=255, green=255, blue=255))
        self.bulb.start_flow(flow)

    def close_window(self):
        self.main_window.destroy()
        # self.main_window.quit()


def main():

    main_window = tk.Tk()
    gui(main_window)
    main_window.mainloop()


if __name__ == "__main__":
    main()
