import cv2
import sounddevice as sd
import numpy as np
import time

print("====================================================")
print("===      MESMER v1.0 // MULTIMODAL FUSION CORE   ===")
print("====================================================")

# 1. PASSERELLE DE SIGNALISATIONS (Variable globale de partage)
dernier_volume_detecte = 0.0
FREQUENCE = 44100
DUREE_BLOC = 0.1

def callback_audio(indata, frames, time_info, status):
    """ Capte le son en arrière-plan et met à jour la passerelle """
    global dernier_volume_detecte
    try:
        dernier_volume_detecte = np.linalg.norm(indata) * 10
    except Exception:
        pass

# 2. ACTIVATION DU CAPTEUR ACOUSTIQUE ASYNCHRONIQUE
flux_audio = sd.InputStream(samplerate=FREQUENCE, channels=1, callback=callback_audio, blocksize=int(FREQUENCE * DUREE_BLOC))
flux_audio.start()

# 3. ACTIVATION DU CAPTEUR OPTIQUE
camera = cv2.VideoCapture(0)
frame_precedente = None

print("[SYS] Fusion multimodale active. Capture Audio + Vidéo synchronisée.")

while camera.isOpened():
    reussite, frame_actuelle = camera.read()
    if not reussite:
        continue

    try:
        # Traitement visuel différentiel
        gris = cv2.cvtColor(frame_actuelle, cv2.COLOR_BGR2GRAY)
        gris = cv2.GaussianBlur(gris, (21, 21), 0)

        if frame_precedente is None:
            frame_precedente = gris
            continue

        difference_frames = cv2.absdiff(frame_precedente, gris)
        _, seuil = cv2.threshold(difference_frames, 25, 255, cv2.THRESH_BINARY)
        score_mouvement = seuil.sum() / 1000000

        # 4. LE NOYAU DE FUSION : CORRÉLATION AUDIO + VIDÉO (Preuve de reniflement)
        # Un pic de mouvement (score > 4) + un pic sonore (volume > 4) au même instant
        if score_mouvement > 4.0 and dernier_volume_detecte > 4.0:
            horodatage = time.strftime("%H:%M:%S")
            print(f"🧬 [MESMER FUSION] {horodatage} -> CORRÉLATION : Reniflement / Sursaut détecté !")
            print(f"   [PREUVES] Mouvement: {score_mouvement:.2f} | Audio: {dernier_volume_detecte:.2f}")
            
            # Affichage sur le HUD visuel
            cv2.putText(frame_actuelle, "🚨 MESMER ALERT: CRITICAL AFFECTIVE SIGN", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Affichage des jauges de télémétrie en direct sur l'écran
        cv2.putText(frame_actuelle, f"Mouvement: {score_mouvement:.2f}", (20, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame_actuelle, f"Audio/Micro: {dernier_volume_detecte:.2f}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        frame_precedente = gris

    except Exception as e:
        print(f"[ERROR] Échec de la fusion : {str(e)}")

    cv2.imshow("MESMER CORE - MULTIMODAL HUD", frame_actuelle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. NETTOYAGE ABSOLU DES INFRASTRUCTURES
camera.release()
cv2.destroyAllWindows()
flux_audio.stop()
flux_audio.close()
print("[SYS] Laboratoire Mesmer éteint proprement.")
