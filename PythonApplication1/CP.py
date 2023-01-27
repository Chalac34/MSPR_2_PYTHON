# -*- coding: utf-8-sig -*-

import ping3
import tkinter
import socket
from ping3 import ping
import subprocess
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import time
from datetime import datetime
import threading
from tkinter import ttk



###Fonction de log###
def log_text(Page,Zone_de_Texte):
    with open(".\\log\\log.txt", "a") as f:
        f.write(Zone_de_Texte.get(1.0, tk.END))


#############################


### Update Barre de progression###
def update_progress(Barre_progression,Page):
    for i in range(100):
        Barre_progression['value'] = i
        Barre_progression.update()
        time.sleep(0.1)
#############################


######Scan_IP
def Scan_IP(reseau,debut,fin,Zone_de_Texte,Page,Barre_progression):
    Barre_progression()
    nombre_hote=0
    i=0
    IP_prise=[]
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 12))
    Zone_de_Texte.tag_config("bold", font=("Sans", 12, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 12, "italic"))

    Barre_progression.start()
    for ip in range(debut,fin+1):
        update_progress(Barre_progression,Page)
        completion=i*(100//(fin+1-debut))
        i+=1
        Template()
        Zone_de_Texte.insert(tk.END, f" {completion}%","bold")
        resp = ping(reseau+"."+str(ip))
        if resp == False:
            continue
        else:
            IP_prise.append(f"{reseau}.{ip}")
            Zone_de_Texte.insert(tk.END, f"IP prise {reseau}.{ip} ","bold")
            nombre_hote+=1
            Page.update()
    if nombre_hote == 0:
        Template()
        Zone_de_Texte.insert(tk.END, f" \"Scan terminé \"Aucun hote trouvé\"\n")
        Page.update()
        Barre_progression.stop()
    elif nombre_hote ==1:
        Template()
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé 1 hote trouvé\"\n")
        Template()
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
        Barre_progression.stop()
    else:
        Template()
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé {nombre_hote} hotes\"\n")
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
        Barre_progression.stop()
    log_text()
    return IP_prise

def on_scan_ip(Page,Barre_progression):
    try:
        reseau = simpledialog.askstring("Reseau", "Entrez le reseau :", parent=Page)
        debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage IP :", parent=Page))
        fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage IP :", parent=Page))
        Scan_IP(reseau, debut, fin)
    except TypeError:
        pass



####Scan Ports Reseau
def Scan_port(IP,debut,fin,Zone_de_Texte,Page,Barre_progression):
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 12))
    Zone_de_Texte.tag_config("bold", font=("Sans", 12, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 12, "italic"))

    i=0
    TCP=[]
    UDP=[]
    Barre_progression.start()
    for port in range(debut,fin+1):
        i+=1
        update_progress(Barre_progression,Page)
        completion=i*(100//(fin-debut))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            Template()
            Zone_de_Texte.insert(tk.END, f"{completion}%")
            Template()
            Zone_de_Texte.insert(tk.END,f"Port {port} est ouvert en TCP.")
            TCP.append(port)
            Page.update()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            Template()
            Zone_de_Texte.insert(tk.END,f"Port {port} est ouvert en UDP.")
            UDP.append(port)
            Page.update()
    Template()
    Zone_de_Texte.insert(tk.END,f"Port {TCP} en TCP.")
    Template()
    Zone_de_Texte.insert(tk.END,f"Port {UDP} en UDP.")
    Zone_de_Texte.config(state="disable")
    Barre_progression.stop()
    sock.close()
    log_text()
    return TCP,UDP

def on_scan_ports(Page,Barre_progression):
    try:
        Host = simpledialog.askstring("host", "Entrez l'ip a scan  :", parent=Page)
        debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage port :", parent=Page))
        fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage port:", parent=Page))
        Scan_port(Host, debut, fin,Barre_progression)
    except TypeError:
        pass


####SpeedTest

def Speedtest(Zone_de_Texte,Page,Barre_progression):
    #Parametrage du texte
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 12))
    Zone_de_Texte.tag_config("bold", font=("Sans", 12, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 12, "italic"))

    Template(Zone_de_Texte)
    Barre_progression.start()
    Zone_de_Texte.insert(tk.END," Speedtest en cours,Veuillez patientez... ")
    Page.update()
    str_DL=""
    str_UP=""
    program_path = ".\\speedtest\\speedtest.exe"

    result = subprocess.run(program_path, shell=True, capture_output=True, text=True)
    output = result.stdout.split('\n')
    update_progress(Barre_progression,Page)()

    for line in output:
        if 'Download:' in line:
             str_DL=line
        if 'Upload:' in line:
             str_UP=line
    DL=str_DL.split()[1]+str_DL.split()[2]
    UP=str_UP.split()[1]+str_DL.split()[2]
    Barre_progression.stop()

    ###Partie du Download
    Template(Zone_de_Texte)
    Zone_de_Texte.insert(tk.END,f" Vitesse de Download ")
    
    Template(Zone_de_Texte)
    Zone_de_Texte.insert(tk.END,f" {DL}", "bold")
    Page.update()
    
    ###Partie du Upload
    Template(Zone_de_Texte)
    Zone_de_Texte.insert(tk.END,f" Vitesse D'upload  ")
    
    Template(Zone_de_Texte)
    Zone_de_Texte.insert(tk.END,f" {UP}", "bold ")
    Page.update()
    Zone_de_Texte.config(state="disable")
    
    log_text()

def Template(Zone_de_Texte):
    hostname=socket.gethostname()
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 12))
    Zone_de_Texte.tag_config("italic", font=("Sans", 12, "italic"))
    Zone_de_Texte.tag_configure('red_text', foreground='red')

    current_time=datetime.now().strftime("%H:%M:%S")
    Zone_de_Texte.insert(tk.END,f"\n{current_time}", "italic")
    Zone_de_Texte.insert(tk.END,f" {hostname} :",'red_text')

