import win32com.client as win32
import win32process
import optuna
import sys
import os
import ast
from optuna.samplers import NSGAIIISampler
import time
from pywintypes import com_error
import psutil

class CalcHandler(object): 
    def OnAfterCalculate(self):
        global flag
        flag = True      

def worker(dest_folder, base_name, node, sheet_name, range_address, target_list, direction_list, storage, max_time, max_iter, lower_bounds_list, upper_bounds_list, num_vars, extension, population, mutation, ex_vis, file_number, attr_list, attr_names):
    global excel, variable_range, objective_cells

    # Function to open the workbook and assign necessary variables
    def open_workbook():
        global excel, variable_range, objective_cells, file_path, id, attr_cells
        excel = win32.DispatchEx('Excel.Application')
        file_path = os.path.join(dest_folder, f'{base_name}_{node}{extension}')
        print(file_path)
        workbook = excel.Workbooks.Open(file_path)
        excel.Visible = ex_vis  # Keep Excel hidden
        excel.Interactive = False
        excel.Application.Calculation = -4135
        excel.AutoRecover.Enabled = False

        t, id = win32process.GetWindowThreadProcessId(excel.Hwnd)

        p = psutil.Process(id)

        p.nice(psutil.HIGH_PRIORITY_CLASS)

        if node ==0:
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if "python" in proc.info['name'].lower():  # Check if it's a Python process
                    p = psutil.Process(proc.info['pid'])
                    p.nice(psutil.HIGH_PRIORITY_CLASS)  # Set high priority
                    print(f"Set high priority for PID {proc.info['pid']} ({proc.info['name']})")


        worksheet = workbook.Sheets(sheet_name)
        variable_range = worksheet.Range(range_address)
        objective_cells=[]
        attr_cells=[]

        print(target_list)
        for i in range(len(target_list)):
            objective_cell = worksheet.Range(target_list[i])
            objective_cells.append(objective_cell)

        if attr_list[0]!='':
            for i in range(len(attr_list)):
                attr_cell = worksheet.Range(attr_list[i])
                attr_cells.append(attr_cell)

        

        win32.WithEvents(excel,CalcHandler)

        print(id)

    def check_stop():
        return os.path.exists("stop_signal.txt")
    
    def restart_node():
        global excel, variable_range, objective_cells, file_path, id
        print(f"Closing Node {node}")
        try:
            psutil.Process(id).kill()
            time.sleep(5)
        except:
            print(f"Node {node} is already closed")
        finally:
            print(f"Restarting Node {node}")
            open_workbook()
            print(f"Restart Node {node} complete")
    
    def calc_excel(vars):
        global excel, variable_range, objective_cells, flag, attr_cells
        variable_range.Value = vars

        start=time.time()

        excel.Calculate()

        while flag == False:
            if time.time()-start<60:
                time.sleep(0.01)
            else:
                print(f"The calculation for Node {node} has taken too long")
                restart_node()
                print(f"Rewrite vars for node {node}")
                variable_range.Value = vars
                print(f"Retry Node {node}")
                start=time.time()
                excel.Calculate()

        objective_values = []
        user_attrs = []

        for i in range(len(target_list)):
            objective_value = objective_cells[i].Value
            objective_values.append(objective_value)

        if len(attr_cells)>0:
            for i in range(len(attr_list)):
                attr_value = attr_cells[i].Value
                user_attrs.append(attr_value)

        flag = False

        return objective_values, user_attrs

    def fun(trial):
        global excel, variable_range, objective_cells
        # now = time.time()

        for i in range(num_vars):
            trial.suggest_int(i, lower_bounds_list[i], upper_bounds_list[i], step=1)

        vars = [[x] for x in list(trial.params.values())]
        
        try:
            objective_values, user_attrs=calc_excel(vars)

        except com_error:
            print(f"Error communicating with Node {node}")
            restart_node()
            objective_values, user_attrs=calc_excel(vars)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            restart_node()
            objective_values, user_attrs=calc_excel(vars)

        if check_stop() == True:
            trial.study.stop()

        if attr_list[0]!='':
            for i in range(len(user_attrs)):
                trial.set_user_attr(attr_names[i], user_attrs[i])

        print(f"Model {file_number}:Trial {trial.number} on Node {node}: {objective_values}")
        return objective_values
    
    open_workbook()

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    if len(target_list) == 1:
        study = optuna.create_study(study_name="AMC_Optimiser", sampler=NSGAIIISampler(population_size=population, mutation_prob=mutation), direction=direction_list[0], storage=storage, load_if_exists=True)
    else:
        study = optuna.create_study(study_name="AMC_Optimiser", sampler=NSGAIIISampler(population_size=population, mutation_prob=mutation), directions=direction_list, storage=storage, load_if_exists=True)

    study.optimize(lambda trial: fun(trial), timeout=max_time*3600, n_trials=max_iter)

if __name__.endswith('__main__'):

    dest_folder = sys.argv[1]
    base_name = sys.argv[2]
    node = int(sys.argv[3])
    sheet_name = sys.argv[4]
    range_address = sys.argv[5]
    target_list = ast.literal_eval(sys.argv[6])
    direction_list = ast.literal_eval(sys.argv[7])
    attr_list = ast.literal_eval(sys.argv[8])
    attr_names = ast.literal_eval(sys.argv[9])
    max_iter = int(sys.argv[10])
    max_time = int(sys.argv[11])
    lower_bounds_list = ast.literal_eval(sys.argv[12])
    upper_bounds_list = ast.literal_eval(sys.argv[13])
    num_vars = int(sys.argv[14])
    extension = sys.argv[15]
    population = int(sys.argv[16])
    mutation = float(sys.argv[17])
    ex_vis = sys.argv[18]
    file_number = int(sys.argv[19])

    print("exvis" + str(ex_vis))

    lock_obj = optuna.storages.journal.JournalFileOpenLock("journal.log")
    storage = optuna.storages.JournalStorage(
    optuna.storages.journal.JournalFileBackend("journal.log", lock_obj=lock_obj),
    )

    worker(dest_folder, base_name, node, sheet_name, range_address, target_list, direction_list, storage, max_time, max_iter, lower_bounds_list, upper_bounds_list, num_vars, extension, population, mutation, ex_vis, file_number, attr_list, attr_names)
