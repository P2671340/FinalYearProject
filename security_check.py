import psutil

def check_open_ports():
    open_ports = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN':
            open_ports.append(f"Open port: {conn.laddr.ip}:{conn.laddr.port}")

    security_issues = []
    if open_ports:
        security_issues.append(f"Found open ports: {', '.join(open_ports)}")

    return security_issues