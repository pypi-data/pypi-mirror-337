import win32com.client as win32
from datetime import datetime
import optuna
import os
import sys
import shutil
from optuna.samplers import NSGAIIISampler
import subprocess
import xlwings as xw
import glob
import time
from amc_optimiser import worker_messages

def close_all_excel_instances():
    keys = list(xw.apps.keys())
    print(f"Active Excel instances: {keys}")
        
    for key in keys:
            excel_instance = xw.apps[key]
            excel_instance.display_alerts = False
            print(f'Trying to quit instance {key}')
            books = excel_instance.books
            for book in books:
                book.close()
            excel_instance.quit()

def settings_cleanup(file_path):
    # Clean up from previous runs
    print("Closing Excel instances")

    close_all_excel_instances()

    file_name = os.path.basename(file_path)
    folder_path = os.path.dirname(file_path)
    _name=os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]
    base_name ="node"

    # Script with objective function
    #current_path = os.path.realpath(__file__)
    #current_directory = os.path.dirname(current_path)
    script_to_execute = worker_messages.__file__
    #print(os.path.realpath(__file__))
    
    # Storage location
    journal_path='journal.log'#os.path.join(current_directory,journal_name)
    jounal_lock='journal.log.lock'#os.path.join(current_directory,lock_name)

    return folder_path,base_name,journal_path,jounal_lock, _name, script_to_execute, extension

def get_params(file_path, sheet_name, range_address, target):

    print("Getting variables from Excel")
    print(file_path)

    excel = win32.DispatchEx('Excel.Application')
    workbook = excel.Workbooks.Open(file_path, ReadOnly=False)
    excel.Visible = False  # Keep Excel hidden
    excel.AutoRecover.Enabled = False

    # Reference the specified sheet and range
    worksheet = workbook.Sheets(sheet_name)
    variable_range = worksheet.Range(range_address)

    # Read the number of variables based on the number of rows in the range
    num_vars = variable_range.Rows.Count
    param_list = [int(cell.Value) for cell in variable_range]
    print(param_list)

    # Read the lower bounds from Excel (assuming they are in column -3)
    lower_bounds_range = variable_range.GetOffset(0,-3)
    lower_bounds_list = [int(cell.Value) for cell in lower_bounds_range]

    # Read the upper bounds from Excel (assuming they are in column -2)
    upper_bounds_range = variable_range.GetOffset(0, -2)
    upper_bounds_list = [int(cell.Value) for cell in upper_bounds_range]

    target_list=target.split(',')
    vals=[]

    for i in range(len(target_list)):
            objective_cell = worksheet.Range(target_list[i])
            vals.append(objective_cell.Value)

    close_all_excel_instances()

    return(num_vars,lower_bounds_list,upper_bounds_list,param_list, vals)

def copy_excel_files(file_path, num_copies, base_name, folder_path, extension):
    # Copy the source file to the destination folder

    print("Copying Excel files (workers)")

    for i in range(num_copies):
        dest_file = os.path.join(folder_path, f'{base_name}_{i}{extension}')
        shutil.copy(file_path, dest_file)

def run_opt(sheet_name, range_address, target, directions, attr_target, attr_names, max_time, lower_bounds_list, upper_bounds_list, num_vars, folder_path, journal_path, jounal_lock, cpu_num, max_iter, _name, base_name, distributed, script_to_execute, extension, population, param_list, mutation, ex_vis, file_number):

    print("Starting optimisation")

    target_list=target.split(',')
    direction_list = [direction.lower() for direction in directions.split(',')]

    attr_list=attr_target.split(',')
    attr_names=attr_names.split(',')
    
    if distributed==False:
        try: 
            os.remove(journal_path)
        except OSError:
            pass

        try: 
            os.remove(jounal_lock)
        except OSError:
            pass
    else:
        pass
    
    lock_obj = optuna.storages.journal.JournalFileOpenLock(journal_path)
    storage = optuna.storages.JournalStorage(
    optuna.storages.journal.JournalFileBackend(journal_path, lock_obj=lock_obj),
    )

    # Create a study
    if len(target_list) == 1:
        study = optuna.create_study(study_name="AMC_Optimiser", sampler=NSGAIIISampler(), direction=direction_list[0], storage=storage, load_if_exists=True)
 
    else:
        study = optuna.create_study(study_name="AMC_Optimiser", sampler=NSGAIIISampler(), directions=direction_list, storage=storage, load_if_exists=True)

    param_dict={i: param_list[i] for i in range(len(param_list))}
    print(param_dict)

    #study.optimize(lambda trial: fun(trial,vals), n_trials=1)
    
    procs = [subprocess.Popen([sys.executable, script_to_execute, folder_path, base_name, str(i), sheet_name, range_address, str(target_list), str(direction_list), str(attr_list), str(attr_names), str(max_iter), str(max_time), str(lower_bounds_list), str(upper_bounds_list), str(num_vars), extension, str(population), str(mutation), str(ex_vis), str(file_number)]) for i in range(cpu_num)]

    for p in procs:
        p.wait()

    close_all_excel_instances()

    print("Exporting to Csv")

    # Save results
    timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    f_name=os.path.join(folder_path,f"{_name}_results_{timestamp}.csv")
    df = study.trials_dataframe()
    df.to_csv(f_name, index=False)

    if len(target_list) == 1:
        print(study.best_params)
        print(study.best_value)
    else:
        print(study.best_trials)

    time.sleep(5)

    print("Deleting Nodes")
    patterns = ['*node*.xlsx', '*node*.xlsb', '*node*.xlsm']
    for pattern in patterns:
        # Join the folder path with the pattern
        files_to_delete = glob.glob(os.path.join(folder_path, pattern))

    for i in range(30):
        try:
            print(f"Deleting nodes attempt {i+1}")
            for file in files_to_delete:
                os.remove(file)
            print("Deleted nodes")
            break
        except Exception as e:
            time.sleep(1)
            if(i==29):
                print(e)

    if os.path.exists("stop_signal.txt"):
        os.remove("stop_signal.txt")
        print(f"Previous stop_signal.txt deleted.")

    print("Optimisation Complete")    

def main(file_paths,sheet_name,range_address,target, directions, attr_target, attr_names, cpu_num,max_time,max_iter, population, mutation, ex_vis, distributed):
    print(file_paths,sheet_name,range_address,target, directions, attr_target, attr_names, cpu_num,max_time,max_iter, population, mutation, ex_vis, distributed)
    file_number=0
    for file_path in file_paths.split(', '):
        print(file_path)
        file_number += 1
        folder_path,base_name,journal_path,jounal_lock, _name, script_to_execute, extension = settings_cleanup(file_path)
        num_vars,lower_bounds_list,upper_bounds_list, param_list, vals = get_params(file_path, sheet_name, range_address, target)
        copy_excel_files(file_path, cpu_num, base_name, folder_path, extension)
        run_opt(sheet_name, range_address, target, directions, attr_target, attr_names, max_time, lower_bounds_list, upper_bounds_list, num_vars, folder_path, journal_path, jounal_lock, cpu_num, max_iter, _name, base_name, distributed, script_to_execute, extension, population, param_list, mutation, ex_vis, file_number)

if __name__=='__main__':
    main()
