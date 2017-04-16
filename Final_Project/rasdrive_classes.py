#! /usr/bin/env python3

class RASD_Client(object):
    def __init__(self, name, connection, schedule):
        self.name = name
        self.connection = connection
        self.schedule = schedule


class RASD_Server(object):
    def __init__(self, connection, priority, status):
        self.connection = connection
        self.priority = priority
        self.status = status


class RASD_Backup(object):
    def __init__(self, connection, status):
        self.connection = connection
        self.status = status


class RASD_Status(object):
    def __init__(self, cpu_percent, net_stats, disk_usage):
        self.cpu_percent = cpu_percent
        self.net_stats = net_stats
        self.disk_usage = disk_usage

    def __str__(self):
        return "CPU Utilization: " + self.cpu_percent + \
               "\nNetwork Statistics: " + self.net_stats + \
               "\nDisk Usage: " + self.disk_usage

class RASD_Net_Load(object):
    def __init__(self, bytes_sent, bytes_recv, errin, errout, dropin, dropout):
        self.bytes_sent = bytes_sent
        self.bytes_recv = bytes_recv
        self.errin = errin
        self.errout = errout
        self.dropin = dropin
        self.dropout = dropout

    def __str__(self):
        return "Bytes Sent: " + self.bytes_sent + " Bytes Recieved: " + self.bytes_recv + \
               "\nError In: " + self.errin + " Error Out: " + self.errout + \
               "\nDrop In: " + self.dropin + " Drop Out: " + self.dropout
