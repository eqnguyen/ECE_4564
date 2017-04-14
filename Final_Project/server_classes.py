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
    def __init__(self, cpu_load, net_load):
        self.cpu_load = cpu_load
        self.net_load = net_load