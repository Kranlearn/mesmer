import cv2
import time

# Initialisation de la caméra (Webcam 0)
camera = cv2.VideoCapture(0)

# Variables de traitement de signal
frame_precedente = None
historique_mouvements = []  # LISTE (Jour 5) pour stocker la télémétrie

print("[MESMER INFRA] Recherche de pics de mouvement... Appuie sur 'q' pour couper.")

while camera.isOpened():
    reussite, frame_actuelle = camera.read()  # <-- Assure-toi qu'il y a exactement 4 espaces ici
    if not reussite:
        continue


    try:
        # 1. Prétraitement : Conversion en Niveaux de Gris et Floutage pour éliminer le bruit du salon
        gris = cv2.cvtColor(frame_actuelle, cv2.COLOR_BGR2GRAY)
        gris = cv2.GaussianBlur(gris, (21, 21), 0)

        # Si c'est la première frame, on l'initialise et on passe à la suivante
        if frame_precedente is None:
            frame_precedente = gris
            continue

        # 2. Calcul de la différence absolue entre l'image d'avant et l'image actuelle
        difference_frames = cv2.absdiff(frame_precedente, gris)
        
        # 3. Seuil (Threshold) : convertit les pixels modifiés en blanc, le reste en noir
        _, seuil = cv2.threshold(difference_frames, 25, 255, cv2.THRESH_BINARY)
        
        # Calcul du score de mouvement (somme des pixels blancs)
        score_mouvement = seuil.sum() / 1000000
        
        # Enregistrement dans notre structure dynamique
        historique_mouvements.append(score_mouvement)
        if len(historique_mouvements) > 50:  # On garde uniquement les 50 dernières variations
            historique_mouvements.pop(0)

        # 4. Détection d'un Pic Émotionnel / Reniflement (Ajuste le seuil de 5.0 selon ta caméra)
        if score_mouvement > 5.0:
            horodatage = time.strftime("%H:%M:%S")
            print(f"🚨 [MESMER ALERT] {horodatage} -> Pic de mouvement détecté ! Score : {score_mouvement:.2f}")
            cv2.putText(frame_actuelle, "ALERT: SUDDEN MOVEMENT DETECTED", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Mise à jour de la frame de référence pour la prochaine itération
        frame_precedente = gris

    except Exception as e:
        # Armure de sécurité du Jour 6 pour éviter que la boucle crash en direct
        print(f"[ERROR] Échec de l'analyse différentielle : {str(e)}")

    # Affichage du HUD de Mesmer
    cv2.imshow("MESMER CORE - SIGNAL PROCESSING", frame_actuelle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
print("[SYS] Fin de run Mesmer.")
