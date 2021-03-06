# Letzte Aenderungen vom: 14.08.2020 - 08:50
###########################################################
# JPEG-Converter von Tom Levin Schwenzle
# Konvertiert Bilddateien in JPEG2000(OpenJPEG) oder regulaeres JPEG(LibJPEG)
# Mit abgestufter Kompression

# Programmiert als Teil der Hausarbeit fuer die Vorlesung
# Postproduction an der Hochschule der Medien Stuttgart

# Folgender Code um .EXE zu generieren:
# pyinstaller  --icon=icon.ico --noconsole  --onefile --name "JPEGConverter" jpegconverterMAIN.py 
# 
# 
# Fuer Bearbeitung und ggf. Ausfuehrung werden folgende Programme und Librarys benoetigt:
# Python 3, Tkinter, Pillow, OpenJPEG, libjpeg

###########################################################

import PIL.Image  # Importiert PIL Package
from PIL import *
# Tkinter für UI
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter.ttk import Progressbar
from tkinter import messagebox
# OS und Systemfiles fuer Datenzugriff
import os
from pathlib import Path
import tempfile
# Project Daten:
import jpegconverterCONVERTER as converter



###########################################################

# Globale Variablen Initialisieren
filePath = ""
outputPath = ""
imageLoaded = False
outputSelected = False

# GUI Initialisierung:
window = Tk()
window.title("Image Converter: J2K & JPG")


# GUI Styling
color1 = "#f2f2f2"
color2 = "#262626"
color3 = "#737373"

window.configure(background=color2)
window.resizable(False, False)
window.option_add("*Label.Font", "helvetica 11")
window.option_add("*Button.Font", "helvetica 11")
window.option_add("*Button.Foreground", color1)
window.option_add("*Button.Background", color2)
window.option_add("*Text.Font", "helvetica 9")
window.option_add("*Text.Background", color3)
window.option_add("*Text.Foreground", color1)
window.option_add("*Label.Background", color2)
window.option_add("*Label.Foreground", color1)
window.option_add("*Frame.Background", color2)
window.option_add("*Frame.Foreground", color1)
window.option_add("*Entry.Font", "helvetica 11")
window.option_add("*Entry.Background", color1)
window.option_add("*Entry.Foreground", color2)
window.option_add("*Checkbutton.Background", color1)
window.option_add("*Checkbutton.Foreground", color2)
window.option_add("*Checkbutton.Font", "helvetica 11")
window.option_add("*Checkbutton.Background", color2)
window.option_add("*Checkbutton.Foreground", color1)
window.option_add("*Spinbox.Font", "helvetica 11")
window.option_add("*Spinbox.Background", color2)
window.option_add("*Spinbox.Foreground", color1)
window.option_add("*Progressbar.Background", color3)
window.option_add("*Progressbar.Foreground", color3)

# Ende GUI Initialsierung

###########################################################
# --------------- GUI INHALTE
###########################################################

# --------------- TOP FRAME

frameTopFrame = Frame(window)
frameTopFrame.grid(column=0, row=1, pady=10, padx=10)

###########################################################

# --------------- SOURCE FILE


def btnSourceFileClicked():
    file = filedialog.askopenfilename(filetypes=[("Image: TGA", "*.tga")])
    possibleFileExtensions = [".tga"]
    if any(x in Path(file).suffix for x in possibleFileExtensions):
        global filePath
        filePath = str(file)
        txtChosenFile.configure(state=NORMAL)
        txtChosenFile.delete(1.0, END)
        txtChosenFile.insert(INSERT, (filePath))
        txtChosenFile.configure(state=DISABLED)
        txtPrefix.configure(state=NORMAL)
        txtPrefix.delete(0, END)
        txtPrefix.insert(INSERT, (Path(filePath).stem + "_"))
        global imageLoaded
        imageLoaded = True

    else:
        messagebox.showinfo(
            'Error', 'Fehler beim Laden des Bildes. Prüfe die Bilddatei.')


# Label fuer Quelldatei
lblSourceFile = Label(frameTopFrame, text="Quelldatei:")
lblSourceFile.grid(column=0, row=0, sticky=E, padx=8)

# Kontrollfeld fuer Quelldatei
txtChosenFile = Text(frameTopFrame, height=3, width=35)
txtChosenFile.insert(INSERT, "Noch keine Datei ausgewählt.")
txtChosenFile.grid(column=1, row=0, rowspan=2, pady=5)
txtChosenFile.configure(state=DISABLED)

# Button fuer Quelldatei
btnSourceFile = Button(frameTopFrame, text="Quelle",
                       command=btnSourceFileClicked, width=10)
btnSourceFile.grid(column=2, row=0, sticky=W, padx=8)

#####################################################

# --------------- OUTPUT DIRECTORY


def btnOutputFolderClicked():
    outputDirectory = filedialog.askdirectory(
        initialdir=os.path.dirname(__file__))
    if outputDirectory != "":
        global outputPath
        outputPath = str(outputDirectory)
        txtOutputFolder.configure(state=NORMAL)
        txtOutputFolder.delete(1.0, END)
        txtOutputFolder.insert(INSERT, (outputPath))
        txtOutputFolder.configure(state=DISABLED)
        global outputSelected
        outputSelected = True
    else:
        messagebox.showinfo(
            'Error', 'Fehler beim Auswählen des Zielverzeichnis. Prüfe die Auswahl.')


# Label fuer Output Ordner
lblOutputFolder = Label(frameTopFrame, text="Zielverzeichnis:")
lblOutputFolder.grid(column=0, row=2, sticky=E, padx=8)
# Kontrollfeld fuer Output Ordner
txtOutputFolder = Text(frameTopFrame, height=3, width=35)
txtOutputFolder.insert(INSERT, "Noch kein Ziel ausgewählt.")
txtOutputFolder.grid(column=1, row=2, rowspan=2, pady=5)
txtOutputFolder.configure(state=DISABLED)
# Button fuer Output Ordner
btnOutputFolder = Button(frameTopFrame, text="Ziel",
                         command=btnOutputFolderClicked, width=10)
btnOutputFolder.grid(column=2, row=2, sticky=W, padx=8)

#####################################################

# --------------- PREFIX

# Label fuer Prefix
lblPrefix = Label(frameTopFrame, text="Prefix:")
lblPrefix.grid(column=0, row=4, sticky=E, padx=8, pady=5)
# Set Prefix
txtPrefix = Entry(frameTopFrame, width=35)
txtPrefix.insert(INSERT, "Prefix_")
txtPrefix.grid(column=1, row=4, pady=5)
txtPrefix.configure(state=DISABLED)

#####################################################

# --------------- TASK CHECKER
frameChecker = Frame(window)
frameChecker.grid(column=0, row=2)

# JPEG2000 Checker
chkShouldJ2k_state = BooleanVar()
chkShouldJ2k_state.set(True)
chkShouldJ2k = Checkbutton(
    frameChecker, text="Konvertieren in .J2K (JPEG2000)", var=chkShouldJ2k_state)
chkShouldJ2k.grid(column=0, row=0)

# JPEG Checker
shouldJPEG = False
chkShouldJPEG_state = BooleanVar()
chkShouldJPEG_state.set(True)
chkShoulJPEG = Checkbutton(
    frameChecker, text="Konvertieren in .JPG", var=chkShouldJPEG_state)
chkShoulJPEG.grid(column=0, row=1)

#####################################################

# --------------- COMPRESSION

frameCompressions = Frame(window)
frameCompressions.grid(column=0, row=3, pady=15)

# Anzahl an Compressions Spinbox
lblCompAmount = Label(frameCompressions, text="Anzahl an Kompressionen:")
lblCompAmount.grid(column=0, row=0)
compAmount = IntVar()
compAmount.set(6)
spinCompAmount = Spinbox(frameCompressions, from_=1,
                         to=6, width=3, textvariable=compAmount)
spinCompAmount.grid(column=1, row=0)

#####################################################

# --------------- PROGRESS BAR

frameProgress = Frame(window)
frameProgress.grid(column=0, row=4)
# Progress Bar
varProgress = IntVar()
varProgressLabel = StringVar()
varProgressLabel.set("Status: Wartet")
bar = Progressbar(frameProgress, length=200, variable=varProgress)
bar.grid(column=0, row=0)
lblProgress = Label(frameProgress, textvariable=varProgressLabel)
lblProgress.grid(column=1, row=0)

#####################################################

# --------------- START CONVERSION


def btnRunConversionClicked():
    
    if imageLoaded == False:
        messagebox.showinfo(
            'Error', 'Quelldatei muss ausgewählt werden.')
    elif outputSelected == False:
        messagebox.showinfo(
            'Error', 'Zielverzeichnis muss ausgewählt werden.')
    else:
        prefix = txtPrefix.get()
        varProgress.set(50)
        varProgressLabel.set("Status: Läuft...")
        window.update()

        #Folgende Funktion startet Umwandlungen/ Kompression – Folgende Parameter werden verwendet
            #Boolean – Ob J2K Dateien generiert werden sollen
            #Boolean – Ob JPG Dateien generiert werden sollen
            #String – Pfad zum Quellbild
            #String – Zielverzeichnis
            #Integer – Anzahl der Kompressionsstufen
            #String – Prefix fuer neue Dateien
        converter.runConversion(chkShouldJ2k_state.get(),chkShouldJPEG_state.get(),
            filePath, outputPath, compAmount.get(), prefix)

        varProgress.set(100)
        varProgressLabel.set("Status: Fertig!")
        messagebox.showinfo('Status', 'Konvertierung und Kompression erfolgreich!')


btnRunConversion = Button(window, width=10, text="Start",
                          command=btnRunConversionClicked).grid(padx=15, pady=15)

#####################################################

# --------------- COPYRIGHT

lblFooter1 = Label(window, font="helvetica 8", text="Realisiert mit: Python, Pillow, OpenJPEG, libjpeg & Tkinter")
lblFooter2 = Label(window, font="helvetica 8", text="(C) 2020: TLS - TS171")
lblFooter3 = Label(window, font="helvetica 8",
                   text="Postproduction | Sommer 2020 | HdM Stuttgart")

lblFooter1.grid()
lblFooter2.grid()
lblFooter3.grid()

#####################################################

#####################################################
# -------------- ENDE - GUI INHALTE
#####################################################

# Fuehrt Interface aus
window.mainloop()
