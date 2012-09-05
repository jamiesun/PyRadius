#coding:utf-8
from pyrad import tools
from pyrad.packet import AuthPacket
from pyrad.packet import AcctPacket
from pyrad.packet import AccessRequest
from pyrad.packet import AccessAccept
from pyrad.packet import AccountingRequest
from settings import vendor_cfg
from settings import log
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
            log.error("set_filter_id error,%s"%(str(e)))        

    def set_special_str(self,vendor,name,value):
        if not value:return
        try:
            if not vendor_cfg.has_key(int(vendor)):
                return
            key = vendor_cfg[int(vendor)][name]
            if key:
                self.AddAttribute(key,tools.EncodeString(value))
        except Exception, e:
            log.error("set_special error,vendor=%s,name=%s,value=%s;err=%s"\
                %(vendor,name,value,str(e)))

    def set_special_int(self,vendor,name,value):
        try:
            if not vendor_cfg.has_key(int(vendor)):
                return
            key = vendor_cfg[int(vendor)][name]
            self.AddAttribute(key,tools.EncodeInteger(value))
        except Exception, e:
            log.error("set_special error,vendor=%s,name=%s,value=%s;err=%s"\
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


def is_valid_date(dstr1,dstr2):
    d1 = datetime.datetime.strptime("%s 00:00:00"%dstr1,"%Y-%m-%d %H:%M:%S")
    d2 = datetime.datetime.strptime("%s 23:59:59"%dstr2,"%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    return now >= d1 and now <= d2




