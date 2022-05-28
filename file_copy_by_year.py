# file_copy_by_year.py
"""
Usage:
file_copy_by_year.py INPUT_ROOT_PATH OUTPUT_ROOT_PATH
file_copy_by_year.py --version

Options:
 -h --help  Display help
 -q --quit  exit
 --version  Version 1.0
"""
import sys
import argparse
from docopt import docopt
import pathlib
from datetime import datetime as dt
import os
import shutil


def get_year(timestamp: float):
    return dt.fromtimestamp(timestamp).strftime("%Y")


def get_file_timestamp(file_path, time_type="modified"):
    """
    Obtain timestamp from file properties
    :param file_path:
    :param time_type: One of three types: `"modified"`, `"accessed` or `"created"`
    :return:
    """
    if time_type == "modified":
        return os.stat(file_path).st_mtime
    elif time_type == "accessed":
        return os.stat(file_path).st_atime
    elif time_type == "created":
        return os.stat(file_path).st_ctime
    else:
        raise ValueError(f"wrong time_type {time_type} provided")


def access_all_files(file_path):
    for root, dir, file in os.walk(file_path):
        for file_name in file:
            yield os.path.join(root, file_name)


def copy_file_to_dir_with_attributes(source_file_name, dest_file_path):
    try:
        shutil.copy2(source_file_name, dest_file_path)
    except IOError:
        return False
    return True


'''
Current issues
File deep inside some folder lose the context
'''


def copy_files_to_year(path, output_base_path):
    failed_copies = []
    count = 0
    for full_file_path in access_all_files(path):
        file_year = get_year(get_file_timestamp(full_file_path))
        output_path = os.path.join(output_base_path, file_year)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        copy_success = copy_file_to_dir_with_attributes(full_file_path, output_path)
        if not copy_success:
            failed_copies.append(full_file_path)
        else:
            count += 1

        if count % 100 == 0:
            print(f'Total {count} files copied')

    return count, failed_copies


def main(args):
    # args = docopt(__doc__)
    input_root_path = args['INPUT_ROOT_PATH']
    output_root_path = args['OUTPUT_ROOT_PATH']
    message = f'Received Input root directory:{input_root_path}\n' \
              f'Output Write Directory:{output_root_path}\n' \
              f'Confirm y to continue:'

    do_continue = input(message)
    if do_continue.lower() == 'y':
        count, failed_copies = copy_files_to_year(input_root_path, output_root_path)
        print(f'Total {count} files copied to {output_root_path}')
        if failed_copies:
            print(f'Total {len(failed_copies)} files not copied. List of all such files is')
            for index, name in enumerate(failed_copies):
                print(index, name)
    else:
        print('Copying process cancelled')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # args = sys.argv
    # main()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('INPUT_ROOT_PATH', type=str,
                        help='Input path for copying files')
    parser.add_argument('OUTPUT_ROOT_PATH', type=str,
                        help='Output path for writing')

    args = parser.parse_args()
    main(vars(args))
