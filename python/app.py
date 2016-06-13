#!/usr/bin/env python2
"""Lele"""
import json
from tkFileDialog import askopenfilename
from Tkinter import Tk, Message, Menu, Frame, Listbox, Button, END, SINGLE
from methods import regula_falsi, regula_falsi_interval, MyError, newton, newton_interval

def function_from_list(variable, coefficients_list):
    """Function that defines a polynomial given a list of coefficients"""
    i = len(coefficients_list) - 1
    result = 0
    for item in coefficients_list:
        result += item * variable ** i
        i -= 1
    return result

def load_file():
    """Opens filedialog window to pick a file"""
    return askopenfilename(filetypes=[("JavaScript object Nation file", "*.json")])

class Application(Frame):
    """Main application class"""
    json_file_name = "functions.json" # should be none after tests
    json_data = None
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        master.title("Regula falsi")
        master.minsize(width=100, height=100)
        master.config(menu=self.menubar)

    def calculate(self):
        """Does all the work"""
        item_number = self.fields.curselection()
        polynomial = self.json_data["functions"][int(item_number[0])]
        result_floating = None
        result_interval = None
        if self.json_data["method"] == "regula_falsi":
            try:
                result_floating = regula_falsi(polynomial["a"],
                                               polynomial["b"],
                                               function_from_list,
                                               polynomial["coeff"]
                                              )
            except MyError as error:
                result_floating = error.value
            except ZeroDivisionError:
                result_floating = "Unfortunately, division by 0 happened"
            try:
                result_interval = regula_falsi_interval(polynomial["a"],
                                                        polynomial["b"],
                                                        function_from_list,
                                                        polynomial["coeff"]
                                                       )
                result_interval = result_interval.format('%.20E')[9:]
                result_interval = result_interval[:-1]
            except MyError as error:
                result_interval = error.value
        elif self.json_data["method"] == "newton":
            try:
                result_floating = newton(polynomial["x"],
                                         polynomial["epsilon"],
                                         polynomial["max_iterations"],
                                         function_from_list,
                                         polynomial["coeff"],
                                         polynomial["derivative_coeff"]
                                        )
            except ZeroDivisionError:
                result_floating = "Unfortunately, division by zero happened"
            except MyError as error:
                result_floating = error.value
            try:
                result_interval = newton_interval(polynomial["x"],
                                                  polynomial["epsilon"],
                                                  polynomial["max_iterations"],
                                                  function_from_list,
                                                  polynomial["coeff"],
                                                  polynomial["derivative_coeff"]
                                                 )
                result_interval = result_interval.format('%.20E')[9:]
                result_interval = result_interval[:-1]
            except MyError as error:
                result_interval = error.value
        else:
            result_interval = "You propably"
            result_floating = "gave me wrong JSON"
        self.show_result_floating.config(text=result_interval)
        self.show_result_interval.config(text=result_floating)

    def read_json_file(self):
        """Reads function coefficients from json files"""
        self.fields.delete(0, END)
        self.json_file_name = load_file()
        with open(self.json_file_name) as json_file:
            self.json_data = json.load(json_file)
        for item in self.json_data["functions"]:
            self.fields.insert(END, item["coeff"])

    def create_widgets(self):
        """Creates buttons on the window and binds actions to them"""
        #listbox for the equations
        self.fields = Listbox(self, selectmode=SINGLE)
        self.fields.config(width=100)
        self.fields.pack()
        #button for calculating
        self.calculate_button = Button(self)
        self.calculate_button["text"] = "Calculate"
        self.calculate_button["command"] = self.calculate
        self.calculate_button.pack({"side": "left"})
        #to the end
        self.show_result_floating = Message(self, width=250)
        self.show_result_floating.pack()
        #second Message
        self.show_result_interval = Message(self, width=250)
        self.show_result_interval.pack()
        #adding menu buttons to the window
        self.menubar = Menu(self)
        self.menubar.add_command(label="Load file", command=self.read_json_file)
        self.menubar.add_command(label="Quit", command=self.quit)

ROOT = Tk()
APP = Application(master=ROOT)
APP.mainloop()
ROOT.destroy()
