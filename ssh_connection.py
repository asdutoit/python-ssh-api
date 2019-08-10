import paramiko
import os.path
import time
import sys
import re

current_working_path = os.getcwd()

# Checking username/password file
# Prompting user for input - USERNAME/PASSWORD FILE
user_file = current_working_path + "/user.txt"

ontSN = input("\n# Enter the ONT SN you are looking for:")

# Verifying the validity of the USERNAME/PASSWORD file
if os.path.isfile(user_file) == True:
    print("\n* Username/password file is valid :)\n")

else:
    print(
        "\n* File {} does not exist :( Please check and try again.\n".format(user_file))
    sys.exit()

# Checking commands file
# Prompting user for input - COMMANDS FILE
cmd_file = current_working_path + "/cmd.txt"

# Verifying the validity of the COMMANDS FILE
if os.path.isfile(cmd_file) == True:
    print("\n* Command file is valid :)\n")

else:
    print(
        "\n* File {} does not exist :( Please check and try again.\n".format(cmd_file))
    sys.exit()

# Open SSHv2 connection to the device


def ssh_connection(device):

    global user_file
    global cmd_file

    device = device.rstrip("\n")
    ip = device.split(',')[0].rstrip("\n")
    port = device.split(',')[1].rstrip("\n")

    # Creating SSH CONNECTION
    try:
        # Define SSH parameters
        selected_user_file = open(user_file, 'r')

        # Starting from the beginning of the file
        selected_user_file.seek(0)

        # Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")

        # Starting from the beginning of the file
        selected_user_file.seek(0)

        # Reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")

        # Logging into device
        session = paramiko.SSHClient()

        # For testing purposes, this allows auto-accepting unknown host keys
        # Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the device using username and password
        session.connect(ip.rstrip("\n"), port,
                        username=username, password=password)

        # Start an interactive shell session on the router
        connection = session.invoke_shell()
        connection.recv(58).decode()
        if not connection.recv_ready():
            connection.send('\x1b1;1R\n')

        # Setting terminal length for entire output - disable pagination
        # connection.send("\n")
        # # connection.send("terminal length 0\n")
        # time.sleep(1)

        # # Entering global config modeq
        # connection.send("\n")
        # # connection.send("configure terminal\n")
        # time.sleep(4)

        # Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')

        # Starting from the beginning of the file
        selected_cmd_file.seek(0)

        # Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)

        # Closing the user file
        selected_user_file.close()

        # Closing the command file
        selected_cmd_file.close()

        # Checking command output for IOS syntax errors
        router_output = connection.recv(65535)
        a = str(router_output)
        b = '\n'.join(a.split('\\r\\n')).lstrip('b').replace('\\r', '')
        print(b)

        if re.search('(' + ontSN + ')', b):
            print('The ONT has been found and unregistered')
        else:
            connection.send("show remote ont filter {} \n".format(ontSN))
            time.sleep(2)
            router_output2 = connection.recv(65535)
            router_output2_str = str(router_output2)
            bb = '\n'.join(router_output2_str.split('\\r\\n')
                           ).lstrip('b').replace('\\r', '')
            print(bb)
            if re.search('(' + ontSN + ')', bb):
                x = re.search("(ont-\d-\d-\d+)", bb)
                print(x[0])
                connection.send("show remote ont {} \n".format(x[0]))
                time.sleep(2)
                router_output3 = connection.recv(65535)
                router_output3_str = str(router_output3)
                bbb = '\n'.join(router_output3_str.split('\\r\\n')
                                ).lstrip('b').replace('\\r', '')
                print(bbb)

        if re.search(b"% Invalid input", router_output):
            print(
                "* There was at least one IOS syntax error on device {} :(".format(ip))

        else:
            print("\nDONE for device {} :)\n".format(ip))

        # Test for reading command output
        # print(re.findall(
        #     r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str(router_output))[1])

        # Closing the connection
        session.close()

    except paramiko.AuthenticationException:
        print("* Invalid username or password :( \n* Please check the username/password file or the device configuration.")
        print("* Closing program... Bye!")
