# -*- coding: utf-8-sig -*-

from http.client import responses
from optparse import Option
from xmlrpc.client import DateTime
import ping3
import tkinter
import socket
from ping3 import ping
import subprocess
import time
import tkinter as tk
from tkinter import END, filedialog
from tkinter import simpledialog
import time
from datetime import datetime
import threading
from tkinter import ttk
import requests
import sqlite3
import asyncio
import concurrent.futures
import aioping
import aiohttp
import ipaddress
from tkinter import messagebox



###Test de latence###
def latency_ping_test(host="google.fr"):
    ping = subprocess.Popen(["ping", "-n", "3", host], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, error = ping.communicate()
    out_str=str(out)
    lines=out_str.splitlines()
    moyenne_ms=""
    for line in lines:   
        moyenne_ms=((line.split('\\r')[-2]).split(",")[-1]).split('=')[-1]
    return moyenne_ms


###Qualité de connexion###
def qualite_connexion():
    try:
        latence= int(latency_ping_test().split('ms')[0])
    except TypeError:
        color="#8B0000"
        msg="Pas de connexion"
    except ValueError:
        color="#8B0000"
        msg="Pas de connexion"
        return color,msg       
    else:
        if latence <= 30:
            color="blue"
            msg="CONNEXION AU TOP"
        elif latence >30 and latence<=60:
            color="green"
            msg="CONNEXION OK"
        elif latence >60 and latence<=100:
            color="#FA6A06"
            msg="Connexion Moyenne"
        else:
            color="#FFCD00"
            msg="Mauvaise Connexion"
    return color,msg
    

###Fonction de log###
def log_text(Page,Zone_de_Texte):
    with open(".\\log\\log.txt", "a") as f:
        f.write(Zone_de_Texte.get(1.0, tk.END))





### Update Barre de progression###
def update_progress(Barre_progression,Page,Percent):
    #for i in range(200):
        Barre_progression['value'] = Percent
        Barre_progression.update()
        



######Scan_IP Complet
def Scan_IP(reseau, masque, Zone_de_Texte, Page, Barre_progression):
    #Barre_progression.start()
    nombre_hote=0
    i=0
    IP_prise=[]
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    # Calculation of the IP range using the network address and subnet mask
    net = ipaddress.IPv4Network(f'{reseau}/{masque}', strict=False)
    debut = int(net[1])
    fin = int(net[-2])

    #Barre_progression.start()
    for ip in range(debut, fin + 1):
       #update_progress(Barre_progression,Page)
        completion=i*(100//(fin+1-debut))
        i+=1
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f" {completion}% ","bold")
        ip_str = str(ipaddress.IPv4Address(ip))
        resp = ping(ip_str,1)
        print("ok"+str(i))
        if resp == False:
            continue
        else:
            IP_prise.append(ip_str)
            Zone_de_Texte.insert(tk.END, f"IP prise {ip_str} ","bold")
            nombre_hote+=1
            Page.update()
    if nombre_hote == 0:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f" \"Scan terminé \"Aucun hote trouvé\"\n")
        Page.update()
        #Barre_progression.stop()
    elif nombre_hote ==1:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé 1 hote trouvé\"\n")
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       # Barre_progression.stop()
    else:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé {nombre_hote} hotes\"\n")
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       # Barre_progression.stop()
    log_text(Page,Zone_de_Texte)
    return IP_prise
def on_scan_ip(Zone_de_Texte,Page,Barre_progression):
        reseau = simpledialog.askstring("Reseau", "Entrez le réseau (ex. 192.168.0.0):", parent=Page)
        masque = simpledialog.askstring("Masque", "Entrez le masque de sous-réseau (ex. 255.255.255.0) :", parent=Page)
        Scan_IP(reseau, masque,  Zone_de_Texte, Page, Barre_progression)

###Scan IP Partiel
def Scan_IP2(reseau,debut,fin,Zone_de_Texte,Page,Barre_progression):
    #Barre_progression.start()
    nombre_hote=0
    i=0
    IP_prise=[]
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    #Barre_progression.start()
    for ip in range(debut,fin+1):
       #update_progress(Barre_progression,Page)
        completion=i*(100//(fin+1-debut))
        i+=1
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f" {completion}% ","bold")
        resp = ping(reseau+"."+str(ip))
        if resp == False:
            continue
        else:
            IP_prise.append(f"{reseau}.{ip}")
            Zone_de_Texte.insert(tk.END, f"IP prise {reseau}.{ip} ","bold")
            nombre_hote+=1
            Page.update()
    if nombre_hote == 0:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f" \"Scan terminé \"Aucun hote trouvé\"\n")
        Page.update()
        #Barre_progression.stop()
    elif nombre_hote ==1:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé 1 hote trouvé\"\n")
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       # Barre_progression.stop()
    else:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé {nombre_hote} hotes\"\n")
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       # Barre_progression.stop()
    log_text(Page,Zone_de_Texte)
    return IP_prise
def on_scan_ip2(Zone_de_Texte,Page,Barre_progression):
    reseau = simpledialog.askstring("Adresse Reseau", "Entrez le reseau (ex. 192.168.0):", parent=Page)
    debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage IP :", parent=Page))
    fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage IP :", parent=Page))
    Scan_IP2(reseau, debut, fin,Zone_de_Texte,Page,Barre_progression)
 
###Choix du Scan IP
def Scan_IP_Choice(Zone_de_Texte,Page,Barre_progression):
    Choix=messagebox.askquestion("Type de Scan", "Scan complet ?")
    if Choix == 'yes':
       on_scan_ip(Zone_de_Texte,Page,Barre_progression)
    else:
       on_scan_ip2(Zone_de_Texte,Page,Barre_progression)

####Scan Ports Reseau
def Scan_port(IP,debut,fin,Zone_de_Texte,Page,Barre_progression):
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    i=0
    TCP=[]
    UDP=[]
    Barre_progression.start()
    Zone_de_Texte.insert(tk.END,"debut")
    for port in range(debut,fin+1):
        i+=1
        update_progress(Barre_progression,Page,100)
        completion=i*(100//(fin-debut))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            Template(Zone_de_Texte)
            Zone_de_Texte.insert(tk.END, f"{completion}%")
            Template(Zone_de_Texte)
            Zone_de_Texte.insert(tk.END,f"Port {port} est ouvert en TCP.")
            TCP.append(port)
            Page.update()
        Zone_de_Texte.insert(tk.END,"millieu")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            Template(Zone_de_Texte)
            Zone_de_Texte.insert(tk.END,f"Port {port} est ouvert en UDP.")
            UDP.append(port)
            Page.update()
    Template(Zone_de_Texte)
    Zone_de_Texte.insert(tk.END,f"Port {TCP} en TCP.")
    Template(Zone_de_Texte)
    Zone_de_Texte.insert(tk.END,f"Port {UDP} en UDP.")
    Zone_de_Texte.config(state="disable")
    Barre_progression.stop()
    Zone_de_Texte.insert(tk.END,"fini")
    sock.close()
    log_text(Page,Zone_de_Texte)
    return TCP,UDP
def on_scan_ports(Zone_de_Texte,Page,Barre_progression):
    Host = simpledialog.askstring("host", "Entrez l'ip a scan  :", parent=Page)
    debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage port :", parent=Page))
    fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage port:", parent=Page))
    Scan_port(Host, debut, fin,Zone_de_Texte,Page,Barre_progression)



####SpeedTest
DL=""
UP=""
def Speedtest(Zone_de_Texte,Page,Barre_progression):
    #Parametrage du texte
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    #SQL
    conn = sqlite3.connect('Base.db')
    cursor = conn.cursor()

    Template(Zone_de_Texte)
    Barre_progression.start()
    Zone_de_Texte.insert(tk.END," Speedtest en cours,Veuillez patientez... ")
    Page.update()
    str_DL=""
    str_UP=""
    program_path = ".\\speedtest\\speedtest.exe"

    result = subprocess.run(program_path, shell=True, capture_output=True, text=True)
    output = result.stdout.split('\n')
    update_progress(Barre_progression,Page,100)

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
    
    log_text(Page,Zone_de_Texte)
    cursor.execute(f"INSERT INTO data (up_speed,dl_speed) VALUES ('{UP}','{DL}')")
    conn.commit()
    conn.close()


##TEMPLATE
def Template(Zone_de_Texte):
    hostname=socket.gethostname()
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))
    Zone_de_Texte.tag_configure('red_text', foreground='red')

    current_time=datetime.now().strftime("%H:%M:%S")
    Zone_de_Texte.insert(tk.END,f"\n{current_time}", "italic")
    Zone_de_Texte.insert(tk.END,f" {hostname} :",'red_text')



###Recupere IP Public###
async def get_public_ip():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.ipify.org") as resp:
            public_ip = await resp.text()
            return public_ip

###Recupere @Reseau
async def get_network_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    await asyncio.get_event_loop().sock_connect(s, ("8.8.8.8", 80))
    return s.getsockname()[0]

###Connexion sqlite BDD
def Connexion_BDD(BDD):
      conn = sqlite3.connect(BDD)
      cursor = conn.cursor()
      return cursor,conn

###Recupére Nom d'hote
async def get_host_name_from_ip(ip_address):
    try:
        host_name = await asyncio.get_event_loop().run_in_executor(None, socket.gethostbyaddr, ip_address)
        return str(host_name[0])
    except socket.herror:
        return None


###Merci Sani#1234###
###Remplie la Listbox
async def Remplir_listbox(listbox, debut, fin):
    network_address = await get_network_address()
    addr_reseau = network_address.split(".")[0]+"."+network_address.split(".")[1]+"."+network_address.split(".")[2]
    coros = []
    for ip in range(debut, fin+1):
        IP = addr_reseau + "." + str(ip)
        coros.append(do_ping(IP,listbox))
    await asyncio.gather(*coros)
async def do_ping(IP, listbox):
    try:
        response = await aioping.ping(IP, 1)
        if response:
            nom = await get_host_name_from_ip(IP)
            if nom:
                listbox.insert(tk.END, str(nom) + ":  " + str(IP))
    except TimeoutError:
        pass

def Recuperation_donnees_DB(DataBase):
    conn = sqlite3.connect(DataBase)
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("SELECT * FROM data")
    results = cursor.fetchall()
    conn.close()
    return results

def MaJ_Label(Upload,Download,Latence,Connexion_Value,Page):
    color, msg = qualite_connexion()
    New_upload=""
    New_Download=""
    New_Latence=latency_ping_test()
    New_Connexion_Value=msg
    

    Valeurs = Recuperation_donnees_DB("Base.db")
    
    for results  in Valeurs:
      New_upload = Valeurs[1]
      New_Download = Valeurs[2]
      print(New_upload,New_Download)


    Upload.configure(text=New_upload)
    Upload.update()
    Download.configure(text=New_Download)
    Download.update()
    Latence.configure(text=New_Latence)
    Latence.update()
    Connexion_Value.configure(text=New_Connexion_Value,fg=color)
    Connexion_Value.update()
    Page.update()
