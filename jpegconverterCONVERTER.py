###########################################################
# Diese Datei beinhaltet alle Converter-Funktionen
#
###########################################################
import PIL.Image  # Importiert PIL Package
from PIL import *
import os
###########################################################

# Pruefung der benoetigten Umwandlungen und Start dieser:


def runConversion(shouldJ2k, shouldJPEG, imgPath, outputPath, compAmount, prefix):

    # Prueft Conversion in .J2K und fuehrt aus
    if shouldJ2k == True:
        startConversion = j2k_exporter(imgPath, compAmount, prefix, outputPath)
    else:
        print("Skipping J2K Conversion")

    # Prueft Conversion in .JPG und fuehrt aus
    if shouldJPEG == True:
        startConversion = jpeg_exporter(imgPath, compAmount, prefix, outputPath)
    else:
        print("Skipping JPEG DCT Conversion")


###########################################################
# FUNKTION A: Konvertiert in JPEG mit libjpeg und komprimiert

def jpeg_exporter(imgPath, compressionSteps, outputPrefix, exportPath):
    # Startet die Conversion in .JPG und exportiert entpsprechend der Kompressionsschritte
    counter = 1
    quality = 100
    imagename=imgPath
    sourceImage = PIL.Image.open(imgPath)
    while counter <= compressionSteps:
        #Ermittelt empirisch die benoetigte Qualitaetsstufe um Zielgroesse der Datei zu erreichen
    	#Uebergibt Quelldatei, Dateinamen mit Pfad, aktuelle Qualitaet, aktuellen Durchgang
        quality=getNextQuality(sourceImage, imagename, quality, counter)
        imagename=exportPath + "/" + outputPrefix + "_JPG_" + str(counter) + ".jpg"
        sourceImage.save(imagename, "JPEG", optimize = True, quality = quality)
        print("Successfully written: " + os.path.basename(imagename))
        counter += 1
        
# ----- ENDE FUNKTION A ////


###########################################################
# FUNKTION B: Konvertiert in JPEG2000 mit OpenJPEG und komprimiert
def j2k_exporter(imgPath, compressionSteps, outputPrefix, exportPath):

    # Startet die Conversion in J2K und exportiert unkomprimiert und entpsprechend der Compressionsschritte
    counter=1
    compressionRatio=4
    sourceImage = PIL.Image.open(imgPath)
    while counter <= compressionSteps:
        quality=[compressionRatio]

        imagename=exportPath + "/" + outputPrefix + "_J2K_" + str(counter) + ".j2k"
        # Speichert J2K Datei
        sourceImage.save(imagename, "JPEG2000",
                         quality_mode = "rates", quality_layers = quality)
        print("Successfully written: " + os.path.basename(imagename))
        j2kImage=Image.open(imagename)
        tga_converter(j2kImage, counter, outputPrefix, exportPath)
        compressionRatio += compressionRatio
        counter += 1

# ----- ENDE FUNKTION B ////


###########################################################
# FUNKTION C: Konvertiert J2K Dateien in TGA
def tga_converter(tgaSource, counter, outputPrefix, exportPath):
    tgaName=exportPath + "/" + outputPrefix + "_J2K_TGA_" + str(counter) + ".tga"
    tgaSource.save(tgaName, "TGA")  # Speichert .tga
    print("Successfully written: " + os.path.basename(tgaName))
# ----- ENDE FUNKTION C ////


###########################################################
# Ermittelt naechsten Qualitaetsschritt fuer JPEG
def getNextQuality(sourceImage, currentImageName, currentQuality, compressionStep):

    # Definiert geforderte Dateigroesse und initialisiert Variablen fuer Ober- und Untergrenze
    if compressionStep == 1:
        goalSize=(os.path.getsize(currentImageName)/4)
    else:    
        goalSize=(os.path.getsize(currentImageName)/2)
    sizeCache=goalSize
    # Schleife die Schrittweise die Qualitaet in ganzzahligen Schritten herabsetzt
    # bis gewuenschte Groesse erreicht ist
    # Um Dateigroessen zu bestimmen werden je die Bilder mit der aktuellen Qualitaet
    # und der Qualitaet-1 generiert, analysiert und entfernt
    while (sizeCache >= goalSize and currentQuality > 1):
        cacheImage=sourceImage.save(
            "cacheImage.jpg", "JPEG", optimize=True, quality=currentQuality)
        sizeCache = os.path.getsize('cacheImage.jpg')
        os.remove("cacheImage.jpg")
        # Prueft ob geforderte oder minimale Qualitaet (1) erreicht ist, wenn nicht -> Reduzierung
        if (sizeCache >= goalSize and currentQuality > 1):
            currentQuality -= 1

    return (currentQuality+1)

# ----- ENDE Qualitaetsermittlung
