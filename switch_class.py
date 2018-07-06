#coding=utf-8
#!/usr/bin/python
#交换机控制类

import telnetlib
import time
class switch():
    shutdown_int = False
    host = ''
    user = ''
    passwd = ''
    port =''
    int_model =''
    """docstring for ClassName"""
    #def __init__(self, config):
    #    pass
        #self.host=config['host']
        #self.user=config['user']
        #self.passwd=config['passwd']
        #self.int=config['int']
        
    def set_config(self,config):
        self.host=config['host']
        self.user=config['user']
        self.passwd=config['passwd']
        self.int_model='GigabitEthernet' if config['int_model'] == 'GE' else 'XGigabitEthernet'
        self.port =config['int']
    
    def run(self):
        self.get_shutdown_switch()
        if self.shutdown_int != False:
            self.off_int_all()
            self.on_int(self.shutdown_int)

    def is_shutdown(self):
    	tn = telnetlib.Telnet(self.host, port=23, timeout=50)
	tn.read_until('Username:')
	tn.write(self.user+ '\n')
	tn.write(self.passwd + '\n')
	time.sleep(1)
	tn.write('system' + '\n')  
	tn.write('interface '+self.int_model+'0/0/'+self.port + '\n')
	tn.write('display this' + '\n')
	time.sleep(1)
	result1 = tn.read_very_eager()
	#print result1
	if result1.find("shutdown") >= 0:
	    return True
	tn.close()

    def	get_shutdown_switch(self):
        for key in self.int:
            if self.is_shutdown(self.int[key]) == True:
                self.shutdown_int = self.int[key]
        

    def off_int(self):
        tn = telnetlib.Telnet(self.host, port=23, timeout=50)
        tn.read_until('Username:')
        tn.write(self.user+ '\n')
        tn.write(self.passwd + '\n')
        time.sleep(1)
        tn.write('system' + '\n')
        tn.write('interface '+self.int_model+'0/0/'+self.port + '\n')
        tn.write('shutdown' + '\n')
        time.sleep(1)
        result1 = tn.read_very_eager()
        tn.close()
             
    def off_int_all(self):
        for key in self.int:
           self.off_int(self.int[key])

    def on_int(self):
        tn = telnetlib.Telnet(self.host, port=23, timeout=50)
        tn.read_until('Username:')
        tn.write(self.user+ '\n')
        tn.write(self.passwd + '\n')
        time.sleep(1)
        tn.write('system' + '\n')
        tn.write('interface '+self.int_model+'0/0/'+self.port + '\n')
        tn.write('undo shutdown' + '\n')
        time.sleep(1)
        result1 = tn.read_very_eager()
        tn.close()






