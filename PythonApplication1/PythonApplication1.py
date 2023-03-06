# -*- coding: utf-8-sig -*-

import socket
import tkinter as tk
from tkinter import ttk
import CP
import sqlite3
import socket
from tkinter import *
import asyncio


Upload_label=tk.Label()
Download_label=tk.Label()
Latence=tk.Label()
Connexion_value=tk.Label()



def lancement():
        
        Version_APP= str(0.8)
        color, msg = CP.qualite_connexion()
        hostname=socket.gethostname()

        ###SQL###
        conn = sqlite3.connect('Base.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS entreprise 
                                        (ent_id INTEGER PRIMARY KEY AUTOINCREMENT ,
                                         ent_name TEXT ,
                                         ent_adresse TEXT ,
                                         ent_siret TEXT)
                                         ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS semabox
                                        (sem_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         sem_client int,
                                         sem_name TEXT ,                     
                                         sem_inf_version_OS TEXT,
                                         sem_inf_up_speed TEXT,
                                         sem_inf_dl_speed TEXT,
                                         FOREIGN KEY(sem_client) REFERENCES entreprise(ent_id))
                                         ''')

                  

            ###ENTREPRISE BIDON
    
        ####
        conn.commit()
        cursor.execute("SELECT sem_inf_version_OS,sem_inf_up_speed,sem_inf_dl_speed FROM semabox")
        results = cursor.fetchall()
    
        # Boucle pour afficher les données dans un label
        version_OS="NON_RENSEIGNER"
        up_speed = "NON_RENSEIGNER"
        dl_speed = "NON_RENSEIGNER"
        for result in results:
            version_OS=result[0]
            up_speed = result[1]
            dl_speed = result[2]

        if version_OS=="NON_RENSEIGNER":
            cursor.execute("INSERT INTO entreprise (ent_name,ent_adresse,ent_siret) VALUES ('Capsule_Corp','29 rue des chiens','1023202549875420')")
        
            cursor.execute(f"""INSERT INTO semabox (sem_client,sem_name,sem_inf_version_OS) 
                               VALUES (1,'{hostname}','{Version_APP}')""")
        
        
        else:
            cursor.execute(f"""UPDATE semabox
                               SET sem_inf_version_OS ='{version_OS}',
                               sem_inf_up_speed ='{up_speed}',
                               sem_inf_dl_speed='{dl_speed}'
                               WHERE sem_client = (SELECT ent_id 
                                                   FROM entreprise
                                                   WHERE sem_client = ent_id)
                               """ )
        conn.commit()
        conn.close()        



       ##Creation de la page
        Page = tk.Tk()
        Page.geometry("1009x1000+450+50")
        Page.title("SemaOS")

        text = tk.Text(Page,width=130,height=30)

        ####LOGO###

        Page.wm_iconbitmap(".\\image\\SEMAOS.ico")

            

    
        ####BOUTONS####

        speedtest_button = tk.Button(Page, text="SpeedTest", command=lambda:  CP.Speedtest(text, Page, Upload_label,Download_label), width=15, height=3, bg="#B991A3", bd=8)
        speedtest_button.place(x=580, y=200)

        scan_button = tk.Button(Page, text="Scan Ports", command=lambda:  CP.on_scan_ports(text, Page), width=15, height=3, bg="#1B97C6", bd=8)
        scan_button.place(x=480, y=200)

        scan_IP_button = tk.Button(Page, text="Scan IP", command=lambda: CP.Scan_IP_Choice(text, Page), width=15, height=3, bg="#B991A3", bd=8)
        scan_IP_button.place(x=380, y=200)
   

        Latence=tk.Label()
        Upload_label=tk.Label()
        Download_label=tk.Label()
        Connexion_value=tk.Label()
        #LABEL_TEXT
        async def LABEL():
            Inf=tk.Label(Page,text="DERNIERE INFO ",font=("Arial",10,"bold"))
            Inf.place(x=840, y=0)

            _ip_pub=str(await CP.get_public_ip())
            Ip_pub=tk.Label(Page,text=f"Mon IP PUBLIC:"+_ip_pub,font=("Arial",10,"bold"))
            Ip_pub.place(x=780, y=160)

            Latence=tk.Label(Page,text="Latence Moyenne :"+ CP.latency_ping_test("google.fr"),font=("Arial",10,"bold"))
            Latence.place(x=780, y=40)

            Upload_label=tk.Label(Page,text=f"Vitesse Upload: {up_speed}",font=("Arial",10,"bold"))
            Upload_label.place(x=780, y=60)

            Download_label=tk.Label(Page,text=f"Vitesse de Download: {dl_speed}",font=("Arial",10,"bold"))
            Download_label.place(x=780, y=80)

            Nom_hote=tk.Label(Page,text=f"HOTE: {hostname}",font=("Arial",10,"bold"))
            Nom_hote.place(x=780, y=290)

            _network_address = str(await CP.get_network_address())
            Mon_Reseau=tk.Label(Page,text="Mon IP: "+_network_address,font=("Arial",10,"bold"))
            Mon_Reseau.place(x=780, y=310)

            Connexion_value=tk.Label(Page,text=msg, font=("Arial",10,"bold"),fg=color)
            Connexion_value.place(x=780, y=330)

            Version_OS=tk.Label(Page,text=f"Version: {version_OS}",font=("Arial",10,"bold"))
            Version_OS.place(x=780, y=350)

        
        asyncio.run(LABEL())
    


        ###Zone de texte

        text.config(state="disable")
        text.config(bg='#1e1e29', fg='#e0e1e6')
        text.place(x=0, y=480)
        #####
    

        ###Maj Label
        MaJ_Button=tk.Button(Page,text="Maj Info",command=lambda:CP.MaJ_Label(Upload_label,Download_label,Latence,Connexion_value,Page), width=20, height=3, bg="#FF5B2B", bd=8)
        MaJ_Button.place(x=780, y=380)


        

        ##Bouton de redémarrage##
        restart_button = tk.Button(Page, text="Relancer", command=lambda: restart(), width=20, height=3, bg="red", bd=8)
        restart_button.place(x=450, y=0)

   
        scrollbar = Scrollbar()
        def restart():
            Page.destroy()
            lancement()
            
    

        listbox = Listbox(Page, yscrollcommand=scrollbar.set)
        listbox.pack(side=LEFT, fill=BOTH)
        scrollbar = Scrollbar(Page)
        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set,height=27, width=40)
    
        listbox.place(x=20, y=10)
        scrollbar.place(x=0, y=0)

        #Ajouter des éléments à la liste
        asyncio.run(CP.Remplir_listbox(listbox,1,254))
    
     
            

        Page.resizable(False, False)
        Page.mainloop()
 
        
lancement()



