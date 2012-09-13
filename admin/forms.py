#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from web import form
from utils import get_db
import models

db = get_db()

def node_seq():
    nodes = db.query(models.RadNode)
    return [(node.id,node.name) for node in nodes]

def nas_seq():
    nass = db.query(models.RadNas).filter(models.RadNas.status == 0)
    return [(nas.ip_addr,nas.ip_addr) for nas in nass]

def product_seq():
    products = db.query(models.RadProduct).filter(models.RadProduct.status == 0)
    return [(product.id,product.name) for product in products]







is_email = form.regexp('[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$',"无效的email格式")
is_chars = form.regexp("^[A-Za-z]+$","必须是英文字符串")
is_alphanum = lambda x:form.regexp("^[A-Za-z0-9]{%s}$"%x,"必须是长度为%s的数字字母组合"%x)
is_alphanum2 = lambda x,y:form.regexp("^[A-Za-z0-9]{%s,%s}$"%(x,y),"必须是长度为%s到%s的数字字母组合"%(x,y))
is_number = form.regexp("^[0-9]*$","必须是数字")
is_cn = form.regexp("^[\u4e00-\u9fa5],{0,}$","必须是汉字")
is_url = form.regexp('[a-zA-z]+://[^\s]*',"无效的url")
is_phone = form.regexp('^(\(\d{3,4}\)|\d{3,4}-)?\d{7,8}$',"无效的电话号码")
is_idcard = form.regexp('^\d{15}$|^\d{18}$|^\d{17}[Xx]$',"无效的身份证号码")
is_ip = form.regexp("\d+\.\d+\.\d+\.\d+","无效ip")
is_rmb = form.regexp('^(([1-9]\d*)|0)(\.\d{1,2})?$',"无效的人民币金额")
len_of = lambda x,y:form.regexp(".{%s,%s}$"%(x,y),"长度必须为%s到%s"%(x,y))


input_style = {"class":"text-input large-input"}
button_style = {"class":"button"}

node_add_form = form.Form(
    form.Textbox("node_id",is_alphanum(6),description="节点编号:(由定长6位数字或字母组成）",**input_style),
    form.Textbox("node_name", len_of(1,32),description="节点名称：（1-32个汉字以内）",**input_style),
    form.Textbox("opr_name",is_alphanum2(6,32), description="管理员名称：（6-32位不定长数字或字母组成）",**input_style),
    form.Textbox("opr_ip", description="管理员工作IP:（如192.168.1.1）",**input_style),
    form.Password("opr_passwd", is_alphanum2(6,20),description="管理员密码：（密码由6-20个字符组成）",**input_style),
    form.Password("opr_passwd2", is_alphanum2(6,20),description="管理员密码确认",**input_style),
    form.Textarea("node_desc", len_of(0,254),description="节点描述：（127个汉字以内）", rows="5",**input_style),
    form.Dropdown("nas_bind", nas_seq(), description="Nas绑定",size=8,multiple="true"),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
    validators = [
        form.Validator("密码确认不符", lambda i: i.opr_passwd == i.opr_passwd2)]
)

node_update_form = form.Form(
    form.Textbox("node_id",description="节点编号:(由定长6位数字或字母组成）",readonly="readonly",**input_style),
    form.Textbox("node_name", len_of(1,32),description="节点名称：（1-32个汉字以内）",**input_style),
    form.Hidden("opr_id",description="管理员名称：（6-32位不定长数字或字母组成）"),
    form.Textbox("opr_name",is_alphanum2(6,32), description="管理员名称：（6-32位不定长数字或字母组成）",**input_style),
    form.Textbox("opr_ip", description="管理员工作IP:（如192.168.1.1）",**input_style),
    form.Password("opr_passwd", is_alphanum2(6,20),description="管理员密码：（密码由6-20个字符组成）",**input_style),
    form.Textarea("node_desc", len_of(0,254),description="节点描述：（127个汉字以内）", rows="5",**input_style),
    form.Dropdown("nas_bind", nas_seq(), description="Nas绑定",size=8,multiple="true"),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)


group_add_form = form.Form(
    form.Textbox("node_id",description="节点编号:(由定长6位数字或字母组成）",readonly="readonly",**input_style),
    form.Textbox("group_id", is_alphanum2(1,10),description="用户组编码：（由10位不定长的字母或数字组合）",**input_style),
    form.Textbox("group_name",len_of(1,32), description="用户组名称：（32个汉字以内）",**input_style),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)

group_update_form = form.Form(
    form.Textbox("node_id",description="节点编号:(由定长6位数字或字母组成）",readonly="readonly",**input_style),
    form.Textbox("group_id",description="用户组编码：（由10位不定长的字母或数字组合）",readonly="readonly",**input_style),
    form.Textbox("group_name",len_of(1,32), description="用户组名称：（32个汉字以内）",**input_style),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)




nas_add_form = form.Form(
    form.Textbox("ip_addr",is_ip,description="IP地址：",**input_style),
    form.Textbox("name", len_of(1,32),description="名称：（32个汉字以内）",**input_style),
    form.Textbox("auth_secret",is_alphanum2(6,31), description="认证密钥 ：（由6-31位内字母开头，字母和数字组合）",**input_style),
    form.Textbox("acct_secret", is_alphanum2(6,31),description="计费密钥 ：（由6-31位内字母开头，字母和数字组合）",**input_style),
    form.Textbox("vendor_id", is_number,description="厂家标识：",**input_style),
    form.Dropdown("time_type",  [(0,"标准时区/北京时间"),(1,"北京时区/北京时间")],description="时区/时间类型："),
    form.Dropdown("status",  [(0,"正常"),(1,"停用")],description="状态：（正常|停用）"),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)

nas_update_form = form.Form(
    form.Hidden("id",readonly="readonly"),
    form.Textbox("ip_addr",description="IP地址：",readonly="readonly",**input_style),
    form.Textbox("name", len_of(1,32),description="名称：（32个汉字以内）",**input_style),
    form.Textbox("auth_secret",is_alphanum2(6,31), description="认证密钥 ：（由6-31位内字母开头，字母和数字组合）",**input_style),
    form.Textbox("acct_secret", is_alphanum2(6,31),description="计费密钥 ：（由6-31位内字母开头，字母和数字组合）",**input_style),
    form.Textbox("vendor_id", is_number,description="厂家标识：",**input_style),
    form.Dropdown("time_type",  [(0,"标准时区/北京时间"),(1,"北京时区/北京时间")],description="时区/时间类型："),
    form.Dropdown("status",  [(0,"正常"),(1,"停用")],description="状态：（正常|停用）"),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)

product_add_form = form.Form(
    form.Textbox("id", is_alphanum2(6,32),description="产品套餐编号：（6-32个字母数字组合以内）",**input_style),
    form.Textbox("name", len_of(1,32),description="产品套餐名称：（32个汉字以内）",**input_style),
    form.Dropdown("policy", [(0,"买断包月"),(1,"预付费时长")],description="产品套餐策略：(买断包月|预付费时长)"),
    form.Textbox("fee_num", is_number,description="产品买断月数（包月）",**input_style),
    form.Textbox("fee_price",is_rmb, description="产品总价格（包月）/每小时价格（计时）：（单位：元）",**input_style),
    form.Textbox("concur_number",is_number, description="用户并发数：（0表示不限定|并发数不能超过20）",**input_style),
    form.Radio("bind_mac", [(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定MAC地址："),
    form.Radio("bind_vlan", [(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定VLAN/QINQ："),
    form.Textbox("bandwidth_code", is_alphanum2(0,8),description="限速属性编码：（字母开头,数字和字母组成,最大8位）",**input_style),
    form.Textbox("input_max_limit",is_number, description="上行最大速率：（单位:bps,2M=2097152）",**input_style),
    form.Textbox("output_max_limit",is_number, description="下行最大速率：（单位:bps,4M=4194304）",**input_style),
    form.Textbox("input_rate_code", is_alphanum2(0,20),description="上行速率编码：（20位内字符组成）",**input_style),
    form.Textbox("output_rate_code", is_alphanum2(0,20),description="下行速率编码：（20位内字符组成）",**input_style),
    form.Textbox("domain_code", is_alphanum2(0,32),description="产品域：",**input_style),
    form.Dropdown("status",  [(0,"正常"),(1,"停用")],description="状态：（正常|停用）",value=0),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)

product_update_form = form.Form(
    form.Textbox("id", description="产品套餐编号：（6-32个字母数字组合以内）",readonly="readonly",**input_style),
    form.Textbox("name", len_of(1,32),description="产品套餐名称：（32个汉字以内）",**input_style),
    form.Dropdown("policy", [(0,"买断包月"),(1,"预付费时长")],description="产品套餐策略：(买断包月|预付费时长)",disabled="disabled"),
    form.Textbox("fee_num", is_number,description="产品买断月数（包月）",**input_style),
    form.Textbox("fee_price",is_rmb, description="产品总价格（包月）/每小时价格（计时）：（单位：元）",**input_style),
    form.Textbox("concur_number",is_number, description="用户并发数：（0表示不限定|并发数不能超过20）",**input_style),
    form.Radio("bind_mac", [(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定MAC地址："),
    form.Radio("bind_vlan", [(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定VLAN/QINQ："),
    form.Textbox("bandwidth_code", is_alphanum2(0,8),description="限速属性编码：（字母开头,数字和字母组成,最大8位）",**input_style),
    form.Textbox("input_max_limit",is_number, description="上行最大速率：（单位:bps,2M=2097152）",**input_style),
    form.Textbox("output_max_limit",is_number, description="下行最大速率：（单位:bps,4M=4194304）",**input_style),
    form.Textbox("input_rate_code", is_alphanum2(0,20),description="上行速率编码：（20位内字符组成）",**input_style),
    form.Textbox("output_rate_code", is_alphanum2(0,20),description="下行速率编码：（20位内字符组成）",**input_style),
    form.Textbox("domain_code", is_alphanum2(0,32),description="产品域：",**input_style),
    form.Dropdown("status",  [(0,"正常"),(1,"停用")],description="状态：（正常|停用）"),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)


user_add_form = form.Form(
    form.Textbox("node_id",description="节点：",readonly="readonly",**input_style),
    form.Textbox("user_name",is_alphanum2(6,32),description="上网帐号：（字母和数字组合 6-32位以内）",**input_style),
    form.Textbox("user_cname",len_of(1,32),description="客户名称：（32个汉字以内）",**input_style),
    form.Password("password",is_alphanum2(6,20),description="上网密码(6-20字母数字)：",**input_style),
    form.Dropdown("group_id",[],description="选择用户组："),
    form.Dropdown("product_id",product_seq(),description="选择产品套餐："),
    form.Dropdown("status", [(0,"未生效"),(1,"有效"),(2,"停机"),(3,"销户"),(4,"到期")],description="用户状态："),
    form.Textbox("auth_begin_date",description="生效日期：",**input_style),
    form.Textbox("auth_end_date",description="截止日期：",**input_style),
    form.Radio("user_control",[(0,"不使用"),(1,"使用")],value=0,description="是否使用用户绑定策略："),
    form.Textbox("concur_number",is_number,value=0,description="并发数：（0表示不限定|并发数不能超过20）",**input_style),
    form.Radio("user_vlan",[(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定VLAN："),
    form.Radio("user_mac",[(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定MAC："),
    form.Textbox("ip_addr",description="IP地址：",**input_style),
    form.Textbox("install_address",len_of(1,128),description="装机地址：",**input_style),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)

user_update_form = form.Form(
    form.Hidden("id",readonly="readonly"),
    form.Textbox("node_id",description="节点：",readonly="readonly",**input_style),
    form.Textbox("user_name",description="上网帐号：（字母和数字组合 6-32位以内）",readonly="readonly",**input_style),
    form.Textbox("user_cname",len_of(1,32),description="客户名称：（32个汉字以内）",**input_style),
    form.Password("password",is_alphanum2(6,20),description="上网密码(6-20字母数字)：",**input_style),
    form.Dropdown("group_id",[],description="选择用户组："),
    form.Dropdown("product_id",product_seq(),description="选择产品套餐："),
    form.Dropdown("status", [(0,"未生效"),(1,"有效"),(2,"停机"),(3,"销户"),(4,"到期")],description="用户状态："),
    form.Textbox("auth_begin_date",description="生效日期：",**input_style),
    form.Textbox("auth_end_date",description="截止日期：",**input_style),
    form.Radio("user_control",[(0,"不使用"),(1,"使用")],value=0,description="是否使用用户绑定策略："),
    form.Textbox("concur_number",is_number,value=0,description="并发数：（0表示不限定|并发数不能超过20）",**input_style),
    form.Radio("user_vlan",[(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定VLAN："),
    form.Radio("user_mac",[(0,"不绑定"),(1,"绑定")],value=0,description="是否绑定MAC："),
    form.Textbox("ip_addr",description="IP地址：",**input_style),
    form.Textbox("install_address",len_of(1,128),description="装机地址：",**input_style),
    form.Button("submit", type="submit",html="<b>提交</b>",**button_style),
)