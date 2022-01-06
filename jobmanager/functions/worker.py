from jobmanager.functions.add_column import add_columns

dict_func = {
    'Add Columns': add_columns,

}

def run_jobs():
    #get the jobs
    #run function based on job.func_name
    #
    for job in jobs:
        func_name = job.func_name
        dict_func[func_name](job)
