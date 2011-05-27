#!/usr/bin/env python

import sqlite3
import time

class AbstractDataHandler():

  def __init__(self,config):
    pass
    
  def render_data(self,sensors):
    pass

class SQLiteDataHandler(AbstractDataHandler):
  
  def __init__(self,config):
    AbstractDataHandler.__init__(self,config)   
    #todo, get from confi
    self.__conn = None
    self.sqlFile = ('data.sqlite')
    
    self.__get_cursor().execute("CREATE TABLE IF NOT EXISTS sensor_data (stamp DATETIME,type TEXT, sensor_id Text,date Text)")
    self.__conn.commit()

  #def __del__(self):
  #  self.conn.close()

  def __get_cursor(self):
    try:
      if self.__conn == None:
        self.__conn = sqlite3.connect(self.sqlFile)
      return self.__conn.cursor()
    except sqlite3.ProgrammingError:
      self.__conn = sqlite3.connect(self.sqlFile)
      return self.__conn.cursor()

  def render_data(self,sensors):
    now = time.time()
    for s in sensors:
      self.__get_cursor().execute(
        'INSERT INTO sensor_data VALUES(?,?,?,?)' , (now,s.get_type(),s.get_id(),s.get_data())
        )
      self.__conn.commit()
      print(s.get_data())

class WaterMLDataHandler(AbstractDataHandler):
 
  def __init__(self,conifg):
    AbstractDataHandler.__init__(self,config)
    
  def render_data(self,sensors):
    pass

