import ping3
import tkinter
import socket
from ping3 import ping
import subprocess
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import requests
import time
from datetime import datetime
import threading





######Scan_IP
def Scan_IP(reseau,debut,fin):
    nombre_hote=0
    i=0
    IP_prise=[]
    text.config(state="normal")
    for ip in range(debut,fin+1):
        completion=i*(100//(fin-debut))
        i+=1
        print(completion)
        resp = ping(reseau+"."+str(ip))
        if resp == False:
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text.insert(tk.END, f"{current_time} {completion}%\n")
            root.update()
            continue
        else:
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text.insert(tk.END, f"{current_time} {completion}%\n")
            IP_prise.append(f"{reseau}.{ip}")
            nombre_hote+=1
            root.update()
    if nombre_hote == 0:
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text.insert(tk.END, f"{current_time} \"Scan terminé \"Aucun hote trouvé\"")
        root.update()
    elif nombre_hote ==1:
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text.insert(tk.END, f"{current_time}\"Scan terminé 1 hote trouvé\"\n")
        text.insert(tk.END, IP_prise)
        root.update()
    else:
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text.insert(tk.END, f"{current_time} Scan terminé {nombre_hote} hotes\n")
        text.insert(tk.END, IP_prise)
        root.update()

def on_scan_ip():
    reseau = simpledialog.askstring("Reseau", "Entrez le reseau :", parent=root)
    debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage IP :", parent=root))
    fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage IP :", parent=root))
    Scan_IP(reseau, debut, fin)



####Scan Ports Reseau
def Scan_port(IP,debut,fin):
    text.config(state="normal")
    i=0
    for port in range(debut,fin+1):
        i+=1
        completion=i*(100//(fin-debut))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text.insert(tk.END, f"{current_time} {completion}%\n")
            text.insert(tk.END,f"{current_time} Port {port} est ouvert en TCP.\ n")
            root.update()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text.insert(tk.END, f"{current_time} {completion}%\n")
            text.insert(tk.END,f"{current_time} Port {port} est ouvert en UDP.\n")
            root.update()
    text.config(state="disable")
    sock.close()


def on_scan_ports():
    Host = simpledialog.askstring("host", "Entrez l'ip a scan  :", parent=root)
    debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage port :", parent=root))
    fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage port:", parent=root))
    Scan_port(Host, debut, fin)


####SpeedTest

def Speedtest():
    text.config(state="normal")
    current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text.insert(tk.END,f"{current_time} Speedtest en cours,Veuillez patientez... \n")
    root.update()
    str_DL=""
    str_UP=""
    program_path = "C:\\Users\\b.dezord\\Desktop\\spped\\speedtest.exe"
    result = subprocess.run(program_path, shell=True, capture_output=True, text=True)
    output = result.stdout.split('\n')
    for line in output:
        if 'Download:' in line:
             str_DL=line
        if 'Upload:' in line:
             str_UP=line
    DL=str_DL.split()[1]+str_DL.split()[2]
    UP=str_UP.split()[1]+str_DL.split()[2]
    current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text.insert(tk.END, f"{current_time} Vitesse de Download {DL}\n")
    text.insert(tk.END, f"{current_time} Vitesse D'upload {UP}\n")
    root.update()
    text.config(state="disable")






###Titre de la page
root = tk.Tk()
root.title("SEMALYNK")
####

####Bouton Scan SPEEDTEST

speedtest_button = tk.Button(root, text="SpeedTest", command=Speedtest)

speedtest_button.pack()
#####
###Bouton Scan_Port
scan_button = tk.Button(root, text="Scan Ports", command=on_scan_ports)

scan_button.pack()
###


####Bouton Scan IP

scan_IP_button = tk.Button(root, text="Scan IP", command=on_scan_ip)
scan_IP_button.pack()
########



text = tk.Text(root)
text.config(state="disable")
text.pack()

root.mainloop()



