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
import CP

#A FAIRE
#Changer les chemin absolu en relatif
#Essayer de mettre les fonction dans un fichier a part
#Fonction de reboot
#Optimisation
#Gestion d'erreur pour le SpeedTest



###Titre de la page
Page = tk.Tk()
Page.geometry("725x800+600+100")
Page.title("SemaOS")
####
text = tk.Text(Page)

####LOGO###

Page.wm_iconbitmap(".\\image\\SEMAOS.ico")




###Progress Bar
progress = ttk.Progressbar(Page, orient="horizontal", length=200, mode="determinate")
progress.pack()


####BOUTONS####

###Bouton Test###
bouton_Template= tk.Button(Page, text="Template", command=lambda:CP.Template(text), width = 20, height = 3,bg="#1B97C6", bd=8)
bouton_Template.pack()

####Bouton Scan SPEEDTEST
speedtest_button = tk.Button(Page, text="SpeedTest", command=lambda:CP.Speedtest(text,Page,progress), width = 20, height = 3,bg="#B991A3", bd=8)
speedtest_button.pack()
#####

###Bouton Scan_Port
scan_button = tk.Button( text="Scan Ports", command=lambda: CP.on_scan_ports(Page,progress), width = 20, height = 3,bg="#1B97C6", bd=8)
scan_button.pack()
###


####Bouton Scan IP

scan_IP_button = tk.Button(Page, text="Scan IP", command=lambda:CP.on_scan_ip(Page,progress), width = 20, height = 3,bg="#B991A3", bd=8)
scan_IP_button.pack()
########



###Zone de texte

text.config(state="disable")
text.config(bg='#1e1e29', fg='#e0e1e6')
text.config(width=100,height=50)
text.pack()
#####




Page.mainloop()




