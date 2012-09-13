#coding:utf-8
from pyrad import tools
from pyrad.packet import AuthPacket
from pyrad.packet import AcctPacket
from pyrad.packet import AccessRequest
from pyrad.packet import AccessAccept
from pyrad.packet import AccountingRequest
from settings import vendor_cfg
from settings import radiuslog
import datetime
import hashlib
import six

md5_constructor = hashlib.md5

def ndebug():
    import pdb
    pdb.set_trace()

def encrypt(s,key=128):
    b = bytearray(str(s).encode("utf8"))
    n = len(b) 
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key 
        c1 = b2 % 16
        c2 = b2 // 16 
        c1 = c1 + 65
        c2 = c2 + 65 
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("utf8")

def decrypt(s,key=128):
    c = bytearray(str(s).encode("utf8"))
    n = len(c) 
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("utf8")
    except:
        return "failed"


def is_valid_date(dstr1,dstr2):
    d1 = datetime.datetime.strptime("%s 00:00:00"%dstr1,"%Y-%m-%d %H:%M:%S")
    d2 = datetime.datetime.strptime("%s 23:59:59"%dstr2,"%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    return now >= d1 and now <= d2        


class AuthPacket2(AuthPacket):

    def __init__(self, code=AccessRequest, id=None, secret=six.b(''),
            authenticator=None, **attributes):
        AuthPacket.__init__(self, code, id, secret, authenticator, **attributes)   

    def CreateReply(self, msg=None,**attributes):
        reply = AuthPacket2(AccessAccept, self.id,
            self.secret, self.authenticator, dict=self.dict,
            **attributes)
        if msg:
            reply.set_reply_msg(tools.EncodeString(msg))
        return reply


    def set_reply_msg(self,msg):
        if msg:self.AddAttribute(18,msg)

    def set_framed_ip_addr(self,ipaddr):
        if ipaddr:self.AddAttribute(8,tools.EncodeAddress(ipaddr))

    def set_session_timeout(self,timeout):
        if timeout:self.AddAttribute(27,tools.EncodeInteger(timeout))

    def set_filter_id(self,vendor,filterid):
        if not filterid:return
        try:
            if not vendor_cfg.has_key(int(vendor)):
                return
            if vendor_cfg[int(vendor)]['filter_id']:
                self.AddAttribute(11,tools.EncodeString(filterid))
        except Exception, e:
            radiuslog.error("set_filter_id error,%s"%(str(e)))        

    def set_special_str(self,vendor,name,value):
        if not value:return
        try:
            if not vendor_cfg.has_key(int(vendor)):
                return
            key = vendor_cfg[int(vendor)][name]
            if key:
                self.AddAttribute(key,tools.EncodeString(value))
        except Exception, e:
            radiuslog.error("set_special error,vendor=%s,name=%s,value=%s;err=%s"\
                %(vendor,name,value,str(e)))

    def set_special_int(self,vendor,name,value):
        try:
            if not vendor_cfg.has_key(int(vendor)):
                return
            key = vendor_cfg[int(vendor)][name]
            self.AddAttribute(key,tools.EncodeInteger(value))
        except Exception, e:
            radiuslog.error("set_special error,vendor=%s,name=%s,value=%s;err=%s"\
                %(vendor,name,value,str(e)))            

    def get_nasaddr(self):
        try:return tools.DecodeAddress(self.get(4)[0])
        except:return None
        
    def get_macaddr(self):
        try:return tools.DecodeString(self.get(31)[0]).replace("-",":")
        except:return None

    def get_username(self):
        try:return tools.DecodeString(self.get(1)[0])
        except:return None
        
    def get_vlanids(self):
        try:
            #attr87 = tools.DecodeString(self.get(87)[0])
            return 0,0
        except:return 0,0

    def get_passwd(self):
        try:return self.PwDecrypt(self.get(2)[0])
        except:return None        

    def get_chappwd(self):
        try:return tools.DecodeString(self.get(3)[0])
        except:return None    

    def encrypt_chap(self,password):
        if isinstance(password, six.text_type):
            password = password.encode('utf-8')
        return md5_constructor("%s%s%s"%(self.id,password,self.authenticator)).digest()

    def is_valid_pwd(self,userpwd):
        if not self.get_chappwd():
            pwd = self.get_passwd()
            return pwd == userpwd
        else:
            return self.encrypt_chap(userpwd) == self.get_chappwd()

class AcctPacket2(AcctPacket):
    def __init__(self, code=AccountingRequest, id=None, secret=six.b(''),
            authenticator=None, **attributes):
        AcctPacket.__init__(self, code, id, secret, authenticator, **attributes)

    def get_username(self):
        try:return tools.DecodeString(self.get(1)[0])
        except:return None        

    def get_macaddr(self):
        try:return tools.DecodeString(self.get(31)[0]).replace("-",":")
        except:return None

    def get_nasaddr(self):
        try:return tools.DecodeAddress(self.get(4)[0])
        except:return None

    def get_nasport(self):
        try:return tools.DecodeInteger(self.get(5)[0])
        except:return None

    def get_servicetype(self):
        try:return tools.DecodeInteger(self.get(0)[0])
        except:return None
        
    def get_framedipaddr(self):
        try:return tools.DecodeAddress(self.get(8)[0])
        except:return None

    def get_framednetmask(self):
        try:return tools.DecodeAddress(self.get(9)[0])
        except:return None

    def get_nasclass(self):
        try:return tools.DecodeString(self.get(25)[0])
        except:return None   

    def get_sessiontimeout(self):
        try:return tools.DecodeInteger(self.get(27)[0])
        except:return None

    def get_callingstationid(self):
        try:return tools.DecodeString(self.get(31)[0])
        except:return None   

    def get_acctstatustype(self):
        try:return tools.DecodeInteger(self.get(40)[0])
        except:return None

    def get_acctinputoctets(self):
        try:return tools.DecodeInteger(self.get(42)[0])
        except:return None

    def get_acctoutputoctets(self):
        try:return tools.DecodeInteger(self.get(43)[0])
        except:return None

    def get_acctsessionid(self):
        try:return tools.DecodeString(self.get(44)[0])
        except:return None                                                         

    def get_acctsessiontime(self):
        try:return tools.DecodeInteger(self.get(46)[0])
        except:return None                                                             

    def get_acctinputpackets(self):
        try:return tools.DecodeInteger(self.get(47)[0])
        except:return None                                                       

    def get_acctoutputpackets(self):
        try:return tools.DecodeInteger(self.get(48)[0])
        except:return None           

    def get_acctterminatecause(self):
        try:return tools.DecodeInteger(self.get(49)[0])
        except:return None           

    def get_acctinputgigawords(self):
        try:return tools.DecodeInteger(self.get(52)[0])
        except:return None       

    def get_acctoutputgigawords(self):
        try:return tools.DecodeInteger(self.get(53)[0])
        except:return None                                                         

    def get_eventtimestamp(self,timetype=0):
        try:
            _time = tools.DecodeDate(self.get(55)[0])
            if timetype == 0:
                return datetime.datetime.fromtimestamp(_time).strptime("%Y-%m-%d %H:%M:%S")
            else:
                return datetime.datetime.fromtimestamp(_time-(8*3600)).strptime("%Y-%m-%d %H:%M:%S")
        except:
            return None

    def get_nasporttype(self):
        try:return tools.DecodeInteger(self.get(61)[0])
        except:return None   

    def get_nasportid(self):
        try:return tools.DecodeString(self.get(87)[0])
        except:return None        

    def get_ticket(self):
        return dict(
        username = self.get_username(),
        macaddr = self.get_macaddr(),
        nasaddr = self.get_nasaddr(),
        nasport = self.get_nasport(),
        servicetype = self.get_servicetype(),
        framedipaddr = self.get_framedipaddr(),
        framednetmask = self.get_framednetmask(),
        nasclass = self.get_nasclass(),
        sessiontimeout = self.get_sessiontimeout(),
        callingstationid = self.get_callingstationid(),
        acctstatustype = self.get_acctstatustype(),
        acctinputoctets = self.get_acctinputoctets(),
        acctoutputoctets = self.get_acctoutputoctets(),
        acctsessionid = self.get_acctsessionid(),
        acctsessiontime = self.get_acctsessiontime(),
        acctinputpackets = self.get_acctinputpackets(),
        acctoutputpackets = self.get_acctoutputpackets(),
        acctterminatecause = self.get_acctterminatecause(),
        acctinputgigawords = self.get_acctinputgigawords(),
        acctoutputgigawords = self.get_acctoutputgigawords(),
        eventtimestamp = self.get_eventtimestamp(),
        nasporttype=self.get_nasporttype(),
        nasportid=self.get_nasportid())







