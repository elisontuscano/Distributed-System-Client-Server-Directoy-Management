# Distributed-System-Client-Server-Directoy-Management

## Steps for Running and Compiling the program 

Step 1: For windows system run the “run.bat” file to open 1 Server UI application and 3 Client UI applications. Or else can manually compile and run Server.py file and Client.py file from command prompt. 

Step 2: First Server UI Will start The Server UI will dynamically show, and update number of clients connected, Log of total usernames in the session and currently active usernames. After that Client UI Will start.

Step 3: Enter Unique Client username on the client UI prompt 
Step 4: The Username if Unique, the client will login. Else, if the username exists and is currently active, the client will be asked to enter the username again. 

Step 5: Client is given option to select an identifier. Clients cannot have same identifiers.

Step 6: Once username is accepted Server checks if client has an existing directory and makes it Clients home directory.Else creates a new directory for the Client. Once identifier is accepted the client creates a folder with that name which will be clients home directory. 

Step 7:Client will be prompt options to create, delete, rename, move and list Directories. Also will be provided with options to sync and desync directories from the server. Server logs all the activities and client has the option to undo activities.

Step 8: Based on the input, the client will be asked to enter appropriates inputs as per the required operation. Server will execute those operations and send a response to client. In case of any error Server will send the error to the client. Client will Show the response on the UI 

Step 7: The client will return to the options menu after one complete iteration. To Quit, enter ‘bye’ in the input box which will close the client UI or press the Quit button.

Step 8: Can run the “close.bat” file to close all Client and Server applications.

## Important:
When asked for path in the option Keep empty to be in Home directory and enter path to go inside a certain folder in home directory. Example to go inside "test" folder in home directory Enter path "/test".
 
## Notes: 
•	Client & Server run through their respective UI. 
•	Not more than 3 clients can run simultaneously 
•	Clients must provide Unique username and no special characters. 
•	Create, Delete, rename, move and list directory work. 
•	Server handles disconnections from client. 
•	Server handles client usernames and keeps requesting new username if the username is not unique. 
•	Server has a list to store all client’s usernames and currently active usernames. 
•	Server handles all directory operations of client and in case of error displays them on client application
