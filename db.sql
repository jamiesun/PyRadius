-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.5-m8 - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL version:             7.0.0.4160
-- Date/time:                    2012-08-31 12:18:28
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
  `id` varchar(15) NOT NULL,
  `ip_addr` varchar(15) NOT NULL,
  `name` varchar(64) NOT NULL,
  `auth_secret` varchar(31) NOT NULL,
  `acct_secret` varchar(31) NOT NULL,
  `vendor_id` int(9) NOT NULL COMMENT '厂商标识',
  `time_type` int(1) NOT NULL COMMENT '时区类型，0表示标准时区，北京时间，1表示时区和时间同区',
  `status` int(1) NOT NULL COMMENT '0：表示正常；1：表示停用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_addr` (`ip_addr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_nas_node
DROP TABLE IF EXISTS `rad_nas_node`;
CREATE TABLE IF NOT EXISTS `rad_nas_node` (
  `node_id` varchar(32) NOT NULL,
  `ip_addr` varchar(15) NOT NULL,
  PRIMARY KEY (`node_id`,`ip_addr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_node
DROP TABLE IF EXISTS `rad_node`;
CREATE TABLE IF NOT EXISTS `rad_node` (
  `id` varchar(32) NOT NULL,
  `name` varchar(64) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_opr
DROP TABLE IF EXISTS `rad_opr`;
CREATE TABLE IF NOT EXISTS `rad_opr` (
  `id` varchar(32) NOT NULL,
  `node_id` varchar(32) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `password` varchar(32) NOT NULL,
  `type` int(1) NOT NULL COMMENT '0：表示普通操作员；1：表示组织管理员',
  `ip_addr` varchar(15) DEFAULT NULL,
  `status` int(1) NOT NULL COMMENT '0：表示正常；1：表示停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_opr_log
DROP TABLE IF EXISTS `rad_opr_log`;
CREATE TABLE IF NOT EXISTS `rad_opr_log` (
  `id` varchar(32) NOT NULL,
  `opr_id` varchar(32) NOT NULL,
  `user_id` varchar(32) DEFAULT NULL,
  `node_id` varchar(32) NOT NULL,
  `ip_addr` varchar(15) NOT NULL,
  `log_time` varchar(19) NOT NULL,
  `log_desc` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_product
DROP TABLE IF EXISTS `rad_product`;
CREATE TABLE IF NOT EXISTS `rad_product` (
  `id` varchar(16) NOT NULL,
  `node_id` varchar(32) NOT NULL,
  `name` varchar(64) NOT NULL,
  `policy` int(1) NOT NULL COMMENT '产品套餐策略：0买断包月，1预付费时长',
  `status` int(1) NOT NULL COMMENT '产品状态：0正常，1停用',
  `fee_num` int(10) NOT NULL COMMENT '计费量，包月为有效月数',
  `fee_price` int(10) NOT NULL COMMENT '计费价格,单位：分',
  `bind_mac` int(1) NOT NULL,
  `bind_vlan` int(1) NOT NULL,
  `concur_number` int(10) NOT NULL,
  `bandwidth_code` varchar(32) DEFAULT NULL COMMENT '下发给bas限速的qos属性编码字母和数组成，首字母不能为数字',
  `input_max_limit` int(10) NOT NULL COMMENT '上行最大速率',
  `output_max_limit` int(10) NOT NULL COMMENT '下行最大速率',
  `input_rate_code` varchar(32) DEFAULT NULL COMMENT '上行qos属性编码',
  `output_rate_code` varchar(32) DEFAULT NULL COMMENT '下行qos属性编码',
  `domain_code` varchar(32) DEFAULT NULL COMMENT '产品状态：0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_roster
DROP TABLE IF EXISTS `rad_roster`;
CREATE TABLE IF NOT EXISTS `rad_roster` (
  `id` varchar(32) NOT NULL,
  `mac_addr` varchar(17) NOT NULL,
  `node_id` varchar(32) NOT NULL,
  `type` int(1) NOT NULL COMMENT '名单类型：0黑名单，1白名单',
  `user_name` varchar(32) DEFAULT NULL,
  `begin_time` varchar(19) NOT NULL,
  `end_time` varchar(19) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mac_addr` (`mac_addr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user
DROP TABLE IF EXISTS `rad_user`;
CREATE TABLE IF NOT EXISTS `rad_user` (
  `id` varchar(32) NOT NULL,
  `user_name` varchar(32) NOT NULL,
  `user_cname` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `node_id` varchar(32) NOT NULL,
  `product_id` varchar(16) NOT NULL,
  `group_id` varchar(10) NOT NULL,
  `opr_id` varchar(32) DEFAULT NULL,
  `auth_begin_date` varchar(10) NOT NULL,
  `auth_end_date` varchar(10) NOT NULL,
  `mobile` varchar(32) DEFAULT NULL,
  `idcard` varchar(32) DEFAULT NULL,
  `install_address` varchar(128) NOT NULL,
  `create_time` varchar(19) NOT NULL,
  `status` int(10) NOT NULL COMMENT '用户状态（0:预定 1:有效 2：停机 3：销户 4：到期）',
  `user_control` int(1) NOT NULL COMMENT '是否使用用户控制(0/1,不使用/使用)',
  `user_mac` int(1) NOT NULL COMMENT '是否绑定mac地址(0/1,不绑定/绑定)',
  `user_vlan` int(1) NOT NULL COMMENT '是否绑定vlan(0/1,不绑定/绑定)',
  `user_concur_number` int(10) NOT NULL COMMENT '并发数(0为不限制)',
  `mac_addr` varchar(17) DEFAULT NULL,
  `vlan_id` int(10) DEFAULT NULL,
  `vlan_id2` int(10) DEFAULT NULL,
  `ip_address` varchar(15) DEFAULT NULL,
  `domain_code` varchar(6) DEFAULT NULL,
  `balance` int(10) NOT NULL COMMENT '用户余额',
  `time_length` int(10) NOT NULL COMMENT '用户所剩时长',
  `basic_fee` int(10) NOT NULL COMMENT '用户基本费',
  `user_desc` varchar(128) DEFAULT NULL,
  `salesman_code` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name` (`user_name`),
  KEY `node_id` (`node_id`),
  KEY `group_id` (`group_id`),
  KEY `auth_begin_date` (`auth_begin_date`),
  KEY `auth_end_date` (`auth_end_date`),
  KEY `create_time` (`create_time`),
  KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_acct
DROP TABLE IF EXISTS `rad_user_acct`;
CREATE TABLE IF NOT EXISTS `rad_user_acct` (
  `id` varchar(32) NOT NULL,
  `node_id` varchar(32) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `acct_start_time` varchar(19) NOT NULL,
  `acct_stop_time` varchar(19) NOT NULL,
  `acct_session_time` int(10) NOT NULL,
  `acct_fee` int(10) NOT NULL,
  `actual_fee` int(10) NOT NULL,
  `acct_time` varchar(19) NOT NULL,
  `is_deduct` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_bill
DROP TABLE IF EXISTS `rad_user_bill`;
CREATE TABLE IF NOT EXISTS `rad_user_bill` (
  `id` varchar(32) NOT NULL,
  `fee_type` int(1) NOT NULL,
  `fee_value` int(10) NOT NULL,
  `node_id` varchar(32) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `opr_id` varchar(32) NOT NULL,
  `bill_desc` varchar(512) NOT NULL,
  `bill_time` varchar(19) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_group
DROP TABLE IF EXISTS `rad_user_group`;
CREATE TABLE IF NOT EXISTS `rad_user_group` (
  `id` varchar(32) NOT NULL,
  `node_id` varchar(32) NOT NULL,
  `name` varchar(64) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table pyradius.rad_user_order
DROP TABLE IF EXISTS `rad_user_order`;
CREATE TABLE IF NOT EXISTS `rad_user_order` (
  `id` varchar(32) NOT NULL,
  `user_name` varchar(32) NOT NULL,
  `product_id` varchar(16) NOT NULL,
  `auth_begin_date` varchar(10) NOT NULL,
  `auth_end_date` varchar(10) NOT NULL,
  `operate_time` varchar(19) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
