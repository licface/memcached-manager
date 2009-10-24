from datetime import datetime
import time

def breakdownSize(space):
	if space > 0:
		bytes = space % 1024
		space = int(space/1024)
		kbytes = space % 1024
		space = int(space/1024)
		mbytes = space % 1024
		space = int(space/1024)
		gbytes = space % 1024
		space = int(space/1024)
		tbytes = space % 1024
		space = int(space/1024)
		pbytes = space % 1024
		return {'b': bytes, 'k': kbytes, 'm': mbytes, 'g': gbytes, 't': tbytes, 'p': pbytes}
	else:
		return {'b': 0, 'k': 0, 'm': 0, 'g': 0, 't': 0, 'p': 0}
	
def formatSize(space, length = 6):
	total = breakdownSize(space)
	tStr = ''
	currentLength = 0
	if total['p'] != 0:
		tStr += str(total['p']) +'PB '
		currentLength +=1
	if total['t'] != 0 and length >= currentLength:
		tStr += str(total['t']) +'TB '
		currentLength +=1
	if total['g'] != 0 and length >= currentLength:
		tStr += str(total['g']) +'GB '
		currentLength +=1
	if total['m'] != 0 and length >= currentLength:
		tStr += str(total['m']) +'MB '
		currentLength +=1
	if total['k'] != 0 and length >= currentLength:
		tStr += str(total['k']) +'KB '
		currentLength +=1
	if total['b'] != 0 and length >= currentLength:
		tStr += str(total['b']) +'B '
		currentLength +=1
		
	if tStr == '':
		tStr = '0B'
		
	return tStr

class MemcachedStats(object):
	def __init__(self, mcClient):
		self.servers = []
		for server in mcClient.get_stats():
			self.servers.append(StatsServer(server[0], server[1]))
	
	def getServers(self):
		return self.servers
	
	def getTotalItems(self):
		return self._getServersAttrib('TotalItems')
	
	def getItems(self):
		return self._getServersAttrib('CurrItems')
	
	def getTotalConnections(self):
		return self._getServersAttrib('TotalConnections')
	
	def getConnections(self):
		return self._getServersAttrib('CurrConnections')
	
	def getHits(self):
		return self._getServersAttrib('GetHits')
	
	def getMisses(self):
		return self._getServersAttrib('GetMisses')
	
	def getGets(self):
		return self._getServersAttrib('CMDGet')
	
	def getSets(self):
		return self._getServersAttrib('CMDSet')
	
	def getTotalSpace(self):
		return self._getServersAttrib('LimitMaxBytes')
	def getFormatedTotalSpace(self):
		return formatSize(self.getTotalSpace())
	
	def getFreeSpace(self):
		return self._callServersFunc('getFreeSpace')
	def getFormatedFreeSpace(self):
		return formatSize(self.getFreeSpace())
	
	def getUsedSpace(self):
		return self._getServersAttrib('Bytes')
	def getFormatedUsedSpace(self):
		return formatSize(self.getUsedSpace())
	
	def getRequestRate(self):
		return self._callServersFunc('getRequestRate')
	
	def getHitRate(self):
		return self._callServersFunc('getHitRate')
	
	def getMissRate(self):
		return self._callServersFunc('getMissRate')
	
	def getSetRate(self):
		return self._callServersFunc('getSetRate')
	
	def getGetRate(self):
		return self._callServersFunc('getGetRate')
	
	def getEvictionRate(self):
		return self._callServersFunc('getEvictionRate')
	
	def getRequestRateAvg(self):
		"""
		Avg Request Rate per server
		"""
		rate = self._callServersFunc('getRequestRate')
		for server in self.servers:
			rate += server.getRequestRate()
		if rate > 0:
			return rate/len(self.servers)
		else:
			return 0
	
	def getSetRateAvg(self):
		"""
		Avg Set Rate per server
		"""
		rate = self._callServersFunc('getSetRate')
		if rate > 0:
			return rate/len(self.servers)
		else:
			return 0
	
	def getGetRateAvg(self):
		"""
		Avg Get Rate per server
		"""
		rate = self._callServersFunc('getGetRate')
		if rate > 0:
			return rate/len(self.servers)
		else:
			return 0
	
	def getHitRateAvg(self):
		"""
		Avg Hit Rate per server
		"""
		rate = self._callServersFunc('getHitRate')
		if rate > 0:
			return rate/len(self.servers)
		else:
			return 0
	
	def getMissRateAvg(self):
		"""
		Avg Miss Rate per server
		"""
		rate = self._callServersFunc('getMissRate')
		if rate > 0:
			return rate/len(self.servers)
		else:
			return 0
	
	def getEvictionRateAvg(self):
		"""
		Avg Evistion Rate per server
		"""
		rate = self._callServersFunc('getEvictionRate')
		if rate > 0:
			return rate/len(self.servers)
		else:
			return 0
	
	def getThreads(self):
		return self._getServersAttrib('Threads')
	
	def _getServersAttrib(self, attribute):
		total = 0
		for server in self.servers:
			total += server.__getattribute__(attribute)
		return total
	
	def _callServersFunc(self, function):
		total = 0
		for server in self.servers:
			total += server.__getattribute__(function)()
		return total
		
class StatsServer(object):
	def __init__(self, name, items):
		self.CurrentTime = datetime.today()
		
		self.Name = name
		self.PID = items.get('pid', 0)
		self.Uptime = datetime.fromtimestamp(int(items.get('uptime', 0)))
		self.UptimeTimestamp = int(items.get('uptime', 0))
		self.Time = datetime.fromtimestamp(int(items.get('time', 0)))
		self.Timestamp = int(items.get('time', 0))
		self.Version = items.get('version', 'N/A')
		
		#Default size of pointers on the host OS (generally 32 or 64)
		self.PointerSize = int(items.get('pointer_size', 0))
		
		#Accumulated user time for this process (seconds:microseconds)
		self.RUsageUser = items.get('rusage_user', 0)
		
		#Accumulated system time for this process (seconds:microseconds)
		self.RUsageSystem = items.get('rusage_system', 0)
		
		self.CurrConnections = int(items.get('curr_connections', 0))
		self.TotalConnections = int(items.get('total_connections', 0))
		
		#Number of connection structures allocated by the serve
		self.ConnectionStructures = int(items.get('connection_structures', 0))
		
		self.CMDGet = int(items.get('cmd_get', 0))
		self.CMDSet = int(items.get('cmd_set', 0))
		self.CMDFlush = int(items.get('cmd_flush', 0))
		self.GetHits = int(items.get('get_hits', 0))
		self.GetMisses = int(items.get('get_misses', 0))
		self.DeleteMisses = int(items.get('delete_misses', 0))
		self.DeleteHits = int(items.get('delete_hits', 0))
		self.IncrMisses = int(items.get('incr_misses', 0))
		self.IncrHits = int(items.get('incr_hits', 0))
		self.DecrMisses = int(items.get('decr_misses', 0))
		self.DecrHits = int(items.get('decr_hits', 0))
		self.CasMisses = int(items.get('cas_misses', 0))
		self.CasHits = int(items.get('cas_hits', 0))
		self.CasBadval = int(items.get('cas_badval', 0))
		
		#Total number of bytes read by this server from network
		self.BytesRead = int(items.get('bytes_read', 0))
		
		#Total number of bytes sent by this server from network
		self.BytesWritten = int(items.get('bytes_written', 0))
		
		#Number of bytes this server is allowed to use for storage.
		self.LimitMaxBytes = int(items.get('limit_maxbytes', 0))
		
		self.AcceptingConns = int(items.get('accepting_conns', 0))
		self.ListenDisabledNum = int(items.get('listen_disabled_num', 0))
		self.Threads = int(items.get('threads', 0))
		self.ConnYields = int(items.get('conn_yields', 0))
		
		#Current number of bytes used by this server to store items
		self.Bytes = int(items.get('bytes', 0))
		
		self.CurrItems = int(items.get('curr_items', 0))
		self.TotalItems = int(items.get('total_items', 0))
		self.Evictions = items.get('evictions', 0)
		
	def getFreeSpace(self):
		return self.LimitMaxBytes-self.Bytes
	def getFormatedFreeSpace(self):
		return formatSize(self.getFreeSpace())
	def getFormatedUsedSpace(self):
		return formatSize(self.Bytes)
	def getFormatedTotalSpace(self):
		return formatSize(self.LimitMaxBytes)
	def getFormatedBytesRead(self):
		return formatSize(self.BytesRead)
	def getFormatedBytesWrite(self):
		return formatSize(self.BytesWritten)
	
	def getTotalRequests(self):
		return self.CMDSet + self.CMDGet + self.CMDFlush
	
	def getRequestRate(self):
		return (float(self.getTotalRequests()))/float(self.UptimeTimestamp)
	
	def getSetRate(self):
		return float(self.CMDSet)/float(self.UptimeTimestamp)
	def getGetRate(self):
		return float(self.CMDGet)/float(self.UptimeTimestamp)
	def getFlushRate(self):
		return float(self.CMDFlush)/float(self.UptimeTimestamp)
	
	def getHitRate(self):
		return float(self.GetHits)/float(self.UptimeTimestamp)
	def getMissRate(self):
		return float(self.GetMisses)/float(self.UptimeTimestamp)
	
	def getEvictionRate(self):
		return float(self.Evictions)/float(self.UptimeTimestamp)
		
if __name__ == '__main__':
	import memcache
	stats = MemcachedStats(memcache.Client(['localhost:11211']))
	for server in stats.getServers():
		print server.__dict__