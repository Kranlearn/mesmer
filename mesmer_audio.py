import sounddevice as sd
import numpy as np
import time

print("====================================================")
print("===      MESMER v1.0 // AUDIO SENSOR CORE        ===")
print("====================================================")

# Configuration de la fréquence d'échantillonnage (Standard : 44100 Hz)
FREQUENCE = 44100 
DUREE_BLOC = 0.1 # Le bot analyse le son par blocs de 100 millisecondes

print("[SYS] Capteurs acoustiques en écoute... Parle ou fais un bruit.")

def analyser_flux_audio(indata, frames, time_info, status):
    """ Cette fonction est appelée automatiquement à chaque bloc de son reçu """
    try:
        # Calcul de la puissance brute du signal (Volume RMS)
        volume = np.linalg.norm(indata) * 10
        
        # Si le volume dépasse le seuil d'un bruit sec (Ajuste le 5.0 selon ton micro)
        if volume > 5.0:
            horodatage = time.strftime("%H:%M:%S")
            print(f"🎤 [AUDIO ALERT] {horodatage} -> Pic sonore détecté ! Intensité : {volume:.2f}")
            
    except Exception as e:
        print(f"Erreur audio : {str(e)}")

# Ouverture du canal d'écoute en arrière-plan (Stream)
with sd.InputStream(samplerate=FREQUENCE, channels=1, callback=analyser_flux_audio, blocksize=int(FREQUENCE * DUREE_BLOC)):
    try:
        while True:
            time.sleep(0.1) # Maintient le script en vie
    except KeyboardInterrupt:
        print("\n[SYS] Extinction des capteurs acoustiques.")
