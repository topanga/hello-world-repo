-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Jan 14, 2020 at 11:01 PM
-- Server version: 5.0.96-community
-- PHP Version: 5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `onpick_test`
--

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE IF NOT EXISTS `employees` (
  `emp_id` int(11) NOT NULL auto_increment,
  `sup_id` int(11) NOT NULL default '0',
  `login` varchar(50) collate utf8_unicode_ci NOT NULL,
  `pwd` varchar(50) collate utf8_unicode_ci NOT NULL,
  `emp_title` varchar(11) collate utf8_unicode_ci NOT NULL default '',
  PRIMARY KEY  (`emp_id`),
  KEY `sup_id` (`sup_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `employee`
--

INSERT INTO `employees` (`emp_id`, `sup_id`, `login`, `pwd`, `emp_title`) VALUES
(1, 0, 'potus', 'db89865da0819ad44af0032dd63a7d7b', 'pres');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
