"""Controlled local HTTP experiment, not an industrial case study.
Captures raw socket bytes: HTTP clients may hide an illegal HEAD body.
"""
from pathlib import Path
import socket, socketserver, threading, json, hashlib, base64
from model import base_record,evaluate
from experiments import savecsv
ROOT=Path(__file__).resolve().parent
PAYLOADS={f'/n{n}':b'x'*n for n in (0,1,7,64,1024)}

def collect(mode):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            request=b''
            while b'\r\n\r\n' not in request:
                piece=self.request.recv(4096)
                if not piece:return
                request+=piece
            method,path,_=request.split(b'\r\n',1)[0].decode('ascii').split()
            payload=PAYLOADS[path]
            content=payload if method=='GET' or mode=='body_bug' else b''
            headers=b'HTTP/1.1 200 OK\r\nConnection: close\r\n'
            if not (method=='HEAD' and mode=='omit_length'):
                length=0 if method=='HEAD' and mode=='length_bug' else len(payload)
                headers+=f'Content-Length: {length}\r\n'.encode('ascii')
            self.request.sendall(headers+b'\r\n'+content)
    traces=[];pairs=[]
    with socketserver.TCPServer(('127.0.0.1',0),Handler) as server:
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            for path,payload in PAYLOADS.items():
                responses={}
                for method in ('GET','HEAD'):
                    request=f'{method} {path} HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n'.encode('ascii')
                    with socket.create_connection(server.server_address,timeout=5) as s:
                        s.sendall(request);raw=b''
                        while True:
                            part=s.recv(4096)
                            if not part:break
                            raw+=part
                    head,body=raw.split(b'\r\n\r\n',1)
                    headers=dict(line.decode('ascii').split(': ',1) for line in head.split(b'\r\n')[1:])
                    responses[method]=(headers,body)
                    traces.append(dict(mode=mode,path=path,method=method,response_base64=base64.b64encode(raw).decode(),sha256=hashlib.sha256(raw).hexdigest()))
                assert responses['GET'][1]==payload
                hh,hb=responses['HEAD'];c1=len(hb)==0
                c2='Content-Length' not in hh or int(hh['Content-Length'])==len(responses['GET'][1])
                pairs.append(dict(mode=mode,path=path,get_bytes=len(payload),head_bytes=len(hb),
                                  head_length=hh.get('Content-Length','absent'),C1=c1,C2=c2))
        finally:server.shutdown();thread.join()
    return pairs,traces

def main():
    rows=[];raw=[];records=[]
    for mode in ('correct','omit_length','body_bug','length_bug'):
        pairs,traces=collect(mode);rows+=pairs;raw+=traces
        r=base_record();r.update(requirement='RFC9110-HEAD',version='scope-v1',implementation=mode)
        r['alternatives'][1]['mass']=0
        for i,e in enumerate(r['evidence']):
            e.update(requirement=r['requirement'],version=r['version'],implementation=mode,
                     source='http_pairs.csv#'+mode,reviewer='automated-oracle-v1',
                     result='pass' if all(x[f'C{i+1}'] for x in pairs) else 'fail')
        out=evaluate(r);expected='accepted' if mode in ('correct','omit_length') else 'failed'
        assert out['acceptance']==expected
        records.append(dict(mode=mode,record=r,status=out))
    savecsv('http_pairs.csv',rows)
    (ROOT/'http_raw.json').write_text(json.dumps(raw,indent=2),encoding='utf-8')
    (ROOT/'http_records.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    print(dict(requests=len(raw),pairs=len(rows),statuses={x['mode']:x['status']['acceptance'] for x in records}))

if __name__=='__main__':main()
