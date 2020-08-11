###########################################################
# JPEG-Converter von Tom Levin Schwenzle
# Konvertiert Bilddateien in JPEG2000 oder regulaeres JPEG
# Mit abgestufter Kompression

# Programmiert als Teil der Hausarbeit fuer die Vorlesung:
# Postproduction
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
window.title("Image Converter: JPEG2000 & JPEG-DCT")


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
    file = filedialog.askopenfilename(filetypes=(("Images: TGA, PNG, JPEG, JPG, TIFF", "*"), ("TGA",
                                                                                              "*.tga"), ("PNG", "*.png*"), ("TIFF", "*.tiff*"), ("JPG", "*.jpg*"), ("JPEG", "*.jpeg*")))
    possibleFileExtensions = [".tga", ".jpg", ".jpeg", ".tiff", ".png"]
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
            'Error', 'Error while loading image. Check selected file.')


# Label fuer Quelldatei
lblSourceFile = Label(frameTopFrame, text="Quelldatei:")
lblSourceFile.grid(column=0, row=0, sticky=E, padx=8)

# Kontrollfeld fuer Quelldatei
txtChosenFile = Text(frameTopFrame, height=3, width=35)
txtChosenFile.insert(INSERT, "Noch keine Datei ausgewählt.")
txtChosenFile.grid(column=1, row=0, rowspan=2, pady=5)
txtChosenFile.configure(state=DISABLED)

# Button fuer Quelldatei
btnSourceFile = Button(frameTopFrame, text="Open",
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


# Label fuer Output Ordner
lblOutputFolder = Label(frameTopFrame, text="Ausgabeverzeichnis:")
lblOutputFolder.grid(column=0, row=2, sticky=E, padx=8)
# Kontrollfeld fuer Output Ordner
txtOutputFolder = Text(frameTopFrame, height=3, width=35)
txtOutputFolder.insert(INSERT, "Noch kein Ziel ausgewählt.")
txtOutputFolder.grid(column=1, row=2, rowspan=2, pady=5)
txtOutputFolder.configure(state=DISABLED)
# Button fuer Output Ordner
btnOutputFolder = Button(frameTopFrame, text="Save to",
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
    frameChecker, text="Convert to JPEG2000", var=chkShouldJ2k_state)
chkShouldJ2k.grid(column=0, row=0)

# JPEG DCT Checker
shouldJPEG = False
chkShoulJPEG_state = BooleanVar()
chkShoulJPEG_state.set(True)
chkShoulJPEG = Checkbutton(
    frameChecker, text="Convert to JPEG DCT", var=chkShoulJPEG_state)
chkShoulJPEG.grid(column=0, row=1)

#####################################################

# --------------- COMPRESSION

frameCompressions = Frame(window)
frameCompressions.grid(column=0, row=3, pady=15)

# Anzahl an Compressions Spinbox
lblCompAmount = Label(frameCompressions, text="Anzahl an Compressions:")
lblCompAmount.grid(column=0, row=0)
compAmount = IntVar()
compAmount.set(6)
spinCompAmount = Spinbox(frameCompressions, from_=1,
                         to=8, width=3, textvariable=compAmount)
spinCompAmount.grid(column=1, row=0)

#####################################################

# --------------- PROGRESS BAR

frameProgress = Frame(window)
frameProgress.grid(column=0, row=4)
# Progress Bar
varProgress = IntVar()
varProgressLabel = StringVar()
varProgressLabel.set("Status: Wait")
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
        img = PIL.Image.open(filePath)
        prefix = txtPrefix.get()
        varProgress.set(50)
        varProgressLabel.set("Status: Running")
        window.update()
        converter.runConversion(chkShouldJ2k_state.get(
        ), chkShoulJPEG_state.get(), img, outputPath, compAmount.get(), prefix)
        varProgress.set(100)
        varProgressLabel.set("Status: Done!")
        messagebox.showinfo('Conversion Status', 'Konvertierung und Kompression erfolgreich!')


btnRunConversion = Button(window, text="Start Conversion",
                          command=btnRunConversionClicked).grid(padx=15, pady=15)

#####################################################

# --------------- COPYRIGHT

lblFooter1 = Label(window, font="helvetica 8", text="(C) 2020: TLS - TS171")
lblFooter2 = Label(window, font="helvetica 8",
                   text="Programmiert für Postproduction im Sommersemester 2020")

lblFooter1.grid()
lblFooter2.grid()

#####################################################

#####################################################
# -------------- ENDE - GUI INHALTE
#####################################################

# Fuehrt Interface aus
window.mainloop()
