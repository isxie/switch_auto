#coding=utf-8
#!/usr/bin/python
import thread
import time ,signal
import sys
from switch_class import switch;
from ping_class import ping;

def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit()

def get_status(config,switch):
    status_obj = {};
    for key in config['int_group']:
        int_all = 0
        int_down = 0
        for key2 in config['int_group'][key]:
	    pass
            for key3 in config['int_group'][key][key2]:
                int_all += 1
                config_ = config['SW_'][key2]
                config_['int'] = key3
		switch.set_config(config_)
		#config_.clear()
                if switch.is_shutdown()==True:
		    int_down +=1
		#print config_
        #print int_all
        if int_all == int_down and int_all != 0:
	    if status_obj.has_key('down_group') != False:
	        return False
	    status_obj['down_group'] = key
	else:
	    status_obj['on_group'] = key
	
    if status_obj.has_key('down_group') == False:
	return False
    return  status_obj
            
def shutdown_all (config,switch):
    for key in config['int_group']:
        for key2 in config['int_group'][key]:
            for key3 in config['int_group'][key][key2]:
		config_ = config['SW_'][key2]
                config_['int'] = key3
		switch.set_config(config_)
		switch.off_int()
def on_all (config,switch,on_int):
	for key2 in config['int_group'][on_int['down_group']]:
	    for key3 in config['int_group'][on_int['down_group']][key2]:
	        config_ = config['SW_'][key2]
		config_['int'] = key3
		switch.set_config(config_)
		switch.on_int()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    #配置字典
    config = {
    #交换机组
    'SW_':{'SW1':{
                'host':'192.10.30.217',
                'user':'',
                'passwd':'',
                'int_model':'GE'#网口模式
                },
            'SW2':{
                'host':'192.10.30.218',
                'user':'',
                'passwd':'',
                'int_model':'XGE'#网口模式
                }
    },
    #端口组,格式{'交换机':['端口1'],['端口2']},支持无限个端口和交换机
    #两个端口组需有一组全部shutdown,
    'int_group':{
            'group1':{'SW1':['33'],'SW2':['34']},
            'group2':{'SW1':['35','36']}
    },
    'ping':'',#监控ip
    'timeout':10, #ping 丢包持续多少秒则切换端口
    'bind_ip':''#依赖ip
    };
    switch = switch()
    #开始运行
    #switch = switch(config)
    ping = ping(config)
    ping.setDaemon(True)
    ping.start()
    while (True):
        #print ping.err
        if ping.get_err()>=config['timeout'] and ping.get_bind_ping() == True:
            print 'run.....'
	    is_on = get_status(config,switch)
    	    if is_on != False:
                shutdown_all(config,switch)
                on_all(config,switch,is_on)
            fo = open("log.txt", "a")
            fo.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+\
            '    UP:'+is_on['down_group']+\
            '    Down:' + is_on['on_group']+ "\n")
            fo.close()
            time.sleep(10)
            #print 'end.....'
            ping.del_err()
    #print switch.is_shutdown()
    

