
#####
##### Collects techsupport files from list of devices simultaneously and uploads results to FTP
#####

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException



import devices

def get_ssh_user_pass():
 import getpass
 global ssh_username, ssh_password
 ssh_username = raw_input('Enter a username: ')
 ssh_password = getpass.getpass()


get_ssh_user_pass()

start_time = datetime.now()
from netmiko import ConnectHandler

FTP_SERVER = 'YOUR_FTP_ADDRESS'

def connect_ssh(ip_add):
 try:
  hostname=''
  output=''
  net_connect = ConnectHandler(device_type='alcatel_sros', ip=ip_add, username=ssh_username, password=ssh_password)
  #output = net_connect.send_command('show system information | match  Name')
  #hostname = output.split()[3]
  #print (hostname)
  #print('Connection to device: '+ str(ip_add)+' '+str(hostname) )
  output = net_connect.send_command('show system information | match  Name')
  hostname = output.split()[3]
  print('Connection to device: '+ str(ip_add)+' '+str(hostname) )
  output = net_connect.send_command('admin tech-support '+FTP_SERVER+' '+str(ip_add)+'_'+str(hostname)+'_TS')
  net_connect.disconnect()
 except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
  print(e)
 return output


def threads_conn(function, devices, limit=20):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices)
    return list(f_result)
# devices.all7750_MEN contains a list of network device's management ip
all_done = threads_conn(connect_ssh, devices.all7750_MEN)
#print(all_done)


print(datetime.now() - start_time)











