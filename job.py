#job.py
import threading
import time

#project specific modules
import shared_module
from sshutil import Ssh_Util
from send_mail import send_email


timestamp_dict = {}

def repeat_task():
    connections_list = shared_module.get_config_var('connections')

    for connection in connections_list:
        connection_in_str = "".join(connection)

        ssh_obj = Ssh_Util(*connection)
        command = "ls -l " +connection[3] +" | awk -F ' ' '{print $6\" \"$7\" \"$8}'"
        command_output, result_flag = ssh_obj.execute_command(command)

        if result_flag:
            last_timestamp = timestamp_dict.get(connection_in_str)
            print(last_timestamp)
            if last_timestamp:
                if command_output[0] != last_timestamp:

                    #connecting and downloading the target remote file
                    ssh_obj.download_file()

                    #parsing and storing the data into mongodb database
                    ssh_obj.parsefile(connection_in_str, connection[4])

                    #sendingthe mail to user with updated file as attachement
                    mail_inst = send_email(connection[4])
                    mail_inst.send_mail_alert()
                    timestamp_dict[connection_in_str] = command_output[0]

                else:
                    print("file didn't modified since %s" %(timestamp_dict.get(connection_in_str)))
            else:
                timestamp_dict[connection_in_str] = command_output[0]
                print(timestamp_dict)
        else:
            if command_output:
                print("there is problem while executing the commanda: %s" %(command_output[0]))
            else:
                print("there is problem while executing the command please check the connection")

        print(time.ctime())

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)