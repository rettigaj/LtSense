#!/usr/bin/env python

#import sqlite3
import time
from xml.dom.minidom import Document
import fcntl, socket, struct 

class AbstractDataHandler(object):

  def __init__(self):
    object.__init__(self)
    self.transports = None
    self.identifier = None 
    #Network Adapter for uniqueIds
    self.adapter = 'eth0'
    self._security = None

  def render_data(self,sensors):
    pass
    
  def _init_security(self,security):
    self._security = security
    security.initalize_security()

  security = property(lambda self : self._security,lambda self,value:self._init_security(value) )    

  def transport_data(self,payload):
    if self.transports != None:
      for t in self.transports:
        t.send_package(payload)
   
  #Taken from http://stackoverflow.com/questions/159137/getting-mac-address
  """"@property
  def unique_id(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', self.adapter[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]"""

"""       
class SQLiteDataHandler(AbstractDataHandler):
  
  def __init__(self):
    AbstractDataHandler.__init__(self)   
    self.__conn = None

  def _getDataFile(self):
    return self.sqlFile
  
  def _setDataFile(self,df):
      self.sqlFile = df
      self.__get_cursor().execute("CREATE TABLE IF NOT EXISTS sensor_data (stamp DATETIME,type TEXT, sensor_id Text,date Text)")
      self.__conn.commit()      

  dataFile = property(_getDataFile,_setDataFile)

  def __cursor(self):
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
      self.__cursor().execute(
        'INSERT INTO sensor_data VALUES(?,?,?,?)' , (now,s.get_type(),s.get_id(),s.get_data())
        )
      self.__conn.commit()
"""

class GreenOvenDataHandler(AbstractDataHandler):

  def __init__(self):
    AbstractDataHandler.__init__(self)

  def render_data(self,sensors):
    now = time.time()
    doc = Document()
    root = doc.createElement('GreenData')

    pack = doc.createElement('package')
    #Webservice expects time as a long in miliseconds. 
    #time.time() is seconds as a float
    pack.setAttribute("timestamp", "%d" % round(time.time()* 1000) )
    pack.setAttribute("timezone", "UTC")
    pack.setAttribute("id",self.identifier.identify())

    sens = doc.createElement('sensors')

    for s in sensors:
      senNode = doc.createElement('sensor')

      senNode = doc.createElement('sensor')
      senNode.setAttribute('id',s.id)
      senNode.setAttribute('type',s.type)
      senNode.setAttribute('units',s.units)

      ddata = doc.createElement('data')
      ddata.appendChild(doc.createTextNode(s.data))
 
      senNode.appendChild(ddata)
      sens.appendChild(senNode)

    pack.appendChild(sens)
    
    #Data Signature
    if self.security != None:
      signature = self.security.sign_data(pack.toxml())
      sig = doc.createElement('signature')
      sig.appendChild(doc.createTextNode(signature))
      root.appendChild(pack)
      root.appendChild(sig)
    else:
      root.appendChild(pack)
      
    doc.appendChild(root)
    self.transport_data(doc.toxml())
    return doc.toxml()

class WaterMLDataHandler(AbstractDataHandler):
 
  def __init__(self,conifg):
    AbstractDataHandler.__init__(self,config)
    
  def render_data(self,sensors):
    pass

