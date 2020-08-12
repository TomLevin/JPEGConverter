###########################################################
# Diese Datei beinhaltet alle Converter-Funktionen
#
###########################################################
from PIL import Image
import os
###########################################################

# Pruefung der benoetigten Umwandlungen und Start dieser:


def runConversion(shouldJ2k, shouldJPEG, img, outputPath, compAmount, prefix):

    # Prueft Conversion in .J2K und fuehrt aus
    if shouldJ2k == True:
        startConversion = j2k_exporter(img, compAmount, prefix, outputPath)
    else:
        print("Skipping J2K Conversion")

    # Prueft Conversion in .JPG und fuehrt aus
    if shouldJPEG == True:
        startConversion = jpeg_exporter(img, compAmount, prefix, outputPath)
    else:
        print("Skipping JPEG DCT Conversion")


###########################################################
# FUNKTION A: Konvertiert in JPEG-DCT und komprimiert

def jpeg_exporter(sourceImage, compressionSteps, outputPrefix, exportPath):

    # Startet die Conversion in J2K und exportiert unkomprimiert und entpsprechend der Compressionsschritte
    counter = 1
    quality = 100
    while (counter <= compressionSteps):
        print("Converting image to DCT-JPEG: " +
              str(counter) + " / " + str(compressionSteps))

        imagename=exportPath + "/" + outputPrefix + "_JPG_" + str(counter) + ".jpg"

        print("Current JPG Quality:" + str(quality))
        sourceImage.save(imagename, "JPEG", optimize = True, quality = quality)

        if quality > 0:
            quality=getNextQuality(sourceImage, imagename, quality, counter)

        counter += 1
        
# ----- ENDE FUNKTION A ////


###########################################################
# FUNKTION B: Konvertiert in JPEG2000 und komprimiert
def j2k_exporter(sourceImage, compressionSteps, outputPrefix, exportPath):

    # Startet die Conversion in J2K und exportiert unkomprimiert und entpsprechend der Compressionsschritte
    counter=1
    compressionRatio=4
    while (counter <= compressionSteps):
        print("Converting image to JPEG2000: " +
              str(counter) + " / " + str(compressionSteps))
        quality=[compressionRatio]

        imagename=exportPath + "/" + outputPrefix + "_J2K_" + str(counter) + ".j2k"
        # this converts png image as jpeg
        sourceImage.save(imagename, "JPEG2000",
                         quality_mode = "rates", quality_layers = quality)
        print("Saving: " + imagename)
        j2kImage=Image.open(imagename)
        tga_converter(j2kImage, counter, outputPrefix, exportPath)
        compressionRatio += compressionRatio
        counter += 1

# ----- ENDE FUNKTION B ////


###########################################################
# FUNKTION C: Konvertiert J2K Dateien in TGA
def tga_converter(tgaSource, counter, outputPrefix, exportPath):
    tgaName=exportPath + "/" + outputPrefix + "_J2K_TGA_" + str(counter) + ".tga"
    tgaPath=tgaName
    tgaSource.save(tgaPath, "TGA")  # this converts png image as jpeg
# ----- ENDE FUNKTION C ////


###########################################################
# Ermittelt naechsten Qualitaetsschritt fuer JPEG-DCT
def getNextQuality(sourceImage, currentImageName, currentQuality, compressionStep):

    # Definiert geforderte Dateigroesse und initialisiert Variablen fuer Ober- und Untergrenze
    goalSize=(os.path.getsize(currentImageName)/2)
    sizeImage1=goalSize
    sizeImage2=goalSize

    # Schleife die Schrittweise die Qualitaet in ganzzahligen Schritten herabsetzt bis gewuenschte Groesse erreicht ist
    # Um Dateigroessen zu bestimmen werden je die Bilder mit der aktuellen Qualitaet und der Qualitaet-1 generiert, analysiert und entfernt
    counter=0
    while (sizeImage1 >= goalSize and sizeImage2 >= goalSize and currentQuality > 1):

        cacheImageBig=sourceImage.save(
            "cacheImage1.jpg", "JPEG", optimize=True, quality=currentQuality)
        cacheImageSmall = sourceImage.save(
            "cacheImage2.jpg", "JPEG", optimize=True, quality=(currentQuality-1))
        sizeImage1 = os.path.getsize('cacheImage1.jpg')
        sizeImage2 = os.path.getsize('cacheImage2.jpg')
        os.remove("cacheImage1.jpg")
        os.remove("cacheImage2.jpg")

        if currentQuality > 1:
            currentQuality -= 1

    return (currentQuality)

# ----- ENDE Qualitaetsermittlung
