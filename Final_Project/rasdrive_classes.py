#! /usr/bin/env python3

class RASD_Client(object):
    def __init__(self, hostname, schedule=None):
        self.hostname = hostname
        self.schedule = schedule


class RASD_Server(object):
    def __init__(self, hostname, status=None):
        self.hostname = hostname
        self.status = status


class RASD_Backup(object):
    def __init__(self, hostname, status=None):
        self.hostname = hostname
        self.status = status


class RASD_Status(object):
    def __init__(self, cpu_percent, net_stats, disk_usage):
        self.cpu_percent = cpu_percent
        self.net_stats = net_stats
        self.disk_usage = disk_usage

    def __str__(self):
        return "CPU Utilization: {}\nNetwork Statistics: {}\nDisk Usage: {}".format(
            self.cpu_percent, self.net_stats, self.disk_usage)


class RASD_Net_Load(object):
    def __init__(self, bytes_sent, bytes_recv, errin, errout, dropin, dropout):
        self.bytes_sent = bytes_sent
        self.bytes_recv = bytes_recv
        self.errin = errin
        self.errout = errout
        self.dropin = dropin
        self.dropout = dropout

    def __str__(self):
        return "Bytes Sent: {} Bytes Recieved: {}\nError In: {} Error Out: {}\nDrop In: {} Drop Out: {}".format(
            self.bytes_sent, self.bytes_recv, self.errin, self.errout, self.dropin, self.dropout)
