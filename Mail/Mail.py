''' ######### The Smart Mailer program (GMAIL) ########

Name: Charlotte Lim Wee Teng
ID: A0185403J
Date: Completed at 3/10/20


1) List of recipients
File name: Sendto.csv
ID CSV format:
Email ID | Names | Department 

Example:
-----------------------------
bob@gmail.com| Bob | 3103
Alice@gmail.com| Alice| 4543
-----------------------------


2) Message Body and Subject
File Name: Content.txt
Format:
Subject: <Your subject>

<Your content>


Example Content.txt:
----------------------------
Subject: Your subject here

Dear #name# from department #department#,
How do I be better and smarter like my peers. 

----------------------------

Note: Use '#department#' or '#name#' to insert reciever's department code and name

'''
import sys
import csv
import smtplib
import getpass
import ssl
from time import sleep

port = 587
context = ssl.create_default_context()
senderID = "default"
senderPass = "password"



""" 
    Reads the mailing list and filter it using the depcode that was provided
    Input: (String) depCode => (department code/All)
    Output: (dict) filtered dictionary of mailing list
"""
def read_mailing_list(filDepCode):
    dictionary = {}
    id = 0
    csv.register_dialect('myDialect',
                     delimiter='|',
                     skipinitialspace=True,
                     quoting=csv.QUOTE_ALL)
    with open('Sendto.csv', 'r') as file:
        reader = csv.reader(file , dialect='myDialect')
        for row in reader:
            try:
                EmailID = row[0].strip()
                Name = row[1].strip()
                depCode = row[2].strip()
            except:
                raise Exception("Smart Mailer: Sendto.csv Format unable to parse.. please check the guidelines again")
            
            # Fill up dictionary with filter
            if (filDepCode == 'All' or filDepCode == 'all' or depCode == filDepCode):
                dictionary[id] = {"EmailID" : EmailID,"Name" : Name, "DepCode": depCode }
                id = id + 1
            else:
                continue

    if(len(dictionary) == 0):
        raise Exception("\nSmart Mailer: No such person(s) exist in this department or this department does not exist")
    else:
        return dictionary       

""" 
    Reads and Generates the content for each person based on mailing list
    Input: (dict) => filtered mailing list 
    Output: (dict) => content of the mail for every reciever
"""
def read_and_process_mail(mailingList):
    
    with open ('./Mail/Content.txt', 'rt') as myfile:  
        raw_contents = myfile.read()

    # Make content for each person
    contentDict = {}
    header =  "From: {}\nTo: {}\n"
    for index, person in mailingList.items():
        
        to = person["EmailID"]
        Name = person["Name"]
        content = raw_contents
        content = content.replace("#name#", Name)
        content =  header.format(senderID, to)+ content
        contentDict[index] = content
    return contentDict
        


"""
    Secure connection with GMAIL
    output: (server) => (smtpServer)
"""
def connect_to():
    global senderID
    senderID = input('Login Email ID (e.g xxx@gmail.com): ')
    global senderPass
    senderPass = getpass.getpass(prompt='Password (Hidden): ')
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', port)
        server.ehlo()
        server.starttls(context=context)
        server.login(senderID, senderPass)
        print("Successful login!")
        return server
        # ...send emails
    except Exception as err:
        print("\nSmart Mailer: Something went wrong with connection...")
        print(err)
        exit()


"""
    Sends content to mailingList recipient
    input: (server, dict, dict) => (smtpserver, content of mail, filtered mailinglist)
    output: (Dict) => dict of successful sent mail
"""
def send_to(server, Mails, mailingList):
    """
    Start sending
    """
    for index, person in mailingList.items():
        to = person["EmailID"]
    
        try:
            print("Smart Mailer: Sending your mails(" + str(index) + ") ......" )
            server.sendmail(senderID, to, Mails[index])
        except Exception as e:
            print("\nSmart Mailer: Failed to send letter to " + to)
            print(e)
        sleep(2)



def main(EmailID, Name):

    print(EmailID + " " + Name)
    #Read filedata
    mailingList = { 1 : {"EmailID" : EmailID, "Name" : Name}}

    # Connect to server
    server = connect_to()

    #Get mail content
    mails = read_and_process_mail(mailingList)

    # Send to server
    success = send_to(server, mails, mailingList)


    print("====== End =======")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Too little args! Follow this format: python Mail.py RecieverID RecieverName")
        exit(0)
    main(sys.argv[1], sys.argv[2])