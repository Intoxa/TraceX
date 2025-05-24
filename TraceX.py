import tkinter as tk
from tkinter import messagebox
import requests

# Couleurs et styles
BG_COLOR = "#121417"
FG_COLOR = "#E0E6ED"
ACCENT_COLOR = "#00B8D9"
ENTRY_BG = "#1E2128"
BTN_BG = ACCENT_COLOR
BTN_FG = "#FFFFFF"
TEXT_BG = "#1E2128"

def geolocate_ip():
    ip = entry_ip.get().strip()
    if not ip:
        messagebox.showerror("Erreur", "Veuillez entrer une adresse IP.")
        return
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        if 'bogon' in data:
            messagebox.showerror("Erreur", "Adresse IP invalide ou privée.")
            return

        result_text = (
            f"🌐 IP : {data.get('ip')}\n"
            f"🏙️ Ville : {data.get('city')}\n"
            f"📍 Région : {data.get('region')}\n"
            f"🌍 Pays : {data.get('country')}\n"
            f"📡 Coordonnées : {data.get('loc')}\n"
            f"🛰️ Fournisseur : {data.get('org')}\n"
            f"⏰ Fuseau horaire : {data.get('timezone')}\n"
            f"🛑 Attention ! Toute les informations qui on était données sont approximatives !\n"
        )
        text_result.config(state='normal')
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, result_text)
        text_result.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de récupérer les données : {e}")

def create_logo(canvas, width, height):
    margin = 20
    canvas.create_line(margin, margin, width - margin, height - margin, fill=ACCENT_COLOR, width=6)
    canvas.create_line(width - margin, margin, margin, height - margin, fill=ACCENT_COLOR, width=6)
    r = 8
    points = [(margin, margin), (width - margin, margin), (margin, height - margin), (width - margin, height - margin)]
    for (x, y) in points:
        canvas.create_oval(x - r, y - r, x + r, y + r, outline=ACCENT_COLOR, width=3)

def show_splash(root, splash_frame, main_frame):
    splash_frame.pack(fill="both", expand=True)
    root.after(3000, lambda: (splash_frame.pack_forget(), main_frame.pack(fill="both", expand=True)))

def main():
    global entry_ip, text_result

    root = tk.Tk()
    root.title("TraceX - IP Geolocation")
    root.geometry("520x420")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    # Splash Frame
    splash_frame = tk.Frame(root, bg=BG_COLOR)
    canvas = tk.Canvas(splash_frame, width=150, height=150, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(pady=30)
    create_logo(canvas, 150, 150)
    label = tk.Label(splash_frame, text="TraceX", font=("Segoe UI", 36, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
    label.pack()
    sub = tk.Label(splash_frame, text="IP Geolocation Tool", font=("Segoe UI", 14), fg=FG_COLOR, bg=BG_COLOR)
    sub.pack(pady=(5, 20))

    # Main Frame (caché au départ)
    main_frame = tk.Frame(root, bg=BG_COLOR)

    title = tk.Label(main_frame, text="TraceX", font=("Segoe UI", 28, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
    title.pack(pady=(15, 5))

    subtitle = tk.Label(main_frame, text="Entre une adresse IP pour en obtenir la géolocalisation",
                        font=("Segoe UI", 11), bg=BG_COLOR, fg=FG_COLOR)
    subtitle.pack(pady=(0, 20))

    frame_input = tk.Frame(main_frame, bg=BG_COLOR)
    frame_input.pack(padx=20, fill='x')

    entry_ip = tk.Entry(frame_input, bg=ENTRY_BG, fg=FG_COLOR, font=("Segoe UI", 14),
                        insertbackground=ACCENT_COLOR, relief="flat")
    entry_ip.pack(side="left", fill="x", expand=True, ipady=8)

    btn_search = tk.Button(frame_input, text="Chercher", bg=BTN_BG, fg=BTN_FG,
                           font=("Segoe UI", 14, "bold"), relief="flat",
                           activebackground="#0099b3", command=geolocate_ip)
    btn_search.pack(side="left", padx=(10, 0), ipady=6, ipadx=10)

    frame_result = tk.Frame(main_frame, bg=BG_COLOR)
    frame_result.pack(padx=20, pady=20, fill='both', expand=True)

    scrollbar = tk.Scrollbar(frame_result)
    scrollbar.pack(side="right", fill="y")

    text_result = tk.Text(frame_result, bg=TEXT_BG, fg=FG_COLOR, font=("Segoe UI", 12),
                          wrap="word", yscrollcommand=scrollbar.set, relief="flat", state="disabled")
    text_result.pack(fill="both", expand=True)

    scrollbar.config(command=text_result.yview)

    # Affiche splash puis main
    show_splash(root, splash_frame, main_frame)

    root.mainloop()

if __name__ == "__main__":
    main()
