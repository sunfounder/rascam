import asyncio
import websockets
import json
import time, os, shutil
import re
from camera import Vilib
import google_upload as google

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

ip = getIP()

Vilib.camera_start()

class Websocket():
    recv_dict = {
        'TA':'off',  #拍照
        'SH':'off',  #分享
        
    }

    send_dict = {
        'AD':'http://' + ip + ':8888/mjpg',
        'PD':"a"
    } 
    upload_flag = 'flase'
    
    async def recv_server_func(self, websocket):
        while 1:
            tmp = await websocket.recv()
            # print(tmp)
            tmp = json.loads(tmp)
            
            for key in tmp:
                self.recv_dict[key] = tmp[key]
            # print("recv_dict: %s"%self.recv_dict)
            if self.recv_dict['TA'] == 'on':
                Vilib.snapstart()
                self.recv_dict['TA'] = "off"
                self.upload_flag = 'reset'
            if self.recv_dict['SH'] == 'on':
                name = google.upload(file_path='/home/pi/picture_file', file_name=Vilib.filename)
                self.recv_dict['SH'] = "off"
                if name == Vilib.filename:
                    self.upload_flag = 'Successful'
                else:
                    self.upload_flag = 'failed'
                    
            
    
    
    async def send_server_func(self, websocket): 
        while 1:
            self.send_dict['PD'] = self.upload_flag
            await websocket.send(json.dumps(self.send_dict))
            await asyncio.sleep(0.01)
        
        
    
    async def main_logic_1(self, websocket, path):
        while 1:
            await self.recv_server_func(websocket)

    async def main_logic_2(self, websocket, path):
        while 1:
            await self.send_server_func(websocket)
            
    def test(self):
        try:
            for _ in range(10):
                # ip = getIP()
                if ip:
                    print("IP Address: "+ ip)
                    # start_http_server()
                    break
                time.sleep(1)
            # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            # localhost_pem = pathlib.Path(__file__).with_name("server.pem")
            # ssl_context.load_cert_chain(localhost_pem)
            start_server_1 = websockets.serve(self.main_logic_1, ip, 8765)
            start_server_2 = websockets.serve(self.main_logic_2, ip, 8766)
            print('Start!')
            tasks = [start_server_1,start_server_2]
            asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
            asyncio.get_event_loop().run_forever()
 
        finally:
            print("Finished")
   
   
if __name__ == "__main__":
    ws = Websocket()
    ws.test()

