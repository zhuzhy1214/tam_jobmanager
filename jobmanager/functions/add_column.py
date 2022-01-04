import os
import pandas as pd


class Job:
    def __init__(self, func_name, job_id=None, notes='', log=''):
        self.id = job_id
        self.func_name = func_name
        self.notes = ''
        self.date_requested = ''
        self.status = ''
        self.log = ''
        self.input_file = ''
        self.output_file = ''
        self.server_output_file = ''
        self.input_folder = ''

    def cleanup(self):
        # clean up, clear job id, delete local input and output file
        self.id = None
        # delete job data file
        if self.input_file != 'No input file uploaded.':
            try:
                os.remove(self.input_file)
            except:
                print("Error while deleting file ", self.input_file)

        if self.output_file != '':
            try:
                os.remove(self.output_file)
            except:
                print("Error while deleting file ", self.output_file)


def add_columns(job):
    'a sample function to add all columns'

    if job.input_file == 'No input file uploaded.':
        job.log = 'No Input file was provided for:{}'.format(job.func_name)
        job.status = 'Input Error'
        return 'Failed'

    try:
        local_file_path = job.input_file
        input_notes = job.notes

        # read file
        df = pd.read_excel(local_file_path)

        # get the file name
        base = os.path.basename(local_file_path)
        filename = os.path.splitext(base)[0]

        # do job
        df['result'] = df.sum(axis=1)

        # export output
        df_out = df
        output_filepath = os.path.join('./job_output', r'{}.csv'.format(filename))
        df_out.to_csv(output_filepath, index=False)

        job.output_file = output_filepath
        # print(output_filepath,job.output_file)
        job.log = 'no additional calculation log.'
        job.status = 'Function Complete'

        return 'Success'
    except:
        job.log = 'Error occured processing function:{}'.format(job.func_name)
        job.status = 'Function Error'
        job.output_file = ''
        return 'Failed'