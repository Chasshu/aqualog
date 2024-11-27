-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 27, 2024 at 02:11 PM
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
(1, 'arianne', '123');

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

--
-- Dumping data for table `bin`
--

INSERT INTO `bin` (`id`, `userid`, `name`, `vessel`, `date`, `reportid`) VALUES
(1, 1, '', '', 0, 9),
(2, 1, '', '', 0, 11),
(3, 2, 'test', 'test', 0, 12);

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
  `volume1` int(11) NOT NULL,
  `volume2` int(11) NOT NULL,
  `volume3` int(11) NOT NULL,
  `volume4` int(11) NOT NULL,
  `volume5` int(11) NOT NULL,
  `site` int(50) NOT NULL,
  `gear` int(50) NOT NULL,
  `hours` int(11) NOT NULL,
  `landing` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `tempid` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`reportid`, `userid`, `name`, `vessel`, `frequent`, `date`, `catch1`, `catch2`, `catch3`, `catch4`, `catch5`, `volume1`, `volume2`, `volume3`, `volume4`, `volume5`, `site`, `gear`, `hours`, `landing`, `price`, `tempid`) VALUES
(4, 2, 'Morlito Caruyan', 'Danica', 0, '2022-10-15', 10, 1, 1, 1, 1, 0, 0, 0, 0, 0, 8, 5, 7, 4, 300, 0),
(5, 0, 'Ruben de Ocampo', 'Sophie', 15, '2022-10-05', 9, 5, 26, 14, 1, 4, 9, 7, 2, 0, 15, 3, 7, 1, 50, 0),
(6, 0, 'Jaime Dilig', 'Butchoy', 0, '2022-08-20', 4, 14, 32, 1, 1, 10, 5, 2, 0, 0, 19, 3, 16, 3, 3000, 0),
(7, 0, 'Ruben Germina', 'Jamjam', 0, '2022-10-14', 39, 1, 1, 1, 1, 3, 0, 0, 0, 0, 16, 5, 6, 3, 2500, 0),
(8, 0, 'Ricardo Hernandez', 'Karen Lorna', 0, '2022-06-02', 19, 24, 14, 31, 32, 10, 5, 10, 3, 4, 18, 3, 16, 3, 250, 0),
(9, 0, 'Leonardo Talicol Jr', 'Oasaha', 0, '2022-10-13', 10, 1, 1, 1, 1, 2, 0, 0, 0, 0, 15, 5, 3, 3, 40, 0),
(17, 0, 'Edwin Limboya', 'Bryan', 0, '2022-06-05', 5, 8, 37, 26, 18, 3, 1, 1, 2, 0, 16, 3, 15, 4, 150, 0),
(18, 0, 'Gina Perez', 'Gina 1', 0, '2022-09-15', 5, 8, 41, 25, 1, 30, 20, 15, 10, 0, 16, 3, 12, 3, 80, 0),
(19, 0, 'William Sulit', '3 King', 0, '2022-08-24', 36, 25, 32, 3, 15, 3, 2, 3, 2, 3, 16, 3, 6, 3, 1000, 0),
(20, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-14', 14, 19, 32, 1, 1, 2, 2, 5, 0, 0, 15, 3, 6, 1, 2270, 0),
(21, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-20', 19, 1, 1, 1, 1, 3, 0, 0, 0, 0, 8, 3, 6, 1, 1050, 0),
(22, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-25', 14, 32, 19, 1, 1, 2, 2, 6, 0, 0, 15, 3, 7, 1, 2237, 0),
(23, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-26', 19, 1, 1, 1, 1, 7, 0, 0, 0, 0, 15, 3, 6, 1, 1974, 0),
(24, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-08-31', 32, 14, 19, 1, 1, 1, 2, 1, 0, 0, 15, 3, 6, 1, 774, 0),
(25, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-06', 32, 19, 1, 1, 1, 1, 2, 0, 0, 0, 15, 3, 7, 1, 780, 0),
(26, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-07', 19, 32, 1, 1, 1, 7, 2, 0, 0, 0, 15, 3, 6, 1, 2350, 0),
(27, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-08', 32, 19, 1, 1, 1, 1, 2, 0, 0, 0, 15, 3, 6, 1, 892, 0),
(28, 0, 'Aldrin de Ocampo', 'Aldrin', 4, '2022-09-12', 32, 1, 1, 1, 1, 2, 0, 0, 0, 0, 15, 3, 6, 1, 490, 0),
(29, 0, 'Rodel B. Roque', 'Rodel', 0, '2022-06-07', 8, 7, 26, 40, 9, 5, 2, 5, 1, 1, 20, 3, 4, 1, 100, 0),
(30, 0, 'Virgilio Himpil', 'Laiza & Lois', 0, '2022-09-10', 3, 21, 28, 23, 36, 5, 10, 3, 1, 2, 17, 8, 11, 3, 400, 0),
(31, 0, 'Rolando Lorio', 'Lord John Gabriel', 8, '2022-09-21', 19, 4, 32, 14, 36, 5, 5, 10, 3, 3, 16, 1, 4, 1, 300, 0),
(32, 0, 'Rodelio Aguilar', 'Rohan Rak', 3, '2022-09-10', 25, 1, 1, 1, 1, 4, 0, 0, 0, 0, 15, 3, 7, 3, 230, 0),
(33, 0, 'Rodelio Aguilar', 'Rohan Rak', 3, '2022-09-22', 28, 1, 1, 1, 1, 11, 0, 0, 0, 0, 5, 3, 12, 3, 380, 0),
(34, 0, 'Lilia Cena', 'Eric', 0, '2022-09-16', 39, 1, 1, 1, 1, 5, 0, 0, 0, 0, 10, 3, 12, 3, 350, 0),
(35, 0, 'Ruel Areglo', 'Ruel', 4, '2022-01-20', 36, 20, 10, 1, 1, 2, 4, 5, 0, 0, 18, 5, 11, 3, 300, 0),
(36, 0, 'Aniceto Compay', 'Rojan 1', 0, '2022-09-10', 36, 32, 6, 34, 35, 2, 2, 4, 2, 5, 16, 3, 17, 4, 1800, 0),
(37, 0, 'Oliver Orqueza', 'Don Ehboy', 0, '2022-09-14', 39, 13, 27, 1, 1, 10, 1, 18, 0, 0, 7, 3, 16, 3, 370, 0),
(38, 0, 'Alvin Atienza', '12 Fingers 1', 0, '2022-06-15', 19, 2, 14, 1, 1, 25, 100, 20, 0, 0, 10, 3, 9, 3, 3000, 0),
(39, 0, 'Jerry Linga', 'Cameron', 0, '2022-09-10', 19, 14, 6, 11, 36, 2, 3, 1, 2, 5, 18, 3, 16, 3, 1200, 0),
(40, 0, 'Virgie Corpus', 'Emma 4', 0, '2022-09-16', 42, 17, 1, 1, 1, 45, 45, 0, 0, 0, 14, 7, 5, 3, 160, 0),
(41, 0, 'Emerson Morcoso', 'Athena Joy', 0, '2022-09-27', 36, 29, 4, 36, 32, 12, 13, 13, 12, 12, 6, 4, 48, 4, 400, 0),
(42, 0, 'Noel Arcena', 'Zara Zoe', 14, '2022-07-15', 3, 7, 5, 33, 37, 10, 7, 7, 7, 7, 12, 2, 12, 3, 220, 0),
(43, 0, 'Gervin Mentel', 'Ayeshia Nicole', 20, '2022-08-27', 32, 30, 6, 31, 19, 10, 5, 5, 1, 1, 13, 4, 0, 1, 250, 0),
(44, 0, 'Jimmy Villegas', 'Tonton', 16, '2022-08-19', 19, 36, 32, 14, 8, 5, 1, 5, 1, 1, 13, 1, 3, 1, 280, 0),
(45, 0, 'Julito Torrente', 'Manager', 0, '2022-08-19', 19, 12, 4, 36, 1, 10, 10, 10, 10, 0, 7, 3, 2, 2, 180, 0),
(46, 0, 'Jessie Molina', 'Noah', 0, '2022-09-07', 9, 36, 10, 38, 1, 7, 2, 2, 1, 0, 9, 3, 1, 2, 1900, 0),
(47, 0, 'Ronald A. Arendela', 'Allan', 0, '2022-11-22', 35, 1, 1, 1, 1, 2, 0, 0, 0, 0, 16, 5, 6, 3, 150, 0),
(48, 0, 'Joel Duran', 'Pula', 0, '2022-11-27', 22, 36, 15, 1, 1, 6, 23, 6, 0, 0, 20, 5, 5, 3, 300, 0),
(52, 0, 'testcha', '1', 1, '2002-01-01', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 19, 1, 1, 1, 1, 0),
(125, 1, 'lasttest', '12321', 123, '2024-11-01', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 0),
(126, 1, 'lasttesttulogna', '1', 1, '2024-11-01', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1, 14);

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
  `volume1` int(50) NOT NULL,
  `volume2` int(50) NOT NULL,
  `volume3` int(50) NOT NULL,
  `volume4` int(50) NOT NULL,
  `volume5` int(50) NOT NULL,
  `site` int(50) NOT NULL,
  `gear` int(50) NOT NULL,
  `hours` int(11) NOT NULL,
  `landing` int(50) NOT NULL,
  `price` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `site`
--

CREATE TABLE `site` (
  `siteid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `site`
--

INSERT INTO `site` (`siteid`, `name`) VALUES
(5, 'Bataan'),
(6, 'Batangas'),
(7, 'Caballo Island'),
(8, 'Capipisa'),
(9, 'Ciockno'),
(10, 'Corregidor'),
(11, 'Labac'),
(12, 'Mabulo'),
(13, 'Manila Bay'),
(14, 'Mindoro'),
(15, 'Munting Mapino'),
(16, 'Naic'),
(17, 'Nasugbu'),
(18, 'Prayle'),
(19, 'Puerto Azul'),
(20, 'Timalan Balsahan');

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
  `contact` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userid`, `username`, `password`, `vessel_name`, `reg_number`, `contact`) VALUES
(1, 'qwe', '123', '', '', 0),
(2, 'test1', '123', 'cha123', '123cha', 0),
(3, '[value-2]', '123', 'testreset', 'testreset', 0);

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
  `contact` int(11) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `verification_code` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_temp`
--

INSERT INTO `user_temp` (`userid`, `username`, `password`, `vessel_name`, `reg_number`, `contact`, `verified`, `verification_code`) VALUES
(1, 'qwe', '123', '', '', 0, 0, 0);

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
  ADD KEY `gear` (`gear`),
  ADD KEY `landing` (`landing`),
  ADD KEY `site` (`site`);

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
  MODIFY `adminid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bin`
--
ALTER TABLE `bin`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `catch`
--
ALTER TABLE `catch`
  MODIFY `catchid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `gear`
--
ALTER TABLE `gear`
  MODIFY `gearid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `landing`
--
ALTER TABLE `landing`
  MODIFY `landid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `report`
--
ALTER TABLE `report`
  MODIFY `reportid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=127;

--
-- AUTO_INCREMENT for table `report_temp`
--
ALTER TABLE `report_temp`
  MODIFY `reportid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `site`
--
ALTER TABLE `site`
  MODIFY `siteid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
  ADD CONSTRAINT `gear` FOREIGN KEY (`gear`) REFERENCES `gear` (`gearid`),
  ADD CONSTRAINT `landing` FOREIGN KEY (`landing`) REFERENCES `landing` (`landid`),
  ADD CONSTRAINT `site` FOREIGN KEY (`site`) REFERENCES `site` (`siteid`);

--
-- Constraints for table `report_temp`
--
ALTER TABLE `report_temp`
  ADD CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
