import mysql.connector
from tkinter import *
from tkinter import ttk

db = mysql.connector.connect(host = "localhost",user = "root",password = "password")

def create_database():
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS boutique;")
        cursor.execute("USE boutique;")
        cursor.execute("CREATE TABLE IF NOT EXISTS categorie (id INT AUTO_INCREMENT PRIMARY KEY,nom VARCHAR(255));")
        cursor.execute("CREATE TABLE IF NOT EXISTS produit (id INT AUTO_INCREMENT PRIMARY KEY,nom VARCHAR(255),description TEXT,prix INT,quantité INT,id_catégorie INT,FOREIGN KEY (id_catégorie) REFERENCES categorie(id));")
        cursor.execute("INSERT INTO categorie(nom) SELECT * FROM (SELECT 'électronique' AS nom UNION SELECT 'électro-ménager') AS tmp WHERE NOT EXISTS (SELECT nom FROM categorie WHERE nom IN ('électronique', 'électro-ménager'))")
        cursor.execute("INSERT INTO produit(nom, description, prix, quantité) SELECT 'Téléviseur LED', 'pass', 1800, 122 WHERE NOT EXISTS(SELECT * FROM produit WHERE nom = 'Téléviseur LED') UNION ALL SELECT 'Lecteur Blu-ray', 'pass', 80, 10 WHERE NOT EXISTS(SELECT * FROM produit WHERE nom = 'Lecteur Blu-ray') UNION ALL SELECT 'Aspirateur sans sac', 'pass', 250, 100 WHERE NOT EXISTS(SELECT * FROM produit WHERE nom = 'Aspirateur sans sac');")
        db.commit()
        cursor.close()


db.autocommit = True
create_database()

gui = Tk()
gui.title("Gestion de stock")
gui.geometry("800x600")

notebook = ttk.Notebook(gui)
table_frame = Frame(notebook, width=750, height=600)
add_frame = Frame(notebook, width=750, height=600)
edit_frame = Frame(notebook, width=750, height=600)
delete_frame = Frame(notebook, width=750, height=600)
notebook.add(table_frame, text="Affichage")
notebook.add(add_frame, text="Ajout")
notebook.add(edit_frame, text="Modifier")
notebook.add(delete_frame, text="Supprimer")
notebook.pack(pady=5)

def reload():
    display_products()
    gui.after(500, reload)


def display_products():
    for widget in table_frame.winfo_children():
        widget.destroy()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM produit")
    products = cursor.fetchall()
    cursor.close()

    headers = ["ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"]
    for i, header in enumerate(headers):
        Label(table_frame, text=header, font="bold").grid(row=0, column=i, padx=5, pady=5)

    for i, product in enumerate(products):
        for j, value in enumerate(product):
            Label(table_frame, text=value).grid(row=i+1, column=j, padx=5, pady=5)


def delete_product():
    id = id_entry.get()

    cursor = db.cursor()
    cursor.execute("DELETE FROM produit WHERE id=%s", (id,))
    db.commit()
    cursor.close()

    id_entry.delete(0, END)

    success_label = Label(delete_frame, text="Le produit a été supprimé avec succès!", fg="green")
    success_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    display_products()

def add_product():
    nom = nom_entry.get()
    description = description_entry.get()
    prix = prix_entry.get()
    quantite = quantite_entry.get()

    try:
        prix = int(prix)
        quantite = int(quantite)
    except ValueError:
        success_label = Label(add_frame, text="Veuillez vous assurer que le prix et/ou la quantité soit un nombre", fg="red")
        success_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        return

    cursor = db.cursor()
    cursor.execute("INSERT INTO produit (nom, description, prix, quantité) VALUES (%s, %s, %s, %s)", (nom, description, prix, quantite))
    db.commit()
    cursor.close()

    nom_entry.delete(0, END)
    description_entry.delete(0, END)
    prix_entry.delete(0, END)
    quantite_entry.delete(0, END)

    for widget in add_frame.grid_slaves():
        if int(widget.grid_info()["row"]) == 5 and int(widget.grid_info()["column"]) == 0:
            widget.grid_forget()

    success_label = Label(add_frame, text="Le produit a été ajouté avec succès!", fg="green")
    success_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


nom_label = Label(add_frame, text="Nom:")
nom_label.grid(row=0, column=0, padx=5, pady=5)
nom_entry = Entry(add_frame)
nom_entry.grid(row=0, column=1, padx=5, pady=5)

description_label = Label(add_frame, text="Description:")
description_label.grid(row=1, column=0, padx=5, pady=5)
description_entry = Entry(add_frame)
description_entry.grid(row=1, column=1, padx=5, pady=5)

prix_label = Label(add_frame, text="Prix:")
prix_label.grid(row=2, column=0, padx=5, pady=5)
prix_entry = Entry(add_frame)
prix_entry.grid(row=2, column=1, padx=5, pady=5)

quantite_label = Label(add_frame, text="Quantité:")
quantite_label.grid(row=3, column=0, padx=5, pady=5)
quantite_entry = Entry(add_frame)
quantite_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = Button(add_frame, text="Ajouter", command=add_product)
add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

id_label = Label(delete_frame, text="ID:")
id_label.grid(row=0, column=0, padx=5, pady=5)
id_entry = Entry(delete_frame)
id_entry.grid(row=0, column=1, padx=5, pady=5)

delete_boutton = Button(delete_frame, text="Supprimer", command=delete_product)
delete_boutton.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def edit_product():
    id = id_entry.get()
    nom = nom_entry.get()
    description = description_entry.get()
    prix = prix_entry.get()
    quantite = quantite_entry.get()

    try:
        prix = int(prix)
        quantite = int(quantite)
    except ValueError:
        success_label = Label(edit_frame, text="Veuillez vous assurer que le prix et/ou la quantité soit un nombre", fg="red")
        success_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        return

    cursor = db.cursor()
    cursor.execute("UPDATE produit SET nom=%s, description=%s, prix=%s, quantité=%s WHERE id=%s", (nom, description, prix, quantite, id))
    db.commit()
    cursor.close()

    id_entry.delete(0, END)
    nom_entry.delete(0, END)
    description_entry.delete(0, END)
    prix_entry.delete(0, END)
    quantite_entry.delete(0, END)

    for widget in edit_frame.grid_slaves():
        if int(widget.grid_info()["row"]) == 5 and int(widget.grid_info()["column"]) == 0:
            widget.grid_forget()

    success_label = Label(edit_frame, text="Le produit a été modifié avec succès!", fg="green")
    success_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


def display_edit_product():
    for widget in edit_frame.winfo_children():
        widget.destroy()

    Label(edit_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = Entry(edit_frame)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(edit_frame, text="Nom:").grid(row=1, column=0, padx=5, pady=5)
    nom_entry = Entry(edit_frame)
    nom_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(edit_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
    description_entry = Entry(edit_frame)
    description_entry.grid(row=2, column=1, padx=5, pady=5)

    Label(edit_frame, text="Prix:").grid(row=3, column=0, padx=5, pady=5)
    prix_entry = Entry(edit_frame)
    prix_entry.grid(row=3, column=1, padx=5, pady=5)

    Label(edit_frame, text="Quantité:").grid(row=4, column=0, padx=5, pady=5)
    quantite_entry = Entry(edit_frame)
    quantite_entry.grid(row=4, column=1, padx=5, pady=5)

    submit_button = Button(edit_frame, text="Modifier", command=edit_product)
    submit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


display_edit_product()


reload()
display_products()
mainloop()