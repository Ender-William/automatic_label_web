/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : localhost:3306
 Source Schema         : AutoLabel

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 01/04/2023 13:53:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `username` varchar(200) NOT NULL,
  `passwd` varchar(200) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `login_state` varchar(2) DEFAULT NULL,
  `account_state` varchar(2) NOT NULL,
  PRIMARY KEY (`username`,`phone`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of account
-- ----------------------------
BEGIN;
INSERT INTO `account` (`username`, `passwd`, `phone`, `login_state`, `account_state`) VALUES ('123', '123', '123', '0', '1');
INSERT INTO `account` (`username`, `passwd`, `phone`, `login_state`, `account_state`) VALUES ('admin', 'admin123', '+8612345678909', '1', '1');
COMMIT;

-- ----------------------------
-- Table structure for credits
-- ----------------------------
DROP TABLE IF EXISTS `credits`;
CREATE TABLE `credits` (
  `username` varchar(255) NOT NULL,
  `credits` varchar(30) NOT NULL,
  `onlineTime` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of credits
-- ----------------------------
BEGIN;
INSERT INTO `credits` (`username`, `credits`, `onlineTime`) VALUES ('123', '10000', '0000-00-00');
INSERT INTO `credits` (`username`, `credits`, `onlineTime`) VALUES ('admin', '9178', '0000-00-00');
COMMIT;

-- ----------------------------
-- Table structure for log
-- ----------------------------
DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `username` varchar(255) NOT NULL,
  `time` varchar(255) DEFAULT NULL,
  `operate` longtext,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for model
-- ----------------------------
DROP TABLE IF EXISTS `model`;
CREATE TABLE `model` (
  `model` varchar(64) NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`model`,`path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of model
-- ----------------------------
BEGIN;
INSERT INTO `model` (`model`, `path`) VALUES ('five_gesture', '/weight/five_gesture.pt');
INSERT INTO `model` (`model`, `path`) VALUES ('five_gesture_en', '/weight/five_gesture_en.pt');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
