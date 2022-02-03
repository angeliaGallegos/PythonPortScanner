#################################################
#
#
# NAME: Angelia Gallegos-Loveland
#
# COURSE: CYBER 260-40
#
# SECTION: 2021F7A
#
# DATE: 10/13/2021
#
# PURPOSE: Performs a port scan on a targeted server / generates a text file / emails results file to CIO.
# For the purpose of turning in the assignment, the IP address and email will be asked for input from the user.
# However, for the scenario the IP and email addresses are statically coded, but commented out to be used later.
# It's sole purpose is testing for this project.
#
#
#################################################

# Importing all the different libraries that will be used throughout the program
import smtplib
import datetime
import socket
import os
import sys
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart


######
# Function: sendEmail
# Purpose: Takes the results text file that has been created and emails them to specified address
# Inputs: completeName from main
# Returns: None
######
def sendEmail(completeName):

    # Setting the variables for sender and receiver for email
    # Again, for the scenario the email is statically coded, but is commented out.
    # However, for the purpose of turning this assignment in, the user will plug in the email they wish the results get sent to
    sender = 'youremail@gmail.com'
    receiver = input("\nPlease enter the email in which to send the results: ")
    #receiver = ['youremail@email.com'] # Insert the email you would like the results sent to

    # Setting up the subject line as well as the sender and receiver info for email
    msg = MIMEMultipart()
    msg['Subject'] = 'Port Scan Results'
    msg['From'] = sender
    msg['To'] = receiver

    # Sending attachment in email
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(completeName, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename = "ScanResults.txt"')
    msg.attach(part)

    # Email authentication via SSL through Google SMTP server
    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    s.login(user=sender, password="yourPassword")  # Test email created
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    # Printing message that the email has been sent and at what time
    print("\nResults have been emailed to {}".format(receiver) + " at " + str(datetime.datetime.now()))

######
# Function: portScanner
# Purpose: Performs the scanning of the ports for the targeted system
# Inputs: file1 and serverIP from main
# Returns: None
######
def portScanner(file1):

    # For turning in this assignment (make it easy for end user to run) IP will be gathered by user
    # Scenario wise, the statically coded IP is commented out
    targetIP = input("Please enter the server IP: ")
    serverIP = socket.gethostbyname(targetIP)

    # Commented section for statically coded server IP
    # remoteServer = "192.168.x.xxx" # Plug in static IP of the server you wish to run port scan on
    #serverIP = socket.gethostbyname(remoteServer)

    print("\nBeginning scan on IP: {}".format(serverIP))
    print("-" * 60)

    try:
        # For loop that will loop through the port number range specified
        # Not doing a full scan.. because that would take forever!
        for port in range(1, 1024 + 1):
            # Creating the socket flag
            scanSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scanSoc.settimeout(0.5)
            result = scanSoc.connect_ex((serverIP, port))

            # If 0 is returned it means the port is open
            if result == 0:
                file1.write("IP: {}  |  Port {} - OPEN\n".format(serverIP, port))

            # Else port is closed
            else:
                file1.write("IP: {}  |  Port {} - CLOSED\n".format(serverIP, port))

            # CLosing the socket
            scanSoc.close()

    # Exception for keyboard interrupt
    except KeyboardInterrupt:
        print("\nExiting the program!")
        sys.exit()

    # Exception for if the server is down
    except socket.error:
        file1.write("Could not connect to server")
        sys.exit()

    # Message print for when scan has completed
    print("\nScan complete!")

    # Closing out the file being written
    file1.close()

######
# Function: main
# Purpose: Main function of program
# Inputs: None
# Returns: None
######
def main():

    # Header for the program
    print("Port Scanner Final Project")
    print("-" * 60)
    print()

    # Creating a value for path in which the file will be saved (change depending on hard drive setup)
    # Creating a value for the name of the port scanner document
    # Joining the file name and the location together into one variable name
    savePath = 'D:/Desktop'
    portScan = "ScanResults.txt"
    completeName = os.path.join(savePath, portScan)

    # Creating the port scan document
    file1 = open(completeName, "w")
    file1.write("Results of server port scan on " + str(datetime.datetime.now()))
    file1.write("\n---------------------------------------------------------")
    file1.write("\n")
    file1.write("\n")

    # Calling on the portScanner function
    # Passing the port scan text file being created as well as the IP of the server
    portScanner(file1)

    # Calling on the sendEmail function and passing completeName to it
    sendEmail(completeName)

# Program starts here

main()

# Program ends here


