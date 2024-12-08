import nmap


def scan_ports(ip_or_domain):
    scanner = nmap.PortScanner()

    try:
        scanner.scan(ip_or_domain, arguments='-p 22-443')
    except Exception as e:
        print(f"Error scanning {ip_or_domain}: {e}")
        return []

    open_ports = []
    for host in scanner.all_hosts():
        print("Host:", host)
        print("State:", scanner[host].state())
        for proto in scanner[host].all_protocols():
            print("Protocol:", proto)
            ports = scanner[host][proto].keys()
            for port in ports:
                print(f"Port: {port}, State: {scanner[host][proto][port]['state']}")
                open_ports.append(port)

    return open_ports

