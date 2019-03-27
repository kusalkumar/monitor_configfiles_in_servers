#from config_parser import config
import paramiko_params as pp

from configparser import ConfigParser

def get_dict_from_file(file_path):
    config = ConfigParser()
    config.read_file(open(file_path))
    config_var_dict = {}
    for section in config.sections():
        config_var_dict[section] = dict(config.items(section))
    print(config_var_dict)
    return config_var_dict



def string_to_list(var_value):
    connection_array = []
    for connection in var_value.split(','):
        connection_array.append(connection.split(" "))
    return connection_array

def list_to_string(list_array):
    connection_string = ''
    for connection in list_array:
        for element in connection:
            connection_string += str(element)+' '
        connection_string = connection_string.strip()+','
    return connection_string[:-1]

def get_config_var(var):
    config = ConfigParser()
    fp = open(pp.config_file)
    config.readfp(fp)
    var_value = config.get('project_config',var)
    if var == 'connections':
        var_value = string_to_list(var_value)
    return var_value

def set_config_var(list_array, receiver_mail):
    config = ConfigParser()
    fp = open(pp.config_file)
    config.readfp(fp)
    config.set('project_config', 'connections', list_to_string(list_array))
    config.set('project_config', 'user_mail', receiver_mail)
    with open(pp.config_file, 'w') as f:
        config.write(f)
    fp.close()
