from datetime import datetime
import time

class MemcachedStats(object):
    def __init__(self, stats):
        self.servers = []
        for server in stats:
            self.servers.append(StatsServer(server))
    
    def getTotalItems(self):
        totalItems = 0
        for server in self.servers:
            totalItems += server.getTotalItems()
        return totalItems
    
    def getItems(self):
        items = 0
        for server in self.servers:
            items += server.getItems()
        return items
    
    def getTotalConnections(self):
        totalConnections = 0
        for server in self.servers:
            totalConnections += server.getTotalConnections()
        return totalConnections
    
    def getConnections(self):
        connections = 0
        for server in self.servers:
            connections += server.getConnections()
        return connections
    
    def getHits(self):
        hits = 0
        for server in self.servers:
            hits += server.getHits()
        return hits
    
    def getMisses(self):
        misses = 0
        for server in self.servers:
            misses += server.getMisses()
        return misses
    
    def getGets(self):
        gets = 0
        for server in self.servers:
            gets += server.getGets()
        return gets
    
    def getSets(self):
        sets = 0
        for server in self.servers:
            sets += server.getSets()
        return sets
    
    def getTotalSpace(self):
        space = 0
        for server in self.servers:
            space += server.getTotalSpace()
        return space
    
    def getFreeSpace(self):
        space = 0
        for server in self.servers:
            space += server.getFreeSpace()
        return space
    
    def getUsedSpace(self):
        space = 0
        for server in self.servers:
            space += server.getUsedSpace()
        return space
    
    def getRequestRate(self):
        rate = 0
        for server in self.servers:
            rate += server.getRequestRate()
        return rate/len(self.servers)
    
    def getHitRate(self):
        rate = 0
        for server in self.servers:
            rate += server.getHitRate()
        return rate/len(self.servers)
    
    def getMissRate(self):
        rate = 0
        for server in self.servers:
            rate += server.getMissRate()
        return rate/len(self.servers)
    
    def getSetRate(self):
        rate = 0
        for server in self.servers:
            rate += server.getSetRate()
        return rate/len(self.servers)
        
class StatsServer(object):
    def __init__(self, stats):
        self.CurrentTime = datetime.today()
        
        self.Name = stats[0]
        self.PID = int(stats[1]['pid'])
        self.TotalItems = int(stats[1]['total_items'])
        self.Uptime = datetime.fromtimestamp(int(stats[1]['uptime']))
        self.UptimeTimestamp = int(stats[1]['uptime'])
        self.Version = stats[1]['version']
        self.LimitMaxBytes = int(stats[1]['limit_maxbytes'])
        self.RUsageUser = stats[1]['rusage_user']
        self.BytesRead = int(stats[1]['bytes_read'])
        self.RUsageSystem = stats[1]['rusage_system']
        self.CMDGet = int(stats[1]['cmd_get'])
        self.CurrConnections = int(stats[1]['curr_connections'])
        self.Threads = int(stats[1]['threads'])
        self.TotalConnections = int(stats[1]['total_connections'])
        self.CMDSet = int(stats[1]['cmd_set'])
        self.CurrItems = int(stats[1]['curr_items'])
        self.GetMisses = int(stats[1]['get_misses'])
        self.Evictions = stats[1]['evictions']
        self.Bytes = int(stats[1]['bytes'])
        self.ConnectionStructures = int(stats[1]['connection_structures'])
        self.BytesWritten = int(stats[1]['bytes_written'])
        self.Time = datetime.fromtimestamp(int(stats[1]['time']))
        self.Timestamp = int(stats[1]['time'])
        self.PointerSize = int(stats[1]['pointer_size'])
        self.GetHits = int(stats[1]['get_hits'])
    
    def getTotalItems(self):
        return self.TotalItems
    def getItems(self):
        return self.CurrItems
    def getTotalConnections(self):
        return self.TotalConnections
    def getConnections(self):
        return self.CurrConnections
    def getHits(self):
        return self.GetHits
    def getMisses(self):
        return self.GetMisses
    def getGets(self):
        return self.CMDGet
    def getSets(self):
        return self.CMDSet
    def getTotalSpace(self):
        return self.LimitMaxBytes
    def getFreeSpace(self):
        return self.getTotalSpace()-self.getUsedSpace()
    def getUsedSpace(self):
        return self.Bytes
    def getRequestRate(self):
        return float(self.getGets())/float(self.getUptimeUnix())*100
    def getHitRate(self):
        return float(self.getHits())/float(self.getUptimeUnix())*100
    def getMissRate(self):
        return float(self.getMisses())/float(self.getUptimeUnix())*100
    def getSetRate(self):
        return float(self.getSets())/float(self.getUptimeUnix())*100
    def getTime(self):
        return self.Time
    def getTimeUnix(self):
        return self.Timestamp
    def getUptime(self):
        return self.Uptime
    def getUptimeUnix(self):
        return self.UptimeTimestamp
        