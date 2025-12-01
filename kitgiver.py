# dependencies: meteorclient and FileAPI
import sys
import re
import time
import threading
import traceback
# config

ApiPath = "/home/bar/.local/share/PrismLauncher/instances/2b2t/minecraft/FileApi/"
#           | that must be here
you = "burning_rubber"
friends = ("‰", "burning_rubber")
chat = True
FriendsChatOnly = False # chat must be true

class api_c:
    def tochat(self, data, ApiPath):
        tochatf = open(ApiPath + "tochat.txt", "w")
        tochatf.write(data)
        tochatf.close()
    def command(self, data, ApiPath):
        commandf = open(ApiPath + "command.txt", "w")
        commandf.write(data)
        commandf.close()
    def lastchat(self, ApiPath):
        lastchatf = open(ApiPath + "lastchat.txt", "r")
        lastchatt = lastchatf.read()
        lastchatt = lastchatt.strip()
        return lastchatt
    def localprint(self, data, ApiPath):
        printf = open(ApiPath + "print.txt", "w")
        printf.write(data)
        printf.close()
api = api_c()


def kit(name, api):
    try:
        kitf = open(ApiPath + "kits/" + name, "r")
        for line in kitf.readlines():
            if line.startswith("/"):
                line = line.replace("/", "")
                api.command(line, ApiPath)
            elif line.startswith("@echo"):
                match = re.search(r'@echo\s+(\S+)', line)
                if match:
                    api.localprint(str(match.group(1)), ApiPath)
                if line.startswith("##"):
                    pass
                else:
                    api.tochat(line, ApiPath)
            time.sleep(0.1)
        kitf.close()
    except Exception as e:
        print("kit faild", traceback.print_exc())

def chatf(ApiPath, chat, FriendsChatOnly, you):
    if chat == False:
        return
    oldlast = ""
    while True:
        chat = api.lastchat(ApiPath)
        if chat != oldlast:
            if chat.startswith("<"+you, 0, 30) == True:
                match = re.search(r'@kit\s+(\S+)', chat)
                if match:
                    print("Starting kit: ", match.group(1))
                    kit(match.group(1), api)
                    lastchatf = open(ApiPath + "lastchat.txt", "w")
                    lastchatf.write("done")
                    lastchatf.close()
                match = re.search(r'@help', chat)
                if match:
                    api.localprint("""help:
@kit <kit name>
@help - give you this""", ApiPath)
                    lastchatf = open(ApiPath + "lastchat.txt", "w")
                    lastchatf.write("done")
                    lastchatf.close()
            if FriendsChatOnly == True:
                for f in friends:
                    if chat.startswith("<"+f, 0, 30) == True:
                        sys.stdout.write(str(chat))
                        sys.stdout.flush()
                        print()
                        oldlast = chat
                    if chat.startswith(f+" ", 0, 30) == True:
                        sys.stdout.write(str(chat))
                        sys.stdout.flush()
                        print()
                        oldlast = chat
                if chat.startswith("<", 0, 1) == False:
                    sys.stdout.write(str(chat))
                    sys.stdout.flush()
                    print()
                    oldlast = chat
            else:
                sys.stdout.write(str(chat))
                sys.stdout.flush()
                print()
                oldlast = chat
        time.sleep(0.047)
chatt = threading.Thread(target=chatf, args=(ApiPath,chat,FriendsChatOnly,you))
chatt.start()
print("V0.2")
while True:
    line = input()
    if line.startswith("/"):
        line = line.replace("/", "")
        api.command(line, ApiPath)
    elif line.startswith("@echo"):
        match = re.search(r'@echo\s+(\S+)', line)
        if match:
            api.localprint(str(match.group(1)), ApiPath)
    elif line.startswith("##"):
        pass
    else:
        api.tochat(line, ApiPath)
