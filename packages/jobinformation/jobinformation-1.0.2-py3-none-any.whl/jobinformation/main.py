#!/usr/bin/python3

import argparse
import csv
from . import __version__
from cowpy import cow

def table(data, simple):
    '''
    Create an ASCII table to format the output.
    
    Args:
        data list[mxn]: The data to be formatted.
        simple (boolean): Indicates if simple formatting (no table) is requested.
    
    Returns:
        str: The formatted string to be printed to the standard output.
        
    Examples usage:
        >>> table([['item (1,1)', 'item (1,2)'], ['item (2,1)', 'item (2,2)']], Fasle)
    '''
    
    width = [max([len(row[i]) for row in data]) for i in range(len(data[0]))]
    
    output = 'ERROR: Analysis done but output text was not formatted correctly!'
    if (simple):
        output = ''
        for row in data:
            data_row = ': '.join(f'{str(cell).ljust(w)} ' for cell, w in zip(row, width)) + '\n'
            output += data_row
    else:
        border = '+' + '+'.join(['-' * (w + 2) for w in width]) + '+\n'
        output = border
        for row in data:
            data_row = '|' + '|'.join(f' {str(cell).ljust(w)} ' for cell, w in zip(row, width)) + '|\n'
            output += data_row + border

    return output

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Easily extract useful information about your jobs',
                                     epilog=f'''
Example usage:
  ./jobinfo.py -f FILE -u USER -a\t Shows the allocation code(s)
  ./jobinfo.py -f FILE -u USER -cms\t Shows the total CPU and memoray usage in simple formatting

This tool assumes your job information file is in CSV format with exactly the following header,
Username,Allocation,JobID,CPUs,JobDuration,Memory

* Please report issues to arc.support@ubc.ca
* Documentation available at https://arc.ubc.ca/
{cow.Moose().milk("Written by Mohammad Zandsalimy")}
                                     ''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
    parser.add_argument('-f', '--file', required=True, help='job information file (CSV)')
    parser.add_argument('-u', '--user', required=True, help='the username')
    parser.add_argument('-a', '--alloc', action='store_true', help='show allocation code(s)')
    parser.add_argument('-r', '--recent', action='store_true', help='show most recent job ID')
    parser.add_argument('-c', '--cpu', action='store_true', help='show total CPU usage in core-hours')
    parser.add_argument('-m', '--mem', action='store_true', help='show total memory usage in GB')
    parser.add_argument('-s', '--simple', action='store_true', help='simple output formatting (no table)')
    parser.add_argument('-v', '--version', action='version', version=f'jobinfo version {__version__}\n{cow.Milk().milk("Written by Mohammad Zandsalimy")}', help='prints version information and exit')
    
    args = parser.parse_args()

    try:
        # Read and parse the job information file
        with open(args.file, 'r') as file:
            csv_reader = csv.DictReader(file)
            jobs = [row for row in csv_reader if row['Username'] == args.user]
            
            if (not jobs):
                print(f'No jobs were found for user {args.user}')
                return

            output = []
            
            # Find allocation codes
            if (args.alloc):
                codes = {job['Allocation'] for job in jobs}
                output.append(['Allocation Code(s)', ', '.join(codes)])
            
            # Find the most recent job ID
            if (args.recent):
                latest = max(jobs, key=lambda x: int(x['JobID']))
                output.append(['Most Recent Job ID', latest['JobID']])
                
            # Find the total CPU usage
            if (args.cpu):
                total = sum(int(job['CPUs'])*int(job['JobDuration'])/60.0 for job in jobs)
                output.append(['Total CPU Usage [core-hours]', f'{total:0.2f}'])
            
            # Find the total memory usage
            if (args.mem):
                total = sum(int(job['Memory']) for job in jobs)
                output.append(['Total Memory Usage [GB]', f'{total:d}'])
            
            # Handle missing input arguments or print to standard output
            if not any([args.alloc, args.recent, args.cpu, args.mem]):
                parser.print_help()
            else:
                print(table(output, args.simple))
    
    # Error handling
    except FileNotFoundError:
        print(f'ERROR: Job information file `{args.file}` was not found.')
    except Exception as e:
        print(f'ERROR: Exception in processing data {str(e)}')

if __name__ == '__main__':
    main()