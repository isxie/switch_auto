#coding=utf-8
#!/usr/bin/python
import os
import time
import threading

class ping(threading.Thread):
    err = 0
    #初始化ping线程
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.ip = config['ping']
	self.bind = config['bind_ip']
	#self.err = 0
	#self.start()
    def run(self):
        self.start_1();

    def start_1(self):
	while (True):
            if(os.system('ping -c 1 -w 1 '+ self.ip + '> /dev/null')==0):
                self.del_err()
            else:
                self.err+=1
            time.sleep(1)
    
    def del_err(self):
        self.err = 0
     
    def get_err(self):
        return self.err

    def get_bind_ping(self):
	if(os.system('ping -c 1 -w 1 '+ self.bind + '> /dev/null')==0):
	   return True
        

