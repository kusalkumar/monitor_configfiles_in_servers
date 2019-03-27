#sshutil.py
#general imports
import os
import paramiko
import socket
import sys
from scp import SCPClient

#project specific imports
import shared_module
from mongo_db_connection import MongoDbConnection

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Ssh_Util:
    #"Class to connect to remote server"
    def __init__(self,*args):
        list_arry = []
        self.Connectiondetails(*args)

    def connect(self):
        "Login to the remote server"
        try:
            #Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            print("Establishing ssh connection 9990999")
            self.client = paramiko.SSHClient()
            # Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Connect to the server

            #Connecting using RSAkey for future purpose
            if self.password == '':
                self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey)
                self.client.connect(hostname=self.host, port=self.port, username=self.username, pkey=self.pkey,
                                    timeout=self.timeout, allow_agent=False, look_for_keys=False)
                print("Connected to the server {}".format(self.host))
            else:
                print("=--- here")
                self.client.connect(hostname=self.host, port=self.port, username=self.username,
                                    password=self.password,
                                    timeout=None, allow_agent=False, look_for_keys=False)
                                    #timeout=self.timeout, allow_agent=False, look_for_keys=False)
                print("Connected to the server {}".format(self.host))
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            print("Connection timed out")
            result_flag = False
        except Exception as e :
            print("Exception in connecting to the server\n")
            print('PYTHON SAYS:'.format(e))
            result_flag = False
            self.client.close()
        else:
            result_flag = True

        return result_flag

    def execute_command(self, command):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and a two strings, the first containing stdout
        and the second containing stderr from the command."""
        self.ssh_output = None
        result_flag = True
        output_list = []
        try:
            if self.connect():
                stdin, stdout, stderr = self.client.exec_command(command, timeout=10)

                if stdout.channel.recv_exit_status():
                    print("problem in executing command")
                    output_list.append(stderr.read().decode('ascii').strip("\n"))
                    #command_output = stderr.read()
                    result_flag = False
                else:
                    for line in stdout.readlines():
                        output_list.append(line)

                    print("{} execution completed successfully".format(command))
                if self.ssh_error:
                    #print("Problem occurred while running command:" + command + " The error is " + self.ssh_error)
                    output_list.append(self.ssh_error)
                    result_flag = False
                    self.client.close()
                #return list_output
            else:
                #print("Could not establish SSH connection")
                output_list.append("Could not establish SSH connection")
                result_flag = False
        except socket.timeout as e:
            #print("Command timed out.", command)
            output_list.append("Command timed out")
            self.client.close()
            result_flag = False
        except paramiko.SSHException:
            #print("Failed to execute the command!", command)
            output_list.append("Failed to execute the command")
            self.client.close()
            result_flag = False

        print(output_list)
        return (output_list,result_flag,)


    def upload_file(self, uploadlocalfilepath, uploadremotefilepath):
        "This method uploads the file to remote server"
        result_flag = True
        try:
            if self.connect():
                scpclient = SCPClient(self.client.get_transport(), socket_timeout=15.0)
                scpclient.put(uploadlocalfilepath, uploadremotefilepath)
                self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False
        except Exception as e:
            print("Unable to upload the file to the remote server {}".format(uploadremotefilepath))
            print('PYTHON SAYS:{}'.format(e))
            result_flag = False
            #ftp_client.close()
            self.client.close()

        return result_flag

    def download_file(self):
        "This method downloads the file from remote server"
        result_flag = True
        try:
            if self.connect():
                scpclient = SCPClient(self.client.get_transport(), socket_timeout=15.0)
                scpclient.get(self.downloadremotefilepath, self.localpath)
                self.client.close()
                print("file saved successfully")
            else:
                print("Could not establish SSH connection")
                result_flag = False
        except Exception as e:
            print("\nUnable to download the file from the remote server :{}".format(self.downloadremotefilepath))
            print("PYTHON SAYS:{}".format(e))
            result_flag = False
            #ftp_client.close()
            self.client.close()

        return result_flag

    def parsefile(self, connection_in_str, filepath):
        connection_config_dict = {"server_name":connection_in_str, "values" :shared_module.get_dict_from_file(filepath)}

        mongodb = MongoDbConnection()
        mongodb.connect_to_db()
        mongodb.check_and_update(connection_config_dict)


    def Connectiondetails(self,host,user,pwd,remotepath,localpath,port):
        self.username =user
        self.password=pwd
        self.host = host
        self.port =port
        self.downloadremotefilepath = remotepath
        self.localpath = localpath
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        #self.timeout = float(conf_file.TIMEOUT)
        #self.commands = conf_file.COMMANDS
        ##self.pkey = conf_file.PKEY
        #self.uploadremotefilepath = conf_file.UPLOADREMOTEFILEPATH
        #self.uploadlocalfilepath = conf_file.UPLOADLOCALFILEPATH
        self.downloadlocalfilepath = './test.xml'


    def Defaultfile(self):
        #self.downloadremotefilepath = conf_file.DOWNLOADREMOTEFILEPATH
        #self.host = conf_file.HOST
        #self.username = conf_file.USERNAME
        #self.password = conf_file.PASSWORD
        #self.port = conf_file.PORT
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        #self.timeout = float(conf_file.TIMEOUT)
        #self.commands = conf_file.COMMANDS
        #self.pkey = conf_file.PKEY
        #self.uploadremotefilepath = conf_file.UPLOADREMOTEFILEPATH
        #self.uploadlocalfilepath = conf_file.UPLOADLOCALFILEPATH
        #self.downloadlocalfilepath = conf_file.DOWNLOADLOCALFILEPATH

# ---USAGE EXAMPLES
