from os import system
# from ezblock import getIP
import time
import os
import re


CODE_DIR = "/home/pi/rascam/web_control"

def getIP(ifaces=['wlan0', 'eth0']):
    if isinstance(ifaces, str):
        ifaces = [ifaces]
    for iface in list(ifaces):
        search_str = 'ip addr show {}'.format(iface)
        result = os.popen(search_str).read()
        com = re.compile(r'(?<=inet )(.*)(?=\/)', re.M)
        ipv4 = re.search(com, result)
        if ipv4:
            ipv4 = ipv4.groups()[0]
            return ipv4
    return False


def start_http_server():
    system(f"cd {CODE_DIR}/web_client && sudo python3 -m http.server 80 2>&1 1>/dev/null &")

def close_http_server():
    system("sudo kill $(ps aux | grep 'http.server' | awk '{ print $2 }') 2>&1 1>/dev/null")
    
def start_websocket():
    system(f"cd {CODE_DIR}/web_server && sudo python3 web_server.py ")

def close_websocket():
    system("sudo kill $(ps aux | grep 'web_server.py' | awk '{ print $2 }') 2>&1 1>/dev/null")



if __name__ == '__main__':
    try:
        for _ in range(10):
            ip = getIP()
            if ip:
                break
            time.sleep(1)
        start_http_server()
        start_websocket()
        
        # print("Web example starts at %s" % (ip)) 
        # print("Open http://%s in your web browser to control !" % (ip))
        while 1:
            
            pass 
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        print("Finished")
        close_websocket()
        close_http_server()