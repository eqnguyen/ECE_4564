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
    def __init__(self, cpu_percent, net_load):
        self.cpu_percent = cpu_percent
        self.net_load = net_load

class RASD_Net_Load(object):
    def __init__(self, bytes_sent, bytes_recv, errin, errout, dropin, dropout):
        self.bytes_sent = bytes_sent
        self.bytes_recv = bytes_recv
        self.errin = errin
        self.errout = errout
        self.dropin = dropin
        self.dropout = dropout
