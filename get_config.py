##################
# get_config.py
##################
import json
### Class GET CONFIG from config.json
class get_config():
  def __init__(self):
    with open("config.json","r") as target_file:
      try:
        self.data = json.load(target_file)
        for d in self.data['target_database']:
          self.target_host = d['host']
          self.target_port = d['port']
          self.target_db = d['db']
          self.target_user = d['user']
          # target_type not yet in use // use it for your own purposes. Ex: dev,tst,prd or app,mon,conf or something else
          self.target_type = d['type']
          self.tab_prefix = d['table_prefix']
          self.tab_suffix = d['table_suffix']
      except Exception as e:
        print("ERR(get_target_db): " + str(e))

  def target_conn(self):
    #return(self.target_host,self.target_port,self.target_db,self.target_user)
    connect_string = "host='"+self.target_host+"' port='"+self.target_port+"' dbname='"+self.target_db+"' user='"+self.target_user+"'"
    return(connect_string)
  def table_conf(self):
    return(self.tab_prefix,self.tab_suffix)
