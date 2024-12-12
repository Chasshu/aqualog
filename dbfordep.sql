-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2024 at 12:25 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aqualog`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `adminid` int(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`adminid`, `username`, `password`) VALUES
(1, 'admin', 'admin123'),
(2, 'danaic', 'fishcatch2024');

-- --------------------------------------------------------

--
-- Table structure for table `bin`
--

CREATE TABLE `bin` (
  `id` int(50) NOT NULL,
  `userid` int(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `vessel` varchar(50) NOT NULL,
  `date` int(11) NOT NULL,
  `reportid` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `catch`
--

CREATE TABLE `catch` (
  `catchid` int(50) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `catch`
--

INSERT INTO `catch` (`catchid`, `name`) VALUES
(1, 'null'),
(2, 'Alamang'),
(3, 'Alimasag'),
(4, 'Alumahan'),
(5, 'Asube'),
(6, 'Bagaong'),
(7, 'Bakoko'),
(8, 'Banak'),
(9, 'Bangus'),
(10, 'Bidbid'),
(11, 'Bikao'),
(12, 'Bisugu'),
(13, 'Duhay'),
(14, 'Espada'),
(15, 'Garopa'),
(17, 'Gulyasan'),
(18, 'Hipon'),
(19, 'Kabayas'),
(20, 'Kandaong'),
(21, 'Lapu Lapu'),
(22, 'Loba'),
(23, 'Lobster'),
(24, 'Lumahan'),
(25, 'Mamale'),
(26, 'Mayatoy'),
(27, 'Pahabela'),
(28, 'Pargo'),
(29, 'Salay batang'),
(30, 'Salay ginto'),
(31, 'Salay-salay'),
(32, 'Salengga'),
(33, 'Samaral'),
(34, 'Sapsap'),
(35, 'Sekoy'),
(36, 'Talakitok'),
(37, 'Tambol'),
(38, 'Tampal'),
(39, 'Tanigue'),
(40, 'Torsilyo'),
(41, 'Twakang'),
(42, 'Yellowfin tuna');

-- --------------------------------------------------------

--
-- Table structure for table `gear`
--

CREATE TABLE `gear` (
  `gearid` int(50) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `gear`
--

INSERT INTO `gear` (`gearid`, `name`) VALUES
(0, 'null'),
(1, 'Net-Pangbarangay'),
(2, 'Net-Pangalimasag'),
(3, 'lambat'),
(4, 'kas-kas'),
(5, 'kawil'),
(6, 'sibid'),
(7, 'payao'),
(8, 'bubu');

-- --------------------------------------------------------

--
-- Table structure for table `landing`
--

CREATE TABLE `landing` (
  `landid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `landing`
--

INSERT INTO `landing` (`landid`, `name`) VALUES
(0, 'null'),
(1, 'Munting Mapino'),
(2, 'Bucana Malaki'),
(3, 'Labac'),
(4, 'others');

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `reportid` int(50) NOT NULL,
  `userid` int(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `vessel` varchar(50) NOT NULL,
  `frequent` int(11) NOT NULL,
  `date` date NOT NULL,
  `catch1` int(11) NOT NULL,
  `catch2` int(11) NOT NULL,
  `catch3` int(11) NOT NULL,
  `catch4` int(11) NOT NULL,
  `catch5` int(11) NOT NULL,
  `volume1` double NOT NULL,
  `volume2` double NOT NULL,
  `volume3` double NOT NULL,
  `volume4` double NOT NULL,
  `volume5` double NOT NULL,
  `site1` int(50) NOT NULL,
  `site2` int(11) NOT NULL,
  `site3` int(11) NOT NULL,
  `site4` int(11) NOT NULL,
  `site5` int(11) NOT NULL,
  `gear1` int(50) NOT NULL,
  `gear2` int(11) NOT NULL,
  `gear3` int(11) NOT NULL,
  `gear4` int(11) NOT NULL,
  `gear5` int(11) NOT NULL,
  `hours1` int(11) NOT NULL,
  `hours2` int(11) NOT NULL,
  `hours3` int(11) NOT NULL,
  `hours4` int(11) NOT NULL,
  `hours5` int(11) NOT NULL,
  `landing1` int(11) NOT NULL,
  `landing2` int(11) NOT NULL,
  `landing3` int(11) NOT NULL,
  `landing4` int(11) NOT NULL,
  `landing5` int(11) NOT NULL,
  `price1` int(11) NOT NULL,
  `price2` int(11) NOT NULL,
  `price3` int(11) NOT NULL,
  `price4` int(11) NOT NULL,
  `price5` int(11) NOT NULL,
  `tempid` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`reportid`, `userid`, `name`, `vessel`, `frequent`, `date`, `catch1`, `catch2`, `catch3`, `catch4`, `catch5`, `volume1`, `volume2`, `volume3`, `volume4`, `volume5`, `site1`, `site2`, `site3`, `site4`, `site5`, `gear1`, `gear2`, `gear3`, `gear4`, `gear5`, `hours1`, `hours2`, `hours3`, `hours4`, `hours5`, `landing1`, `landing2`, `landing3`, `landing4`, `landing5`, `price1`, `price2`, `price3`, `price4`, `price5`, `tempid`) VALUES
(4, 0, 'Morlito Caruyan', 'Danica', 0, '2022-10-15', 10, 1, 1, 1, 1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 5, 0, 0, 0, 0, 7, 0, 0, 0, 0, 4, 0, 0, 0, 0, 300, 0, 0, 0, 0, 0),
(5, 0, 'Ruben de Ocampo', 'Sophie', 15, '2022-10-05', 9, 5, 26, 14, 1, 4, 9, 7, 2, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0),
(6, 0, 'Jaime Dilig', 'Butchoy', 0, '2022-08-20', 4, 14, 32, 1, 1, 10, 5, 2, 0, 0, 19, 19, 19, 19, 19, 3, 0, 0, 0, 0, 16, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3000, 0, 0, 0, 0, 0),
(7, 0, 'Ruben Germina', 'Jamjam', 0, '2022-10-14', 39, 1, 1, 1, 1, 3, 0, 0, 0, 0, 16, 0, 16, 16, 16, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2500, 0, 0, 0, 0, 0),
(8, 0, 'Ricardo Hernandez', 'Karen Lorna', 0, '2022-06-02', 19, 24, 14, 31, 32, 10, 5, 10, 3, 4, 18, 18, 18, 18, 18, 3, 0, 0, 0, 0, 16, 0, 0, 0, 0, 3, 0, 0, 0, 0, 250, 0, 0, 0, 0, 0),
(9, 0, 'Leonardo Talicol Jr', 'Oasaha', 0, '2022-10-13', 10, 1, 1, 1, 1, 2, 0, 0, 0, 0, 15, 15, 15, 15, 15, 5, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0),
(17, 0, 'Edwin Limboya', 'Bryan', 0, '2022-06-05', 5, 8, 37, 26, 18, 3, 1, 1, 2, 0, 16, 16, 16, 16, 16, 3, 0, 0, 0, 0, 15, 0, 0, 0, 0, 4, 0, 0, 0, 0, 150, 0, 0, 0, 0, 0),
(18, 0, 'Gina Perez', 'Gina 1', 0, '2022-09-15', 5, 8, 41, 25, 1, 30, 20, 15, 10, 0, 16, 16, 16, 16, 16, 3, 0, 0, 0, 0, 12, 0, 0, 0, 0, 3, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0),
(19, 0, 'William Sulit', '3 King', 0, '2022-08-24', 36, 25, 32, 3, 15, 3, 2, 3, 2, 3, 16, 16, 16, 16, 16, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1000, 0, 0, 0, 0, 0),
(20, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-14', 14, 19, 32, 1, 1, 2, 2, 5, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2270, 0, 0, 0, 0, 0),
(21, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-20', 19, 1, 1, 1, 1, 3, 0, 0, 0, 0, 8, 8, 8, 8, 8, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1050, 0, 0, 0, 0, 0),
(22, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-25', 14, 32, 19, 1, 1, 2, 2, 6, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2237, 0, 0, 0, 0, 0),
(23, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-26', 19, 1, 1, 1, 1, 7, 0, 0, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1974, 0, 0, 0, 0, 0),
(24, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-31', 32, 14, 19, 1, 1, 1, 2, 1, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 774, 0, 0, 0, 0, 0),
(25, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-06', 32, 19, 1, 1, 1, 1, 2, 0, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 780, 0, 0, 0, 0, 0),
(26, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-07', 19, 32, 1, 1, 1, 7, 2, 0, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2350, 0, 0, 0, 0, 0),
(27, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-08', 32, 19, 1, 1, 1, 1, 2, 0, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 892, 0, 0, 0, 0, 0),
(28, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-12', 32, 1, 1, 1, 1, 2, 0, 0, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 490, 0, 0, 0, 0, 0),
(29, 0, 'Rodel B. Roque', 'Rodel', 0, '2022-06-07', 8, 7, 26, 40, 9, 5, 2, 5, 1, 1, 20, 20, 20, 20, 20, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0),
(30, 0, 'Virgilio Himpil', 'Laiza & Lois', 0, '2022-09-10', 3, 21, 28, 23, 36, 5, 10, 3, 1, 2, 17, 17, 17, 17, 17, 8, 0, 0, 0, 0, 11, 0, 0, 0, 0, 3, 0, 0, 0, 0, 400, 0, 0, 0, 0, 0),
(31, 0, 'Rolando Lorio', 'Lord John Gabriel', 8, '2022-09-21', 19, 4, 32, 14, 36, 5, 5, 10, 3, 3, 16, 16, 16, 16, 16, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 300, 0, 0, 0, 0, 0),
(32, 0, 'Rodelio Aguilar', 'Rohan Rak', 3, '2022-09-10', 25, 1, 1, 1, 1, 4, 0, 0, 0, 0, 15, 15, 15, 15, 15, 3, 0, 0, 0, 0, 7, 0, 0, 0, 0, 3, 0, 0, 0, 0, 230, 0, 0, 0, 0, 0),
(33, 0, 'Rodelio Aguilar', 'Rohan Rak', 3, '2022-09-22', 28, 1, 1, 1, 1, 11, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 0, 0, 0, 12, 0, 0, 0, 0, 3, 0, 0, 0, 0, 380, 0, 0, 0, 0, 0),
(34, 0, 'Lilia Cena', 'Eric', 0, '2022-09-16', 39, 1, 1, 1, 1, 5, 0, 0, 0, 0, 10, 0, 0, 0, 0, 3, 0, 0, 0, 0, 12, 0, 0, 0, 0, 3, 0, 0, 0, 0, 350, 0, 0, 0, 0, 0),
(35, 0, 'Ruel Areglo', 'Ruel', 4, '2022-01-20', 36, 20, 10, 1, 1, 2, 4, 5, 0, 0, 18, 18, 18, 18, 0, 5, 0, 0, 0, 0, 11, 0, 0, 0, 0, 3, 0, 0, 0, 0, 300, 0, 0, 0, 0, 0),
(36, 0, 'Aniceto Compay', 'Rojan 1', 0, '2022-09-10', 36, 32, 6, 34, 35, 2, 2, 4, 2, 5, 16, 16, 16, 16, 16, 3, 0, 0, 0, 0, 17, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1800, 0, 0, 0, 0, 0),
(37, 0, 'Oliver Orqueza', 'Don Ehboy', 0, '2022-09-14', 39, 13, 27, 1, 1, 10, 1, 18, 0, 0, 7, 7, 7, 7, 7, 3, 0, 0, 0, 0, 16, 0, 0, 0, 0, 3, 0, 0, 0, 0, 370, 0, 0, 0, 0, 0),
(38, 0, 'Alvin Atienza', '12 Fingers 1', 0, '2022-06-15', 19, 2, 14, 1, 1, 25, 100, 20, 0, 0, 10, 10, 10, 10, 10, 3, 0, 0, 0, 0, 9, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3000, 0, 0, 0, 0, 0),
(39, 0, 'Jerry Linga', 'Cameron', 0, '2022-09-10', 19, 14, 6, 11, 36, 2, 3, 1, 2, 5, 18, 18, 18, 8, 18, 3, 0, 0, 0, 0, 16, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1200, 0, 0, 0, 0, 0),
(40, 0, 'Virgie Corpus', 'Emma 4', 0, '2022-09-16', 42, 17, 1, 1, 1, 45, 45, 0, 0, 0, 14, 14, 14, 14, 14, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 0, 0, 0, 160, 0, 0, 0, 0, 0),
(41, 0, 'Emerson Morcoso', 'Athena Joy', 0, '2022-09-27', 36, 29, 4, 36, 32, 12, 13, 13, 12, 12, 6, 6, 6, 6, 6, 4, 0, 0, 0, 0, 48, 0, 0, 0, 0, 4, 0, 0, 0, 0, 400, 0, 0, 0, 0, 0),
(42, 0, 'Noel Arcena', 'Zara Zoe', 14, '2022-07-15', 3, 7, 5, 33, 37, 10, 7, 7, 7, 7, 12, 12, 12, 12, 12, 2, 0, 0, 0, 0, 12, 0, 0, 0, 0, 3, 0, 0, 0, 0, 220, 0, 0, 0, 0, 0),
(43, 0, 'Gervin Mentel', 'Ayeshia Nicole', 20, '2022-08-27', 32, 30, 6, 31, 19, 10, 5, 5, 1, 1, 13, 13, 13, 13, 13, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 250, 0, 0, 0, 0, 0),
(44, 0, 'Jimmy Villegas', 'Tonton', 16, '2022-08-19', 19, 36, 32, 14, 8, 5, 1, 5, 1, 1, 13, 13, 13, 13, 13, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 280, 0, 0, 0, 0, 0),
(45, 0, 'Julito Torrente', 'Manager', 0, '2022-08-19', 19, 12, 4, 36, 1, 10, 10, 10, 10, 0, 7, 7, 7, 7, 7, 3, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 180, 0, 0, 0, 0, 0),
(46, 0, 'Jessie Molina', 'Noah', 0, '2022-09-07', 9, 36, 10, 38, 1, 7, 2, 2, 1, 0, 9, 9, 9, 9, 9, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1900, 0, 0, 0, 0, 0),
(47, 0, 'Ronald A. Arendela', 'Allan', 0, '2022-11-22', 35, 1, 1, 1, 1, 2, 0, 0, 0, 0, 16, 16, 16, 16, 16, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 3, 0, 0, 0, 0, 150, 0, 0, 0, 0, 0),
(48, 0, 'Joel Duran', 'Pula', 0, '2022-11-27', 22, 36, 15, 1, 1, 6, 23, 6, 0, 0, 20, 20, 20, 20, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 0, 0, 0, 300, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `report_temp`
--

CREATE TABLE `report_temp` (
  `reportid` int(50) NOT NULL,
  `userid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `vessel` varchar(50) NOT NULL,
  `frequent` int(50) NOT NULL,
  `date` date NOT NULL,
  `catch1` int(50) NOT NULL,
  `catch2` int(50) NOT NULL,
  `catch3` int(50) NOT NULL,
  `catch4` int(50) NOT NULL,
  `catch5` int(11) NOT NULL,
  `volume1` double NOT NULL,
  `volume2` double NOT NULL,
  `volume3` double NOT NULL,
  `volume4` double NOT NULL,
  `volume5` double NOT NULL,
  `site1` int(50) NOT NULL,
  `site2` int(11) NOT NULL,
  `site3` int(11) NOT NULL,
  `site4` int(11) NOT NULL,
  `site5` int(11) NOT NULL,
  `gear1` int(50) NOT NULL,
  `gear2` int(11) NOT NULL,
  `gear3` int(11) NOT NULL,
  `gear4` int(11) NOT NULL,
  `gear5` int(11) NOT NULL,
  `hours1` int(11) NOT NULL,
  `hours2` int(11) NOT NULL,
  `hours3` int(11) NOT NULL,
  `hours4` int(11) NOT NULL,
  `hours5` int(11) NOT NULL,
  `landing1` int(50) NOT NULL,
  `landing2` int(11) NOT NULL,
  `landing3` int(11) NOT NULL,
  `landing4` int(11) NOT NULL,
  `landing5` int(11) NOT NULL,
  `price1` int(50) NOT NULL,
  `price2` int(11) NOT NULL,
  `price3` int(11) NOT NULL,
  `price4` int(11) NOT NULL,
  `price5` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `report_temp`
--

INSERT INTO `report_temp` (`reportid`, `userid`, `name`, `vessel`, `frequent`, `date`, `catch1`, `catch2`, `catch3`, `catch4`, `catch5`, `volume1`, `volume2`, `volume3`, `volume4`, `volume5`, `site1`, `site2`, `site3`, `site4`, `site5`, `gear1`, `gear2`, `gear3`, `gear4`, `gear5`, `hours1`, `hours2`, `hours3`, `hours4`, `hours5`, `landing1`, `landing2`, `landing3`, `landing4`, `landing5`, `price1`, `price2`, `price3`, `price4`, `price5`) VALUES
(17, 5, 'Fernando Castro', 'Mapino', 10, '2024-12-09', 11, 12, 3, 19, 9, 2, 5, 5, 8, 7, 16, 10, 9, 12, 7, 3, 3, 2, 4, 3, 8, 4, 3, 5, 5, 1, 2, 3, 1, 2, 62, 77, 110, 100, 110),
(18, 5, 'Fernando Castro', 'Mapino', 6, '2024-11-12', 2, 10, 23, 42, 8, 126, 36, 30, 12, 50, 13, 16, 18, 19, 10, 3, 1, 6, 1, 1, 7, 6, 8, 9, 6, 3, 1, 2, 2, 1, 86, 58, 150, 300, 58),
(19, 6, 'Kyle Cedric Balsigan ', 'Anastacia', 13, '2024-11-24', 7, 42, 17, 14, 3, 36, 10, 32, 46, 50, 16, 19, 14, 14, 7, 1, 3, 5, 4, 2, 11, 9, 4, 12, 8, 1, 3, 2, 3, 2, 86, 300, 64, 100, 66),
(20, 7, 'Mike Dela Cruz', 'Sta Maria', 8, '2024-10-17', 9, 7, 10, 14, 3, 36, 55, 33, 55, 36, 14, 10, 14, 10, 14, 4, 4, 5, 3, 2, 9, 6, 11, 11, 7, 2, 2, 3, 1, 1, 80, 69, 64, 64, 58),
(21, 10, 'Gloria Velazquez ', 'Amor', 8, '2024-11-19', 15, 12, 5, 3, 1, 173, 50, 63, 71, 0, 11, 13, 14, 16, 0, 7, 1, 5, 2, 0, 13, 6, 11, 7, 0, 2, 3, 3, 2, 0, 65, 45, 54, 64, 0),
(22, 7, 'test', 'unittest1', 1, '2000-02-01', 43, 1, 1, 1, 1, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `site`
--

CREATE TABLE `site` (
  `siteid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `lat` double NOT NULL,
  `lng` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `site`
--

INSERT INTO `site` (`siteid`, `name`, `lat`, `lng`) VALUES
(0, 'null', 0, 0),
(5, 'Bataan', 14.4111, 120.514381),
(6, 'Batangas', 13.700321, 120.987843),
(7, 'Caballo Island', 14.370277, 120.614922),
(8, 'Capipisa', 14.355401, 120.78673),
(9, 'Ciockno', 14.286153, 120.656006),
(10, 'Corregidor', 14.39779, 120.584267),
(12, 'Mabulo', 14.318295, 120.746833),
(13, 'Manila Bay', 14.549123, 120.739503),
(14, 'Mindoro', 13.45438, 121.058368),
(15, 'Munting Mapino', 14.337654, 120.769706),
(16, 'Naic', 14.332421, 120.766352),
(17, 'Nasugbu', 14.181806, 120.567495),
(18, 'Prayle', 14.305086, 120.631022),
(19, 'Puerto Azul', 14.2805, 120.681005),
(20, 'Timalan Balsahan', 14.344131, 120.777254),
(23, 'Sapang', 14.290018, 120.707587),
(24, 'Ternate', 14.4111, 120.514381);

-- --------------------------------------------------------

--
-- Table structure for table `trash`
--

CREATE TABLE `trash` (
  `id` int(50) DEFAULT NULL,
  `reportid` int(50) NOT NULL,
  `userid` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userid` int(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `vessel_name` varchar(50) NOT NULL,
  `reg_number` varchar(50) NOT NULL,
  `contact` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userid`, `username`, `password`, `vessel_name`, `reg_number`, `contact`) VALUES
(5, 'Fernando Castro', 'fernando355', 'Mapino', 'CAV355', '09148562489'),
(6, 'Kyle Cedric Balsigan', 'kyle356', 'Anastacia', 'CAV356', '09673921283'),
(7, 'Mike Dela Cruz', 'mike267', 'Sta Maria', 'CAV267', '09672853902'),
(10, 'Gloria Velazquez', 'gloria198', 'Amor', 'CAV198', '09836530178'),
(11, 'Fernando Ortega', 'fernando468', 'Sophia Martina', 'CAV468', '09114568821'),
(14, 'Andrei Alcantara', 'andrei378', 'Kagayan', 'CAV378', '09437718421'),
(15, 'James Mapigo', 'james466', 'Star voyage', 'CAV466', '09498672234'),
(18, 'Gabriel Corpus', 'gabriel097', 'Corpus', 'CAV097', '09432267315'),
(19, 'Mark Joseph Madrigal', 'mark667', 'Munting lupa', 'CAV667', '09546674821');

-- --------------------------------------------------------

--
-- Table structure for table `user_temp`
--

CREATE TABLE `user_temp` (
  `userid` int(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `vessel_name` varchar(50) NOT NULL,
  `reg_number` varchar(50) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `verification_code` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_temp`
--

INSERT INTO `user_temp` (`userid`, `username`, `password`, `vessel_name`, `reg_number`, `contact`, `verified`, `verification_code`) VALUES
(8, 'Alvin Sisracon', 'alvin1510', 'Bornok', 'CAV1510', '09372397201', 0, 0),
(9, 'Juanito Tayao', 'tayao1611', 'Butch', 'CAV1611', '09578342190', 0, 0),
(12, 'Ramon Ligaya', 'ligaya901', 'Pangil1', 'CAV901', '09876554679', 0, 0),
(13, 'Emilio Baltazar', 'emilio457', 'Agila', 'CAV457', '09246778241', 0, 0),
(16, 'Cedric Benson', 'cedric865', 'Voyager', 'CAV865', '09678492341', 0, 0),
(17, 'Amelia belsigo', 'amelia288', 'Rosas', 'CAV288', '09457718231', 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`adminid`);

--
-- Indexes for table `bin`
--
ALTER TABLE `bin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qwe` (`userid`);

--
-- Indexes for table `catch`
--
ALTER TABLE `catch`
  ADD PRIMARY KEY (`catchid`);

--
-- Indexes for table `gear`
--
ALTER TABLE `gear`
  ADD PRIMARY KEY (`gearid`);

--
-- Indexes for table `landing`
--
ALTER TABLE `landing`
  ADD PRIMARY KEY (`landid`);

--
-- Indexes for table `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`reportid`),
  ADD KEY `catch1` (`catch1`),
  ADD KEY `catch2` (`catch2`),
  ADD KEY `catch3` (`catch3`),
  ADD KEY `catch4` (`catch4`),
  ADD KEY `catch5` (`catch5`),
  ADD KEY `gear` (`gear1`),
  ADD KEY `landing` (`landing1`),
  ADD KEY `site` (`site1`),
  ADD KEY `site2` (`site2`),
  ADD KEY `site3` (`site3`),
  ADD KEY `site4` (`site4`),
  ADD KEY `site5` (`site5`),
  ADD KEY `gear2_fk` (`gear2`),
  ADD KEY `gear3_fk` (`gear3`),
  ADD KEY `gear4_fk` (`gear4`),
  ADD KEY `gear5_fk` (`gear5`),
  ADD KEY `landing2_fk` (`landing2`),
  ADD KEY `landing3_fk` (`landing3`),
  ADD KEY `landing4_fk` (`landing4`),
  ADD KEY `landing5_fk` (`landing5`);

--
-- Indexes for table `report_temp`
--
ALTER TABLE `report_temp`
  ADD PRIMARY KEY (`reportid`),
  ADD KEY `userid` (`userid`);

--
-- Indexes for table `site`
--
ALTER TABLE `site`
  ADD PRIMARY KEY (`siteid`);

--
-- Indexes for table `trash`
--
ALTER TABLE `trash`
  ADD KEY `reportid` (`reportid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userid`);

--
-- Indexes for table `user_temp`
--
ALTER TABLE `user_temp`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `adminid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bin`
--
ALTER TABLE `bin`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `catch`
--
ALTER TABLE `catch`
  MODIFY `catchid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `gear`
--
ALTER TABLE `gear`
  MODIFY `gearid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `landing`
--
ALTER TABLE `landing`
  MODIFY `landid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `report`
--
ALTER TABLE `report`
  MODIFY `reportid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=128;

--
-- AUTO_INCREMENT for table `report_temp`
--
ALTER TABLE `report_temp`
  MODIFY `reportid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `site`
--
ALTER TABLE `site`
  MODIFY `siteid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `user_temp`
--
ALTER TABLE `user_temp`
  MODIFY `userid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bin`
--
ALTER TABLE `bin`
  ADD CONSTRAINT `qwe` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`);

--
-- Constraints for table `report`
--
ALTER TABLE `report`
  ADD CONSTRAINT `catch1` FOREIGN KEY (`catch1`) REFERENCES `catch` (`catchid`),
  ADD CONSTRAINT `catch2` FOREIGN KEY (`catch2`) REFERENCES `catch` (`catchid`),
  ADD CONSTRAINT `catch3` FOREIGN KEY (`catch3`) REFERENCES `catch` (`catchid`),
  ADD CONSTRAINT `catch4` FOREIGN KEY (`catch4`) REFERENCES `catch` (`catchid`),
  ADD CONSTRAINT `catch5` FOREIGN KEY (`catch5`) REFERENCES `catch` (`catchid`),
  ADD CONSTRAINT `gear2_fk` FOREIGN KEY (`gear2`) REFERENCES `gear` (`gearid`),
  ADD CONSTRAINT `gear3_fk` FOREIGN KEY (`gear3`) REFERENCES `gear` (`gearid`),
  ADD CONSTRAINT `gear4_fk` FOREIGN KEY (`gear4`) REFERENCES `gear` (`gearid`),
  ADD CONSTRAINT `gear5_fk` FOREIGN KEY (`gear5`) REFERENCES `gear` (`gearid`),
  ADD CONSTRAINT `landing2_fk` FOREIGN KEY (`landing2`) REFERENCES `landing` (`landid`),
  ADD CONSTRAINT `landing3_fk` FOREIGN KEY (`landing3`) REFERENCES `landing` (`landid`),
  ADD CONSTRAINT `landing4_fk` FOREIGN KEY (`landing4`) REFERENCES `landing` (`landid`),
  ADD CONSTRAINT `landing5_fk` FOREIGN KEY (`landing5`) REFERENCES `landing` (`landid`),
  ADD CONSTRAINT `site1` FOREIGN KEY (`site1`) REFERENCES `site` (`siteid`),
  ADD CONSTRAINT `site2` FOREIGN KEY (`site2`) REFERENCES `site` (`siteid`),
  ADD CONSTRAINT `site3` FOREIGN KEY (`site3`) REFERENCES `site` (`siteid`),
  ADD CONSTRAINT `site4` FOREIGN KEY (`site4`) REFERENCES `site` (`siteid`),
  ADD CONSTRAINT `site5` FOREIGN KEY (`site5`) REFERENCES `site` (`siteid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
