# -*- coding: utf-8-sig -*-

import socket
from ping3 import ping
import subprocess
import time
import tkinter as tk
from tkinter import simpledialog
import time
from datetime import datetime
from tkinter import ttk
import sqlite3
import asyncio
import aioping
import aiohttp
import ipaddress
from tkinter import messagebox




###Test de latence###
def latency_ping_test(host="check-host.net"):
    ping = subprocess.Popen(["ping", "-n", "3", host], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out = ping.communicate()
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
    

##Fonction de log###
def log_text(Page,Zone_de_Texte):
    with open(".\\log\\log.txt", "a") as f:
        f.write(Zone_de_Texte.get(1.0, tk.END))


        



######Scan_IP Complet
def Scan_IP(reseau, masque, Zone_de_Texte, Page, ):
   
    nombre_hote=0
    i=0
    IP_prise=[]
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    # IP par rapport au masque
    net = ipaddress.IPv4Network(f'{reseau}/{masque}', strict=False)
    debut = int(net[1])
    fin = int(net[-2])

    
    for ip in range(debut, fin + 1):
       
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
        
    elif nombre_hote ==1:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé 1 hote trouvé\"\n")
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       
    else:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé {nombre_hote} hotes\"\n")
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       
    log_text(Page,Zone_de_Texte)
    return IP_prise

def on_scan_ip(Zone_de_Texte,Page):
        reseau = simpledialog.askstring("Reseau", "Entrez le réseau (ex. 192.168.0.0):", parent=Page)
        masque = simpledialog.askstring("Masque", "Entrez le masque de sous-réseau (ex. 255.255.255.0) :", parent=Page)
        Scan_IP(reseau, masque,  Zone_de_Texte, Page )

###Scan IP Partiel
def Scan_IP2(reseau,debut,fin,Zone_de_Texte,Page):
    
    nombre_hote=0
    i=0
    IP_prise=[]
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    
    for ip in range(debut,fin+1):
       
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
        
    elif nombre_hote ==1:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé 1 hote trouvé\"\n")
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       
    else:
        Template(Zone_de_Texte)
        Zone_de_Texte.insert(tk.END, f"\"Scan terminé {nombre_hote} hotes\"\n")
        Zone_de_Texte.insert(tk.END, f"{IP_prise}")
        Page.update()
       
    log_text(Page,Zone_de_Texte)
    return IP_prise
def on_scan_ip2(Zone_de_Texte,Page):
    reseau = simpledialog.askstring("Adresse Reseau", "Entrez le reseau (ex. 192.168.0):", parent=Page)
    debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage IP :", parent=Page))
    fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage IP :", parent=Page))
    Scan_IP2(reseau, debut, fin,Zone_de_Texte,Page)
 
###Choix du Scan IP
def Scan_IP_Choice(Zone_de_Texte,Page):
    Choix=messagebox.askquestion("Type de Scan", "Scan complet ?")
    if Choix == 'yes':
       on_scan_ip(Zone_de_Texte,Page)
    else:
       on_scan_ip2(Zone_de_Texte,Page)

####Scan Ports Reseau
def Scan_port(IP,debut,fin,Zone_de_Texte,Page):
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    i=0
    TCP=[]
    UDP=[]
   
    Zone_de_Texte.insert(tk.END,"debut")
    for port in range(debut,fin+1):
        i+=1
        
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
    Zone_de_Texte.insert(tk.END,"fini")
    sock.close()
    log_text(Page,Zone_de_Texte)
    return TCP,UDP
def on_scan_ports(Zone_de_Texte,Page):
    Host = simpledialog.askstring("host", "Entrez l'ip a scan  :", parent=Page)
    debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage port :", parent=Page))
    fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage port:", parent=Page))
    Scan_port(Host, debut, fin,Zone_de_Texte,Page)



####SpeedTest
DL=""
UP=""
def Speedtest(Zone_de_Texte,Page,label_upload,label_download):
    #Parametrage du texte
    Zone_de_Texte.config(state="normal")
    Zone_de_Texte.config(font=("Sans", 10))
    Zone_de_Texte.tag_config("bold", font=("Sans", 10, "bold"))
    Zone_de_Texte.tag_config("italic", font=("Sans", 10, "italic"))

    #SQL
    conn = sqlite3.connect('Base.db')
    cursor = conn.cursor()

    Template(Zone_de_Texte)
    Zone_de_Texte.insert(tk.END," Speedtest en cours,Veuillez patientez... ")
    Page.update()
    str_DL=""
    str_UP=""
    program_path = ".\\speedtest\\speedtest.exe"

    result = subprocess.run(program_path, shell=True, capture_output=True, text=True)
    output = result.stdout.split('\n')
   

    for line in output:
        if 'Download:' in line:
             str_DL=line
        if 'Upload:' in line:
             str_UP=line
    DL=str_DL.split()[1]+str_DL.split()[2]
    UP=str_UP.split()[1]+str_DL.split()[2]
    

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
    cursor.execute(f"""UPDATE semabox 
                       SET sem_inf_up_speed ='{UP}',
                           sem_inf_dl_speed='{DL}'
                       WHERE sem_client = (SELECT ent_id 
                                           FROM entreprise
                                           WHERE sem_client = ent_id)
                       """ )
    conn.commit()
    conn.close()

    label_upload.destroy()
    label_upload=tk.Label(Page,text=f"Vitesse Upload: {UP}",font=("Arial",10,"bold"))
    label_upload.place(x=780, y=60)
    label_upload.update()

    label_download.destroy()
    label_download=tk.Label(Page,text=f"Vitesse de Download: {DL}",font=("Arial",10,"bold"))
    label_download.place(x=780, y=80)
    label_download.update()

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
    cursor.execute("SELECT * FROM semabox")
    results = cursor.fetchall()
    conn.close()
    return results

def MaJ_Label(Upload_label,Download_label,Latence,Connexion_Value,Page):
    start=time.time()
    color, msg = qualite_connexion()
    New_upload=""
    New_Download=""
    New_Latence=latency_ping_test()
    New_Connexion_Value=msg
    

    Valeurs = Recuperation_donnees_DB("Base.db")
    for result in Valeurs:
        New_upload = result[4]
        New_Download = result[5]

    Upload_label.destroy()
    Upload_label=tk.Label(Page,text=f"Vitesse Upload: {New_upload}",font=("Arial",10,"bold"))
    Upload_label.place(x=780, y=60)
    Upload_label.update()

    Download_label.destroy()
    Download_label=tk.Label(Page,text=f"Vitesse de Download: {New_Download}",font=("Arial",10,"bold"))
    Download_label.place(x=780, y=80)
    Download_label.update()

    Latence.destroy()
    Latence=tk.Label(Page,text=f"Latence Moyenne :{New_Latence}",font=("Arial",10,"bold"))
    Latence.place(x=780, y=40)
    Latence.update()

    Connexion_Value.destroy()
    Connexion_value=tk.Label(Page,text=msg, font=("Arial",10,"bold"),fg=color)
    Connexion_value.place(x=780, y=330)
    Connexion_Value.update()

    Page.update()


