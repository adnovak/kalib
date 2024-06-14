"""
@author: adam.novak@skgeodesy.sk
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import font

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Main window
        self.master.title("KaliberX v1.0")
        self.master.geometry('500x650')  # Adjusted size to accommodate widgets
        self.master.resizable(True, True)
        
        custom_font = font.Font(family="Trebuchet MS", size=int(11.5))  # font for standard widget labels
        custom_font_panel = font.Font(family="Trebuchet MS", size= int(11.5), weight="bold")  # font for labeling panel names
        custom_font_display = font.Font(family="Trebuchet MS", size= int(9))  # font for displaying filnames
        custom_font_widgets = font.Font(family="Trebuchet MS", size= int(10))  # font displayed within entry window widgets

        p1 = tk.LabelFrame(self.master, text='Vstupný súbor', bg='#f0f0f0', relief=tk.GROOVE, borderwidth=2.5,font=custom_font_panel)
        p1.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.27)

        button_choose_file = tk.Button(p1, text="Vyber súbor z merania", bg='#e7e7e7', command=self.choose_input_files, font=custom_font)
        button_choose_file.place(relx=0.02, rely=0.05, relwidth=0.35, relheight=0.2)

        self.show_local_path = tk.Label(p1, text="", bg='#f0f0f0', anchor="w", font=custom_font_display)
        self.show_local_path.place(relx=0.4, rely=0.05, relwidth=0.55, relheight=0.15)

        label_instrument = tk.Label(p1, text="kalibrovaný prístroj", bg='#f0f0f0', anchor="w", font=custom_font)
        label_instrument.place(relx=0.02, rely=0.32, relwidth=0.42, relheight=0.15)
        instrument_options = tk.OptionMenu(p1, tk.StringVar(value="Scintrex CG5"), "Scintrex CG5", "CG6 Autograv")
        instrument_options.place(relx=0.72, rely=0.3, relwidth=0.24, relheight=0.19)
        
        label_header_lines = tk.Label(p1, text="počet riadkov hlavičky", bg='#f0f0f0', anchor="w", font=custom_font)
        label_header_lines.place(relx=0.02, rely=0.54, relwidth=0.34, relheight=0.15)
        entry_header_lines = tk.Entry(p1, font=custom_font_widgets, justify='center')
        entry_header_lines.insert(0, 34)  # Prefill with the default value 34
        entry_header_lines.place(relx=0.74, rely=0.54, relwidth=0.1, relheight=0.15)

        label_sd_scaling = tk.Label(p1, text="škálovanie strednej chyby", bg='#f0f0f0', anchor="w", font=custom_font)
        label_sd_scaling.place(relx=0.02, rely=0.78, relwidth=0.42, relheight=0.15)
        sd_scaling_options = tk.OptionMenu(p1, tk.StringVar(value="minútové"), "minútové", "sekundové")
        sd_scaling_options.place(relx=0.72, rely=0.75, relwidth=0.2, relheight=0.19)

#________________________________________________________________________________________________________________________________________
        # Panel 2 - Nastavenie merani
        p2 = tk.LabelFrame(self.master, text='Merania', bg='#f0f0f0', relief=tk.GROOVE, borderwidth=2,font = custom_font_panel)
        p2.place(relx=0.02, rely=0.28, relwidth=0.96, relheight=0.52)

        # Ganovce
        Ganovce_label= tk.Label(p2, text="Gánovce", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        Ganovce_label.place(relx=0.02, rely=0.01, relwidth=0.42, relheight=0.1)
        self.radio_ganovce = tk.StringVar(value="main")
        # Radio button:
        radiobuttongan1 = tk.Radiobutton(p2, text="Hlavny bod", variable=self.radio_ganovce, value="main", bg='#f0f0f0', font=custom_font)
        radiobuttongan1.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.1)

        # Radio button:
        radiobuttongan2 = tk.Radiobutton(p2, text="Excenter 1", variable=self.radio_ganovce, value="eccentric1", bg='#f0f0f0', font=custom_font)
        radiobuttongan2.place(relx=0.25, rely=0.1, relwidth=0.2, relheight=0.1)
        
        radiobuttongan3 = tk.Radiobutton(p2, text="Excenter 2", variable=self.radio_ganovce, value="eccentric2", bg='#f0f0f0', font=custom_font)
        radiobuttongan3.place(relx=0.50, rely=0.1, relwidth=0.2, relheight=0.1)
        
        radiobuttongan4 = tk.Radiobutton(p2, text="Excenter 3", variable=self.radio_ganovce, value="eccentric3", bg='#f0f0f0', font=custom_font)
        radiobuttongan4.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.1)
        
        # Stara Lesna
        SL_label= tk.Label(p2, text="Stará Lesná", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        SL_label.place(relx=0.02, rely=0.2, relwidth=0.2, relheight=0.1)
        self.radio_SL = tk.StringVar(value="main")
        # Radio button: 
        radiobuttonSL1 = tk.Radiobutton(p2, text="Hlavny bod", variable=self.radio_SL, value="main", bg='#f0f0f0', font=custom_font)
        radiobuttonSL1.place(relx=0.02, rely=0.3, relwidth=0.2, relheight=0.1)

        # Radio button: 
        radiobuttonSL2 = tk.Radiobutton(p2, text="Excenter 1", variable=self.radio_SL, value="eccentric1", bg='#f0f0f0', font=custom_font)
        radiobuttonSL2.place(relx=0.25, rely=0.3, relwidth=0.2, relheight=0.1)
                
        # Start
        Start_label= tk.Label(p2, text="Start", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        Start_label.place(relx=0.02, rely=0.4, relwidth=0.2, relheight=0.1)
        self.radio_Start = tk.StringVar(value="main")
        # Radio button: 
        radiobuttonstart1 = tk.Radiobutton(p2, text="Hlavny bod", variable=self.radio_Start, value="main", bg='#f0f0f0', font=custom_font)
        radiobuttonstart1.place(relx=0.02, rely=0.5, relwidth=0.2, relheight=0.1)

        # Radio button: 
        radiobuttonstart2 = tk.Radiobutton(p2, text="Excenter 1", variable=self.radio_Start, value="eccentric1", bg='#f0f0f0', font=custom_font)
        radiobuttonstart2.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.1)
        
        # Skalnate Pleso
        SKPL_label= tk.Label(p2, text="Skalnate pleso", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        SKPL_label.place(relx=0.02, rely=0.58, relwidth=0.25, relheight=0.1)
        self.radio_SKPL = tk.StringVar(value="main")
        # Radio button: local data option
        radiobuttonSKPL1 = tk.Radiobutton(p2, text="Hlavny bod", variable=self.radio_SKPL, value="main", bg='#f0f0f0', font=custom_font)
        radiobuttonSKPL1.place(relx=0.02, rely=0.68, relwidth=0.2, relheight=0.1)

        # Radio button: local data combined with MERRA2 option
        radiobuttonSKPL2 = tk.Radiobutton(p2, text="Excenter 1", variable=self.radio_SKPL, value="eccentric1", bg='#f0f0f0', font=custom_font)
        radiobuttonSKPL2.place(relx=0.25, rely=0.68, relwidth=0.2, relheight=0.1)
                
        # Lomnicky stit
        LOMS_label= tk.Label(p2, text="Lomnicky stit", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        LOMS_label.place(relx=0.02, rely=0.78, relwidth=0.25, relheight=0.1)
        self.radio_LOMS = tk.StringVar(value="main")
        # Radio button:
        radiobuttonLOMS1 = tk.Radiobutton(p2, text="Hlavny bod", variable=self.radio_LOMS, value="main", bg='#f0f0f0', font=custom_font)
        radiobuttonLOMS1.place(relx=0.02, rely=0.88, relwidth=0.2, relheight=0.1)

        # Radio button:
        radiobuttonLOMS2 = tk.Radiobutton(p2, text="Excenter 1", variable=self.radio_LOMS, value="eccentric1", bg='#f0f0f0', font=custom_font)
        radiobuttonLOMS2.place(relx=0.25, rely=0.88, relwidth=0.2, relheight=0.1)

        # Panel 3
        p3 = tk.LabelFrame(self.master, text='Výstupný súbor', bg='#f0f0f0', relief=tk.GROOVE, borderwidth=2, font=custom_font_panel)
        p3.place(relx=0.02, rely=0.8, relwidth=0.96, relheight=0.12)
        
        # Panel na vyber suboru
        button_create_report = tk.Button(p3, text="Create report file", bg='#e7e7e7', command=self.create_report_file, font=custom_font)
        button_create_report.place(relx=0.02, rely=0.2, relwidth=0.35, relheight=0.5)

        # Vypis nazvu vybraneho suboru
        self.show_report_path = tk.Label(p3, text="", bg='#f0f0f0', anchor="w", font=custom_font)
        self.show_report_path.place(relx= 0.45, rely=0.2, relwidth=0.45, relheight=0.3)

        # Buttons in the main window
        execute_button = tk.Button(self.master, text='Výpočet', bg='#e7e7e7', command=lambda: print('Executing'), font=custom_font)
        execute_button.place(relx=0.25, rely=0.93, relwidth=0.19, relheight=0.05)

        close_button = tk.Button(self.master, text='Close', bg='#e7e7e7', command=self.master.destroy, font=custom_font)
        close_button.place(relx=0.6, rely=0.93, relwidth=0.19, relheight=0.05)

    def choose_input_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Join the file paths into a string and update the label
            file_paths_str = "\n".join(file_paths)
            self.show_local_path.config(text=file_paths_str)

    def create_report_file(self):
        # You can implement the functionality to handle creating a report file here
        print('Creating report file...')

if __name__ == "__main__":
    root = tk.Tk()
    kaliberx = App(master=root)
    kaliberx.mainloop()
