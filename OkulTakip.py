import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import datetime
from tkinter import font

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'okul_takip',
    'raise_on_warnings': True
}


def sql_baglanti():
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print('MySQL veritabanına başarıyla bağlandı.')
        return conn
    except mysql.connector.Error as err:
        print(f"Hata: {err}")
        return None



def okul_guncelle(tree):
    try:
        conn = sql_baglanti()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM okullar")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Hata", f"Bir hata oluştu: {err}")

def okul_duzenle(tree):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")
    okul_id = values[0]
    kurum_kodu = values[1]
    ilce = values[2]
    okul_ad=values[3]
    mudur_adi=values[4]
    telefon=values[5]

    okul_duzenleme_penceresi = tk.Toplevel(root,background='white')
    okul_duzenleme_penceresi.title("Okul Düzenle")

    tk.Label(okul_duzenleme_penceresi, text="Kurum Kodu:", background='white', foreground='black', font=('Arial', 12)).grid(row=0, column=0)
    kurum_kodu_entry = tk.Entry(okul_duzenleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    kurum_kodu_entry.insert(0, kurum_kodu)
    kurum_kodu_entry.grid(row=0, column=1)
    tk.Label(okul_duzenleme_penceresi, text="İlçe:",background='white', foreground='black', font=('Arial', 12)).grid(row=1, column=0)
    ilce_entry = tk.Entry(okul_duzenleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    ilce_entry.insert(0, ilce)
    ilce_entry.grid(row=1, column=1)

    tk.Label(okul_duzenleme_penceresi, text="Okulun Adı:",background='white', foreground='black', font=('Arial', 12)).grid(row=2, column=0)
    okul_ad_entry = tk.Entry(okul_duzenleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    okul_ad_entry.insert(0, okul_ad)
    okul_ad_entry.grid(row=2, column=1)
    
    tk.Label(okul_duzenleme_penceresi, text="Müdür Adı Soyadı:",background='white', foreground='black', font=('Arial', 12)).grid(row=3, column=0)
    mudur_adi_entry = tk.Entry(okul_duzenleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    mudur_adi_entry.insert(0, mudur_adi)
    mudur_adi_entry.grid(row=3, column=1)

    tk.Label(okul_duzenleme_penceresi, text="Telefon:",background='white', foreground='black', font=('Arial', 12)).grid(row=4, column=0)
    telefon_entry = tk.Entry(okul_duzenleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    telefon_entry.insert(0, telefon)
    telefon_entry.grid(row=4, column=1)

    def okul_duzenle_veritabanina():
        yeni_kurum_kod = kurum_kodu_entry.get()

        yeni_ilce=ilce_entry.get()
        yeni_okul_ad=okul_ad_entry.get()
        yeni_mudur_ad=mudur_adi_entry.get()
        yeni_telefon = telefon_entry.get()

        if not yeni_okul_ad:
            messagebox.showwarning("Uyarı", "Okul adı giriniz.")
            return

        try:
            conn = sql_baglanti()
            cursor = conn.cursor()
            sql = "UPDATE okullar SET kurum_kodu=%s,ilce=%s,okul_adi=%s,mudur_adi=%s,telefon=%s WHERE id=%s"
            val = (yeni_kurum_kod,yeni_ilce,yeni_okul_ad,yeni_mudur_ad,yeni_telefon ,okul_id)
            cursor.execute(sql, val)
        
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Başarılı", "Okul başarıyla güncellendi.")
            okul_duzenleme_penceresi.destroy()
            okul_guncelle(tree)
        except mysql.connector.Error as err:
            messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
    def ekle_ve_guncelle():
        
        okul_duzenle_veritabanina()
    
        okul_goster(frame_all_schools)
        gidilen_okul_goster(frame_visited_schools)
        gidilecek_okullar_pencere(frame_schools_to_visit)

    tk.Button(okul_duzenleme_penceresi, text="Güncelle", command=ekle_ve_guncelle,background='#073456', foreground='white', font=('Arial', 12)).grid(row=5, column=0, columnspan=2)

def okul_ekle():
    okul_ekleme_penceresi = tk.Toplevel(root, background='white')
    okul_ekleme_penceresi.title("Okul Ekle")

    tk.Label(okul_ekleme_penceresi, text="Kurum Kodu:", background='white', foreground='black', font=('Arial', 12)).grid(row=0, column=0)
    kurum_kodu_entry = tk.Entry(okul_ekleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    kurum_kodu_entry.grid(row=0, column=1)

    tk.Label(okul_ekleme_penceresi, text="İlçe:", background='white', foreground='black', font=('Arial', 12)).grid(row=1, column=0)
    ilce_entry = tk.Entry(okul_ekleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    ilce_entry.grid(row=1, column=1)
    tk.Label(okul_ekleme_penceresi, text="Okul Adı:", background='white', foreground='black', font=('Arial', 12)).grid(row=2, column=0)
    okul_adi_entry = tk.Entry(okul_ekleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    okul_adi_entry.grid(row=2, column=1)
    tk.Label(okul_ekleme_penceresi, text="Müdür Adı Soyadı:", background='white', foreground='black', font=('Arial', 12)).grid(row=3, column=0)
    mudur_adi_entry = tk.Entry(okul_ekleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    mudur_adi_entry.grid(row=3, column=1) 

    tk.Label(okul_ekleme_penceresi, text="Telefon:", background='white', foreground='black', font=('Arial', 12)).grid(row=4, column=0)
    telefon_entry = tk.Entry(okul_ekleme_penceresi, background='white', foreground='black', font=('Arial', 12))
    telefon_entry.grid(row=4, column=1)

    def okul_ekle_veritabanina():
        kurum_kodu=kurum_kodu_entry.get()

        ilce=ilce_entry.get()
        okul_adi=okul_adi_entry.get()
        mudur_adi=mudur_adi_entry.get()
        telefon = telefon_entry.get()

        if not okul_adi:
            messagebox.showwarning("Uyarı", "Okul adı giriniz.")
            return

        try:
            conn = sql_baglanti()
            cursor = conn.cursor()
            sql = "INSERT INTO okullar (kurum_kodu, ilce,okul_adi,mudur_adi, telefon) VALUES (%s, %s, %s,%s,%s)"
            val = (kurum_kodu, ilce,okul_adi,mudur_adi, telefon)
            cursor.execute(sql, val)
            
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Başarılı", "Okul başarıyla eklendi.")
            okul_ekleme_penceresi.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
        
  
    def ekle_ve_guncelle():
        
        okul_ekle_veritabanina()
    
    
        okul_goster(frame_all_schools)
        gidilen_okul_goster(frame_visited_schools)
        gidilecek_okullar_pencere(frame_schools_to_visit)

    ekle_button = tk.Button(okul_ekleme_penceresi, text="Ekle", command=ekle_ve_guncelle, background='#073456', foreground='white', font=('Arial', 12))
    ekle_button.grid(row=5, column=1, padx=10, pady=10)



def okul_goster(frame):
  
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                background="#FFFFFF",
                foreground="black",
                rowheight=25,
        
                fieldbackground="#FFFFFF")
    
    style.map('Treeview', background=[('selected', 'dark blue')])

    columns = ("S.N", "KURUM KODU","İLÇE", "OKUL ADI","MÜDÜR ADI SOYADI", "TELEFONU")
    style = ttk.Style()
    style.theme_use("clam")


    tree = ttk.Treeview(frame, columns=columns, show="headings",height=20)
    tree.grid(row=0, column=0,padx=0,pady=(10,400),sticky="nse")
    

    for col in columns:
        tree.heading(col, text=col)
        if col=="S.N":
            tree.column(col, width=50, anchor="nw")
        elif col=="İLÇE":
            tree.column(col, width=180, anchor="nw")
        elif col=="KURUM KODU":
            tree.column(col, width=150, anchor="nw")
        elif col=="OKUL ADI":
            tree.column(col, width=370, anchor="nw")

        else:
            tree.column(col, width=250, anchor="nw")

        

    frame.grid_rowconfigure(0, weight=1)
 
  
    def okul_secme(event):
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, "values")
        okul_id = values[0]
        kurum_kodu = values[1]
        ilce = values[2]
        okul_adi=values[3]
        mudur_adi=values[4]
        telefon=values[5]

        def ayir_girisi(event):
            text = ziyaret_tarihi_entry.get()
            if len(text) == 2 or len(text) == 5: 
                ziyaret_tarihi_entry.insert(tk.END, '/')

        def planla_ziyaret():
            ziyaret_tarihi = ziyaret_tarihi_entry.get()

            if not ziyaret_tarihi :
                messagebox.showwarning("Uyarı", "Planlanan Kontrol tarihi giriniz.")
                return

            try:
                ziyaret_tarihi_date = datetime.datetime.strptime(ziyaret_tarihi, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Hata", "Planlanan Kontrol tarihi yanlış formatında. Lütfen 'gün/ay/yıl' formatında giriniz.")
                return

            try:
                conn = sql_baglanti()
                cursor = conn.cursor()
                
                sql3 = "INSERT INTO gidilecek_okullar (okul_id,ziyaret_tarihi,ilce,okul_adi) VALUES (%s,%s,%s,%s)"
                val3 = (okul_id,ziyaret_tarihi_date.strftime("%Y-%m-%d"),ilce,okul_adi)
                cursor.execute(sql3, val3)
                conn.commit()

                gorev_id = cursor.lastrowid
                # sql4 = "INSERT INTO gorev_tablo(gidilecek_id, planlanan_ziyaret_tarihi) VALUES (%s, %s)"
                # val4 = (gorev_id, ziyaret_tarihi_date.strftime("%Y-%m-%d"))
                # cursor.execute(sql4, val4)
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Başarılı", "Kontrol planı başarıyla eklendi.")
                ziyaret_penceresi.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Hata", f"Bir hata oluştu: {err}")

        ziyaret_penceresi = tk.Toplevel(frame,background="white",height=100)
        ziyaret_penceresi.title("Kontrol Bilgileri")
        ziyaret_penceresi.geometry("500x90")
        tk.Label(ziyaret_penceresi, text="Planlanan Kontrol Tarihi (gün/ay/yıl):",background='white', foreground='black', font=('Arial', 12)).grid(row=0, column=0)
        ziyaret_tarihi_entry = tk.Entry(ziyaret_penceresi,background='white', foreground='black', font=('Arial', 12))
        ziyaret_tarihi_entry.grid(row=0, column=1)
        ziyaret_tarihi_entry.bind('<KeyRelease>', ayir_girisi)

        def ekle_ve_guncelle():
            planla_ziyaret()
            okul_goster(frame_all_schools)
            gidilen_okul_goster(frame_visited_schools)
            gidilecek_okullar_pencere(frame_schools_to_visit)

        ekle_button = tk.Button(ziyaret_penceresi, text="Ekle", command=ekle_ve_guncelle,background='#073456', foreground='white', font=('Arial', 12))
        ekle_button.place(x=200,y=40)

  
        
    try:
        conn = sql_baglanti()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM okullar")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
        
    def okullar_sil(tree):
        secilen_okul = tree.selection()
        if len(secilen_okul) == 0:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz okulu seçin.")
            return

        secilen_okul = secilen_okul[0]
        values = tree.item(secilen_okul, "values")
        okul_id = values[0]
        okul_adi = values[3]

    # Add confirmation dialog
        response = messagebox.askyesno("Onay", f"Okul '{okul_adi}' silmek istediğinize emin misiniz?")
        if response:
            try:
                conn = sql_baglanti()
                cursor = conn.cursor()
                sql = "DELETE FROM okullar WHERE id = %s"
                cursor.execute(sql, (okul_id,))
                conn.commit()
                cursor.close()
                conn.close()

                tree.delete(secilen_okul)
                messagebox.showinfo("Başarılı", "Okul başarıyla silindi.")
            except mysql.connector.Error as err:
                messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
        else:
            messagebox.showinfo("İptal", "Okul silme işlemi iptal edildi.")

    buton1=tk.Button(frame, text="Okul Ekle", command=okul_ekle,background='#073456', foreground='white', font=('Arial', 12))
    buton1.place(x=400,y=550)
    tk.Button(frame, text="Okul Düzenle", command=lambda: okul_duzenle(tree),background='#073456', foreground='white', font=('Arial', 12)).place(x=500,y=550)
    tk.Button(frame, text="Okul Sil", command=lambda: okullar_sil(tree),background='#073456', foreground='white', font=('Arial', 12)).place(x=630,y=550)
    tk.Button(frame, text="Kontrol Planla", command=lambda: okul_secme(tree),background='#073456', foreground='white', font=('Arial', 12)).place(x=720,y=550)
    frame.grid_rowconfigure(1, weight=1)
# Product By...
# ALİ VOLKAN ÇINAR
# KERİM CAN GÜRLER
# CAN BALAMİR
def okul_sil(tree):
    secilen_okul = tree.selection()[0]
    values = tree.item(secilen_okul, "values")
    gorev_id = values[0]
    okul_id = values[1]

    ziyaret_tarihi = values[2]
    ilce=values[3]
    okul_adi = values[4]

    
    response = messagebox.askyesno("Onay", f"Okul '{okul_adi}' Raporu Sonlandırmak İstediğinize Emin misiniz?")
    if response:
        try:
            conn = sql_baglanti()
            cursor = conn.cursor()
            sql_delete = "DELETE FROM gidilen_okullar WHERE gidilecek_id = %s"
            cursor.execute(sql_delete, (gorev_id,))

            
            
            ziyaret_penceresi = tk.Toplevel(tree, background="white", height=100)
            ziyaret_penceresi.title("Yeni Kontrol Tarihi")
            ziyaret_penceresi.geometry("500x100")

            def ayir_girisi(event):
                text = ziyaret_tarihi_entry.get()
                if len(text) == 2 or len(text) == 5: 
                    ziyaret_tarihi_entry.insert(tk.END, '/')

            tk.Label(ziyaret_penceresi, text="Yeni Kontrol Tarihi (gün/ay/yıl):", background='white', foreground='black', font=('Arial', 12)).grid(row=0, column=0)
            ziyaret_tarihi_entry = tk.Entry(ziyaret_penceresi, background='white', foreground='black', font=('Arial', 12))
            ziyaret_tarihi_entry.grid(row=0, column=1)
            ziyaret_tarihi_entry.bind('<KeyRelease>', ayir_girisi)

            def planla_ziyaret():
                yeni_ziyaret_tarihi = ziyaret_tarihi_entry.get()

                if not yeni_ziyaret_tarihi:
                    messagebox.showwarning("Uyarı", "Yeni Kontrol tarihi giriniz.")
                    return

                try:
                    yeni_ziyaret_tarihi_date = datetime.datetime.strptime(yeni_ziyaret_tarihi, "%d/%m/%Y")
                except ValueError:
                    messagebox.showerror("Hata", "Yeni kontrol tarihi yanlış formatında. lütfen 'gün/ay/yıl' formatında giriniz.")
                    return

                
                sql2 = "INSERT INTO gidilecek_okullar (gidilecek_id, okul_id, ziyaret_tarihi, ilce, okul_adi) VALUES (%s, %s, %s, %s, %s)"
                val2 = (gorev_id, okul_id, yeni_ziyaret_tarihi_date.strftime("%Y-%m-%d"), ilce, okul_adi)
                cursor.execute(sql2, val2)

                conn.commit()
                cursor.close()
                conn.close()

                tree.delete(secilen_okul)

                messagebox.showinfo("Başarılı", "Rapor Başarıyla Sonlandırıldı Ve Programa Eklendi.")
                ziyaret_penceresi.destroy()

            def ekle_ve_guncelle():
                planla_ziyaret()
                okul_goster(frame_all_schools)
                gidilen_okul_goster(frame_visited_schools)
                gidilecek_okullar_pencere(frame_schools_to_visit)

            ekle_button = tk.Button(ziyaret_penceresi, text="Ekle", command=ekle_ve_guncelle, background='#073456', foreground='white', font=('Arial', 12))
            ekle_button.place(x=200, y=50)

        except mysql.connector.Error as err:
            messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
    else:
        messagebox.showinfo("İptal", "Rapor Sonlandırma işlemi iptal edildi.")

def gidilen_okul_goster(rapor):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#FFFFFF",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#FFFFFF")

    style.map('Treeview', background=[('selected', 'dark blue')])

    columns = ("TARİH", "İLÇE", "OKUL/KURUM ADI")
    tree = ttk.Treeview(rapor, columns=("Görev ID", "Okul ID") + columns, show="headings")

    tree.column("Görev ID", width=0, stretch=tk.NO)  
    tree.column("Okul ID", width=0, stretch=tk.NO)   

    tree.grid(row=0, column=0, padx=0, pady=10, sticky="nse")

    for col in columns:
        tree.heading(col, text=col)
       
        if col == "TARİH":
            tree.column(col, width=150, anchor="nw")

        elif col == "İLÇE":
            tree.column(col, width=200, anchor="nw")
        
        else:
            tree.column(col, width=500, anchor="nw")
    rapor.grid_columnconfigure(0, weight=1)  
    rapor.grid_columnconfigure(1, weight=0)  
    rapor.grid_columnconfigure(2, weight=1)  
    rapor.grid_columnconfigure(0, weight=2)  
    rapor.grid_columnconfigure(2, weight=2)  
    rapor.grid_rowconfigure(0, weight=1)

    try:
        conn = sql_baglanti()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gidilen_okullar")
        rows = cursor.fetchall()
        from datetime import datetime
        today = datetime.now().date()
        
        for row in rows:
            ziyaret_tarihi = row[2]  
            from datetime import datetime
            fark = (today - ziyaret_tarihi).days
            
            if fark > 320:
                tree.insert("", tk.END, values=row, tags=("highlight_red",))
            else:
                tree.insert("", tk.END, values=row,tags=("highlight_green",))

        cursor.close()
        conn.close()

        # Kriterlere göre arka plan rengini ayarlama
        tree.tag_configure("highlight_red", background="#DC143C")
        tree.tag_configure("highlight_green", background="#008000")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
    def sil_ve_guncelle():
        okul_sil(tree)
        okul_goster(frame_all_schools)
        gidilen_okul_goster(frame_visited_schools)
        gidilecek_okullar_pencere(frame_schools_to_visit)
    ekle_button = tk.Button(rapor, text="KONTROL PLANLA", command=sil_ve_guncelle,background='#073456', foreground='white', font=('Arial', 12)).place(x=515,y=620)
    rapor.grid_rowconfigure(1, weight=1)
 
 
def gidilecek_sil(tree):
            secilen_okul = tree.selection()
            if len(secilen_okul) == 0:  
                messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz öğeyi seçin.")
                return

            secilen_okul = secilen_okul[0]  
            values = tree.item(secilen_okul, "values")
            gorev_id = values[0]
            response = messagebox.askyesno("Onay", "Seçili Okulu Periyodik Kontrol Programından Kaldırmak istediğinize emin misiniz?")
            if response:
                try:
                    conn = sql_baglanti()
                    cursor = conn.cursor()
                    sql = "DELETE FROM gidilecek_okullar WHERE gidilecek_id = %s"
                    cursor.execute(sql, (gorev_id,))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    tree.delete(secilen_okul)
                    messagebox.showinfo("Başarılı", "Seçilen Okul Periyodik Kontrol Programından Başarıyla Kaldırıldı.")
                except mysql.connector.Error as err:
                    messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
            else:
                messagebox.showinfo("İptal", "Periyodik Kontrol Programından kaldırma işlemi iptal edildi.")
def gidilecek_okul_duzenle(tree):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")
    gidilecek_id = values[0]
    okul_id = values[1]
    okul_adi = values[4]


    ilce=values[3]

    ziyaret_tarihi=values[2]

    ziyaret_duzenleme_penceresi = tk.Toplevel(root,background="white")
    ziyaret_duzenleme_penceresi.title("Tarihi Düzenle")
    ziyaret_duzenleme_penceresi.geometry("300x80")

    tk.Label(ziyaret_duzenleme_penceresi, text="Kontrol Tarihi:",background='white', foreground='black', font=('Arial', 12)).grid(row=0, column=0)
    ziyaret_tarihi_entry = tk.Entry(ziyaret_duzenleme_penceresi,background='white', foreground='black', font=('Arial', 12))
    ziyaret_tarihi_entry.insert(0, ziyaret_tarihi)
    ziyaret_tarihi_entry.grid(row=0, column=1)


    def okul_duzenle_veritabanina():
        yeni_tarih_ad = ziyaret_tarihi_entry.get()

        if not ziyaret_tarihi:
            messagebox.showwarning("Uyarı", "Okul adı giriniz.")
            return

        try:
            conn = sql_baglanti()
            cursor = conn.cursor()
            sql = "UPDATE gidilecek_okullar SET ziyaret_tarihi=%s WHERE gidilecek_id=%s"
            val = (datetime.datetime.strptime(yeni_tarih_ad, "%Y-%m-%d"), gidilecek_id,)
            cursor.execute(sql, val)
            # sql1="UPDATE gorev_tablo SET planlanan_ziyaret_tarihi=%s WHERE gidilecek_id=%s"
            # val1=(datetime.datetime.strptime(yeni_tarih_ad, "%Y-%m-%d"),gidilecek_id,)
            #cursor.execute(sql1,val1)
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Başarılı", "Ziyaret başarıyla güncellendi.")
            ziyaret_duzenleme_penceresi.destroy()
            okul_guncelle(tree)
        except mysql.connector.Error as err:
            messagebox.showerror("Hata", f"Bir hata oluştu: {err}")
    def ekle_ve_guncelle():
        # Ekle butonunun eski fonksiyonu
        okul_duzenle_veritabanina()
    
    # UI güncellemesi
        okul_goster(frame_all_schools)
        gidilen_okul_goster(frame_visited_schools)
        gidilecek_okullar_pencere(frame_schools_to_visit)

    tk.Button(ziyaret_duzenleme_penceresi, text="Güncelle", command=ekle_ve_guncelle,background='#073456', foreground='white', font=('Arial', 12)).grid(row=1, column=0, columnspan=2)

def gidilecek_okullar_pencere(frame):
    # Görünmesi gereken sütunlar
    columns = ("TARİH", "İLÇE", "OKUL/KURUM ADI")
    tree = ttk.Treeview(frame, columns=("Görev ID", "Okul ID") + columns, show="headings")
# Product By...
# ALİ VOLKAN ÇINAR
# KERİM CAN GÜRLER
# CAN BALAMİR
    # Gizli sütunlar
    tree.column("Görev ID", width=0, stretch=tk.NO)  # Görev ID gizli
    tree.column("Okul ID", width=0, stretch=tk.NO)   # Okul ID gizli

    tree.grid(row=0, column=0, padx=0, pady=10, sticky="nse")

    for col in columns:
        tree.heading(col, text=col)
       
        if col == "TARİH":
            tree.column(col, width=150, anchor="nw")

        elif col == "İLÇE":
            tree.column(col, width=200, anchor="nw")
        else:
            tree.column(col, width=500, anchor="nw")
    frame.grid_columnconfigure(0, weight=1)  # Sol boşluk
    frame.grid_columnconfigure(1, weight=0)  # Treeview için
    frame.grid_columnconfigure(2, weight=1)  # Sağ boşluk

    # Yanlardaki boşlukları minimize et
    frame.grid_columnconfigure(0, weight=2)  # Sol boşluk
    frame.grid_columnconfigure(2, weight=2)  # Sağ boşluk

    frame.grid_rowconfigure(0, weight=1)
    try:
        conn = sql_baglanti()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gidilecek_okullar")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Hata", f"Bir hata oluştu: {err}")

    def ziyareti_tamamla():
        secilen_okul = tree.selection()[0]
        values = tree.item(secilen_okul, "values")
        gorev_id = tree.set(secilen_okul, "#1")  # Gizli Görev ID sütunu
        okul_id = tree.set(secilen_okul, "#2")   # Gizli Okul ID sütunu
        
        okul_adi = values[4]
    
        ilce = values[3]
      

        def ayir_girisi(event):
            text = ziyaret_tarihi_entry.get()
            if len(text) == 2 or len(text) == 5: 
                ziyaret_tarihi_entry.insert(tk.END, '/')
          
        def ekle_ziyaret():
            ziyaret_tarihi = ziyaret_tarihi_entry.get()


            if not ziyaret_tarihi :
                messagebox.showwarning("Uyarı", "Ziyaret tarihi giriniz.")
                return

            try:
                ziyaret_tarihi_date = datetime.datetime.strptime(ziyaret_tarihi, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Hata", "Kontrol tarihi yanlış formatında. Lütfen 'gün/ay/yıl' formatında giriniz.")
                return

            try:
                conn = sql_baglanti()
                cursor = conn.cursor()

                sql3 = "INSERT INTO gidilen_okullar (gidilecek_id, okul_id, ziyaret_tarihi,ilce,okul_adi) VALUES (%s, %s, %s, %s, %s)"
                val3 = (gorev_id, okul_id,ziyaret_tarihi_date.strftime("%Y-%m-%d"),ilce,okul_adi)
                cursor.execute(sql3, val3)

                sql_delete = "DELETE FROM gidilecek_okullar WHERE gidilecek_id = %s"
                val_delete = (gorev_id,)
                cursor.execute(sql_delete, val_delete)

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Başarılı", "Rapor başarıyla kaydedildi.")
                ziyaret_penceresi.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Hata", f"Bir hata oluştu: {err}")

        ziyaret_penceresi = tk.Toplevel(root, background="white")
        ziyaret_penceresi.title("Kontrol Bilgileri")
        ziyaret_penceresi.geometry("400x100")
        tk.Label(ziyaret_penceresi, text="Kontrol Tarihi (gün/ay/yıl):", background='white', foreground='black', font=('Arial', 12)).grid(row=0, column=0)
        
        ziyaret_tarihi_entry = tk.Entry(ziyaret_penceresi, background='white', foreground='black', font=('Arial', 12))
        ziyaret_tarihi_entry.bind('<KeyRelease>', ayir_girisi)
        ziyaret_tarihi_entry.grid(row=0, column=1)

        def ekle_ve_guncelle():
            ekle_ziyaret()
            okul_goster(frame_all_schools)
            gidilen_okul_goster(frame_visited_schools)
            gidilecek_okullar_pencere(frame_schools_to_visit)

        ekle_button = tk.Button(ziyaret_penceresi, text="Kontrolü Tamamla", command=ekle_ve_guncelle, background='#073456', foreground='white', font=('Arial', 12))
        ekle_button.place(x=100, y=40)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=1, column=0)
    button_frame.columnconfigure((0, 1, 2, 3), weight=1)

    tk.Button(frame, text="Kontrolü Tamamla", command=ziyareti_tamamla, background='#073456', foreground='white', font=('Arial', 12)).place(x=400, y=620)
    tk.Button(frame, text="Tarihi Düzenle", command=lambda: gidilecek_okul_duzenle(tree), background='#073456', foreground='white', font=('Arial', 12)).place(x=570, y=620)
    tk.Button(frame, text="Kontrolü Kaldır", command=lambda: gidilecek_sil(tree), background='#073456', foreground='white', font=('Arial', 12)).place(x=710, y=620)
    frame.grid_rowconfigure(1, weight=1)

root = tk.Tk()
root.title("OKUL KONTROL PROGRAMI")

root.configure(bg="#D3D3D3")  # Pencerenin arka plan rengini beyaz yap

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10,sticky="n" )
# notebook.pack( )

# Frame oluştur
frame_all_schools = tk.Frame(notebook, bg='#D3D3D3')
frame_visited_schools = tk.Frame(notebook, bg='#D3D3D3')
frame_schools_to_visit = tk.Frame(notebook, bg='#D3D3D3')

# Frame'leri Notebook'a ekle
notebook.add(frame_all_schools, text="OKULLAR")
notebook.add(frame_schools_to_visit, text="PERİYODİK KONTROL PROGRAMI")
notebook.add(frame_visited_schools, text="RAPORU YAZILAN OKULLAR")

okul_goster(frame_all_schools)
gidilen_okul_goster(frame_visited_schools)
gidilecek_okullar_pencere(frame_schools_to_visit)

root.mainloop()

# Product By...
# ALİ VOLKAN ÇINAR
# KERİM CAN GÜRLER
# CAN BALAMİR