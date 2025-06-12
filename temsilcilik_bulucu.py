#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Türkiye Temsilcilik Bulucu - Modern GUI
Basit ve modern arayüzlü Python programı
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import re
from typing import List, Optional, Tuple, Any
import threading


class ModernKonsoloslukBulucu:
    def __init__(self):
        """Modern Konsolosluk Bulucu GUI"""
        self.konsolosluklar = []
        self.ulkeler = []
        
        # Ana pencere
        self.root = tk.Tk()
        self.root.title("🇹🇷 Türkiye Temsilcilik Bulucu")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Modern renkler
        self.colors = {
            'primary': '#2E86AB',      # Ana mavi
            'secondary': '#A23B72',    # Mor
            'success': '#F18F01',      # Turuncu
            'background': '#F5F7FA',   # Açık gri
            'white': '#FFFFFF',
            'text': '#2C3E50',         # Koyu gri
            'light_gray': '#ECF0F1'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.load_data()
    
    def setup_styles(self):
        """Modern stil ayarları"""
        self.root.configure(bg=self.colors['background'])
        
        # TTK stilleri
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button stili
        style.configure('Modern.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['secondary'])])
        
        # Entry stili
        style.configure('Modern.TEntry',
                       borderwidth=1,
                       relief='solid',
                       padding=10)
        
        # Combobox stili
        style.configure('Modern.TCombobox',
                       borderwidth=1,
                       relief='solid',
                       padding=10)
    
    def create_widgets(self):
        """Modern arayüz bileşenlerini oluştur"""
        # Ana frame
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Başlık
        title_frame = tk.Frame(main_frame, bg=self.colors['background'])
        title_frame.pack(fill='x', pady=(0, 30))
        
        title_label = tk.Label(title_frame,
                              text="🇹🇷 Türkiye Temsilcilik Bulucu",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['background'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Posta koduna göre sorumlu konsolosluk bulun",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text'],
                                 bg=self.colors['background'])
        subtitle_label.pack(pady=(5, 0))
        
        # Arama kartı
        search_card = tk.Frame(main_frame, bg=self.colors['white'], relief='solid', bd=1)
        search_card.pack(fill='x', pady=(0, 20))
        
        # Kart içeriği
        card_content = tk.Frame(search_card, bg=self.colors['white'])
        card_content.pack(fill='x', padx=30, pady=30)
        
        # Posta kodu girişi
        tk.Label(card_content,
                text="📮 Posta Kodu:",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w')
        
        self.posta_kodu_var = tk.StringVar()
        self.posta_kodu_entry = ttk.Entry(card_content,
                                         textvariable=self.posta_kodu_var,
                                         style='Modern.TEntry',
                                         font=('Segoe UI', 11))
        self.posta_kodu_entry.pack(fill='x', pady=(5, 15))
        self.posta_kodu_entry.bind('<Return>', lambda e: self.ara())

        # Placeholder text efekti
        self.posta_kodu_entry.insert(0, "Örn: 10001")
        self.posta_kodu_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.posta_kodu_entry.bind('<FocusOut>', self.on_entry_focus_out)
        
        # Ülke seçimi
        tk.Label(card_content,
                text="🌍 Ülke (İsteğe bağlı):",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w')
        
        self.ulke_var = tk.StringVar()
        self.ulke_combo = ttk.Combobox(card_content,
                                      textvariable=self.ulke_var,
                                      style='Modern.TCombobox',
                                      font=('Segoe UI', 11),
                                      state='readonly')
        self.ulke_combo.pack(fill='x', pady=(5, 20))
        
        # Arama butonu
        self.ara_button = ttk.Button(card_content,
                                    text="🔍 Ara",
                                    style='Modern.TButton',
                                    command=self.ara,
                                    state='disabled')
        self.ara_button.pack(pady=10)
        
        # Sonuç alanı
        result_frame = tk.Frame(main_frame, bg=self.colors['background'])
        result_frame.pack(fill='both', expand=True)
        
        # Sonuç başlığı
        self.result_label = tk.Label(result_frame,
                                    text="",
                                    font=('Segoe UI', 14, 'bold'),
                                    fg=self.colors['text'],
                                    bg=self.colors['background'])
        self.result_label.pack(anchor='w', pady=(0, 10))
        
        # Sonuç metni
        self.result_text = scrolledtext.ScrolledText(result_frame,
                                                    font=('Segoe UI', 10),
                                                    bg=self.colors['white'],
                                                    fg=self.colors['text'],
                                                    relief='solid',
                                                    bd=1,
                                                    wrap='word')
        self.result_text.pack(fill='both', expand=True)
        
        # Durum çubuğu
        status_frame = tk.Frame(main_frame, bg=self.colors['light_gray'], height=30)
        status_frame.pack(fill='x', pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                    text="Program başlatılıyor...",
                                    font=('Segoe UI', 9),
                                    fg=self.colors['text'],
                                    bg=self.colors['light_gray'])
        self.status_label.pack(side='left', padx=10, pady=5)
    
    def load_data(self):
        """Verileri arka planda yükle"""
        def load_thread():
            try:
                self.status_label.config(text="Veriler yükleniyor...")
                
                with open("konsolosluk_verileri.json", "r", encoding="utf-8") as f:
                    veriler = json.load(f)
                
                ulke_set = set()
                for veri in veriler:
                    konsolosluk = {
                        'temsilcilik': veri.get("Temsilcilik", ""),
                        'ulke': veri.get("Ülke", ""),
                        'eyalet': veri.get("Görev bölgesindeki Eyalet/Kanton", ""),
                        'sehir': veri.get("Görev bölgesindeki Şehir/Semt", ""),
                        'posta_kodu': veri.get("PostaKodu", "")
                    }
                    self.konsolosluklar.append(konsolosluk)

                    # Ülke bilgisi varsa ve boş değilse ekle
                    if konsolosluk['ulke'] and konsolosluk['ulke'].strip():
                        ulke_set.add(konsolosluk['ulke'].title())
                
                self.ulkeler = ['Tüm Ülkeler'] + sorted(list(ulke_set))
                
                # UI güncelleme
                self.root.after(0, self.update_ui_after_load)
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Veri yükleme hatası: {e}"))
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def update_ui_after_load(self):
        """Veri yüklendikten sonra UI'yi güncelle"""
        self.ulke_combo['values'] = self.ulkeler
        self.ulke_combo.set('Tüm Ülkeler')
        self.status_label.config(text=f"✅ {len(self.konsolosluklar):,} konsolosluk kaydı yüklendi")
        self.ara_button.config(state='normal')
    
    def show_error(self, message):
        """Hata mesajı göster"""
        messagebox.showerror("Hata", message)
        self.status_label.config(text="❌ Hata oluştu")

    def on_entry_focus_in(self, event):
        """Entry'ye odaklanıldığında placeholder'ı temizle"""
        if self.posta_kodu_var.get() == "Örn: 10001":
            self.posta_kodu_var.set("")

    def on_entry_focus_out(self, event):
        """Entry'den çıkıldığında boşsa placeholder'ı geri koy"""
        if not self.posta_kodu_var.get().strip():
            self.posta_kodu_var.set("Örn: 10001")
    
    def posta_kodu_ayristir(self, posta_kodu_araligi: Any) -> List[Tuple[int, int]]:
        """Posta kodu aralığını ayrıştır"""
        araliklar = []
        
        if isinstance(posta_kodu_araligi, int):
            araliklar.append((posta_kodu_araligi, posta_kodu_araligi))
            return araliklar
        
        if not posta_kodu_araligi or not isinstance(posta_kodu_araligi, str):
            return araliklar
        
        for aralik in posta_kodu_araligi.split(','):
            aralik = aralik.strip()
            match = re.match(r'(\d+)\s*-\s*(\d+)', aralik)
            if match:
                baslangic = int(match.group(1))
                bitis = int(match.group(2))
                araliklar.append((baslangic, bitis))
            else:
                try:
                    tek_kod = int(aralik)
                    araliklar.append((tek_kod, tek_kod))
                except ValueError:
                    pass
        
        return araliklar
    
    def ara(self):
        """Arama işlemini gerçekleştir"""
        posta_kodu_str = self.posta_kodu_var.get().strip()

        # Placeholder kontrolü
        if not posta_kodu_str or posta_kodu_str == "Örn: 10001":
            messagebox.showwarning("Uyarı", "Lütfen bir posta kodu girin!")
            return
        
        try:
            posta_kodu = int(posta_kodu_str)
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçersiz posta kodu! Sadece sayı girin.")
            return
        
        # Ülke filtresi
        secili_ulke = self.ulke_var.get()
        ulke_filtresi = None if secili_ulke == 'Tüm Ülkeler' else secili_ulke.lower()
        
        # Arama yap
        sonuclar = []
        for konsolosluk in self.konsolosluklar:
            # Ülke filtresi kontrolü - None kontrolü eklendi
            if ulke_filtresi and (not konsolosluk['ulke'] or konsolosluk['ulke'].lower() != ulke_filtresi):
                continue

            araliklar = self.posta_kodu_ayristir(konsolosluk['posta_kodu'])
            for baslangic, bitis in araliklar:
                if baslangic <= posta_kodu <= bitis:
                    sonuclar.append(konsolosluk)
                    break
        
        # Sonuçları göster
        self.sonuclari_goster(sonuclar, posta_kodu, secili_ulke)
    
    def sonuclari_goster(self, sonuclar: List[dict], posta_kodu: int, ulke: str):
        """Sonuçları göster"""
        self.result_text.delete(1.0, tk.END)
        
        if sonuclar:
            ulke_metni = f" ({ulke})" if ulke != 'Tüm Ülkeler' else ""
            self.result_label.config(text=f"✅ {len(sonuclar)} sonuç bulundu", fg=self.colors['success'])
            
            for i, konsolosluk in enumerate(sonuclar, 1):
                # Güvenli string işleme
                ulke_adi = konsolosluk['ulke'].title() if konsolosluk['ulke'] else 'Belirtilmemiş'

                result = f"""
{'='*60}
📍 {i}. SONUÇ
{'='*60}
🏛️  Temsilcilik: {konsolosluk['temsilcilik']}
🌍  Ülke: {ulke_adi}
📍  Eyalet/Bölge: {konsolosluk['eyalet'] or 'Belirtilmemiş'}
🏙️  Şehir: {konsolosluk['sehir'] or 'Belirtilmemiş'}
📮  Posta Kodu: {konsolosluk['posta_kodu']}

"""
                self.result_text.insert(tk.END, result)
        else:
            ulke_metni = f" {ulke} ülkesinde" if ulke != 'Tüm Ülkeler' else ""
            self.result_label.config(text="❌ Sonuç bulunamadı", fg='red')
            self.result_text.insert(tk.END, f"{posta_kodu} posta kodu için{ulke_metni} sorumlu konsolosluk bulunamadı.")
        
        self.status_label.config(text=f"Arama tamamlandı - {len(sonuclar)} sonuç")
    
    def run(self):
        """Programı çalıştır"""
        self.root.mainloop()


def main():
    """Ana program"""
    try:
        app = ModernKonsoloslukBulucu()
        app.run()
    except Exception as e:
        messagebox.showerror("Kritik Hata", f"Program başlatılamadı: {e}")


if __name__ == "__main__":
    main()
