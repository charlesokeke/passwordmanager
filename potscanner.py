import socket
import re
from IPy import IP

regex_ip = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
regex_domain = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
ipaddress = input("[+] Enter IP Address or Domains Name To Scan\n")
port_num = input("[+] Enter Number of Ports To Scan\n")


def scan_ports(ip, ports):
    data = []
    for value in range(int(ports)):
        try:
            sock = socket.socket()
            #sock.settimeout(0.5)
            sock.connect_ex((ip, value))
            service = decode_data(sock)
            #print("port" + str(value) + " is open service running: " + service)
            data.append({"service": service, "status": "open", "port": str(value)})
        except Exception as err:
            exception_type = type(err).__name__
            print(exception_type + " for port" + str(value))


    return data


def decode_data(s):
    return s.recv(1024)


def test(data):
    if all(re.search(regex_ip, x) or re.search(regex_domain, x) for x in data):
        return [socket.gethostbyname(x) for x in data]
    else:
        return False


def validate_port(port_number):
    try:
        return type(int(port_number)) == int and int(port_number) > 0
    except:
        return False


if test(ipaddress.split(",")) and validate_port(port_num):
    scan_result = {}
    for item in ipaddress.split(","):
        print("scanning " + item)
        scan_result[item] = scan_ports(item, port_num)
    print(scan_result)
else:
    print("invalid")
