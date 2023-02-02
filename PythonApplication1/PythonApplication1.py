# -*- coding: utf-8-sig -*-

from distutils.command.upload import upload
from genericpath import exists
from pickle import GLOBAL
from turtle import bgcolor
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
import sqlite3
import socket
import struct




def Lancement_Programme():
    
    color, msg = CP.qualite_connexion()
    hostname=socket.gethostname()

    # Connect to the database (creates a .db file if not existing)
    conn = sqlite3.connect('Base.db')

    # Create a cursor to execute SQL commands

    cursor = conn.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (ip_pub text, up_speed text, dl_speed text)''')
    #cursor.execute('''CREATE TABLE IF NOT EXISTS data (ip_pub text, up_speed text, dl_speed text,Latence text)''')
    # Validation des changements
    conn.commit()

    # Fermeture de la connexion
    conn.close()


    conn = sqlite3.connect("Base.db")
    cursor = conn.cursor()

    # Exécution de la requête SQL pour sélectionner les données
    cursor.execute("SELECT * FROM data")

    # Récupération des données
    results = cursor.fetchall()

    # Fermeture de la connexion à la base de données
    conn.close()

    # Boucle pour afficher les données dans un label
    for result in results:
        ip_pub = result[0]
        up_speed = result[1]
        dl_speed = result[2]

    #A FAIRE
    #Debuguer la progress_bar
    #Optimisation
    #Gestion d'erreur pour le SpeedTest



    ###Titre de la page
    Page = tk.Tk()

    #Largeur,Hauteur,Pos_Horizontale_page,Pos_Verticale_page
    Page.geometry("1009x915+450+50")

    Page.title("SemaOS")
    ####
    text = tk.Text(Page)

    ####LOGO###

    Page.wm_iconbitmap(".\\image\\SEMAOS.ico")

    # Créer une grille pour les boutons
    grid = tk.Frame(Page)
    grid.pack(side="top", fill="both", expand=True)#pad y = distance entre la grille et le reste en Y

    grid.columnconfigure(0, weight=1, minsize=200)
    grid.columnconfigure(1, weight=1, minsize=200)
    grid.columnconfigure(2, weight=1, minsize=200) 


    ###Progress Bar
    progress = ttk.Progressbar(Page, orient="horizontal", length=200, mode="determinate")
    progress.pack()


    ####BOUTONS####



    speedtest_button = tk.Button(grid, text="SpeedTest", command=lambda: CP.Speedtest(text, Page, progress), width=20, height=3, bg="#B991A3", bd=8)
    speedtest_button.grid(row=1, column=1)

    scan_button = tk.Button(grid, text="Scan Ports", command=lambda: CP.on_scan_ports(text, Page, progress), width=20, height=3, bg="#1B97C6", bd=8)
    scan_button.grid(row=2, column=1)

    scan_IP_button = tk.Button(grid, text="Scan IP", command=lambda: CP.on_scan_ip(text, Page, progress), width=20, height=3, bg="#B991A3", bd=8)
    scan_IP_button.grid(row=3, column=1)

    button = tk.Button(grid, text="TEST", command=lambda: CP.qualite_connexion(), width=20, height=3, bg="#B991A3", bd=8)
    button.grid(row=4, column=1)
    # Centrer la grille
    grid.pack(side="top", fill="both", expand=True)
    grid.grid_rowconfigure(0, weight=1)
    grid.grid_columnconfigure(0, weight=1)


    #LABEL_TEXT
    Inf=tk.Label(Page,text="DERNIERE INFO ",font=("Arial",12,"bold"))
    Inf.place(x=840, y=0)

    Ip_pub=tk.Label(Page,text="Mon IP PUBLIC: "+CP.get_public_ip(),font=("Arial",10,"bold"))
    Ip_pub.place(x=780, y=160)

    Latence=tk.Label(Page,text="Latence Moyenne :"+CP.latency_ping_test("google.fr"),font=("Arial",10,"bold"))
    Latence.place(x=780, y=40)

    Upload_label=tk.Label(Page,text=f"Vitesse Upload: {up_speed}",font=("Arial",10,"bold"))
    Upload_label.place(x=780, y=60)

    Download=tk.Label(Page,text=f"Vitesse de Download: {dl_speed}",font=("Arial",10,"bold"))
    Download.place(x=780, y=80)

    Nom_hote=tk.Label(Page,text=f"HOTE: {hostname}",font=("Arial",10,"bold"))
    Nom_hote.place(x=780, y=340)

    Mon_Reseau=tk.Label(Page,text="Mon IP: "+CP.get_network_address(),font=("Arial",10,"bold"))
    Mon_Reseau.place(x=780, y=360)

    Connexion_value=tk.Label(Page,text=msg, font=("Arial",10,"bold"),fg=color)
    Connexion_value.place(x=780, y=380)

    Version_OS=tk.Label(Page,text="Version: BETA 0.6",font=("Arial",10,"bold"))
    Version_OS.place(x=780, y=400)



    ###Zone de texte

    text.config(state="disable")
    text.config(bg='#1e1e29', fg='#e0e1e6')
    text.config(width=130,height=30)
    text.pack()
    #####


    def show_coords(event):
        x = event.x
        y = event.y
        print("Coords: ({}, {})".format(x, y))



    def restart():
        Page.destroy()
        Lancement_Programme()

    ##Bouton de redémarrage##
    restart_button = tk.Button(grid, text="Relancer", command=lambda: restart(), width=20, height=3, bg="red", bd=8)
    restart_button.grid(row=0, column=1)


    Page.bind("<Button-1>", show_coords)

    Page.resizable(False, False)
    Page.mainloop()

Lancement_Programme()