import sys, datetime, pdf417, mimetypes, smtplib, ssl
import tkinter.messagebox
from tkinter import *
from PIL import Image, ImageTk
from email.message import EmailMessage

def citajC():
    popis = []
    cl = open("clanovi.dat")
    podaci = cl.readlines()
    cl.close()
    for i in range(len(podaci)):
        podaci[i] = podaci[i].rstrip("\n")
        j = podaci[i].split("\t")
        popis.append(j)
    popisA = []
    for i in range(len(popis)):
        if popis[i][4] == "A":
            popisA.append(popis[i])
    return popis, popisA

def pisiC(a):
    cl = open("clanovi.dat", "w")
    text = ""
    for i in range(len(a)):
        for j in range(len(a[0])):
            text = text + a[i][j]
            if j != 5:
                text = text + "\t"
        text = text + "\n"
    cl.write(text)
    cl.close()

def citajP():
    po = open("podaci.dat")
    podaci = po.read()
    x = podaci.split("\n")
    po.close()
    return x

def pisiP(a, b, c, d):
    podaci = open("podaci.dat", "w")
    podaci.write(a)
    podaci.write("\n")
    podaci.write(b)
    podaci.write("\n")
    podaci.write(c)
    podaci.write("\n")
    podaci.write(d)
    podaci.close()

def lista(ulaz):
    text = ""
    for i in range(len(ulaz)):
        if ulaz[i][3] == "O":
            j = "ODRASLI"
        else:
            j = "DJECA"
        if ulaz[i][4] == "A":
            k = "AKTIVAN"
        else:
            k = "NEAKTIVAN"
        text = text+ ulaz[i][0]+" "+ ulaz[i][1]+", e-mail: "+ulaz[i][2]+" "+j+" "+k+"\n"
    return text

def barkod(iznos,platitelj,IBAN,pozivNaBroj,opis,slika):
    text = "HRVHUB30\nHRK\n0000000000"+iznos+"00\n"+platitelj+"\n\n\n\n\n\n"+IBAN+"\nHR00\n"+pozivNaBroj+"\n\n"+opis
    codes = pdf417.encode(text)
    image = pdf417.render_image(codes)
    image.save(slika)

def saljiMail(vrsta,m,primatelj,privitak,iznos,pozivNaBroj,IBAN,brojMailova):
    global posiljatelj, sifra, adresa, potpis
    msg = EmailMessage()
    msg['From'] = posiljatelj
    msg['To'] = primatelj
    if vrsta == 1:
        msg['Subject'] = "AK Musubi - Članarina za "+str(m)+". mjesec"
        msg.add_alternative("""
<p>Poštovani,</p>
<p>u prilogu se nalaze podaci za uplatu članarine za """+str(m)+""". mjesec.</p>
<p>Iznos: """+iznos+""",00 HRK</p>
<p>Model / Poziv na broj: HR00 / """+pozivNaBroj+"""</p>
<p>Opis plaćanja: Članarina za """+str(m)+""". mjesec (ime i prezime polaznika za slučaj da netko drugi vrši uplatu)</p>
<p>Primatelj: """+adresa+"""</p>
<p>Plaćanje treba obaviti na IBAN: """+IBAN+"""</p>
<p>Članarinu je moguće platiti i skeniranjem 2D barkoda u privitku ove poruke (koristeći mobilne aplikacije).</p>
<p>LP</p><p>"""+potpis+"""</p>
""", subtype='html')
        filename = privitak
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(filename, 'rb') as fp:
            msg.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=filename)

    elif vrsta == 2:
        msg['Subject'] = "AK Musubi - Upisnina"
        msg.add_alternative("""
<p>Poštovani,</p>
<p>u prilogu se nalaze podaci za jednokratnu uplatu upisnine za Aikido klub Musubi.</p>
<p>Iznos: """+iznos+""",00 HRK</p>
<p>Model / Poziv na broj: HR00 / """+pozivNaBroj+"""</p>
<p>Opis plaćanja: Upisnina (ime i prezime polaznika za slučaj da netko drugi vrši uplatu)</p>
<p>Primatelj: """+adresa+"""</p>
<p>Plaćanje treba obaviti na IBAN: """+IBAN+"""</p>
<p>Upisninu je moguće platiti i skeniranjem 2D barkoda u privitku ove poruke (koristeći mobilne aplikacije).</p>
<p>LP</p><p>"""+potpis+"""</p>
</p>
""", subtype='html')
        filename = privitak
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(filename, 'rb') as fp:
            msg.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=filename)

    elif vrsta == 3:
        msg['Subject'] = "AK Musubi - Statistika za "+str(m)+". mjesec"
        msg.add_alternative("""
<p>Poštovani,</p>
<p>Za """+str(m)+""". mjesec je poslano """+str(brojMailova)+""" mailova s barkodovima ukupnog iznosa """+str(iznos)+""" HRK.</p>
<p>LP</p><p>"""+potpis+"""</p>
</p>
""", subtype='html')
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp.login(posiljatelj,sifra)
        smtp.send_message(msg)


win = Tk()
win.title("Musubi Članarine")
win.geometry("640x550")
win.resizable(False, False)
p = open("credentials.dat",encoding='utf-8')
podaci = p.read()
posiljatelj, sifra, tajnik, adresa, potpis = podaci.split("\n")
p.close()


def f0_main():          #GLAVNI IZBORNIK
    w0btn1.grid(column=1, row=1, sticky=EW, pady=2)
    w0btn2.grid(column=1, row=2, sticky=EW, pady=2)
    w0btn3.grid(column=1, row=3, sticky=EW, pady=2)
    w0btn4.grid(column=1, row=4, sticky=EW, pady=2)

def f0_delete():
    w0btn1.grid_forget()
    w0btn2.grid_forget()
    w0btn3.grid_forget()
    w0btn4.grid_forget()


def f1_main():           #IZBORNIK 1: SLANJE ČLANARINA
    f0_delete()
    global listaClanova
    listaClanova,l2 = citajC()
    godina = datetime.datetime.now().year
    mjesec = datetime.datetime.now().month
    dan = datetime.datetime.now().day
    if dan >= 25:
        mjesec += 1
        if mjesec == 13:
            mjesec = 1
            godina = godina + 1
    w1entry1.delete(0, END)
    w1entry1.insert(0, mjesec)
    w1entry2.delete(0, END)
    w1entry2.insert(0, godina)
    broj = len(l2)
    f1s(broj)
    w1frame.grid(column=0, row=1, columnspan=4, sticky=EW, padx=20)
    wel.grid(column=0, row=2, columnspan=2)
    w1l1.grid(column=2, row=3,sticky=E)
    w1entry1.grid(column=3, row=3,sticky=W)
    w1l2.grid(column=2, row=4,sticky=E)
    w1entry2.grid(column=3, row=4,sticky=W)
    w1btn1.grid(column=1, row=3, sticky=EW, padx=10, pady=2)
    w1btn2.grid(column=1, row=4, sticky=EW, padx=10, pady=2)
    w1btn3.grid(column=1, row=5, sticky=EW, padx=10, pady=2)
    w1btn4.grid(column=1, row=6, sticky=EW, padx=10, pady=2)
    w1btn5.grid(column=1, row=7, sticky=EW, padx=10, pady=2)
    w1btn6.grid(column=1, row=8, sticky=EW, padx=10, pady=2)

def f1_win1():          #ŠALJI UPLATNICE ZA ČLANARINE
    global win1
    l1,l2=citajC()
    win1 = Toplevel(win)
    a = str(len(l2))
    win1.title("Slanje uplatnica za članarine")
    win1.geometry("360x120")
    win1.resizable(False,False)
    win1.grab_set()
    w1pl1=Label(win1,text="Broj mailova koji će se poslati: "+a)
    w1pb1=Button(win1,text="Šalji",command=f1_send_clanarina)
    w1pb2=Button(win1,text="Otkaži",command=f1_send_clanarina_exit)
    w1pl1.grid(column=0,row=0,columnspan=2,sticky=EW,padx=80,pady=20)
    w1pb1.grid(column=0,row=1,sticky=EW,padx=20,pady=15)
    w1pb2.grid(column=1,row=1,sticky=EW,padx=20,pady=15)


def f1_send_clanarina():
    l1,l2=citajC()
    IBAN,iznos1,iznos2,iznos3 = citajP()
    m=w1entry1.get()
    global tajnik, posiljatelj
    pozivNaBroj=""
    if int(m)<10:
        pozivNaBroj="0"
    pozivNaBroj=pozivNaBroj+m+"-"+w1entry2.get()
    x = 0
    for i in range(len(l2)):
        platitelj = l2[i][0] +" "+ l2[i][1]
        if l2[i][3]=="O":
            iznos=iznos1
        else:
            iznos=iznos2
        if l2[i][5]=="p1":
            iznos=str(int(int(iznos)*0.8))
        elif l2[i][5]=="p2":
            iznos=str(int(iznos)-50)
        opis = "Clanarina za "+m+". mjesec - "+platitelj
        slika = "Barkod_"+pozivNaBroj+"_"+l2[i][1]+l2[i][0]+".jpg"
        barkod(iznos,platitelj,IBAN,pozivNaBroj,opis,slika)
        saljiMail(1,m,l2[i][2],slika,iznos,pozivNaBroj,IBAN,i)
        x += int(iznos)
    saljiMail(3,m,tajnik+"; "+posiljatelj,slika,x,pozivNaBroj,IBAN,i+1)
    w1status.config(text= "Poslano je "+str(len(l2))+" mailova.")
    w1status.grid()
    f1_send_clanarina_exit()

def f1_send_clanarina_exit():
    win1.grab_release()
    win1.destroy()

def f1_win2():          #ŠALJI UPLATNICU ZA UPISNINU
    global win2, w1pb1, w1pl2, listaClanova
    l1,l2=citajC()
    win2 = Toplevel(win)
    a = str(len(l2))
    win2.title("Slanje uplatnice za upisninu")
    win2.geometry("360x275")
    win2.resizable(False,False)
    win2.grab_set()
    w1pl1=Label(win2,text="Odaberite člana kojemu će se poslati\nuplatnica za upisninu.")
    w1pl2=Listbox(win2, height=10, exportselection=False)
    w1pl2.bind("<<ListboxSelect>>", f1_win2_select)
    w1pb1=Button(win2,text="Šalji",command=f1_send_upisnina)
    w1pb1.config(state=DISABLED)
    w1pb2=Button(win2,text="Otkaži",command=f1_send_upisnina_exit)
    w1pl1.grid(column=0,row=0,columnspan=2,sticky=EW,padx=80,pady=5)
    w1pl2.grid(column=0,row=1,columnspan=2,rowspan=10,sticky=EW,padx=20,pady=5)
    w1pb1.grid(column=0,row=12,sticky=EW,padx=20,pady=10)
    w1pb2.grid(column=1,row=12,sticky=EW,padx=20,pady=10)
    for i in range(len(listaClanova)):
        w1pl2.insert(i + 1, listaClanova[i][0] + " " + listaClanova[i][1])

def f1_win2_select(event):
    global clan, listaClanova
    w1pb1.config(state=NORMAL)
    j=w1pl2.curselection()[0]
    clan = listaClanova[j]

def f1_send_upisnina():
    l1,l2=citajC()
    IBAN,iznos1,iznos2,iznos = citajP()
    pozivNaBroj="00-"+w1entry2.get()
    platitelj=clan[0]+" "+clan[1]
    opis = "Upisnina - "+platitelj
    slika = "Barkod_Upisnina_"+clan[1]+clan[0]+".jpg"
    barkod(iznos,platitelj,IBAN,pozivNaBroj,opis,slika)
    saljiMail(2,0,clan[2],slika,iznos,pozivNaBroj,IBAN,1)
    w1status.config(text="Poslana je uplatnica za upisninu za člana "+clan[0]+" "+clan[1])
    w1status.grid()
    f1_send_upisnina_exit()

def f1_send_upisnina_exit():
    win2.grab_release()
    win2.destroy()

def f1_win3():          #GENERIRAJ JEDINSTVENI BARKOD
    global win3, w6entry1, w6entry2, w6entry3, w6entry4, w6entry5, w6entry6, w6entry7
    IBAN,iznos1,iznos2,iznos3 = citajP()
    win3 = Toplevel(win)
    win3.title("Generiranje jedinstvenog barkoda")
    win3.geometry("360x275")
    win3.resizable(False,False)
    win3.grab_set()
    w6l0 = Label(win3,text="Unesite podatke.")
    w6l1 = Label(win3,text="Iznos:")
    w6l1a = Label(win3,text="HRK")
    w6l2 = Label(win3,text="Stvarni dužnik:")
    w6l3 = Label(win3,text="IBAN:")
    w6l4 = Label(win3,text="Model:")
    w6l5 = Label(win3,text="Poziv na broj:")
    w6l6 = Label(win3,text="Opis plaćanja:")
    w6l7 = Label(win3,text="Naziv datoteke:")
    w6l7a = Label(win3,text=".jpg")
    w6btn1 = Button(win3,text="Generiraj barkod", command=f1_create_barcode)
    w6btn2 = Button(win3,text="Odustani", command=f1_create_barcode_exit)
    w6entry1 = Entry(win3)
    w6entry2 = Entry(win3)
    w6entry3 = Entry(win3)
    w6entry3.insert(0, IBAN)
    w6entry3.config(state=DISABLED)
    w6entry4 = Entry(win3)
    w6entry4.insert(0, "HR00")
    w6entry4.config(state=DISABLED)
    w6entry5 = Entry(win3)
    w6entry6 = Entry(win3)
    w6entry7 = Entry(win3)

    w6l0.grid(column=0,row=0,columnspan=2)
    w6l1.grid(column=0,row=1)
    w6entry1.grid(column=1,row=1,columnspan=2,sticky=EW,padx=5)
    w6l1a.grid(column=3,row=1)
    w6l2.grid(column=0,row=2)
    w6entry2.grid(column=1,row=2,columnspan=2,sticky=EW,padx=5)
    w6l3.grid(column=0,row=3)
    w6entry3.grid(column=1,row=3,columnspan=2,sticky=EW,padx=5)
    w6l4.grid(column=0,row=4)
    w6entry4.grid(column=1,row=4,columnspan=2,sticky=EW,padx=5)
    w6l5.grid(column=0,row=5)
    w6entry5.grid(column=1,row=5,columnspan=2,sticky=EW,padx=5)
    w6l6.grid(column=0,row=6)
    w6entry6.grid(column=1,row=6,columnspan=2,sticky=EW,padx=5)
    w6l7.grid(column=0,row=7)
    w6entry7.grid(column=1,row=7,sticky=EW,padx=5)
    w6l7a.grid(column=2,row=7,sticky=W)
    w6btn1.grid(column=0,row=8,sticky=EW,padx=10,pady=10)
    w6btn2.grid(column=1,row=8,sticky=EW,padx=10,pady=10)

def f1_create_barcode():
    barkod(w6entry1.get(),w6entry2.get(),w6entry3.get(),w6entry5.get(),w6entry6.get(),w6entry7.get()+".jpg")
    w1status.config(text="Generiran je prilagođeni barkod.")
    w1status.grid()

def f1_create_barcode_exit():
    win3.grab_release()
    win3.destroy()

def f1_list():      #OTVORI LISTU AKTIVNIH ČLANOVA
    global w1p3
    w1btn4['state'] = 'disable'
    w1p3 = Toplevel(win)
    w1p3.title("Popis članova")
    w1p3.protocol("WM_DELETE_WINDOW", f1_list_close)
    l1,l2=citajC()
    w1p3l=Label(w1p3,text=lista(l2))
    w1p3l.grid()
    w1status.config(text="Otvorena lista aktivnih članova.")
    w1status.grid()

def f1_list_close():
    l1,l2=citajC()
    w1p3.destroy()
    w1btn4['state'] = 'normal'
    f1s(len(l2))

def f1_example():       #OTVORI PRIMJER BARKODA
    global w1p4
    w1btn5['state'] = 'disable'
    w1p4 = Toplevel(win)
    w1p4.title("Barkod")
    w1p4.protocol("WM_DELETE_WINDOW", f1_example_close)
    l1,l2=citajC()
    IBAN,iznos1,iznos2,iznos3 = citajP()
    clan=l2[0]
    m=w1entry1.get()
    pozivNaBroj=""
    if int(m)<10:
        pozivNaBroj="0"
    pozivNaBroj=pozivNaBroj+m+"-"+w1entry2.get()
    platitelj = clan[0] +" "+ clan[1]
    if clan[3]=="O":
        iznos=iznos1
    else:
        iznos=iznos2
    opis = "Clanarina za "+m+". mjesec - "+platitelj
    slika = "Barkod_"+pozivNaBroj+"_"+clan[1]+clan[0]+".jpg"
    barkod(iznos,platitelj,IBAN,pozivNaBroj,opis,slika)
    bar = Canvas(w1p4,width=550,height=170)
    bar.grid(row=0, column=0)
    win.img = img = ImageTk.PhotoImage(Image.open(slika))
    bar.create_image(3, 1, anchor =NW, image=img)
    w1status.config(text="Otvoren primjer barkoda za člana "+l2[0][0]+" "+l2[0][1])
    w1status.grid()

def f1_example_close():
    l1,l2=citajC()
    w1p4.destroy()
    w1btn5.config(state=NORMAL)
    f1s(len(l2))

def f1s(broj):          #STATUS MSG
    if broj == 0:
        w1status.config(text="Neće se poslati uplatnice. Nema aktivnih članova.")
    elif broj == 1:
        w1status.config(text="Poslati će se uplatnice za jednog člana.")
    elif broj < 5:
        w1status.config(text="Poslati će se uplatnice za " + str(broj) + " člana.")
    else:
        w1status.config(text="Poslati će se uplatnice za " + str(broj) + " članova.")
    w1status.grid()

def f1_back():
    w1frame.grid_forget()
    w1status.grid_forget()
    w1btn1.grid_forget()
    w1btn2.grid_forget()
    w1btn3.grid_forget()
    w1btn4.grid_forget()
    w1btn5.grid_forget()
    w1btn6.grid_forget()
    wel.grid_forget()
    w1l1.grid_forget()
    w1entry1.grid_forget()
    w1l2.grid_forget()
    w1entry2.grid_forget()
    f0_main()


def f2_main():          #UREĐIVANJE LISTE ČLANOVA
    f0_delete()
    global listaClanova
    listaClanova,l2 = citajC()
    for i in range(len(listaClanova)):
        w2list.insert(i + 1, listaClanova[i][0] + " " + listaClanova[i][1])
    w2frame.grid(column=0, row=1, columnspan=5, sticky=EW, padx=20)
    w2status.config(text="")
    w2status.grid()
    w2l1.grid(column=3, row=2, pady=2)
    w2list.grid(column=3, row=3, rowspan=7)
    w2l2.grid(column=0, row=3, sticky=E)
    w2entry1.grid(column=1, row=3, columnspan=2, sticky=EW,pady=2)
    w2l3.grid(column=0, row=4, sticky=E)
    w2entry2.grid(column=1, row=4, columnspan=2, sticky=EW,pady=2)
    w2l4.grid(column=0, row=5, sticky=E)
    w2entry3.grid(column=1, row=5, columnspan=2, sticky=EW,pady=2)
    w2l5.grid(column=0, row=6, sticky=E, rowspan=2)
    w2r1a.grid(column=1, row=6, sticky=W)
    w2r1b.grid(column=1, row=7, sticky=W)
    w2l6.grid(column=0, row=8, sticky=E, rowspan=2)
    w2r2a.grid(column=1, row=8, sticky=W)
    w2r2b.grid(column=1, row=9, sticky=W)
    w2l7.grid(column=2, row=6, sticky=EW)
    w2r3a.grid(column=2, row=7, sticky=W)
    w2r3b.grid(column=2, row=8, sticky=W)
    w2r3c.grid(column=2, row=9, sticky=W)
    w2btn3.grid(column=4, row=5, sticky=EW)
    w2btn4.grid(column=4, row=6, sticky=EW, pady=2)
    w2btn1.grid(column=1, row=10, pady=10)
    w2btn2.grid(column=2, row=10, pady=10)

    w2entry1.delete(0, END)
    w2entry2.delete(0, END)
    w2entry3.delete(0, END)
    # w2r1a.deselect()
    # w2r1b.deselect()
    # w2r2a.deselect()
    # w2r2b.deselect()

def f2_save():
    global listaClanova
    clan = [w2entry1.get(), w2entry2.get(), w2entry3.get()]
    if f2radio1() == 1:
        a = "O"
    else:
        a = "D"
    clan.append(a)
    if f2radio2() == 1:
        a = "A"
    else:
        a = "N"
    clan.append(a)
    if f2radio3() == 3:
        a = "p2"
    elif f2radio3() == 2:
        a = "p1"
    else:
        a = "p0"
    clan.append(a)
    j = w2list.curselection()[0]
    listaClanova[j]=clan
    pisiC(listaClanova)
    w2status.config(text="Podaci su uspješno spremljeni.")
    w2status.grid(sticky=W)
    w2list.delete(0, w2list.size())
    for i in range(len(listaClanova)):
        w2list.insert(i + 1, listaClanova[i][0] + " " + listaClanova[i][1])
    w2btn1.config(state=DISABLED)

def f2_new():
    clan = ["Novi", "Clan", "", "O", "N", "p0"]
    global listaClanova
    w2list.insert(len(listaClanova) + 1, clan[0] + " " + clan[1])
    w2btn1.config(state=NORMAL)
    w2status.config(text="Uspješno dodan novi član.")
    listaClanova.append(clan)
    w2btn1.config(state=DISABLED)

def f2_delete():
    global listaClanova
    j = w2list.curselection()[0]
    izbrisaniClan = listaClanova[j]
    listaClanova.remove(izbrisaniClan)
    w2list.delete(0, w2list.size())
    w2btn1.config(state=DISABLED)
    w2btn4.config(state=DISABLED)
    w2entry1.delete(0, END)
    w2entry2.delete(0, END)
    w2entry3.delete(0, END)
    for i in range(len(listaClanova)):
        w2list.insert(i + 1, listaClanova[i][0] + " " + listaClanova[i][1])
    w2status.config(text="Član "+izbrisaniClan[0]+" "+izbrisaniClan[1]+" je uspješno izbrisan.")
    w2status.grid(sticky=W)

def f2_back():
    w2btn1.config(state=DISABLED)
    w2btn4.config(state=DISABLED)
    w2btn1.grid_forget()
    w2btn2.grid_forget()
    w2l1.grid_forget()
    w2list.delete(0, w2list.size())
    w2list.grid_forget()
    w2l2.grid_forget()
    w2entry1.grid_forget()
    w2l3.grid_forget()
    w2entry2.grid_forget()
    w2l4.grid_forget()
    w2entry3.grid_forget()
    w2l5.grid_forget()
    w2r1a.grid_forget()
    w2r1b.grid_forget()
    w2l6.grid_forget()
    w2r2a.grid_forget()
    w2r2b.grid_forget()
    w2l7.grid_forget()
    w2r3a.grid_forget()
    w2r3b.grid_forget()
    w2r3c.grid_forget()
    w2frame.grid_forget()
    w2status.grid_forget()
    w2btn3.grid_forget()
    w2btn4.grid_forget()
    f0_main()

def f2_select(event):
    w2btn1.config(state=NORMAL)
    w2btn4.config(state=NORMAL)
    w2status.grid_forget()
    w2entry1.delete(0, END)
    w2entry1.insert(0, listaClanova[w2list.curselection()[0]][0])
    w2entry2.delete(0, END)
    w2entry2.insert(0, listaClanova[w2list.curselection()[0]][1])
    w2entry3.delete(0, END)
    w2entry3.insert(0, listaClanova[w2list.curselection()[0]][2])
    if listaClanova[w2list.curselection()[0]][3] == "O":
        w2r1a.select()
    else:
        w2r1b.select()

    if listaClanova[w2list.curselection()[0]][4] == "A":
        w2r2a.select()
    else:
        w2r2b.select()

    if listaClanova[w2list.curselection()[0]][5] == "p0":
        w2r3a.select()
    elif listaClanova[w2list.curselection()[0]][5] == "p1":
        w2r3b.select()
    else:
        w2r3c.select()

def f2radio1():
    return var1.get()

def f2radio2():
    return var2.get()

def f2radio3():
    return var3.get()


def f3_main():          #UREĐIVANJE PODATAKA O UPLATI
    f0_delete()
    w3frame.grid(column=0, row=1, columnspan=3, sticky=EW, padx=20)
    w3status.config(text="")
    w3status.grid(sticky=W)
    wel.grid(column=0,row=2)
    w3l1.grid(column=0, row=3, sticky=E)
    w3entry1.grid(column=1, row=3, sticky=EW)
    w3l2.grid(column=2, row=3, sticky=W)
    w3l3.grid(column=0, row=4, sticky=E)
    w3entry2.grid(column=1, row=4, sticky=EW)
    w3l4.grid(column=2, row=4, sticky=W)
    w3l5.grid(column=0, row=5, sticky=E)
    w3entry3.grid(column=1, row=5, sticky=EW)
    w3l6.grid(column=2, row=5, sticky=W)
    w3l7.grid(column=0, row=6, sticky=E)
    w3entry4.grid(column=1, row=6, sticky=EW)
    w3btn1.grid(column=0, row=7, pady=20)
    w3btn2.grid(column=1, row=7, pady=20)

    x = citajP()
    w3entry1.delete(0, END)
    w3entry1.insert(0, x[1])
    w3entry2.delete(0, END)
    w3entry2.insert(0, x[2])
    w3entry3.delete(0, END)
    w3entry3.insert(0, x[3])
    w3entry4.delete(0, END)
    w3entry4.insert(0, x[0])

def f3_save():
    b = w3entry1.get()
    c = w3entry2.get()
    d = w3entry3.get()
    a = w3entry4.get()
    pisiP(a, b, c, d)
    w3status.config(text="Podaci su uspješno spremljeni.")
    w3status.grid(sticky=W)

def f3_back():
    wel.grid_forget()
    w3btn1.grid_forget()
    w3btn2.grid_forget()
    w3l1.grid_forget()
    w3entry1.grid_forget()
    w3l2.grid_forget()
    w3l3.grid_forget()
    w3entry2.grid_forget()
    w3l4.grid_forget()
    w3l5.grid_forget()
    w3entry3.grid_forget()
    w3l6.grid_forget()
    w3l7.grid_forget()
    w3entry4.grid_forget()
    w3frame.grid_forget()
    w3status.grid_forget()
    f0_main()


def f4_exit():
    win.destroy()
    sys.exit()




banner = Canvas(win, width=600, height=240)
banner.grid(row=0, column=0, sticky=W, columnspan=5, padx=15, pady=10)
img = ImageTk.PhotoImage(Image.open("banner.jpg"))
banner.create_image(3, 1, anchor=NW, image=img)

w0btn1 = Button(win, text="SLANJE ČLANARINA", command=f1_main)
w0btn2 = Button(win, text="UREĐIVANJE LISTE ČLANOVA", command=f2_main)
w0btn3 = Button(win, text="UREĐIVANJE PODATAKA O UPLATI", command=f3_main)
w0btn4 = Button(win, text="IZLAZ", command=f4_exit)

wel = Label(win)    #empty label da zauzme prostor
w1frame = LabelFrame(win, text="Status")
w1status = Label(w1frame)
w1btn1 = Button(win, text="ŠALJI UPLATNICE ZA ČLANARINE", command=f1_win1)
w1btn2 = Button(win, text="ŠALJI UPLATNICU ZA UPISNINU", command=f1_win2)
w1btn3 = Button(win, text="GENERIRAJ PRILAGOĐENI BARKOD", command=f1_win3)
w1btn4 = Button(win, text="LISTA AKTIVNIH ČLANOVA", command=f1_list)
w1btn5 = Button(win, text="VIDI PRIMJER BARKODA", command=f1_example)
w1btn6 = Button(win, text="POVRATAK NA GLAVNI IZBORNIK", command=f1_back)
w1l1 = Label(win, text="Mjesec:")
w1l2 = Label(win, text="Godina:")
w1entry1 = Entry(win)
w1entry2 = Entry(win)

w2frame = LabelFrame(win, text="Status")
w2status = Label(w2frame)
w2btn1 = Button(win, text="SPREMI PROMJENE", state=DISABLED, command=f2_save)
w2btn2 = Button(win, text="POVRATAK NA GLAVNI IZBORNIK", command=f2_back)
w2btn3 = Button(win, text="NOVI ČLAN", command=f2_new)
w2btn4 = Button(win, text="IZBRIŠI ČLANA", state=DISABLED, command=f2_delete)
w2l1 = Label(win, text="Odaberite člana:")
w2l2 = Label(win, text="Ime:")
w2l3 = Label(win, text="Prezime:")
w2l4 = Label(win, text="E-mail adresa:")
w2l5 = Label(win, text="Dob:")
w2l6 = Label(win, text="Status:")
w2l7 = Label(win, text="Popust:")
w2entry1 = Entry(win)
w2entry2 = Entry(win)
w2entry3 = Entry(win)
var1 = IntVar()
w2r1a = Radiobutton(win, text="Odrasli", variable=var1, value=1, command=f2radio1)
w2r1b = Radiobutton(win, text="Djeca", variable=var1, value=2, command=f2radio1)
var2 = IntVar()
w2r2a = Radiobutton(win, text="Aktivan", variable=var2, value=1, command=f2radio2)
w2r2b = Radiobutton(win, text="Nekativan", variable=var2, value=2, command=f2radio2)
var3 = IntVar()
w2r3a = Radiobutton(win, text="Bez popusta", variable=var3, value=1, command=f2radio3)
w2r3b = Radiobutton(win, text="Popust 20%", variable=var3, value=2, command=f2radio3)
w2r3c = Radiobutton(win, text="Popust 50 HRK", variable=var3, value=3, command=f2radio3)
w2list = Listbox(win, height=10, exportselection=False)
w2list.bind("<<ListboxSelect>>", f2_select)

w3frame = LabelFrame(win, text="Status")
w3status = Label(w3frame)
w3btn1 = Button(win, text="SPREMI PROMJENE", command=f3_save)
w3btn2 = Button(win, text="POVRATAK NA GLAVNI IZBORNIK", command=f3_back)
w3l1 = Label(win, text="Cijena članarine za odrasle:")
w3l2 = Label(win, text="HRK")
w3l3 = Label(win, text="Cijena članarine za djecu:")
w3l4 = Label(win, text="HRK")
w3l5 = Label(win, text="Cijena upisnine:")
w3l6 = Label(win, text="HRK")
w3l7 = Label(win, text="IBAN:")
w3entry1 = Entry(win)
w3entry2 = Entry(win)
w3entry3 = Entry(win)
w3entry4 = Entry(win)

f0_main()
win.mainloop()
