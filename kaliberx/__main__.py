"""
@author: adam.novak@skgeodesy.sk
"""
import tkinter as tk
from tkinter import filedialog, font, messagebox
import numpy as np
import pandas as pd
from datetime import datetime
import scipy.stats as stats
from scipy.stats import t
import matplotlib.pyplot as plt
import os

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.input_file = None

    def create_widgets(self):
        self.master.title("KaliberX v1.0")
        self.master.geometry('500x650')
        self.master.resizable(True, True)
        
        custom_font = font.Font(family="Trebuchet MS", size=int(11.5))
        custom_font_panel = font.Font(family="Trebuchet MS", size=int(11.5), weight="bold")
        custom_font_display = font.Font(family="Trebuchet MS", size=int(9))
        custom_font_widgets = font.Font(family="Trebuchet MS", size=int(10))
        p1 = tk.LabelFrame(self.master, text='Vstupný súbor', bg='#f0f0f0', relief=tk.GROOVE, borderwidth=2.5, font=custom_font_panel)
        p1.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.27)
        button_choose_file = tk.Button(p1, text="Vyber súbor z merania", bg='#e7e7e7', command=self.choose_input_files, font=custom_font)
        button_choose_file.place(relx=0.02, rely=0.05, relwidth=0.35, relheight=0.2)
        self.show_local_path = tk.Label(p1, text="", bg='#f0f0f0', anchor="w", font=custom_font_display)
        self.show_local_path.place(relx=0.4, rely=0.05, relwidth=0.55, relheight=0.15)
        label_instrument = tk.Label(p1, text="kalibrovaný prístroj", bg='#f0f0f0', anchor="w", font=custom_font)
        label_instrument.place(relx=0.02, rely=0.32, relwidth=0.42, relheight=0.15)
        self.instrument_var = tk.StringVar(value="Scintrex CG5")
        instrument_options = tk.OptionMenu(p1, self.instrument_var, "Scintrex CG5", "CG6 Autograv")
        instrument_options.place(relx=0.72, rely=0.3, relwidth=0.24, relheight=0.19)
        label_header_lines = tk.Label(p1, text="počet riadkov hlavičky", bg='#f0f0f0', anchor="w", font=custom_font)
        label_header_lines.place(relx=0.02, rely=0.54, relwidth=0.34, relheight=0.15)
        self.entry_header_lines = tk.Entry(p1, font=custom_font_widgets, justify='center')
        self.entry_header_lines.insert(0, 34)
        self.entry_header_lines.place(relx=0.74, rely=0.54, relwidth=0.1, relheight=0.15)
        label_sd_scaling = tk.Label(p1, text="škálovanie strednej chyby", bg='#f0f0f0', anchor="w", font=custom_font)
        label_sd_scaling.place(relx=0.02, rely=0.78, relwidth=0.42, relheight=0.15)
        self.sd_scaling_var = tk.StringVar(value="minútové")
        sd_scaling_options = tk.OptionMenu(p1, self.sd_scaling_var, "minútové", "sekundové")
        sd_scaling_options.place(relx=0.72, rely=0.75, relwidth=0.2, relheight=0.19)
        p2 = tk.LabelFrame(self.master, text='Merania', bg='#f0f0f0', relief=tk.GROOVE, borderwidth=2, font=custom_font_panel)
        p2.place(relx=0.02, rely=0.28, relwidth=0.96, relheight=0.52)
        Ganovce_label = tk.Label(p2, text="Gánovce", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        Ganovce_label.place(relx=0.02, rely=0.01, relwidth=0.42, relheight=0.1)
        self.radio_ganovce = tk.StringVar(value="SK-401")
        radiobuttongan1 = tk.Radiobutton(p2, text="SK-401", variable=self.radio_ganovce, value="SK-401", bg='#f0f0f0', font=custom_font)
        radiobuttongan1.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.1)
        radiobuttongan2 = tk.Radiobutton(p2, text="SK-401.10", variable=self.radio_ganovce, value="SK-401.10", bg='#f0f0f0', font=custom_font)
        radiobuttongan2.place(relx=0.25, rely=0.1, relwidth=0.2, relheight=0.1)
        radiobuttongan3 = tk.Radiobutton(p2, text="SK-401.20", variable=self.radio_ganovce, value="SK-401.20", bg='#f0f0f0', font=custom_font)
        radiobuttongan3.place(relx=0.50, rely=0.1, relwidth=0.2, relheight=0.1)
        radiobuttongan4 = tk.Radiobutton(p2, text="SK-401.30", variable=self.radio_ganovce, value="SK-401.30", bg='#f0f0f0', font=custom_font)
        radiobuttongan4.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.1)
        SL_label = tk.Label(p2, text="Stará Lesná", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        SL_label.place(relx=0.02, rely=0.2, relwidth=0.2, relheight=0.1)
        self.radio_SL = tk.StringVar(value="SK-420")
        radiobuttonSL1 = tk.Radiobutton(p2, text="SK-420", variable=self.radio_SL, value="SK-420", bg='#f0f0f0', font=custom_font)
        radiobuttonSL1.place(relx=0.02, rely=0.3, relwidth=0.2, relheight=0.1)
        radiobuttonSL2 = tk.Radiobutton(p2, text="SK-420.10", variable=self.radio_SL, value="SK-420.10", bg='#f0f0f0', font=custom_font)
        radiobuttonSL2.place(relx=0.25, rely=0.3, relwidth=0.2, relheight=0.1)
        Start_label = tk.Label(p2, text="Štart", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        Start_label.place(relx=0.02, rely=0.4, relwidth=0.2, relheight=0.1)
        self.radio_Start = tk.StringVar(value="SK-418")
        radiobuttonstart1 = tk.Radiobutton(p2, text="SK-418", variable=self.radio_Start, value="SK-418", bg='#f0f0f0', font=custom_font)
        radiobuttonstart1.place(relx=0.02, rely=0.5, relwidth=0.2, relheight=0.1)
        radiobuttonstart2 = tk.Radiobutton(p2, text="SK-418.20", variable=self.radio_Start, value="SK-418.20", bg='#f0f0f0', font=custom_font)
        radiobuttonstart2.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.1)
        SKPL_label = tk.Label(p2, text="Skalnaté pleso", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        SKPL_label.place(relx=0.02, rely=0.58, relwidth=0.25, relheight=0.1)
        self.radio_SKPL = tk.StringVar(value="SK-412")
        radiobuttonSKPL1 = tk.Radiobutton(p2, text="SK-412", variable=self.radio_SKPL, value="SK-412", bg='#f0f0f0', font=custom_font)
        radiobuttonSKPL1.place(relx=0.02, rely=0.68, relwidth=0.2, relheight=0.1)
        radiobuttonSKPL2 = tk.Radiobutton(p2, text="SK-412.10", variable=self.radio_SKPL, value="SK-412.10", bg='#f0f0f0', font=custom_font)
        radiobuttonSKPL2.place(relx=0.25, rely=0.68, relwidth=0.2, relheight=0.1)
        LOMS_label = tk.Label(p2, text="Lomnický štít", bg='#f0f0f0', anchor="w", font=custom_font_panel)
        LOMS_label.place(relx=0.02, rely=0.78, relwidth=0.25, relheight=0.1)
        self.radio_LOMS = tk.StringVar(value="SK-419")
        radiobuttonLOMS1 = tk.Radiobutton(p2, text="SK-419", variable=self.radio_LOMS, value="SK-419", bg='#f0f0f0', font=custom_font)
        radiobuttonLOMS1.place(relx=0.02, rely=0.88, relwidth=0.2, relheight=0.1)
        radiobuttonLOMS2 = tk.Radiobutton(p2, text="SK-419.10", variable=self.radio_LOMS, value="SK-419.10", bg='#f0f0f0', font=custom_font)
        radiobuttonLOMS2.place(relx=0.25,  rely=0.88, relwidth=0.2, relheight=0.1)
        p3 = tk.LabelFrame(self.master, text='Výstupný súbor', bg='#f0f0f0', relief=tk.GROOVE, borderwidth=2, font=custom_font_panel)
        p3.place(relx=0.02, rely=0.8, relwidth=0.96, relheight=0.12)
        button_create_report = tk.Button(p3, text="Vytvor report", bg='#e7e7e7', command=self.create_report_file, font=custom_font)
        button_create_report.place(relx=0.02, rely=0.2, relwidth=0.35, relheight=0.5)
        self.show_report_path = tk.Label(p3, text="", bg='#f0f0f0', anchor="w", font=custom_font)
        self.show_report_path.place(relx=0.45, rely=0.2, relwidth=0.45, relheight=0.3)
        execute_button = tk.Button(self.master, text='Výpočet', bg='#e7e7e7', command=self.process_file, font=custom_font)
        execute_button.place(relx=0.25, rely=0.93, relwidth=0.19, relheight=0.05)
        close_button = tk.Button(self.master, text='Zavrieť', bg='#e7e7e7', command=self.master.destroy, font=custom_font)
        close_button.place(relx=0.6, rely=0.93, relwidth=0.19, relheight=0.05)
    
    # store selected points in list variable points_GUI
    def store_selected_points(self):
        """Retrieve and store the selected radio button values."""
        self.points_GUI = [
            self.radio_ganovce.get(),
            self.radio_SL.get(),
            self.radio_Start.get(),
            self.radio_SKPL.get(),
            self.radio_LOMS.get()
        ]
    # chose input file widget function
    def choose_input_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            file_paths_str = "\n".join(file_paths)
            self.show_local_path.config(text=file_paths_str)
            self.input_file = file_paths[0]  # Store the first selected file for processing

    def create_report_file(self):
            self.report_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("txt file", "*.txt")])
            if self.report_path:
                self.show_report_path.config(text=self.report_path)
                if hasattr(self, 'diff_result'):
                    self.save_report(self.diff_result, self.report_path)


    # function that handles clicking on 'vypocet' button
    def process_file(self):
        
        print("Starting process_file...")
        self.store_selected_points()
        points_GUI = self.points_GUI
        # get input_file
        input_file = self.input_file
        header_lines = int(self.entry_header_lines.get()) - 4
        significance = 3
        SD_scale_information = self.sd_scaling_var.get()
        instrument_type = self.instrument_var.get()
        
        if instrument_type == 'Scintrex CG5':
            instrument_manufacturer = 'microg solutions'
        if instrument_type == 'CG6 Autograv':
            instrument_manufacturer = 'microg solutions'
        report_filename = self.report_path
        

             # Check if necessary paths are set
        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return
        if not report_filename:
            messagebox.showerror("Error", "Please specify a report file path.")
            return

        # READ reference file to get 
        # path to gravity calibration line file (static file)
        excel_file_path = 'T:\VGZ_Ganovce_Lomnicky_stit/zakladnica_zhrnutie.xlsx'  
        df = pd.read_excel(excel_file_path)
        
        # indeces where to look for data in the xls file.
        rows = np.array([92, 92, 92, 92, 94, 94, 95, 95, 96, 96, 97, 97, 97])
        column_name = np.array([2, 7, 10, 13, 2, 7, 2, 10, 2, 7, 2, 7, 10])
        # value and std are located after name of file
        column_value = column_name + 1
        column_std = column_name + 2
        
        reference_points_all = pd.DataFrame({
            'pointID': df.values[rows, column_name],
            'reference_value': df.values[rows, column_value],
            'standard_deviation': df.values[rows, column_std]
        })
        
        reference_points_all['pointID'] = reference_points_all['pointID'].apply(lambda x: f"{float(x.split('-')[-1]):.2f}")
        
        # call function and extract directory measured points
        spracovanie_py = gravity_differences(input_file, header_lines,significance, SD_scale_information, instrument_type)
        points_measured = spracovanie_py['stationinfo']['measuredpoints']
        # remove black space for points to match
        points_measured = [point.strip() for point in points_measured]
        # compare measured and reference points
        is_in_measured1 = reference_points_all['pointID'].isin(points_measured)
        # compare measured to reference points
        reference_points_used = reference_points_all[is_in_measured1].copy()
        points_GUI = [f"{float(point.split('-')[-1]):.2f}" for point in points_GUI]
        
        # compare measured and GUI selected points
        is_in_measured2 = reference_points_used['pointID'].isin(points_GUI)
        # compare measured to GUI selected
        reference_points_used = reference_points_used[is_in_measured2]
        
        # Ensure the pointID is a categorical type with the order specified by points_measured
        reference_points_used['pointID'] = pd.Categorical(reference_points_used['pointID'], categories=points_measured, ordered=True)
        
        # Sort reference_points_used to match the order of points_measured
        reference_points_used = reference_points_used.sort_values('pointID').reset_index(drop=True)
        
        # calculate reference value difference
        reference_points_used['reference_diff'] = reference_points_used['reference_value'] - reference_points_used['reference_value'].iloc[0]
        
        std = np.zeros(len(reference_points_used))
        for i in range(0,len(reference_points_used)-1):
            
            std[i+1] = np.sqrt(reference_points_used['standard_deviation'].iloc[0]**2+reference_points_used['standard_deviation'].iloc[i+1]**2)
        
        reference_points_used['reference_diff_std'] = std
        
        # Augment matrix columns for further comparison
        reference_points_used['measured_dif'] = pd.Series([0] + spracovanie_py['adjusted']['differences'])
        reference_points_used['measured_std'] = pd.Series([0] + spracovanie_py['adjusted']['std'])
        
        # Replace 0 with NaN to avoid division by zero and sqrt of zero
        reference_points_used.loc[reference_points_used['measured_dif'] == 0, 'measured_dif'] = np.nan
        reference_points_used.loc[reference_points_used['reference_diff'] == 0, 'reference_diff'] = np.nan
        reference_points_used.loc[reference_points_used['reference_diff_std'] == 0, 'reference_diff_std'] = np.nan
        
        # Calculate calibration factors
        reference_points_used['calibration'] = reference_points_used['reference_diff'] / reference_points_used['measured_dif']
        
        # Ensure the columns are of type Series before performing operations
        ref_diff_std = reference_points_used['reference_diff_std'].astype(float)
        measured_dif = reference_points_used['measured_dif'].astype(float)
        measured_std = reference_points_used['measured_std'].astype(float)
        reference_diff = reference_points_used['reference_diff'].astype(float)
        
        reference_points_used['calibration_std'] = np.sqrt(
            (ref_diff_std / measured_dif) ** 2 + 
            (measured_std * reference_diff / measured_dif ** 2) ** 2
        )
        
        calib_average = np.mean(reference_points_used['calibration'])
        GCAL_novy = spracovanie_py['instrument_info']['GCAL1']*calib_average

        plt.rcParams['figure.dpi'] = 300  # Adjust the dpi value
        # Create a figure and axis
        fig, ax = plt.subplots()
       
        # Plot horizontal lines for each calibration value
        for i in range(len(reference_points_used)):
            point_start = reference_points_used['pointID'].iloc[0]
            point_end = reference_points_used['pointID'].iloc[i]
            calibration_value = reference_points_used['calibration'].iloc[i]
            calibration_std = reference_points_used['calibration_std'].iloc[i]
            
            if calibration_value > 1:  # For values greater than 1
                # Plot the calibration line
                ax.hlines(calibration_value, xmin=point_start, xmax=point_end, color='#A54F27', linewidth=1, label='kalibračná priamka')
                line_full = plt.Line2D([], [], color='#A54F27', linewidth=1, label='kalibračná priamka')
                line_dotted = plt.Line2D([], [], color='#A54F27', linestyle=':', linewidth=0.5, label='konfidenčný interval ±1σ')
                
                # Plot the confidence interval lines
                if not np.isnan(calibration_std):
                    ax.hlines(calibration_value + calibration_std, xmin=point_start, xmax=point_end, color='#A54F27', linestyle=':', linewidth=0.5, label='konfidenčný interval')
                    ax.hlines(calibration_value - calibration_std, xmin=point_start, xmax=point_end, color='#A54F27', linestyle=':', linewidth=0.5, label='konfidenčný interval')
                    
            elif calibration_value < 1:  # For values less than 1
                # Plot the calibration line
                ax.hlines(calibration_value, xmin=point_start, xmax=point_end, color='#1144FF', linewidth=1, label='kalibračná priamka')
                line_full = plt.Line2D([], [], color='#1144FF', linewidth=1, label='kalibračná priamka')
                line_dotted = plt.Line2D([], [], color='#1144FF', linestyle=':', linewidth=0.5, label='konfidenčný interval ±1σ')
                # Plot the confidence interval lines
                if not np.isnan(calibration_std):
                    ax.hlines(calibration_value + calibration_std, xmin=point_start, xmax=point_end, color='#1144FF', linestyle=':', linewidth=0.5, label='konfidenčný interval')
                    ax.hlines(calibration_value - calibration_std, xmin=point_start, xmax=point_end, color='#1144FF', linestyle=':', linewidth=0.5, label='konfidenčný interval')
        # Add a horizontal line at value 1
        ax.axhline(y=1, color='black', linestyle='-', linewidth=1.6, label='y = 1')
        # Plot settings
        ax.set_xlabel('bod')
        # Add the custom lines to the legend
        ax.legend(handles=[line_full, line_dotted])
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=[line_full, line_dotted], bbox_to_anchor=(0.55, 1.2), loc='upper left')
        ax.set_ylabel('kalibračný faktor')
        # Set x-axis labels
        
        ax.set_xticks(range(len(reference_points_used)))
        ax.set_xticklabels(reference_points_used['pointID'], rotation=45)
        # Show plot
        plt.show()
        fig.savefig(report_filename[:-4] + '_grafika.jpg', format='jpg', bbox_inches='tight')
        
        # Create the report as a list of strings
        report = [
            f"Spracovaný súbor: {os.path.basename(spracovanie_py['stationinfo']['filename'])}",
            "Prístroj",
            f"Výrobca: {instrument_manufacturer}",
            f"Typ: {instrument_type}",
            f"Výrobné číslo: {spracovanie_py['instrument_info']['SN']} ",
            f"Presnosť merania: 5microGal"
            f"Dátum merania: {spracovanie_py['stationinfo']['measurement_date']}",
            "Parametre základnice: určené ku dňu 06/2024",
            "__________________________________________________________________________________________________",
            "Prevodový vzťah:",
            "SU = GCAL1(SF/SC) + GCAL2(SF/SC)²",
            " ",
            "Kalibračný faktor k:",
            "k = Δref/Δmer",
            " ",
            "Nová kalibračná konštanta",
            "Gcal1'=Gcal1*k",
            " ",
            "__________________________________________________________________________________________________",
            "Výsledok kalibrácie"
            " ",
            f"Jednotková stredná chyba [μGal]: {spracovanie_py['processing']['RMSE']:.1f}",
            f"Počet akceptovaných meraní: {int(spracovanie_py['processing']['number_of_measurements'])}",
            f"Počet vybočujúcich meraní: {int(spracovanie_py['processing']['rejected_measurements'])}",
            f"Stupeň aproximačného polynómu chodu: {spracovanie_py['drift']['polynomial_degree']}",
            " ",
            "Výsledky príslušných etáp:"
            "začiatočný bod, koncový bod, kalibračný faktor, príslušná štandardná odchýlka"
        ]
        
        # average calibration std6
        std_av = np.sqrt(
            np.sum(
                reference_points_used['calibration_std'][1:]**2/(len(reference_points_used['calibration'])-1))
            )    
        
        # Use zip and list comprehension to build the additional report lines
        report += [f"{reference_points_used['pointID'][0]},{reference_points_used['pointID'][zz+1]},{reference_points_used['calibration'][zz+1]:10.9f},{reference_points_used['calibration_std'][zz+1]:10.9f}" for zz in range(len(reference_points_used['pointID']) - 1)]
        report += [" "]
        report += [f"Priemerná hodnota k: {calib_average:10.9f}, {std_av:10.9f}"]
        report += [f"{calib_average:10.9f}, {std_av:10.9f}"]
        report += ["Pôvodná hodnota"]
        report += [f"Gcal1: {spracovanie_py['instrument_info']['GCAL1']:9.5f}"]
        report += ["Nová hodnota"]
        report += [f"Gcal1': {GCAL_novy:9.5f}"]
        
                
        # Export the report to a .txt file
        with open(report_filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(report))
            

    # calculation function
def gravity_differences(input_file, header_lines, significance, SD_scale_information, instrument_type):
    try:
        
        # Search for the line containing "GCAL1" in the header
        header_line_number = None
        with open(input_file, 'r') as file:
            for i, line in enumerate(file):
                if "Gcal1" in line:
                    header_line_number = i
                    header_info = line.strip()
                    break
        
        # Check if the line with "GCAL1" was found
        if header_line_number is None:
            raise ValueError("The word 'GCAL1' was not found in the file.")
        
        GCAL1_str = header_info[9:]
        GCAL1 = float(GCAL1_str)
                
        # Search for the line containing "GCAL1" in the header
        header_line_number = None
        with open(input_file, 'r') as file:
            for i, line in enumerate(file):
                if "Instrument S/N" in line:
                    header_line_number = i
                    header_info = line.strip()
                    break
        
        # Check if the line with "Serial number of instrument" was found
        if header_line_number is None:
            raise ValueError("The word 'GCAL1' was not found in the file.")
        SN_str = header_info[17:]
        
        # # Read data from file
        filedata = pd.read_csv(input_file, header=header_lines, delimiter=r'\s+', 
                                names=['col1', 'points', 'height', 'grav', 'SD', 'tiltx', 'tilty', 'temp_corr', 'tide_corr', 'duration', 'rejected', 'time', 'dn', 'terrain_col', 'date'],
                                dtype={'points': str, 'height':float, 'time': str})
    
        # Combine date and time into datetime column
        filedata['datetime'] = pd.to_datetime(filedata['date'] + ' ' + filedata['time'], format='%Y/%m/%d %H:%M:%S')
        dtime = filedata['datetime']
        
        # Convert datetime to numeric date format (days since Unix epoch)
        dn = filedata['datetime'].apply(lambda x: x.timestamp() / (24 * 3600))
        
        if instrument_type == 'Scintrex CG5':
            
            # Determine the adjustment based on testheight
            if filedata['height'].iloc[0] > 2:
                # Convert centimeters to meters: Subtract 21.1 and divide by 100
                filedata['height'] = (filedata['height'] - 21.1) / 100
            else:
                # Assume default units are meters: Subtract 0.211
                filedata['height'] = filedata['height'] - 0.211
        
        # Convert measured mGal units to μGal
        grav = filedata['grav'] * 1000
        # Reducing measured values to a point using normal gradient
        grav = grav + filedata['height'] * 308.6
        # Point ID information
        points = filedata['points']
        uniquepoints = filedata['points'].unique()
        measured_points = [p if p.isdigit() else f'{float(p):8.2f}' for p in uniquepoints]
        # Least Square Adjustment - deterministic model
        n0 = len(filedata['points'])  # number of measurements taken
        k = len(uniquepoints)  # number of measured points
        
        # starting drift polynomial degree
        polynomial_degree = 2
        
        # Jacobi matrix, point section
        A = np.zeros((n0, k))
        for i, unique_point in enumerate(uniquepoints):
            ind = points == unique_point
            A[ind, i] = 1
        
        # Jacobi matrix, drift part
        A = np.column_stack([A, np.ones(n0)])
        for i in range(k + 2 , k + 2 + polynomial_degree):
            A = np.column_stack([A, (dn - dn[0])**(i - k - 1)])
        # Regularization - by default first column is removed to fix position 1 as starting 
        A = np.delete(A, 0, axis=1)
        # # Load errors from filedata and transfer from miliGal to microGal
        ERR = filedata['SD'] * 1000
        # Scale errors
        if SD_scale_information == 1:
            ERR = ERR / np.sqrt(60)
            
        C = np.diag(np.square(ERR))
        # Parameter adjustment using LSE formulas
        adjusted_parameters = np.linalg.inv(A.T @ np.linalg.inv(C) @ A) @ A.T @ np.linalg.inv(C) @ grav
        # Measurement errors to adjusted parameters
        v = A @ adjusted_parameters - grav
        # Root mean square error
        rmse1 = np.sqrt((v.T @ np.linalg.inv(C) @ v) / (n0 - k - 2 - polynomial_degree))
        # Covariance matrix of adjusted parameters
        C_theta = (rmse1**2) * np.linalg.inv(A.T @ np.linalg.inv(C) @ A)
        # Standard deviation of adjusted parameters
        SD_theta = np.sqrt(np.diag(C_theta))
        # Drift coefficients
        drift_koef = adjusted_parameters[-polynomial_degree:]
        AA = A[:, -polynomial_degree:]
        # Residual (transportation drift)
        res_drift = AA @ drift_koef
        # Test values
        test = res_drift + v
        # Average drift value to subtract later
        res_drift_av = np.mean(res_drift)
        # Outliers testing
        if significance == 1:
            significance_level = 0.32
        
        elif significance == 2:
            significance_level = 0.05
        
        elif significance == 3:
            significance_level = 0.01
        
        # Outliers indexes
        index_outliers = np.where(np.abs(v) >= 5 *3* rmse1 * significance)[0]
        # Statistical testing of parameters
        Tau = adjusted_parameters[-1] / SD_theta[-1]
        # Quadratic component significance testing
        
        t_value = stats.t.ppf(1-significance_level/2, n0-k)
        
        if np.abs(Tau) < t_value:
            polynomial_degree_new = 1  # Drift approx. function set to linear
        else:
            polynomial_degree_new = 2  # Drift approx. function remains quadratic
        
        # Removing outliers
        grav = np.delete(grav, index_outliers)
        dn = np.delete(dn, index_outliers)
        points = np.delete(points, index_outliers)
        ERR = np.delete(ERR, index_outliers)
        
        n = len(points)
        A = np.zeros((n, k))
        for i, unique_point in enumerate(uniquepoints):
            ind = points == unique_point
            A[ind, i] = 1
        
        # Jacobi matrix, drift part
        A = np.column_stack([A, np.ones(n)])
        for i in range(k + 2 , k + 2 + polynomial_degree):
            A = np.column_stack([A, (dn - dn[0])**(i - k - 1)])
            
        # Regularization - by default first column is removed to fix position 1 as starting 
        A = np.delete(A, 0, axis=1)
        C = np.square(np.diag(ERR))
        
        # New adjusted parameters without considering outliers in the processing
        adjusted_parameters_new = np.linalg.inv(A.T @ np.linalg.inv(C) @ A) @ A.T @ np.linalg.inv(C) @ grav
        
        # Measurements errors to adjusted parameters
        v = A @ adjusted_parameters_new - grav
        rmse2 = np.sqrt((v.T @ np.linalg.inv(C) @ v) / (n - k - 2 - polynomial_degree_new - 1))
        C_theta = (rmse2**2) * np.linalg.inv(A.T @ np.linalg.inv(C) @ A)
        SD_theta_new = np.sqrt(np.diag(C_theta))
        
        drift_koef2 = adjusted_parameters_new[-polynomial_degree_new:]
        AA = A[:, -polynomial_degree_new:]
        
        # New drift
        res_drift_new = AA @ drift_koef2
        res_drift_new_av = np.mean(res_drift_new)
        
        # new Time information dtime (datetime)
        dtime_new = pd.to_datetime(dn, unit='D', origin='unix')
        
        # Output dictionary
        output_gravity_diff = {
            'stationinfo': {
                'filename': input_file.ljust(100),
                'measurement_date': str(dtime_new[0]),
                'measuredpoints': measured_points
            },
            'time': {
                'all_measurements': dtime,
                'no_outliers': dtime_new,
                'outliers': dtime.iloc[index_outliers].tolist()
            },
            'processing': {
                'number_of_measurements': n0,
                'rejected_measurements': n0 - n,
                'RMSE': rmse2,
                'errors_all': (test - res_drift_av).tolist(),
                'errors_outliers': (test.iloc[index_outliers] - res_drift_av).tolist()
            },
            'drift': {
                'polynomial_degree': str(polynomial_degree_new),
                'drift_all_measurements': (res_drift - res_drift_av).tolist(),
                'drift_no_outliers': (res_drift_new - res_drift_new_av).tolist()
            },
            'adjusted': {
                'differences': adjusted_parameters_new[:len(uniquepoints)-1].tolist(),
                'std': SD_theta_new[:len(uniquepoints)-1].tolist()
            },
            'instrument_info': {
                'GCAL1':GCAL1,
                'SN':SN_str
                }
        }
        return output_gravity_diff
    except Exception as e:
        print(f"Error in gravity_differences: {e}")
        raise
        
if __name__ == "__main__":
    root = tk.Tk()
    kaliberx = App(master=root)
    kaliberx.mainloop()
