import os;
import json;
import socket;
class Odrivex():
    def tether():
        with open(os.path.join(os.path.expanduser('~'),'.odrive-agent','.oreg'), 'r') as oreg_f:
            data=json.loads(oreg_f.read());
            port=data["current"]["protocol"];
        socket_odriveagent=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        socket_odriveagent.connect(('127.0.0.1', port));
        return socket_odriveagent;
    def receive(socket_odriveagent):
        data=True;
        buffer='';
        while data:
            data=socket_odriveagent.recv(1024*1024);
            buffer+=data.decode('utf-8');
            while buffer.find('\n') != -1:
                response_odriveagent, buffer= buffer.split('\n', 1);
                jsonresponse_odriveagent = json.loads(response_odriveagent);
        return jsonresponse_odriveagent;
