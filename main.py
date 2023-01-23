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
    for i in range(101):
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
        completion=i*(100//(fin-debut))
        i+=1
        Template()
        text.insert(tk.END, f" {completion}%")
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
            root.update()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        result = sock.connect_ex((IP,port))
        if result == 0:
            Template()
            text.insert(tk.END, f"{completion}%")
            Template()
            text.insert(tk.END,f"Port {port} est ouvert en UDP.")
            root.update()
    text.config(state="disable")
    progress.stop()
    sock.close()
    log_text()

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
    text.insert(tk.END,f"{current_time} ","italic")
    Template()
    progress.start()
    text.insert(tk.END,"Speedtest en cours,Veuillez patientez... ")
    root.update()

    str_DL=""
    str_UP=""
    program_path = "C:\\Users\\b.dezord\\Desktop\\spped\\speedtest.exe"

    result = subprocess.run(program_path, shell=True, capture_output=True, text=True)
    output = result.stdout.split('\n')

    for line in output:
        update_progress()
        if 'Download:' in line:
             str_DL=line
        if 'Upload:' in line:
             str_UP=line

    DL=str_DL.split()[1]+str_DL.split()[2]
    UP=str_UP.split()[1]+str_DL.split()[2]
    progress.stop()

    ###Partie du Download
    Template()
    text.insert(tk.END,f"Vitesse de Download ")
    Template()
    text.insert(tk.END,f"{DL}\n", "bold")
    root.update()

    ###Partie du Upload
    Template()
    text.insert(tk.END,f"Vitesse D'upload  ")
    Template()
    text.insert(tk.END,f"{UP}", "bold ")
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
bouton_Template= tk.Button(root, text="Template", command=Template, width = 10, height = 5)
bouton_Template.pack()
#bouton_test.place(x=10, y=10)

####Bouton Scan SPEEDTEST

speedtest_button = tk.Button(root, text="SpeedTest", command=Speedtest, width = 10, height = 5)
speedtest_button.pack()
#speedtest_button.place(x=120, y=10)
#####
###Bouton Scan_Port
scan_button = tk.Button(root, text="Scan Ports", command=on_scan_ports, width = 10, height = 5)
scan_button.pack()
#scan_button.place(x=230, y=10)
###


####Bouton Scan IP

scan_IP_button = tk.Button(root, text="Scan IP", command=on_scan_ip, width = 10, height = 5)
scan_IP_button.pack()
#scan_IP_button.place(x=340, y=10)
########


###Zone de texte
text = tk.Text(root)
text.config(state="disable")
text.config(bg='#1e1e29', fg='#e0e1e6')
text.pack()
#####



root.mainloop()



