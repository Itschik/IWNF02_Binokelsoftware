from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os

# ImageViewer-Komponente
class ImageViewer(Frame):
    def __init__(self, parent, image_folder, width=180, height=180, delay=2000, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.image_folder = image_folder
        self.width = width
        self.height = height
        self.delay = delay
        self.image_index = 0
        
        self.image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        self.label = Label(self, width=width, height=height)
        self.label.pack(expand=True)
        
        self.show_image()
    
    def show_image(self):
        image_path = os.path.join(self.image_folder, self.image_files[self.image_index])
        image = Image.open(image_path)
        image = image.resize((self.width, self.height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        
        self.label.config(image=self.photo)
        
        self.image_index = (self.image_index + 1) % len(self.image_files)
        
        self.after(self.delay, self.show_image)

root = Tk()
root.title("Binokelsoftware - Willkommensseite")
root.iconbitmap("C:/Users/robin/Desktop/Python_GUI/Binokelicon.ico")
root.state("zoomed")  # Fenster im Maximierten Modus starten

# Farben für das Thema
background_color = "#2f2f2f"
frame_color = "#3d3d3d"
text_color = "#ffd700"
button_color = "#8B0000"
disabled_color = "#2f2f2f"  # Grau für deaktiviertes Eingabefeld

# Fensterhintergrundfarbe
root.configure(bg=background_color)

# Layout-Konfiguration für maximiertes Fenster
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(1, weight=1)

# Header-Bereich mit Formatierung
head = LabelFrame(root, text="Willkommensbereich", bg=frame_color, fg=text_color, font=("Helvetica", 14, "bold"))
head.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))
welcomeText = Label(head, text="Willkommen in der Battlemania!", bg=frame_color, fg="white", font=("Helvetica", 20, "bold"))
welcomeText.pack(pady=10)

# Linker Bereich mit Spielereinstellungen und Start-Button
bodyLeft = LabelFrame(root, text="Spielereinstellungen", bg=frame_color, fg=text_color, font=("Helvetica", 16, "bold"))
bodyLeft.grid(row=1, column=0, sticky="nswe", padx=20, pady=(0, 20))

# Erstellen eines neuen Frames für die Eingabefelder
left_frame = Frame(bodyLeft, bg=frame_color)
left_frame.pack(padx=10, pady=10, fill="both", expand=True)

Label(left_frame, text="Anzahl der Spieler am Tisch wählen:", bg=frame_color, fg="white", font=("Helvetica", 15)).pack(pady=15)

button_frame = Frame(left_frame, bg=frame_color)
button_frame.pack(pady=5)

player_count_label = Label(left_frame, text="Noch keine Anzahl der Spieler ausgewählt", bg=frame_color, fg="white", font=("Helvetica", 12))
player_count_label.pack(pady=5)

# Variablen zur Speicherung der Anzahl der Spieler und Eintragsfelder
player_count = None  # Wird auf 3 oder 4 gesetzt

# Funktion zum Ändern des Texts im Label und Aktivieren/Deaktivieren der Eingabefelder
def update_player_count(players):
    global player_count
    player_count = players
    player_count_label.config(text=f"{players} Spieler ausgewählt")
    entry_player4.config(state=NORMAL if players == 4 else DISABLED, disabledbackground=disabled_color)

Button(button_frame, text="3 Spieler", padx=20, pady=10, bg=button_color, fg="white", font=("Helvetica", 14), command=lambda: update_player_count(3)).pack(side=LEFT, padx=10)
Button(button_frame, text="4 Spieler", padx=20, pady=10, bg=button_color, fg="white", font=("Helvetica", 14), command=lambda: update_player_count(4)).pack(side=LEFT, padx=10)

Label(left_frame, text="Namen der Spieler eingeben:", bg=frame_color, fg="white", font=("Helvetica", 15)).pack(pady=15)

# Spielereingabefelder mit Labels
def create_labeled_entry(parent, text):
    frame = Frame(parent, bg=frame_color)
    frame.pack(pady=5)
    Label(frame, text=text, bg=frame_color, fg="white", font=("Helvetica", 15)).pack(side=LEFT, padx=10)
    entry = Entry(frame, font=("Helvetica", 15), width=30)
    entry.pack(side=LEFT, pady=5)
    return entry

entry_player1 = create_labeled_entry(left_frame, "Spieler 1:")
entry_player2 = create_labeled_entry(left_frame, "Spieler 2:")
entry_player3 = create_labeled_entry(left_frame, "Spieler 3:")
entry_player4 = create_labeled_entry(left_frame, "Spieler 4:")
entry_player4.config(state=DISABLED)

# Eingabefeld für Anzahl der Runden
entry_runden = create_labeled_entry(left_frame, "Runden:")

# Funktion zur Überprüfung der Eingaben und Öffnen des modalen Fensters
def validate_inputs():
    if player_count is None:
        messagebox.showwarning("Warnung", "Bitte Anzahl der Spieler auswählen!")
        return
    
    if not validate_rounds_input():
        return

    # Überprüfen der Spielernamen basierend auf der Anzahl der Spieler
    if not entry_player1.get().strip() or not entry_player2.get().strip() or not entry_player3.get().strip():
        messagebox.showwarning("Warnung", "Bitte die Namen aller Spieler eingeben!")
        return
    if player_count == 4 and not entry_player4.get().strip():
        messagebox.showwarning("Warnung", "Bitte Namen für Spieler 4 eingeben!")
        return

    # Spielfenster als modales Fenster öffnen
    open_game_window()

# Validierungsfunktion für das Runden-Eingabefeld
def validate_rounds_input():
    try:
        rounds = int(entry_runden.get().strip())
        if 1 <= rounds <= 100:
            return True
        else:
            messagebox.showwarning("Warnung", "Bitte eine Zahl zwischen 1 und 100 für die Runden eingeben!")
            return False
    except ValueError:
        messagebox.showwarning("Warnung", "Bitte eine gültige Ganzzahl für die Runden eingeben!")
        return False

####################################################################################################################################################################################

def open_game_window():
    # Prüfe die Spieleranzahl und öffne das entsprechende Spielfenster
    if player_count == 3:
        open_three_player_game_window()
    elif player_count == 4:
        open_four_player_game_window()
    else:
        messagebox.showerror("Fehler", "Bitte wählen Sie entweder 3 oder 4 Spieler.")

def validate_input(P):
    """Diese Funktion prüft, ob die Eingabe eine ganze Zahl ist."""
    if P == "":  # Leeres Feld ist erlaubt
        return True
    try:
        int(P)  # Versuchen, die Eingabe in eine ganze Zahl umzuwandeln
        return True
    except ValueError:
        return False  # Wenn die Umwandlung fehlschlägt, ist die Eingabe ungültig


def open_three_player_game_window():
    # Neues modales Spielfenster für 3 Spieler erstellen
    game_window = Toplevel(root)
    game_window.title("Spiel läuft (3 Spieler)")
    game_window.state("zoomed")
    game_window.iconbitmap("C:/Users/robin/Desktop/Python_GUI/Binokelicon.ico")
    game_window.transient(root)
    game_window.grab_set()

    # Farben und Hintergrund
    background_color = "#2f2f2f"
    frame_color = "#3d3d3d"
    text_color = "#ffd700"
    game_window.configure(bg=background_color)

    # Maximale Rundenanzahl aus der Eingabe auf der Willkommensseite
    max_rounds = int(entry_runden.get().strip())
    current_round = 1
    players = [entry_player1.get(), entry_player2.get(), entry_player3.get()]

    # Funktion zur Berechnung des aktuellen Gebers
    def get_current_dealer(round_num):
        return players[(round_num - 1) % 3]

    # Funktion zur Eingabevalidierung (nur Ganzzahlen von 0 bis 2000)
    def validate_integer(P):
        if P == "" or (P.isdigit() and 0 <= int(P) <= 2000):
            return True
        return False

    # Eingabefelder konfigurieren für die Validierung
    validate_cmd = (game_window.register(validate_integer), '%P')

    # Rundenanzeige und Geberanzeige
    round_label = Label(game_window, text=f"Runde: {current_round} von {max_rounds}", bg=frame_color, fg=text_color, font=("Helvetica", 15))
    round_label.pack(pady=10)

    dealer_label = Label(game_window, text=f"Geber: {get_current_dealer(current_round)}", bg=frame_color, fg=text_color, font=("Helvetica", 15))
    dealer_label.pack(pady=10)

    # Eingabefeld für den Reizwert mit Validierung
    Label(game_window, text="Reizwert:", bg=frame_color, fg="white", font=("Helvetica", 15)).pack(pady=5)
    entry_reizwert = Entry(game_window, font=("Helvetica", 15), width=10, validate="key", validatecommand=validate_cmd)
    entry_reizwert.pack(pady=5)

    # Container für Button "Nächste Runde" und Spieler-Frames
    controls_frame = Frame(game_window, bg=frame_color)
    controls_frame.pack(pady=10, fill="x")  # Layout-Container direkt über den Spielern

    # Eingabefelder für Meldung, Punkte und Summe-Anzeige für jeden Spieler
    player_frames = []
    total_scores = [0, 0, 0]  # Speichert die Gesamtsummen für jeden Spieler

    for i, player_name in enumerate(players):
        player_frame = LabelFrame(controls_frame, text=player_name, bg=frame_color, fg=text_color, font=("Helvetica", 14, "bold"))
        player_frame.pack(padx=20, pady=10, fill="x")
        
        # Meldung und Punkte-Eingabe mit Validierung
        Label(player_frame, text="Meldung:", bg=frame_color, fg="white", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_meldung = Entry(player_frame, font=("Helvetica", 12), width=10, validate="key", validatecommand=validate_cmd)
        entry_meldung.grid(row=0, column=1, padx=10, pady=5)
        
        Label(player_frame, text="Punkte:", bg=frame_color, fg="white", font=("Helvetica", 12)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        entry_punkte = Entry(player_frame, font=("Helvetica", 12), width=10, validate="key", validatecommand=validate_cmd)
        entry_punkte.grid(row=0, column=3, padx=10, pady=5)

        # Gesamtsummen-Anzeige für den Spieler
        total_label = Label(player_frame, text=f"Gesamt: 0", bg=frame_color, fg="white", font=("Helvetica", 12))
        total_label.grid(row=0, column=4, padx=10, pady=5)
        
        player_frames.append((entry_meldung, entry_punkte, total_label))

    # Tabelle erstellen (Treeview-Widget) mit Scrollbars
    table_frame = Frame(game_window, bg=frame_color)
    table_frame.pack(pady=20, fill="both", expand=True)

    columns = ("Runde", "Geber", "Reizwert") + tuple(players) + tuple(f"{p} Gesamt" for p in players)
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Tabellen-Header festlegen und Spaltenbreiten anpassen
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100)  # Jede Spalte wird auf eine Standardbreite gesetzt

    # Scrollbars hinzufügen
    scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
    scrollbar_x.pack(side="bottom", fill="x")

    table.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
    table.pack(fill="both", expand=True)

    # Funktion zum Speichern der Eingaben und zur Vorbereitung der nächsten Runde
    def next_round():
        nonlocal current_round
        reizwert = entry_reizwert.get().strip()
        
        # Werte der Spieler sammeln und Gesamtsummen berechnen
        spielerdaten = []
        round_totals = []
        for i, (meldung_entry, punkte_entry, total_label) in enumerate(player_frames):
            meldung = int(meldung_entry.get().strip() or 0)
            punkte = int(punkte_entry.get().strip() or 0)
            round_total = meldung + punkte
            total_scores[i] += round_total  # Gesamtsumme aktualisieren
            
            # Spielerwert und Gesamt für die Tabelle sammeln
            spielerdaten.append(f"M: {meldung}, P: {punkte}")
            round_totals.append(total_scores[i])
            
            # Gesamtsumme im GUI aktualisieren
            total_label.config(text=f"Gesamt: {total_scores[i]}")
        
        # Zeile in die Tabelle hinzufügen
        table.insert("", "end", values=(current_round, get_current_dealer(current_round), reizwert, *spielerdaten, *round_totals))

        # Rundenfortschritt und Anzeige aktualisieren
        current_round += 1
        round_label.config(text=f"Runde: {current_round} von {max_rounds}")
        dealer_label.config(text=f"Geber: {get_current_dealer(current_round)}")
        
        # Felder für neue Eingaben leeren
        entry_reizwert.delete(0, END)
        for meldung_entry, punkte_entry, _ in player_frames:
            meldung_entry.delete(0, END)
            punkte_entry.delete(0, END)
        
        # Spiel beenden, wenn maximale Rundenanzahl erreicht ist
        if current_round > max_rounds:
            messagebox.showinfo("Spiel beendet", "Die maximale Rundenanzahl ist erreicht!")
            game_window.destroy()

    # Button zur Bestätigung und Fortsetzung der nächsten Runde im controls_frame
    Button(controls_frame, text="Nächste Runde", padx=20, pady=10, bg=button_color, fg="white", font=("Helvetica", 14), command=next_round).pack(pady=10)

    # "Abgang"-Button hinzufügen
    def player_exit():
    # Popup mit der Auswahl des abgegangenen Spielers und des Abgangstyps
        exit_player = simpledialog.askstring("Abgang", "Bitte wähle den abgegangenen Spieler (Spieler 1, Spieler 2, Spieler 3):")
    
        if exit_player:
        # Finden des Index des abgegangenen Spielers
            player_index = None
        if exit_player.lower() == players[0].lower():
            player_index = 0
        elif exit_player.lower() == players[1].lower():
            player_index = 1
        elif exit_player.lower() == players[2].lower():
            player_index = 2
        elif player_count == 4 and exit_player.lower() == players[3].lower():
            player_index = 3
        
        if player_index is not None:
            # Abgangs-Typ auswählen (1000er, Bettel oder normaler Abgang)
            exit_type = simpledialog.askstring("Abgangstyp", "Bitte wähle den Abgangstyp:\n1. Bettel\n2. 1000er\n3. Normal")
            
            # Die Meldung und Punkte des abgegangenen Spielers zurücksetzen
            meldung_entry, punkte_entry, total_label = player_frames[player_index]
            meldung_entry.delete(0, END)
            punkte_entry.delete(0, END)
            
            if exit_type == "1":  # Bettel
                # Abzug von 1000 Punkten
                total_scores[player_index] -= 1000
            elif exit_type == "2":  # 1000er
                # Abzug von 1000 Punkten
                total_scores[player_index] -= 1000
            else:  # Normaler Abgang
                # Abzug von doppeltem Reizwert
                reizwert = int(entry_reizwert.get().strip() or 0)
                total_scores[player_index] -= 2 * reizwert
            
            # Gesamtsumme im Label aktualisieren
            total_label.config(text=f"Gesamt: {total_scores[player_index]}")
            
            # 30 extra Punkte den anderen Spielern hinzufügen
            for i, (meldung_entry, punkte_entry, total_label) in enumerate(player_frames):
                if i != player_index:  # Für alle anderen Spieler, die nicht abgegangen sind
                    total_scores[i] += 30  # Füge 30 Punkte hinzu
                    total_label.config(text=f"Gesamt: {total_scores[i]}")



    
    # Abgang-Button oben rechts im Fenster
    Button(game_window, text="Abgang", command=player_exit, padx=10, pady=5, bg="red", fg="white", font=("Helvetica", 14)).place(x=game_window.winfo_width() - 120, y=20)

    game_window.mainloop()



def open_four_player_game_window():
    # Neues modales Spielfenster für 4 Spieler erstellen
    game_window = Toplevel(root)
    game_window.title("Spiel läuft (4 Spieler)")
    game_window.state("zoomed")
    game_window.iconbitmap("C:/Users/robin/Desktop/Python_GUI/Binokelicon.ico")
    game_window.transient(root)
    game_window.grab_set()
    
    background_color = "#2f2f2f"
    frame_color = "#3d3d3d"
    text_color = "#ffd700"
    game_window.configure(bg=background_color)

   


    
####################################################################################################################################################################################

# Button zum Spielstart mit Validierungsfunktion
buttonSpielStart = Button(left_frame, text="Spiel Start!", padx=20, pady=10, bg=button_color, fg="white", font=("Helvetica", 14), command=validate_inputs)
buttonSpielStart.pack(pady=20)

# Rechter Bereich mit ImageViewer
bodyRight = LabelFrame(root, text="Binokel Diashow", bg=frame_color, fg=text_color, font=("Helvetica", 14, "bold"))
bodyRight.grid(row=1, column=1, sticky="nswe", padx=20, pady=(0, 20))

# ImageViewer-Komponente einfügen
image_folder = "C:/Users/robin/Desktop/Python_GUI/Bilder_ImageViewer"
image_viewer = ImageViewer(bodyRight, image_folder=image_folder, width=600, height=400, delay=2500)
image_viewer.pack(pady=10)

instruction_text = Label(
    bodyRight,
    text="Zum Beginnen des Spiels wähle zuerst die Anzahl der Spieler über die Buttons,\n"
         "gebe anschließend die Namen der Spieler ein und klicke auf Spiel Start!\n"
         "Viel Spaß beim Spielen!",
    bg=frame_color,
    fg="white",
    font=("Helvetica", 15),
    anchor="w",
    justify=LEFT
)
instruction_text.pack(pady=50, anchor="w", padx=100)

root.mainloop()
