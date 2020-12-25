#Elison Tuscano
#1001738728

import datetime
import socket
import tkinter as tk
import sys
import threading
from _thread import *
import os
from os import path
import re
import os.path
import shutil

#CREATING CODE FOR UI
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

#FUNCTION TO HANDLE QUIT
def QUIT(top):
    top.destroy()
    sys.exit(1)

#STATUS OF CLIENTS ON UI
#https://www.python-course.eu/tkinter_labels.php
def MAIN_DISPLAY(NULL):
    top = tk.Tk()
    top.title("Server")
    main = tk.Canvas(top, height= 700,width= 850)
    main.pack()
    global frame
    frame = tk.Frame(main)
    frame.place(relwidth = 1, relheight= 0.9)
    Label1 = tk.Label(frame)
    Label1.pack()
    title_label1 = tk.Label(frame, justify=tk.LEFT, padx = 10)
    title_label1.pack(side = "left")
    title_label1.config(text = "Total Usernames in this Session ->")
    title_label2 = tk.Label(frame, justify=tk.RIGHT, padx = 10)
    title_label2.pack(side = "right")
    title_label2.config(text = "<- Active Usernames in this Session")
    Label2 = tk.Label(frame, justify=tk.LEFT, padx = 10)
    Label2.pack(side ="left")
    Label3 = tk.Label(frame, justify=tk.RIGHT, padx = 10)
    Label3.pack(side ="right")
    UPDATE(Label1,top)
    SHOW_LIST(top, Label2, Label3)
    Button1 = tk.Button(frame, text = 'Quit', command = lambda: QUIT(top))
    Button1.pack()
    top.mainloop()

#CODE TO UPDATE CLIENT STATUS UI IN EVERY 1000MS
def UPDATE(Label1,top):
    global USER_STATUS
    global count
    if USER_STATUS == True:
        PRINT_UI = str(str(count) + " Client(s) Connected")
        Label1.config(text = PRINT_UI)
    else:
        Label1.config(text = "No Client Connected")
    top.after(1000, lambda: UPDATE(Label1, top))

#CODE TO UPDATE USERNAMES AND ACTIVE USERNAMES AND UPDATE EVERY 1000MS
def SHOW_LIST(top, label2, Label3):
    label2.config(text = USERNAMES)
    Label3.config(text = ACTIVE_USERNAMES)
    top.after(1000, lambda: SHOW_LIST(top, label2, Label3))


#CODE FOR THREAD DELETION
def THREAD_DEL():
    global STOP_CLIENT_THREAD
    global count
    STOP_CLIENT_THREAD = True
    count -=1 #UI UPDATE
    newclientthread.join()  #TO CHECK AND DELETE THREAD CONTEXT

#FUNCTION TO PRINT ON UI
def PRINT_LABEL(VALUE):
    label4 = tk.Label(frame, text = VALUE)
    label4.pack()    


#log
def log( operation ,path1 ,path2 , parent,logslist):
    row =[None for i in range(5)]
    if len(logslist)==0:
        row[0] , row[1], row[2], row[3], row[4] = 1,operation ,path1 ,path2 , parent
    else:
        sr=1
        for i in range(len(logslist)):
            sr = max(sr , logslist[i][0])
        row[0] , row[1], row[2], row[3], row[4] = sr+1 ,operation ,path1 ,path2 , parent
    logslist.append(row)


#---------------MAIN CODE---------------------------------#



class ClientThread(threading.Thread):
    def __init__(self, ClientAddr, ClientSock):
        threading.Thread.__init__(self)
        self.csocket = ClientSock
        print("New Client Connection Added from address: ", ClientAddr)
    

    
    # Create Directories 
    def create_directory(self, userdirectory,userdata,logslist):      
        try:
            dirname=self.csocket.recv(2048)
            dirname = dirname.decode()
            if dirname !="Invalid input":
                dirpath =self.csocket.recv(2048)
                dirpath = dirpath.decode()
                if dirpath != "Invalid input":
                    if dirpath == "Create in Home Directory":
                        createdir=userdirectory+"/"+str(dirname) #set user directory to home directory
                    else:
                        userdirectory=userdirectory + str(dirpath)
                        createdir=userdirectory+"/"+str(dirname)  #set user directory to desired path

                    if path.exists(userdirectory): # check if path exists to create directory
                        os.mkdir(createdir)
                        result="Directory Created"
                        log( "Create" ,createdir ,None , userdirectory,logslist)
                        serverDisplay = "log: "+ userdata + " Create "+ createdir 
                        PRINT_LABEL(serverDisplay)
                    else:
                        result = "No such Path or directory exists"

        except Exception as e:
            result=str(e) #print exception on user side
        finally:        
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)
        
    
    #Delete Directory
    def delete_directory(self, userdirectory ,userdata,logslist):
        try:
            dirname=self.csocket.recv(2048)
            dirname=dirname.decode()
            if dirname !="Invalid input":             
                dirpath =self.csocket.recv(2048)
                dirpath=dirpath.decode()
                if dirpath != "Invalid input":
                    if dirpath == "Delete in Home Directory": #set user directory to home directory
                        deletedir=userdirectory+"/"+ dirname
                    else:
                        userdirectory=userdirectory + dirpath   #set user directory to desired path
                        deletedir=userdirectory+"/"+ dirname
                        
                    if path.exists(userdirectory):        # check if path exists to create directory
                        os.rmdir(deletedir)
                        result="Directory Deleted"
                        log( "Delete" ,deletedir ,None , userdirectory,logslist)
                        serverDisplay = "log: "+ userdata + " Delete "+ deletedir 
                        PRINT_LABEL(serverDisplay)
                    else:
                        result = "No such Path or directory exists"
        except Exception as e:
            result=str(e)
        finally:        
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)

    #Move Directory
    def move_directory(self,userdirectory ,userdata,logslist):
        try:
            dirname=self.csocket.recv(2048)
            dirname = dirname.decode()
            if dirname !="Invalid input":
                source_dirpath =self.csocket.recv(2048)
                source_dirpath = source_dirpath.decode()

                if source_dirpath != "Invalid input":
                    dest_dirpath=self.csocket.recv(2048)
                    dest_dirpath = dest_dirpath.decode()

                    if dest_dirpath != "Invalid input":
                        if source_dirpath == "Move from Home Directory":
                            source=userdirectory+"/"+str(dirname )
                        else:
                            source=userdirectory + str(source_dirpath)
                            source= source+"/"+str(dirname )
                        
                        if dest_dirpath == "Move from Home Directory":
                            destination=userdirectory
                            movedestination=destination+"/"+str(dirname )
                        else:
                            destination=userdirectory + str(dest_dirpath)
                            movedestination= destination+"/"+str(dirname)

                        print(source , destination , movedestination)
                        if path.exists(source) and path.exists(destination):
                            shutil.move(source , movedestination  )
                            result="Directory Moved"
                            log( "Move" ,source ,movedestination , destination,logslist)
                            serverDisplay = "log: "+ userdata + " Move "+ source +" "+ movedestination
                            PRINT_LABEL(serverDisplay)
                        else:
                            result = "No such Path or directory exists"
            
        except Exception as e:
            result=str(e)
        finally:        
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)   
    
    # Rename Directory
    def rename_directory(self, userdirectory ,userdata,logslist):
        try:
            dirname=self.csocket.recv(2048)
            dirname = dirname.decode()

            if dirname !="Invalid input":
                newdirname=self.csocket.recv(2048)
                newdirname=newdirname.decode()

                dirpath =self.csocket.recv(2048)
                dirpath = dirpath.decode()
                if dirpath != "Invalid input":
                    if dirpath == "Rename in Home Directory":
                        originalname=userdirectory+"/"+str(dirname)
                        newname=userdirectory+"/"+str(newdirname)
                        print(originalname , newname)
                    else:
                        userdirectory=userdirectory + str(dirpath)
                        originalname=userdirectory+"/"+str(dirname)
                        newname=userdirectory+"/"+str(newdirname)
                        
                    if path.exists(userdirectory):
                        os.rename(originalname , newname)
                        result="Directory Renamed"
                        log( "Rename" ,originalname ,newname , userdirectory,logslist)
                        serverDisplay = "log: "+ userdata + " Rename "+ originalname +" "+ newname
                        PRINT_LABEL(serverDisplay)
                    else:
                        result = "No such Path or directory exists"
        except Exception as e:
            result=str(e)
        finally:        
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)

    #List all directory in user home directory
    def list_directory(self, userdirectory):
        try:
            dirpath=self.csocket.recv(2048)
            dirpath = dirpath.decode()
            if dirpath == "Invalid input":
                return
            elif dirpath == "Show Home Directory":
                dirpath=''
            else:
                userdirectory=userdirectory + str(dirpath)
                
            if path.exists(userdirectory):
                listdirectory = os.listdir(userdirectory)
                result='List of Directories in Your Folder:\n'
                for directory in listdirectory:
                    result = result + directory +" \n"
                if len(listdirectory)==0:
                    result='Directory is Empty'
            else:
                result = "No such Path or directory exists"
        except Exception as e:
            result=str(e)
        finally:        
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)

    #List Home directory available to sync
    def list_Sync_directory(self, userdirectory):
        try:
            dirpath=self.csocket.recv(2048)
            dirpath = dirpath.decode()
            if dirpath == "Invalid input":
                return
            elif dirpath == "Show All Directory":
                dirpath=''
            else:
                userdirectory=userdirectory + str(dirpath)
                
            if path.exists(userdirectory):
                listdirectory = os.listdir(userdirectory)
                result='List of Directories available to sync:\n'
                for directory in listdirectory:
                    result = result + directory +" \n"
                if len(listdirectory)==0:
                    result='Directory is Empty'
            else:
                result = "No such Path or directory exists"
        except Exception as e:
            result=str(e)
        finally:        
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)

    #Sync Home Directory
    def Sync_directory(self, userdirectory):
        try:
            dirpath=self.csocket.recv(2048)
            dirpath = dirpath.decode()
            if dirpath == "Invalid input":
                return
            else:
                userdirectory=userdirectory +'/'+ str(dirpath)
                
            if path.exists(userdirectory):
                listdirectory = os.listdir(userdirectory)
                result= userdirectory
            else:
                result = "No such Path or directory exists"
        except Exception as e:
            result=str(e)
        finally:        
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)

    #send Logs
    def SendLogs(self,logslist):
        result ="logs :\n"
        for row in logslist:
            result =result+ "SR: "+ str(row[0])+ " Operation: "+row[1]+ " Path " + str(row[2])+ " TO " + str(row[3]) +"\n"
        message = bytes(result,'utf-8')
        self.csocket.sendall(message)

    #Undo Logs
    def UndoLogs(self ,userdata,logslist):
        try:
            srNo=self.csocket.recv(2048)
            srNo = int(srNo.decode() )
            found =False
            for index ,row in enumerate(logslist):
                if row[0]==srNo:
                    found=True
                    rowindex =index
                    break
            if found:
                operation = logslist[rowindex][1]
                path1 =logslist[rowindex][2]
                path2 =logslist[rowindex][3]
                parent= logslist[rowindex][4]

                if operation == 'Create':
                    shutil.rmtree(path1)
                    popindexes =[rowindex]
                    for index ,row in enumerate(logslist):
                        if path1 == row[4]:
                            popindexes.append(index)
                    print(popindexes)
                    for index in popindexes[::-1]:
                        logslist.pop(index)
                    result ="Create Operation UNDO"
                    serverDisplay = "UNDOlog: "+ userdata + " CREATE "+ path1
                    PRINT_LABEL(serverDisplay)

                elif operation == 'Delete':
                    os.mkdir(path1)
                    logslist.pop(rowindex)
                    result ="Delete Operation UNDO"
                    serverDisplay = "UNDOlog: "+ userdata + " DELETE "+ path1
                    PRINT_LABEL(serverDisplay)

                elif operation == 'Rename':
                    os.rename(path2 ,path1)
                    # for index in range(len(logslist)):
                    #     if logslist[index][4] == path2:
                    #         logslist[index][4] == path1
                    logslist.pop(rowindex)
                    result ="Rename Operation UNDO"
                    serverDisplay = "UNDOlog: "+ userdata + " Rename "+ path1 + " " +path2 
                    PRINT_LABEL(serverDisplay)

                elif operation == 'Move':
                    shutil.move(path2 ,path1)
                    logslist.pop(rowindex)
                    result ="Move Operation UNDO"
                    serverDisplay = "UNDOlog: "+ userdata + " Move "+ path2 + " " +path1 
                    PRINT_LABEL(serverDisplay)
            else:
                result = "Invalid Sr Number"
        except Exception as e:
            result=str(e)
        finally:
            message = bytes(result,'utf-8')
            self.csocket.sendall(message)
        
    #Function to check whether contains any special character
    #ref : https://www.geeksforgeeks.org/python-program-check-string-contains-special-character/
    def Special_Char_Check(self ,string):  
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')   
        if(regex.search(string) == None): 
            #print("String is accepted") 
            return False
            
        else: 
            #print("String is not accepted.") 
            return True

    #FUNCTION TO GET AND CHECK USERNAME
    def USERNAME_CHECK(self):
        USER_FLAG = False
        while not USER_FLAG:
            username = str(self.csocket.recv(4096),'utf-8')   #USERNAME CHECK RECV 1
            if self.Special_Char_Check(username):
                message = b"Special Character Detected Username not accepted"
                self.csocket.sendall(message)  #SEND special character detected
                continue
            elif (username in USERNAMES) and (username in ACTIVE_USERNAMES):
                message = b"Username Exists and is Active"
                self.csocket.sendall(message)  #SEND 1 USERNAME EXISTS
                continue
            USER_FLAG = True
        #CHECK IF USERNAME NOT ALREADY IN USERNAME LIST
        if username not in USERNAMES:
            USERNAMES.append(username)
             
        ACTIVE_USERNAMES.append(username)
        global USER_STATUS  #FOR UI UPDATE
        USER_STATUS = True  #FOR UI UPDATE
        global count
        count +=1 #FOR UI UPDATE
        message = b"Welcome"
        print("Welcome", username)
        self.csocket.sendall(message) #SEND 1 USERNAME NEW
        return username
    
    #function to get and check identifier
    def Identifier_CHECK(self):
        FLAG = False
        global Identifiers
        Identifier = str(self.csocket.recv(2048),'utf-8')   #
        while not FLAG:
            Identifier = str(self.csocket.recv(2048),'utf-8')   #
            #print("received " + Identifier)
            if Identifier in Identifiers:
                message = b"Identifier Exists"
                self.csocket.sendall(message)  #SEND 1 identifier EXISTS
                continue
            FLAG = True
        #CHECK IF USERNAME NOT ALREADY IN USERNAME LIST
        if Identifier not in Identifiers:
            Identifiers.append(Identifier)

        #print(Identifiers)             
        message = b"Welcome"
        self.csocket.sendall(message) 
        return Identifier
    
    def Directory_Check(self,username):
        userpath='Directory/'+username
        if path.exists(userpath):
            #print("Home Directory Exists")
            message = b"Welcome Back your home directory is ready to use"  #already directory exists
            self.csocket.sendall(message)          
        else:
            os.mkdir(userpath)
            #print("Directory with your username is created")
            message = b"Hello a new home directory has been cre ated for you"    #new directory created
            self.csocket.sendall(message)  
        return userpath
        


    def run(self):
        global STOP_CLIENT_THREAD
        userdata = self.USERNAME_CHECK() #USERNAME FUNCTION CALL 1
        User_Directory = self.Directory_Check(userdata) #Get directory or create one for new user
        identifier = self.Identifier_CHECK() #Identifier FUNCTION CALL 
        shared_Directory = 'Directory'
        logslist =[]

        while True:

            choice = self.csocket.recv(2048) #RECV 2 CLIENT CHAT CHOICE
            choice = choice.decode()
            
            if choice == 'bye':
                ACTIVE_USERNAMES.remove(userdata)  #REMOVING ACTIVE USERNAME FROM LIST
                Identifiers.remove(identifier) # Remove identifier from active list
                THREAD_DEL()
                if STOP_CLIENT_THREAD:
                    break
                                
            if choice == '1':
                self.create_directory(User_Directory ,userdata ,logslist)  # Create Directory
            
            if choice == '2':
                self.delete_directory(User_Directory ,userdata ,logslist) #Delete Directory

            if choice == '3':
                self.move_directory(User_Directory ,userdata ,logslist) # Move Directory
            
            if choice == '4':
                self.rename_directory(User_Directory ,userdata ,logslist) # Rename Directory

            if choice == '5':
                self.list_directory(User_Directory) # List Directory

            if choice == '6':
                self.list_Sync_directory(shared_Directory) # List Home Directories available to 
            
            if choice == '7':                               # return path of directories to be synced
                self.Sync_directory(shared_Directory)

            if choice =='10': #see logs
                self.SendLogs(logslist)

            if choice =='11': #undo logs
                self.UndoLogs(userdata,logslist)




if __name__ == "__main__":
    STOP_CLIENT_THREAD = False
    USER_STATUS = False
    count = 0
    userdata = ''
    USERNAMES = []
    ACTIVE_USERNAMES = []
    Identifiers = []
    HOST = '127.0.0.1'
    PORT = 1395
    

    NULL = ''
    if path.exists('Directory'):
        print('Server directory exists')
    else:
        os.mkdir('Directory')
        print('Server Directory Created')
    

    #http://net-informations.com/python/net/thread.htm
    try:
        myserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        myserver.bind((HOST,PORT))
        print("Starting Server at HOST: "+ HOST + " and PORT: ", PORT)
        start_new_thread(MAIN_DISPLAY,(NULL,))
        while True:
            myserver.listen(3)
            conn, addr = myserver.accept()
            newclientthread = ClientThread(addr, conn)
            newclientthread.start()
    except Exception:
        print('Error occured')
    finally:
        myserver.close()

#Reference : https://github.com/isiddheshrao/Distributed-Systems/blob/master/Server.py