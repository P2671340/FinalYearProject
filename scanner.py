import psutil

def check_system_resources():
    # Check system resource usage (CPU, Memory, Disk)
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    misconfigurations = []

    if cpu_usage > 80:
        misconfigurations.append("High CPU usage: {}%".format(cpu_usage))

    if memory.percent > 80:
        misconfigurations.append("High memory usage: {}%".format(memory.percent))

    if disk.percent > 80:
        misconfigurations.append("High disk usage: {}%".format(disk.percent))

    return misconfigurations