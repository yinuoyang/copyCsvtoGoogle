
import argparse
import csv
import datetime
import gspread
import os
import sys
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient import discovery
from pprint import pprint

def parse_args():
    # get the arguments from the command typed in
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--csv-file', required=True)

    return parser.parse_args()


def get_Sheet():
    #login google acount
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Googlemap-09d7f2d816b7.json',scope)
    gc = gspread.authorize(credentials)
    sh = gc.open("hey").sheet1


    return sh

def update():
    return 1

def main():
    args = parse_args()
    file_name = ""
    t = datetime.datetime.now().timetuple()

    file_name += str(t[0])
    file_name += '-'
    if(t[1] < 10):
        file_name += str(0)
        file_name += str(t[1])
    if(t[1] > 10):
        file_name += str(t[1])
    file_name += '-'
    file_name += str(t[2])
    file_name += '_'
    file_name += args.csv_file
    print(file_name)
    fh = open(file_name, 'rt')
    reader = csv.DictReader(fh)
    sh = get_Sheet()

    column_count = 1
    row_count = 1

    headers_printed = False

    # serach in the row from dicreader and paste
    for row in reader:
        for data in row.keys():
            if not headers_printed:
                for header in list(row.keys()):
                        sh.update_cell(column_count, row_count, header)
                        row_count += 1
                row_count = 1
                column_count += 1
                headers_printed = True
            val = sh.cell(column_count, row_count).value
            if(val != row[data]):
                try:
                    sh.update_cell(column_count, row_count, row[data])
                except gspread.exceptions.RequestError or gspread.exceptions.HTTPError:
                    logging.warning("Cannot access Google Drive. Retry one more time in 10 seconds to access it.")
                    time.sleep(10)
                    sh.update_cell(column_count, row_count, row[data])
            row_count += 1
        column_count += 1
        row_count = 1
        print(column_count)

    fh.close()


if __name__ == "__main__":
    main()
