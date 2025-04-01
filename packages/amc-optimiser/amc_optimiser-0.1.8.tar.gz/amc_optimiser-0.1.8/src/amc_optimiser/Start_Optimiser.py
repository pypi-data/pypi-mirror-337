from re import S
import tkinter
from tkinter import filedialog
import customtkinter as ctk
from amc_optimiser import Optuna_run_cx
import json
import multiprocessing
import webbrowser
import threading
import optuna_dashboard
import optuna
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import os

#dest_folder,file_path,sheet_name,range_address,target,cpu_num,max_time,max_iter
def get_params():
    global file_path

    try:
        file_path = xl_name.get()
        sheet_name = xl_sheet.get()
        range_address = var_rng.get()
        target = obj_cell.get()
        directions = dirs.get()
        attr_target = attr_cell.get()
        attr_names = attn_cell.get()
        cpu_num = int(workers.get())
        max_time = int(m_time.get())
        max_iter = int(m_iter.get())
        population=int(pop.get())
        mutation = mut.get()
        ex_vis = exvis_var.get()
        distributed = dist_var.get()
    except:
        print("Error")
    
    data={
        "file_path": file_path,
        "sheet_name": sheet_name,
        "range_address": range_address,
        "target": target,
        "directions": directions,
        "attr_target": attr_target,
        "attr_names": attr_names,
        "cpu_num": cpu_num,
        "max_time": max_time,
        "max_iter": max_iter,
        "pop": population,
        "mut": mutation,
        "ex_vis": ex_vis,
        "distributed": distributed
        }

    with open("config.json", "w") as file:
            json.dump(data, file)

    file_split=file_path.split(',')
    folder_path = os.path.dirname(file_split[0])

    print("folder_path",folder_path)

    file=os.path.join(folder_path,"config.json")

    print("file_path",file)

    with open(file, "w") as file:
        json.dump(data, file)

    flag={
        "should_stop": False
    }

    with open("stop.json", "w") as file:
            json.dump(flag, file)

    return (file_path,sheet_name,range_address, target, directions, attr_target, attr_names, cpu_num,max_time,max_iter, population, mutation, ex_vis, distributed)
    #Optuna_run.main(dest_folder,file_path,sheet_name,range_address,target,cpu_num,max_time,max_iter)

def run_dashboard_server(file_path):
        optuna_dashboard.run_server(file_path)

def start_dash():
    # Use threading instead of multiprocessing for the dashboard
    dash_thread = threading.Thread(target=dash_main)
    dash_thread.daemon = True
    dash_thread.start()

def dash_main():

    j_path ='journal.log'#os.path.join(current_directory, 'journal.log')

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_dashboard_server, args=(j_path,))
    server_thread.daemon = True
    server_thread.start()

    # Wait for a short while to allow the server to start
    # You can adjust this delay as needed
    server_thread.join(timeout=5)

    # Open the URL in a web browser
    url = 'http://localhost:8080/dashboard/'
    webbrowser.open(url)

def output_csv():
    global file_path
    journal_path='journal.log'

    lock_obj = optuna.storages.JournalFileOpenLock(journal_path)

    storage = optuna.storages.JournalStorage(
        optuna.storages.JournalFileStorage(journal_path, lock_obj=lock_obj),
    )

    study = optuna.load_study(
        study_name="AMC_Optimiser", storage=storage
    )
    folder_path=os.path.dirname(file_path)
    f_name="current_state.csv"
    f_path=os.path.join(folder_path,f_name)
    df = study.trials_dataframe()
    df.to_csv(f_path, index=False)

    def show_popup():
        popup = ctk.CTk()
        popup.geometry("400x150")
        popup.title("Export Complete")

        label = ctk.CTkLabel(popup, text=f"CSV file '{f_name}' has been exported successfully.")
        label.pack(pady=20)

        popup.mainloop()

    show_popup()

def dash_2():
    journal_path='journal.log'

    plt.style.use('bmh')
    fig, ax1=plt.subplots(figsize=(12,6))
    ax2=ax1.twinx()
    ax1.set_xlabel('Number')
    ax1.set_ylabel('Value')
    ax2.set_ylabel('Duration')
    ax1.set_title('Number vs Value')
    ax1.grid(True)
    ax2.grid(False)

    lock_obj = optuna.storages.JournalFileOpenLock(journal_path)

    storage = optuna.storages.JournalStorage(
        optuna.storages.JournalFileStorage(journal_path, lock_obj=lock_obj),
    )

    study = optuna.load_study(
        study_name="AMC_Optimiser", storage=storage
    )

    def update_plot(frame_data):

        df = study.trials_dataframe()

        cumulative_max = df['value'].cummax()
        max_val=max(cumulative_max)
        df['delta']= pd.to_timedelta(df['duration'])
        df['secs']=df['delta'].dt.total_seconds()

        ax1.clear()
        ax2.clear()

        ax1.scatter(df['number'], df['value'], marker='o', s=1)
        ax1.plot(df['number'], cumulative_max, color='red', linestyle='--', label='Cumulative Max')
        ax2.plot(df['number'], df['secs'], color='blue', linestyle='-',linewidth=0.1)

        ax1.set_xlabel('Number')
        ax1.set_ylabel('Value')
        ax2.set_ylabel('Duration')

        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")

        fig.texts.clear()
        plt.figtext(0.1, 0.97, "Current objective: " + "{0:,.0f}".format(max_val))

    ani = FuncAnimation(fig, update_plot, frames=None, interval=5000)

    plt.tight_layout()
    plt.show()

def start_optuna():
    file_path,sheet_name,range_address,target,directions, attr_target, attr_names,cpu_num,max_time,max_iter, population, mutation, ex_vis, distributed=get_params()
    process1=multiprocessing.Process(target=Optuna_run_cx.main, args=(file_path,sheet_name,range_address,target, directions, attr_target, attr_names, cpu_num,max_time,max_iter, population, mutation, ex_vis, distributed,))
    process1.start()

def stop_optuna():
    with open("stop_signal.txt", "w") as file:
        file.write('STOP')

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Excel Files", "*.xlsx *.xlsm *.xlsb")])
    file_paths = list(file_paths)  # Convert the result to a list if it's a tuple
    print(file_paths)
    # Assuming xl_name is a tkinter StringVar or similar
    xl_name.set(", ".join(file_paths))

    folder_path = os.path.dirname(file_paths[0])
    file=os.path.join(folder_path,"config.json")

    try:
        with open(file, "r") as file:
            loaded_data = json.load(file)

        sh_entry.delete(0,tkinter.END)
        sh_entry.insert(0,loaded_data["sheet_name"])
        var_entry.delete(0,tkinter.END)
        var_entry.insert(0,loaded_data["range_address"])
        obj_entry.delete(0,tkinter.END)
        obj_entry.insert(0,loaded_data["target"])
        dirs_entry.delete(0,tkinter.END)
        dirs_entry.insert(0,loaded_data["directions"])
        attr_entry.delete(0,tkinter.END)
        attr_entry.insert(0,loaded_data["attr_target"])
        attn_entry.delete(0,tkinter.END)
        attn_entry.insert(0,loaded_data["attr_names"])
        w_entry.delete(0,tkinter.END)
        w_entry.insert(0,loaded_data["cpu_num"])
        mi_entry.delete(0,tkinter.END)
        mi_entry.insert(0,loaded_data["max_iter"])
        mt_entry.delete(0,tkinter.END)
        mt_entry.insert(0,loaded_data["max_time"])
        pop_entry.delete(0,tkinter.END)
        pop_entry.insert(0,loaded_data["pop"])
        mut_entry.delete(0,tkinter.END)
        mut_entry.insert(0,loaded_data["mut"])
        exvis_var.delete(0,tkinter.END)
        exvis_var.set(loaded_data["exvis"])
        dist_var.delete(0,tkinter.END)
        dist_var.set(loaded_data["distributed"])
    except:
        pass

    return file_paths

if __name__=="__main__":

    try:
        with open("config.json", "r") as file:
            loaded_data = json.load(file)
    except:
        loaded_data = {
            "dest_folder": "input working folder",
            "file_path": "input excel file name",
            "sheet_name": "input sheet name",
            "range_address": "input range address",
            "target": "input objective cell",
            "directions": "Do you want maximize or minimize?",
            "attr_target": "input attribute cell",
            "attr_names": "input attribute names",
            "cpu_num": "input number of workers",
            "max_time": "input max time",
            "max_iter": "input max iterations",
            "pop": "input population size",
            "mut": "input mutation rate",
            "exvis": False,
            "distributed": False
        }

    print(loaded_data)

    if os.path.exists("stop_signal.txt"):
        os.remove("stop_signal.txt")
        print(f"Previous stop_signal.txt deleted.")
    
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    gui = ctk.CTk()
    gui.geometry("825x775")
    gui.title("AMC Optimiser")

    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the amc.ico file
    icon_path = os.path.join(current_directory, 'amc.ico')

    gui.iconbitmap(icon_path)

    #Title
    title = ctk.CTkLabel(gui, text="Settings", font=("Roboto", 24))
    title.grid(row=0, column=0,padx=5, pady=5, sticky="nsew")

    #Warning
    title = ctk.CTkLabel(gui, text="Warning!! \n Running the optimiser will close \n all excel files without saving", font=("Roboto", 15), text_color="red")
    title.grid(row=0, column=1,padx=5, pady=5, sticky="nsew")

    #Excel file
    xl_label= ctk.CTkLabel(gui, text="Excel file:", justify="right")
    xl_label.grid(row=2, column=0,padx=5, pady=5, sticky="e")
    xl_name = tkinter.StringVar()
    xl_entry = ctk.CTkEntry(gui, placeholder_text="Select Excel File", textvariable=xl_name)
    xl_entry.insert(0,loaded_data["file_path"])
    xl_entry.grid(row=2, column=1,padx=5, pady=5, sticky="ew")
    xl_button = ctk.CTkButton(gui, text="Select File", command=select_files)
    xl_button.grid(row=2, column=2,padx=5, pady=5, sticky="w")
    
    #Excel Sheet
    sh_label= ctk.CTkLabel(gui, text="Excel sheet:", justify="right")
    sh_label.grid(row=3, column=0,padx=5, pady=5, sticky="e")
    xl_sheet = tkinter.StringVar()
    sh_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=xl_sheet)
    sh_entry.insert(0,loaded_data["sheet_name"])
    sh_entry.grid(row=3, column=1,padx=5, pady=5, sticky="ew")
    sh_comment= ctk.CTkLabel(gui, text="Enter the sheet name where the variables are located", justify="left")
    sh_comment.grid(row=3, column=2,padx=5, pady=5, sticky="w")

    #Variable Range
    var_label= ctk.CTkLabel(gui, text="Variable Range:", justify="right")
    var_label.grid(row=4, column=0,padx=5, pady=5, sticky="e")
    var_rng = tkinter.StringVar()
    var_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=var_rng)
    var_entry.insert(0,loaded_data["range_address"])
    var_entry.grid(row=4, column=1,padx=5, pady=5, sticky="ew")
    var_comment=ctk.CTkLabel(gui, text="Enter the range of the variables, min/max limits are assumed to be in this range -3 and -2 columns respectively", wraplength=350, justify="left")
    var_comment.grid(row=4, column=2,padx=5, pady=5, sticky="w")

    #Objective
    obj_label= ctk.CTkLabel(gui, text="Objective Cell(s):", justify="right")
    obj_label.grid(row=5, column=0,padx=5, pady=5, sticky="e")
    obj_cell = tkinter.StringVar()
    obj_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=obj_cell)
    obj_entry.insert(0,loaded_data["target"])
    obj_entry.grid(row=5, column=1,padx=5, pady=5, sticky="ew")
    obj_comment=ctk.CTkLabel(gui, text="Split multiple objectives with a comma", justify="left")
    obj_comment.grid(row=5, column=2,padx=5, pady=5, sticky="w")

    #Directions
    dir_label= ctk.CTkLabel(gui, text="Direction(s):", justify="right")
    dir_label.grid(row=6, column=0,padx=5, pady=5, sticky="e")
    dirs = tkinter.StringVar()
    dirs_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=dirs)
    dirs_entry.insert(0,loaded_data["directions"])
    dirs_entry.grid(row=6, column=1,padx=5, pady=5, sticky="ew")
    dir_comment=ctk.CTkLabel(gui, text="Split multiple directions with a comma", justify="left")
    dir_comment.grid(row=6, column=2,padx=5, pady=5, sticky="w")

    #User_attributes_target
    attr_label= ctk.CTkLabel(gui, text="Attribute Range(s):", justify="right")
    attr_label.grid(row=7, column=0,padx=5, pady=5, sticky="e")
    attr_cell = tkinter.StringVar()
    attr_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=attr_cell)
    attr_entry.insert(0,loaded_data["attr_target"])
    attr_entry.grid(row=7, column=1,padx=5, pady=5, sticky="ew")
    attr_comment=ctk.CTkLabel(gui, text="Select attributes to record, Split multiple attribute ranges with a comma.", wraplength=350, justify="left")
    attr_comment.grid(row=7, column=2,padx=5, pady=5, sticky="w")

    #User_attribute_names
    attn_label= ctk.CTkLabel(gui, text="Arrtibute Name(s):", justify="right")
    attn_label.grid(row=8, column=0,padx=5, pady=5, sticky="e")
    attn_cell = tkinter.StringVar()
    attn_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=attn_cell)
    attn_entry.insert(0,loaded_data["attr_names"])
    attn_entry.grid(row=8, column=1,padx=5, pady=5, sticky="ew")
    attn_comment=ctk.CTkLabel(gui, text="Split multiple names with a comma", justify="left")
    attn_comment.grid(row=8, column=2,padx=5, pady=5, sticky="w")

    #Number of workers
    w_label= ctk.CTkLabel(gui, text="Number of Workers:", justify="right")
    w_label.grid(row=9, column=0,padx=5, pady=5, sticky="e")
    workers = tkinter.StringVar()
    w_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=workers)
    w_entry.insert(0,loaded_data["cpu_num"])
    w_entry.grid(row=9, column=1,padx=5, pady=5, sticky="ew")
    w_comment=ctk.CTkLabel(gui, text="This is the numbers of excel instances to launch", justify="left")
    w_comment.grid(row=9, column=2,padx=5, pady=5, sticky="w")

    #Max time
    mt_label= ctk.CTkLabel(gui, text="Max optimisation time:", justify="right")
    mt_label.grid(row=10, column=0,padx=5, pady=5, sticky="e")
    m_time = tkinter.StringVar()
    mt_entry = ctk.CTkEntry(gui, placeholder_text="Enter Working Folder", textvariable=m_time)
    mt_entry.insert(0,loaded_data["max_time"])
    mt_entry.grid(row=10, column=1,padx=5, pady=5, sticky="ew")
    mt_comment=ctk.CTkLabel(gui, text="Enter the max time in Hours", justify="left")
    mt_comment.grid(row=10, column=2,padx=5, pady=5, sticky="w")

    #Max iterations
    mi_label= ctk.CTkLabel(gui, text="Max iterations:", justify="right")
    mi_label.grid(row=11, column=0,padx=5, pady=5, sticky="e")
    m_iter = tkinter.StringVar()
    mi_entry = ctk.CTkEntry(gui, placeholder_text="Enter the max interations", textvariable=m_iter)
    mi_entry.insert(0,loaded_data["max_iter"])
    mi_entry.grid(row=11, column=1,padx=5, pady=5, sticky="ew")
    mi_comment=ctk.CTkLabel(gui, text="Enter the max number of iterations", justify="left")
    mi_comment.grid(row=11, column=2,padx=5, pady=5, sticky="w")

    #Population size
    pop_label= ctk.CTkLabel(gui, text="Population size:", justify="right")
    pop_label.grid(row=12, column=0,padx=5, pady=5, sticky="e")
    pop = tkinter.StringVar()
    pop_entry = ctk.CTkEntry(gui, placeholder_text="Enter the population size", textvariable=pop)
    pop_entry.insert(0,loaded_data["pop"])
    pop_entry.grid(row=12, column=1,padx=5, pady=5, sticky="ew")
    pop_comment=ctk.CTkLabel(gui, text="Enter the population size", justify="left")
    pop_comment.grid(row=12, column=2,padx=5, pady=5, sticky="w")

    #Mutation probability
    mut_label= ctk.CTkLabel(gui, text="Mutation Probability:", justify="right")
    mut_label.grid(row=13, column=0,padx=5, pady=5, sticky="e")
    mut = tkinter.StringVar()
    mut_entry = ctk.CTkEntry(gui, placeholder_text="Enter the population size", textvariable=mut)
    mut_entry.insert(0,loaded_data["mut"])
    mut_entry.grid(row=13, column=1,padx=5, pady=5, sticky="ew")
    mut_comment=ctk.CTkLabel(gui, text="Enter the mutation probability, if set to ""None"" will use 1/number of parameters", wraplength=350, justify="left")
    mut_comment.grid(row=13, column=2,padx=5, pady=5, sticky="w")

    #Excel Visible
    exvis_label= ctk.CTkLabel(gui, text="Select to make excel visible:", justify="right")
    exvis_label.grid(row=14, column=0,padx=5, pady=5, sticky="e")
    exvis_var=tkinter.BooleanVar(value=loaded_data["distributed"])
    exvis_box= ctk.CTkCheckBox(gui, text="Recommended off but useful for debugging", variable = exvis_var, onvalue=True, offvalue=False)
    exvis_box.grid(row=14, column=1,padx=5, pady=5, sticky="ew")

    #Distributed check box
    dist_label= ctk.CTkLabel(gui, text="Is this PC part of a \ndistributed cluster:?", justify="right")
    dist_label.grid(row=15, column=0,padx=5, pady=5, sticky="e")
    dist_var=tkinter.BooleanVar(value=loaded_data["distributed"])
    dist_box= ctk.CTkCheckBox(gui, text="If this is the first PC in the cluster deselect this", variable = dist_var, onvalue=True, offvalue=False)
    dist_box.grid(row=15, column=1,padx=5, pady=5, sticky="ew")

    run_opt = ctk.CTkButton(gui, text="Run Optimisation", command=start_optuna)
    run_opt.grid(row=16, column=1,padx=5, pady=5, sticky="ew")
    
    launch_dash = ctk.CTkButton(gui, text="Launch Dashboard", command=start_dash)
    launch_dash.grid(row=17, column=1,padx=5, pady=5, sticky="ew")

    out_csv = ctk.CTkButton(gui, text="Output CSV", command=output_csv)
    out_csv.grid(row=18, column=1,padx=5, pady=5, sticky="ew")
    out_csv_comment=ctk.CTkLabel(gui, text="This will output a csv of the progress so far \ncan take a while to output", justify="left")
    out_csv_comment.grid(row=18, column=2,padx=5, pady=5, sticky="w")

    stop_opt = ctk.CTkButton(gui, text="Stop Optimisation", command=stop_optuna)
    stop_opt.grid(row=19, column=1,padx=5, pady=5, sticky="ew")

    gui.mainloop()

