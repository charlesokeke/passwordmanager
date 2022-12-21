from flask import Flask
import socket
import re
app = Flask(__name__)
regex_ip = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
regex_domain = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
#ipaddress = input("[+] Enter The IP Address or Domain Name To Scan\n")
#port_num = input("[+] Enter Number of Ports To Scan\n")


def scan_ports(ip, ports):
    data = {"info": []}
    for value in range(int(ports)):
        try:
            sock = socket.socket()
            #sock.settimeout(0.5)
            sock.connect((ip, value))
            service = sock.recv(1024).decode()
            data["info"].append({"service": service, "port": str(value), "status": "open"})
        except:
            data['info'].append({"service": "None", "port": str(value), "status": "closed"})
    return data



def test(data):
    if all(re.search(regex_ip, x) and re.search(regex_domain, x) for x in data):
        print(data)
    else:
        return False

def validate_ip_or_domain(user_input):
    # pass the regular expression
    # and the string in search() method
    if re.search(regex_ip, user_input):
        return user_input

    elif re.search(regex_domain, user_input):
        return socket.gethostbyname(user_input)
    else:
        return False



def validate_port(port_number):
    try:
        return type(int(port_number)) == int and int(port_number) > 0
    except:
        return False


@app.route('/')
def hello_world():
    if validate_ip_or_domain("charles-okeke.com") and validate_port("30"):
        return scan_ports("charles-okeke.com", "30")
    else:
        return "Invalid entry"
