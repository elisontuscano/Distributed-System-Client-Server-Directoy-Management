#Elison Tuscano
#1001738728

import socket
import sys
import tkinter as tk
import re
import os
from os import path
import os.path
import shutil
import pickle
from dirsync import sync


#WORKING ON DISPLAY

#Scroll Bar Frame:
#reference : https://stackoverflow.com/questions/31762698/dynamic-button-with-scrollbar-in-tkinter-python
class VerticalScrolledFrame(tk.Frame):

    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,height=500, yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=600)

        interior.bind('<Configure>', _configure_interior)
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

#FUNCTION TO PRINT ON UI
def PRINT_LABEL(VALUE):
    label1 = tk.Label(scframe.interior, text = VALUE)
    label1.pack()

#FUNCTION TO HANDLE UI INPUTS
def UI_INPUT(Button, IntVal):
    Button.wait_variable(IntVal)
    INPUT = Entry1.get()
    Entry1.delete(0,'end')
    return INPUT


#FUNCTION TO HANDLE QUIT
def QUIT(top):
    USERNAME_STATUS = False
    top.destroy()
    sys.exit(0)

def QUIT2(top):
    response = myclient.send(str.encode('bye'))
    USERNAME_STATUS = False
    top.destroy()
    sys.exit(0)

#Function to check whether contains any special character
#ref : https://www.geeksforgeeks.org/python-program-check-string-contains-special-character/
def Special_Char_Check(string):  
    regex = re.compile('[@_!#$%^&*()<>?\|}{~:]')   
    if(regex.search(string) == None): 
        #print("String is accepted") 
        return False          
    else: 
        #print("String is not accepted.") 
        return True

#FUNCTION TO GET USERNAME UI
def GET_USERNAME():
    USERNAME_STATUS = False
    while not USERNAME_STATUS:
        PRINT_LABEL("Enter Your Username : only alphabet and numbers accepted")  #INPUT TO PRINT LABEL FUNCTION ABOVE
        username = UI_INPUT(Button1,int_var)
        myclient.send(str.encode(username))  #UI SEND 1 CLIENTNAME
        response = str(myclient.recv(1024),'utf-8') #UI RECV 1 USERNAME CHECK
        if response == 'Special Character Detected Username not accepted':
            Label1 = tk.Label(scframe.interior, text='Special Character Detected Username not accepted')
            Label1.pack()
            continue
        elif response == 'Username Exists and is Active':
            Label1 = tk.Label(scframe.interior, text='Username Taken & Active')
            Label1.pack()
            continue
        USERNAME_STATUS = True
    return USERNAME_STATUS, username

#FUNCTION TO GET Identifier UI
def Get_Identifier():
    STATUS = False
    while not STATUS:
        PRINT_LABEL("Enter Your Identifier : A , B , C")  #INPUT TO PRINT LABEL FUNCTION ABOVE
        identifier = UI_INPUT(Button1,int_var)
        #print(identifier)

        if identifier == 'A' or identifier == 'B' or identifier == 'C':
            #print("ok input")
            a=0
        else:
            #print("bad input")
            Label1 = tk.Label(scframe.interior, text='Invalid Identifier')
            Label1.pack()
            continue

        myclient.send(str.encode(identifier))  #UI SEND 
        response = str(myclient.recv(1024),'utf-8') #UI RECV

        if response == 'Identifier Exists':
            Label1 = tk.Label(scframe.interior, text='Identifier Taken')
            Label1.pack()
            continue
        STATUS = True
     
    return identifier

#Function to get response of user directory from server
def Get_Directory(username):
    myclient.send(str.encode(username))
    response = str(myclient.recv(1024),'utf-8')
    return response


def setup():
    #https://realpython.com/python-sockets/
    myclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    myclient.connect((HOST, PORT))
    return myclient, HOST, PORT

#funtion to sync/update local directories with server directories
#ref:https://pypi.org/project/dirsync/
def Sync():
    print('doing sync')
    global logPath
    global Identifier
    with open(logPath , "rb") as fp:
        idsync = pickle.load(fp)
    for key , value in idsync.items():
        dest = Identifier +'/'+ key
        if not path.exists(dest):
            os.mkdir(dest)
        sync(value , dest,"sync",purge=True)
    print("done")

if __name__ == "__main__":

    HOST = '127.0.0.1'
    PORT = 1395

    #ADDING CODE FOR DISPLAY
    ##https://www.python-course.eu/tkinter_labels.php
    top = tk.Tk()
    top.title("Client")
    scframe = VerticalScrolledFrame(top)
    scframe.pack()
    int_var = tk.IntVar() #TO STORE INTEGER VAR
    myclient, HOST, PORT = setup()  #GETTING SETUP DETAILS
    Entry1 = tk.Entry(scframe.interior)
    Entry1.pack()
    Button1 = tk.Button(scframe.interior, text = 'Enter', command = lambda: int_var.set(1))
    Button1.pack()
    USERNAME_STATUS, username = GET_USERNAME() #CHECK ABOVE SEND AND RECV 1 UI
    PRINT_LABEL(str("Client "+username+" Has been connected"))
    Directory_Response = Get_Directory(username) #let serve create or use existing directory
    Identifier = Get_Identifier() #select identifier from(A,B,C)
    

    Entry1.destroy()
    Button1.destroy()
    if USERNAME_STATUS:
        PRINT_LABEL(str("Identifier "+Identifier+" Has been approved"))
        PRINT_LABEL(Directory_Response)

        if path.exists(Identifier):
            print('Identifier directory exists')
        else:
            os.mkdir(Identifier)
            print('Identifier Directory Created')
        
        logPath = Identifier + '/' + 'log.txt'   # create log files to keep record of all sync directories
        idsync={}
        if path.isfile(logPath):
            with open(logPath,"rb") as fp:
                idsync=pickle.load(fp)
            print('log file exists')
        else:
            with open(logPath,"wb") as fp:
                pickle.dump(idsync , fp)
            print('log file created')

        #MAKE CHOICE LOOP
        while USERNAME_STATUS != False:
            PRINT_LABEL("Enter 1: Create Directory \n 2: Delete Directory \n  3: Move Directory \n 4: Rename Directory \n 5:List directory Contents \n 6:List Home directories to sync \n 7:Snyc Home directory \n 8:See local Directory \n 9:Desync local Directory \n 10:See Logs \n 11:Undo from Logs")
            PRINT_LABEL("'bye' To Quit ")
            Entry1 = tk.Entry(scframe.interior)
            Entry1.pack()
            Button1 = tk.Button(scframe.interior, text = 'Enter', command = lambda: int_var.set(1))
            Button1.pack()
            Button2 = tk.Button(scframe.interior, text = 'Quit', command = lambda: QUIT2(top))
            Button2.pack()
            Choice = UI_INPUT(Button1, int_var)  #Get Numerical Choice
            SERVER_RESPONSE = myclient.send(str.encode(Choice))  #UI SEND 2. CHOICE

            #QUIT HANDLING
            if Choice == 'bye':
                QUIT(top)
            
            #Creating Directories
            if Choice == '1':
                PRINT_LABEL("Enter directory name to be created")
                dirname = UI_INPUT(Button1, int_var)
                
                if Special_Char_Check(dirname):
                    PRINT_LABEL("Special Character detected cannot list such directory")
                    myclient.send(str.encode("Invalid input"))
                elif len(dirname)==0:
                    PRINT_LABEL("Name cannot be empty")
                    myclient.send(str.encode("Invalid input"))
                else:
                    myclient.send(str.encode(dirname)) 
                    PRINT_LABEL("Enter Path of directory | Leave Empty to create in home directory")
                    dirPath = UI_INPUT(Button1, int_var)

                    if len(dirPath)==0:
                        myclient.send(str.encode("Create in Home Directory"))
                        response = str(myclient.recv(1024),'utf-8')
                        PRINT_LABEL(response)
                    elif Special_Char_Check(dirPath):
                        PRINT_LABEL("Special Character detected cannot create in such directory")
                        myclient.send(str.encode("Invalid input"))
                    else:
                        myclient.send(str.encode(dirPath))
                        response = str(myclient.recv(1024),'utf-8')
                        PRINT_LABEL(response)


            #Delete Directories
            elif Choice == '2':
                PRINT_LABEL("Enter directory name to be deleted")
                dirname = UI_INPUT(Button1, int_var)
                
                if Special_Char_Check(dirname):
                    PRINT_LABEL("Special Character detected cannot delete such directory")
                    myclient.send(str.encode("Invalid input"))
                elif len(dirname)==0:
                    PRINT_LABEL("Name cannot be empty")
                    myclient.send(str.encode("Invalid input"))
                else:
                    myclient.send(str.encode(dirname)) 
                    PRINT_LABEL("Enter Path of directory | Leave Empty to delete in home directory")
                    dirPath = UI_INPUT(Button1, int_var)
                    if len(dirPath)==0:
                        myclient.send(str.encode("Delete in Home Directory"))
                        response = str(myclient.recv(1024),'utf-8')
                        PRINT_LABEL(response)
                    elif Special_Char_Check(dirPath):
                        PRINT_LABEL("Special Character detected cannot delete in such directory")
                        myclient.send(str.encode("Invalid input"))
                    else:
                        myclient.send(str.encode(dirPath))
                        response = str(myclient.recv(1024),'utf-8')
                        PRINT_LABEL(response)

            #Move Directories
            elif Choice == '3':
                PRINT_LABEL("Enter directory name to be moved")
                dirname = UI_INPUT(Button1, int_var)
                
                if Special_Char_Check(dirname):
                    PRINT_LABEL("Special Character detected cannot move such directory")
                    myclient.send(str.encode("Invalid input"))
                elif len(dirname)==0:
                    PRINT_LABEL("Name cannot be empty")
                    myclient.send(str.encode("Invalid input"))
                else:
                    myclient.send(str.encode(dirname)) 
                    PRINT_LABEL("Enter Source Path of directory | Leave Empty to move from home directory") #enter source
                    source_dirPath = UI_INPUT(Button1, int_var)
                    PRINT_LABEL("Enter Destination Path of directory | Leave Empty to move to home directory") #destination source
                    dest_dirPath = UI_INPUT(Button1, int_var)

                    if Special_Char_Check(source_dirPath) or Special_Char_Check(dest_dirPath):
                        PRINT_LABEL("Special Character detected cannot move in such directory")
                        myclient.send(str.encode("Invalid input"))
                    else:
                        if len(source_dirPath)==0:
                            myclient.send(str.encode("Move from Home Directory")) #source is home directory
                        else:
                            myclient.send(str.encode(source_dirPath))
                        
                        if len(dest_dirPath)==0:
                            myclient.send(str.encode("Move from Home Directory")) #destination is home directory
                        else:
                            myclient.send(str.encode(dest_dirPath))

                        response = str(myclient.recv(1024),'utf-8')
                        PRINT_LABEL(response)

            #Rename Directory
            elif Choice == '4':
                PRINT_LABEL("Enter directory name to be Renamed")
                dirname = UI_INPUT(Button1, int_var)
                PRINT_LABEL("Enter new directory name")
                newdirname = UI_INPUT(Button1, int_var)
                
                if Special_Char_Check(dirname) or Special_Char_Check(newdirname):
                    PRINT_LABEL("Special Character detected cannot rename such directory")
                    myclient.send(str.encode("Invalid input"))
                elif len(dirname)==0 or len(newdirname)==0: #empty input handling
                    PRINT_LABEL("Name cannot be empty")
                    myclient.send(str.encode("Invalid input"))
                else:
                    myclient.send(str.encode(dirname)) 
                    myclient.send(str.encode(newdirname)) 
                    PRINT_LABEL("Enter Path of directory | Leave Empty to delete in home directory")
                    dirPath = UI_INPUT(Button1, int_var)
                    if len(dirPath)==0:
                        myclient.send(str.encode("Rename in Home Directory"))
                        response = str(myclient.recv(1024),'utf-8')
                        PRINT_LABEL(response)
                    elif Special_Char_Check(dirPath):
                        PRINT_LABEL("Special Character detected cannot Rename in such directory")
                        myclient.send(str.encode("Invalid input"))
                    else:
                        myclient.send(str.encode(dirPath))
                        response = str(myclient.recv(1024),'utf-8')
                        PRINT_LABEL(response)

            elif Choice == '5':
                PRINT_LABEL("Enter Path of directory | Leave Empty to see home directory")
                dirPath = UI_INPUT(Button1, int_var)
                if len(dirPath)==0:
                    myclient.send(str.encode("Show Home Directory"))
                    response = str(myclient.recv(1024),'utf-8')
                    PRINT_LABEL(response)
                elif Special_Char_Check(dirPath):
                    PRINT_LABEL("Special Character detected cannot list such directory")
                    myclient.send(str.encode("Invalid input"))
                else:
                    myclient.send(str.encode(dirPath))
                    response = str(myclient.recv(1024),'utf-8')
                    PRINT_LABEL(response)

            elif Choice == '6': # option to list directories that are available to sync from server
                PRINT_LABEL("Enter Path of directory | Leave Empty to All home directory")
                dirPath = UI_INPUT(Button1, int_var)
                if len(dirPath)==0:
                    myclient.send(str.encode("Show All Directory"))
                    response = str(myclient.recv(1024),'utf-8')
                    PRINT_LABEL(response)
                elif Special_Char_Check(dirPath):
                    PRINT_LABEL("Special Character detected cannot list such directory")
                    myclient.send(str.encode("Invalid input"))
                else:
                    myclient.send(str.encode(dirPath))
                    response = str(myclient.recv(1024),'utf-8')
                    PRINT_LABEL(response)
            
            elif Choice == '7': #decide which directory to sync
                PRINT_LABEL("Enter Name of directory to sync")
                dirPath = UI_INPUT(Button1, int_var)
                if len(dirPath)==0:
                    PRINT_LABEL("Field cannot be empty")
                    myclient.send(str.encode("Invalid input"))
                elif Special_Char_Check(dirPath):
                    PRINT_LABEL("Special Character detected cannot sync such directory")
                    myclient.send(str.encode("Invalid input"))
                else:
                    myclient.send(str.encode(dirPath))
                    response = str(myclient.recv(1024),'utf-8')
                    if response =="No such Path or directory exists":
                        PRINT_LABEL(response)
                    else:
                        with open(logPath,"rb") as fp:
                            idsync=pickle.load(fp)
                        idsync[dirPath]=response
                        with open(logPath,"wb") as fp:
                            pickle.dump(idsync,fp)
                        Sync()
                        PRINT_LABEL("Sync Completed")
            
            elif Choice == '8': # view local directory
                Sync()
                PRINT_LABEL("Enter Path of directory | Leave Empty to All Local directory")
                dirPath = UI_INPUT(Button1, int_var)
                if len(dirPath)==0:
                    localPath = Identifier
                elif Special_Char_Check(dirPath):
                    PRINT_LABEL("Special Character detected showing All local directory")
                    localPath = Identifier
                else:
                    localPath = Identifier +dirPath

                print(localPath)
                if path.exists(localPath):
                    listdirectory = os.listdir(localPath)
                    result='List of Directories in Your Folder:\n'
                    for directory in listdirectory:
                        if directory !='log.txt':
                            result = result + directory +" \n"
                    if len(listdirectory)==0:
                        result='Directory is Empty'
                
                PRINT_LABEL(result)
            
            elif Choice == '9': # desync any available directory and delete it.
                PRINT_LABEL("Enter Name of Local Directory to Desync")
                desync = UI_INPUT(Button1, int_var)
                desyncPath = Identifier +'/'+desync
                if path.exists(desyncPath):
                    shutil.rmtree(desyncPath)
                    with open(logPath,"rb") as fp:
                        idsync=pickle.load(fp)
                    idsync.pop(desync,'no key found')
                    with open(logPath,"wb") as fp:
                        pickle.dump(idsync,fp)
                    PRINT_LABEL("Directory Desynced and deleted")   

                else:
                    PRINT_LABEL("No Such Path Exists")   

            elif Choice =='10': #see logs
                response = str(myclient.recv(1024),'utf-8')
                PRINT_LABEL(response)

            elif Choice =='11': #see logs
                PRINT_LABEL("Enter SR. Number to undo")
                srNo = UI_INPUT(Button1, int_var)
                myclient.send(str.encode(srNo))
                response = str(myclient.recv(1024),'utf-8')
                PRINT_LABEL(response)




            Sync()
            Entry1.destroy()
            Button1.destroy()
            Button2.destroy()
            PRINT_LABEL("=========================================")
            

        PRINT_LABEL("Client Disconnected")
        top.mainloop()

#reference : https://github.com/isiddheshrao/Distributed-Systems/blob/master/Client.py
