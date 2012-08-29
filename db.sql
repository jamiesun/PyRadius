-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.5-m8 - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL version:             7.0.0.4160
-- Date/time:                    2012-08-29 19:23:00
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for pyradius
DROP DATABASE IF EXISTS `pyradius`;
CREATE DATABASE IF NOT EXISTS `pyradius` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `pyradius`;


-- Dumping structure for table pyradius.rad_nas
DROP TABLE IF EXISTS `rad_nas`;
CREATE TABLE IF NOT EXISTS `rad_nas` (
  `IP_ADDR` varchar(15) NOT NULL,
  `NAME` varchar(64) NOT NULL,
  `AUTH_SECRET` varchar(31) NOT NULL,
  `ACCT_SECRET` varchar(31) NOT NULL,
  `NAS_TYPE` int(10) NOT NULL COMMENT 'BAS类型,0代表标准,1代表华为,2代表华三,3代表爱立信，4代表中兴，5代表阿尔卡特,',
  `TIME_TYPE` int(1) NOT NULL COMMENT '时区类型，0表示标准时区，北京时间，1表示时区和时间同区',
  `STATUS` int(1) NOT NULL COMMENT '0：表示正常；1：表示停用',
  PRIMARY KEY (`IP_ADDR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_nas_node
DROP TABLE IF EXISTS `rad_nas_node`;
CREATE TABLE IF NOT EXISTS `rad_nas_node` (
  `NODE_ID` varchar(32) NOT NULL,
  `IP_ADDR` varchar(15) NOT NULL,
  PRIMARY KEY (`NODE_ID`,`IP_ADDR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_node
DROP TABLE IF EXISTS `rad_node`;
CREATE TABLE IF NOT EXISTS `rad_node` (
  `ID` varchar(32) NOT NULL,
  `NAME` varchar(64) NOT NULL,
  `DESC` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_opr
DROP TABLE IF EXISTS `rad_opr`;
CREATE TABLE IF NOT EXISTS `rad_opr` (
  `ID` varchar(32) NOT NULL,
  `NODE_ID` varchar(32) NOT NULL,
  `PASSWORD` varchar(32) NOT NULL,
  `TYPE` int(1) NOT NULL COMMENT '0：表示普通操作员；1：表示组织管理员',
  `NAME` varchar(64) DEFAULT NULL,
  `IP_ADDR` varchar(15) DEFAULT NULL,
  `STATUS` int(1) NOT NULL COMMENT '0：表示正常；1：表示停用',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_opr_log
DROP TABLE IF EXISTS `rad_opr_log`;
CREATE TABLE IF NOT EXISTS `rad_opr_log` (
  `ID` varchar(32) NOT NULL,
  `OPR_ID` varchar(32) NOT NULL,
  `USER_ID` varchar(32) DEFAULT NULL,
  `NODE_ID` varchar(32) NOT NULL,
  `IP_ADDR` varchar(15) NOT NULL,
  `LOG_TIME` varchar(19) NOT NULL,
  `LOG_DESC` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_product
DROP TABLE IF EXISTS `rad_product`;
CREATE TABLE IF NOT EXISTS `rad_product` (
  `ID` varchar(16) NOT NULL,
  `NODE_ID` varchar(32) NOT NULL,
  `NAME` varchar(64) NOT NULL,
  `POLICY` int(1) NOT NULL COMMENT '产品套餐策略：0买断包月，1预付费时长',
  `STATUS` int(1) NOT NULL COMMENT '产品状态：0正常，1停用',
  `FEE_NUM` int(10) NOT NULL COMMENT '计费量，包月为有效月数',
  `FEE_PRICE` int(10) NOT NULL COMMENT '计费价格,单位：分',
  `BIND_MAC` int(1) NOT NULL,
  `BIND_VLAN` int(1) NOT NULL,
  `CONCUR_NUMBER` int(10) NOT NULL,
  `BANDWIDTH_CODE` varchar(32) DEFAULT NULL COMMENT '下发给BAS限速的QOS属性编码字母和数组成，首字母不能为数字',
  `INPUT_MAX_LIMIT` int(10) NOT NULL COMMENT '上行最大速率',
  `OUTPUT_MAX_LIMIT` int(10) NOT NULL COMMENT '下行最大速率',
  `INPUT_RATE_CODE` varchar(32) DEFAULT NULL COMMENT '上行QOS属性编码',
  `OUTPUT_RATE_CODE` varchar(32) DEFAULT NULL COMMENT '下行QOS属性编码',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_roster
DROP TABLE IF EXISTS `rad_roster`;
CREATE TABLE IF NOT EXISTS `rad_roster` (
  `MAC_ADDR` varchar(17) NOT NULL,
  `NODE_ID` varchar(32) NOT NULL,
  `TYPE` int(1) NOT NULL COMMENT '名单类型：0黑名单，1白名单',
  `USER_NAME` varchar(32) DEFAULT NULL,
  `BEGIN_TIME` varchar(19) NOT NULL,
  `END_TIME` varchar(19) NOT NULL,
  PRIMARY KEY (`MAC_ADDR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user
DROP TABLE IF EXISTS `rad_user`;
CREATE TABLE IF NOT EXISTS `rad_user` (
  `ID` varchar(32) NOT NULL,
  `USER_NAME` varchar(32) NOT NULL,
  `USER_CNAME` varchar(64) NOT NULL,
  `PASSWORD` varchar(64) NOT NULL,
  `NODE_ID` varchar(32) NOT NULL,
  `PRODUCT_ID` varchar(16) NOT NULL,
  `GROUP_ID` varchar(10) NOT NULL,
  `OPR_ID` varchar(32) DEFAULT NULL,
  `AUTH_BEGIN_DATE` varchar(10) NOT NULL,
  `AUTH_END_DATE` varchar(10) NOT NULL,
  `MOBILE` varchar(32) DEFAULT NULL,
  `IDCARD` varchar(32) DEFAULT NULL,
  `INSTALL_ADDRESS` varchar(128) NOT NULL,
  `CREATE_TIME` varchar(19) NOT NULL,
  `STATUS` int(10) NOT NULL COMMENT '用户状态（0:预定 1:有效 2：停机 3：销户 4：到期）',
  `USER_CONTROL` int(1) NOT NULL COMMENT '是否使用用户控制(0/1,不使用/使用)',
  `USER_MAC` int(1) NOT NULL COMMENT '是否绑定MAC地址(0/1,不绑定/绑定)',
  `USER_VLAN` int(1) NOT NULL COMMENT '是否绑定VLAN(0/1,不绑定/绑定)',
  `USER_CONCUR_NUMBER` int(10) NOT NULL COMMENT '并发数(0为不限制)',
  `MAC_ADDR` varchar(17) DEFAULT NULL,
  `VLAN_ID` int(10) DEFAULT NULL,
  `VLAN_ID2` int(10) DEFAULT NULL,
  `IP_ADDRESS` varchar(15) DEFAULT NULL,
  `DOMAIN_CODE` varchar(6) DEFAULT NULL,
  `BALANCE` int(10) NOT NULL COMMENT '用户余额',
  `TIME_LENGTH` int(10) NOT NULL COMMENT '用户所剩时长',
  `BASIC_FEE` int(10) NOT NULL COMMENT '用户基本费',
  `USER_DESC` varchar(128) DEFAULT NULL,
  `SALESMAN_CODE` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `USER_NAME` (`USER_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_acct
DROP TABLE IF EXISTS `rad_user_acct`;
CREATE TABLE IF NOT EXISTS `rad_user_acct` (
  `ID` varchar(32) NOT NULL,
  `NODE_ID` varchar(32) NOT NULL,
  `USER_ID` varchar(32) NOT NULL,
  `ACCT_START_TIME` varchar(19) NOT NULL,
  `ACCT_STOP_TIME` varchar(19) NOT NULL,
  `ACCT_SESSION_TIME` int(10) NOT NULL,
  `ACCT_FEE` int(10) NOT NULL,
  `ACTUAL_FEE` int(10) NOT NULL,
  `ACCT_TIME` varchar(19) NOT NULL,
  `IS_DEDUCT` int(1) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_bill
DROP TABLE IF EXISTS `rad_user_bill`;
CREATE TABLE IF NOT EXISTS `rad_user_bill` (
  `ID` varchar(32) NOT NULL,
  `FEE_TYPE` int(1) NOT NULL,
  `FEE_VALUE` int(10) NOT NULL,
  `NODE_ID` varchar(32) NOT NULL,
  `USER_ID` varchar(32) NOT NULL,
  `OPR_ID` varchar(32) NOT NULL,
  `BILL_DESC` varchar(512) NOT NULL,
  `BILL_TIME` varchar(19) NOT NULL,
  `STATUS` int(1) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_group
DROP TABLE IF EXISTS `rad_user_group`;
CREATE TABLE IF NOT EXISTS `rad_user_group` (
  `ID` varchar(32) NOT NULL,
  `NAME` varchar(64) NOT NULL,
  `DESC` varchar(255) DEFAULT NULL,
  `STATUS` int(1) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_order
DROP TABLE IF EXISTS `rad_user_order`;
CREATE TABLE IF NOT EXISTS `rad_user_order` (
  `USER_NAME` varchar(32) NOT NULL,
  `PRODUCT_ID` varchar(16) NOT NULL,
  `AUTH_BEGIN_DATE` varchar(10) NOT NULL,
  `AUTH_END_DATE` varchar(10) NOT NULL,
  `OPERATE_TIME` varchar(19) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
