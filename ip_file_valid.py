import os.path
import sys

current_working_path = os.getcwd()

# Checking IP address file and content validity


def ip_file_valid():

    # Prompting user for input
    ip_file = current_working_path + "/ip.txt"

    # Changing exception message
    if os.path.isfile(ip_file) == True:
        print("\n* IP file is valid :)\n")

    else:
        print(
            "\n* File {} does not exist :( Please check and try again.\n".format(ip_file))
        sys.exit()

    # Open user selected file for reading (IP addresses file)
    selected_ip_file = open(ip_file, 'r')

    # Starting from the beginning of the file
    selected_ip_file.seek(0)

    # Reading each line (IP address) in the file
    ip_list = selected_ip_file.readlines()

    # Closing the file
    selected_ip_file.close()

    return ip_list
