#!/usr/bin/python3

import csv
import cowsay
import argparse
from . import __version__
from tabulate import tabulate

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Easily extract useful information about your jobs',
                                     epilog=f'''
Example usage:
  jobinfo FILENAME -u USER -a\t Shows the allocation code(s)
  jobinfo FILENAME -u USER -cms\t Shows the total CPU and memoray usage in simple formatting

This tool assumes your job information file is in CSV format with exactly the following header,
Username,Allocation,JobID,CPUs,JobDuration,Memory

* Please report issues to arc.support@ubc.ca
* Documentation available at https://arc.ubc.ca/
{cowsay.get_output_string("cow", "Written by Mohammad Zandsalimy")}
                                     ''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
    parser.add_argument('FILENAME',  help='job information file (CSV)')
    parser.add_argument('-u', '--user', required=True, help='the username')
    parser.add_argument('-a', '--alloc', action='store_true', help='show allocation code(s)')
    parser.add_argument('-r', '--recent', action='store_true', help='show most recent job ID')
    parser.add_argument('-c', '--cpu', action='store_true', help='show total CPU usage in core-hours')
    parser.add_argument('-m', '--mem', action='store_true', help='show total memory usage in GB')
    parser.add_argument('-s', '--simple', action='store_true', help='simple output formatting (no table)')
    parser.add_argument('-v', '--version', action='version', version=f'jobinfo version {__version__}\n{cowsay.get_output_string("milk", "Written by Mohammad Zandsalimy")}', help='prints version information and exit')
    
    args = parser.parse_args()

    try:
        # Read and parse the job information file
        with open(args.FILENAME, 'r') as file:
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
                if (args.simple):
                    print(tabulate(output, tablefmt='plain'))
                else:
                    print(tabulate(output, tablefmt='grid'))
    
    # Error handling
    except FileNotFoundError:
        print(f'ERROR: Job information file `{args.FILENAME}` was not found.')
    except Exception as e:
        print(f'ERROR: Exception in processing data {str(e)}')

if __name__ == '__main__':
    main()