# cmp2204-Project
CMP2204 Project


Please Read Carefully


To Run The Program:
1) use python3 P2P_Server.py to start our Server.
Our server ask your file to share.The File and other files must be same folder.

Note: Read Important Notes 3 before run the Service_Listener.py
2) use python3 Service_Listener.py to start our Service listener.
No input needed

3) use python3 Service_Announcer.py to start our Service announcer.
No input needed

Before start P2P_Downloader, wait 1 successful listening otherwise it will give an error.
4) use python3 P2P_Downloader.py to start our Client.

You will see the downloadable file names, write one of name to download
Don't forget to write the file extension (For ex: Sharingfile.txt)
Note: All your files need to be same folder.

Important Notes:
1)You need to wait the first announce before start the P2P_Downloader.
Because after first announce Service_Listener will create some files
to work with client.

2) # Fixed

3)If you test the program with same PC.Then
Change -> 14. Line of Service_Listener with if ip == get_my_ip():

4)You can see the download history in client.txt

5)If you use Unix-Like system you can active 50. Line in P2P_Downloader.py

6)If you will try to test the program with Hamachi you need to hardcode your Hamachi ip
To do is:
  6.1) P2P_Server.py update 12. Line with ip = "your_hamachi_ip"
  6.2) Service_Listener.py update 32. Line with IP = "your_hamachi_ip"
  6.3) Service_Announcer.py update 11. Line with IP= "your_hamachi_ip" and
	last line should be
	hamachi_ip = "25.255.255.255" -> You will create
   	announce(hamachi_ip, json_dictionary) -> update the last line like this



