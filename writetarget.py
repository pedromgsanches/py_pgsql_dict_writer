####################################
### writetarget.py 
####################################

import psycopg2, json,datetime, re
from get_config import get_config
import logwriter as lw

# CLASS TARGET WRITE PGSQL #####################################################################################
class target_pgsql:
  def __init__(self):
    # GET CONNECT STRING -> TARGET DATABASE
    self.connect_string = get_config().target_conn()
    try:
      self.db_connection = psycopg2.connect(self.connect_string)
      self.db_cursor = self.db_connection.cursor()
      lw.log.debug("Conn2ected to target Database: " + self.connect_string)
    except Exception as e:
      lw.log.error("Error connecting do Database:" + str(e))

  def __del__(self):
    self.db_connection.close()

# FUNCTION TO RECEIVE DATA AND WRITE IT TO TARGET DB
  def write(self,input_metric,input_tuple):
    lw.log.debug('Start metric processing')
    lw.log.debug("Write call started : metric="+ input_metric)
    self.metric = input_metric
    self.insert_tuple = input_tuple
    self.metric_conf = get_config().table_conf()
    self.metric_prefix = self.metric_conf[0]
    self.metric_suffix = self.metric_conf[1]

    SQL = "INSERT INTO "+self.metric_prefix+self.metric+self.metric_suffix+" ("
    keycount = 0
    for key in self.insert_tuple[0].items():
        if keycount>0:
          SQL = SQL + ", "
        SQL = SQL + key[0]
        keycount=keycount+1
    SQL = SQL + ") VALUES ("
    keycount = 0
    for key in self.insert_tuple[0].items():
        if keycount>0:
          SQL = SQL + ", "
        SQL = SQL + "%s"
        keycount=keycount+1
    SQL = SQL + ")"
    lw.log.debug('sql: ' + SQL)
    COUNTROWS=0
    for insert_dict in self.insert_tuple:
      VALUES=()
      COUNTROWS=COUNTROWS+1
      for value in insert_dict.items():
        VALUES=VALUES+(value[1],)
      lw.log.debug('INSERT_TUPLE= %s' % (VALUES,))
      try:
        self.db_cursor.execute(SQL,VALUES)
      except Exception as e:
        lw.log.error('(Error inserting on: ' + input_metric + ')' + str(e))
    try:
      self.db_connection.commit()
      lw.log.info("metric=" + input_metric + " rows=" + str(COUNTROWS))
    except Exception as e:
      lw.log.error("metric=" + input_metric + " : " + str(e))
    lw.log.debug('Write call ended : metric=' + input_metric)
