#paramiko_maim.py

import signal
import time
import xml.etree.ElementTree as ET

from datetime import timedelta
from xlrd import open_workbook

#project specific imports
import job
import paramiko_params as pp
import shared_module

from job import Job


class ProgramKilled(Exception):
    pass

def signal_handler(signum, frame):
    raise ProgramKilled

def get_choice(options):

    print("please choose the option:")
    for option in options:
        print("- {} - {}".format(option[0].upper(),option[1]))
    print("[]>",end =" ")
    choice = input()
    return choice

def menu_for_manual():
    list_array =[]
    try:
        num_connections = int(input("Enter number of connections should be >= 1 :"))

        list_parametrs = ['host', 'username', 'password', 'remotepath','localpath', 'port']
        for i in range(num_connections):
            list_conn = []
            for j in range(len(list_parametrs)):
                list_conn.append(input("Enter {} connection {} details : ".format(i + 1, list_parametrs[j])))
            list_array.append(list_conn)

    except ValueError:
        print("Enter valid number")
    except:
        print('You have entered an invalid value.')
    return list_array

def menu_for_xml():
    list_array = []
    file_name = input("enter xml file name: ")
    #tree = ET.parse("configuration.xml")
    tree = ET.parse(file_name)
    root = tree.getroot()
    #for future use if required
    for connectns in root.findall('connections'):
        num_connections = int(connectns.find('totalconn').text)
    for server in root.findall('serverdetails'):
        list_array.append([server.find('host').text, server.find('username').text, server.find('password').text,
                          server.find('remotelocation').text, server.find('localfilepath').text, server.find('port').text])
    return list_array

def menu_for_xla():
    list_array = []
    file_name = input("enter xls file name: ")
    wb = open_workbook(file_name)
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            col_value = []
            for col in range(sheet.ncols):
                value = (sheet.cell(row, col).value)
                try:
                    value = str(int(value))
                except:
                    pass
                col_value.append(value)
            list_array.append(col_value)
    return list_array[1:]

def get_email():
    print("plese enter the gmail where you want to get alerts:")
    email = str(input())
    return email

if __name__ == '__main__':
    print("Start of %s" % __file__)

    options = [('manual', 'eneter details manual'), ('xmlfile', 'upload configuration file'), ('excelfile', 'upload excel file')]

    while 1:
        option = get_choice(options)
        if option == "manual":
            list_array = menu_for_manual()
            break
        elif option == "xmlfile":
            list_array = menu_for_xml()
            break
        elif option == "excelfile":
            list_array = menu_for_xla()
            break
        else:
            print("choose proper option")


    if list_array:
        receiver_mail = get_email()
        shared_module.set_config_var(list_array, receiver_mail)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        job = Job(interval=timedelta(seconds=pp.WAIT_TIME_SECONDS), execute=job.repeat_task)
        job.start()

        while True:
            try:
               time.sleep(1)
            except ProgramKilled:
                print("Program killed: running cleanup code")
                job.stop()
                break
    else:
        print("we are unable to find the server details. Please check the input provided")

