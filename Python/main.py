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


hostname=socket.gethostname()

###Titre de la page
root = tk.Tk()
root.geometry("725x800+600+100")
root.title("SemaOS")
####

###Fonction de log###
def log_text():
    with open("log.txt", "a") as f:
        f.write(text.get(1.0, tk.END))

progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress.pack()
#############################


###Barre de progression###
def update_progress():
    for i in range(100):
        progress['value'] = i
        progress.update()
        time.sleep(0.1)
#############################


######Scan_IP
def Scan_IP(reseau,debut,fin):
    nombre_hote=0
    i=0
    IP_prise=[]
    text.config(state="normal")
    text.config(font=("Sans", 12))
    text.tag_config("bold", font=("Sans", 12, "bold"))
    text.tag_config("italic", font=("Sans", 12, "italic"))

    progress.start()
    for ip in range(debut,fin+1):
        update_progress()
        completion=i*(100//(fin+1-debut))
        i+=1
        Template()
        text.insert(tk.END, f" {completion}%","bold")
        resp = ping(reseau+"."+str(ip))
        if resp == False:
            continue
        else:
            IP_prise.append(f"{reseau}.{ip}")
            nombre_hote+=1
            root.update()
    if nombre_hote == 0:
        Template()
        text.insert(tk.END, f" \"Scan terminé \"Aucun hote trouvé\"\n")
        root.update()
        progress.stop()
    elif nombre_hote ==1:
        Template()
        text.insert(tk.END, f"\"Scan terminé 1 hote trouvé\"\n")
        Template()
        text.insert(tk.END, f"{IP_prise}")
        root.update()
        progress.stop()
    else:
        Template()
        text.insert(tk.END, f"\"Scan terminé {nombre_hote} hotes\"\n")
        text.insert(tk.END, f"{IP_prise}")
        root.update()
        progress.stop()
    log_text()
    return IP_prise
def on_scan_ip():
    try:
        reseau = simpledialog.askstring("Reseau", "Entrez le reseau :", parent=root)
        debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage IP :", parent=root))
        fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage IP :", parent=root))
        Scan_IP(reseau, debut, fin)
    except TypeError:
        pass



####Scan Ports Reseau
def Scan_port(IP,debut,fin):
    text.config(state="normal")
    text.config(font=("Sans", 12))
    text.tag_config("bold", font=("Sans", 12, "bold"))
    text.tag_config("italic", font=("Sans", 12, "italic"))

    i=0
    TCP=[]
    UDP=[]
    progress.start()
    for port in range(debut,fin+1):
        i+=1
        update_progress()
        completion=i*(100//(fin-debut))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            Template()
            text.insert(tk.END, f"{completion}%")
            Template()
            text.insert(tk.END,f"Port {port} est ouvert en TCP.")
            TCP.append(port)
            root.update()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            Template()
            text.insert(tk.END,f"Port {port} est ouvert en UDP.")
            UDP.append(port)
            root.update()
    Template()
    text.insert(tk.END,f"Port {TCP} en TCP.")
    Template()
    text.insert(tk.END,f"Port {UDP} en UDP.")
    text.config(state="disable")
    progress.stop()
    sock.close()
    log_text()
    return TCP,UDP
def on_scan_ports():
    try:
        Host = simpledialog.askstring("host", "Entrez l'ip a scan  :", parent=root)
        debut = int(simpledialog.askstring("Debut", "Entrez le debut de plage port :", parent=root))
        fin = int(simpledialog.askstring("Fin", "Entrez la fin de plage port:", parent=root))
        Scan_port(Host, debut, fin)
    except TypeError:
        pass


####SpeedTest

def Speedtest():
    #Parametrage du texte
    text.config(state="normal")
    text.config(font=("Sans", 12))
    text.tag_config("bold", font=("Sans", 12, "bold"))
    text.tag_config("italic", font=("Sans", 12, "italic"))

    Template()
    progress.start()
    text.insert(tk.END," Speedtest en cours,Veuillez patientez... ")
    root.update()
    str_DL=""
    str_UP=""
    program_path = "C:\\Users\\b.dezord\\Desktop\\spped\\speedtest.exe"

    result = subprocess.run(program_path, shell=True, capture_output=True, text=True)
    output = result.stdout.split('\n')
    update_progress()

    for line in output:
        if 'Download:' in line:
             str_DL=line
        if 'Upload:' in line:
             str_UP=line
    DL=str_DL.split()[1]+str_DL.split()[2]
    UP=str_UP.split()[1]+str_DL.split()[2]
    progress.stop()

    ###Partie du Download
    Template()
    text.insert(tk.END,f" Vitesse de Download ")
    Template()
    text.insert(tk.END,f" {DL}", "bold")
    root.update()
    ###Partie du Upload
    Template()
    text.insert(tk.END,f" Vitesse D'upload  ")
    Template()
    text.insert(tk.END,f" {UP}", "bold ")
    root.update()
    text.config(state="disable")
    log_text()

def Template():
    text.config(state="normal")
    text.config(font=("Sans", 12))
    text.tag_config("bold", font=("Sans", 12, "bold"))
    text.tag_config("italic", font=("Sans", 12, "italic"))
    text.tag_configure('red_text', foreground='red')
    current_time=datetime.now().strftime("%H:%M:%S")
    text.insert(tk.END,f"\n{current_time}", "italic")
    text.insert(tk.END,f"  {hostname} :",'red_text')









####LOGO###
root.wm_iconbitmap("C:\\Users\\b.dezord\\Desktop\\SEMAOS.ico")

####BOUTONS####

###Bouton Test###
bouton_Template= tk.Button(root, text="Template", command=Template, width = 20, height = 3,bg="#1B97C6", bd=8)
bouton_Template.pack()
####Bouton Scan SPEEDTEST

speedtest_button = tk.Button(root, text="SpeedTest", command=Speedtest, width = 20, height = 3,bg="#B991A3", bd=8)
speedtest_button.pack()
#####
###Bouton Scan_Port
scan_button = tk.Button(root, text="Scan Ports", command=on_scan_ports, width = 20, height = 3,bg="#1B97C6", bd=8)
scan_button.pack()
###


####Bouton Scan IP

scan_IP_button = tk.Button(root, text="Scan IP", command=on_scan_ip, width = 20, height = 3,bg="#B991A3", bd=8)
scan_IP_button.pack()
########


###Zone de texte
text = tk.Text(root)
text.config(state="disable")
text.config(bg='#1e1e29', fg='#e0e1e6')
text.config(width=100,height=50)
text.pack()
#####



root.mainloop()



