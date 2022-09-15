# RaidReceiver



# db table
-- Exportiere Datenbank Struktur für raid_receiver
CREATE DATABASE IF NOT EXISTS `raid_receiver` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `raid_receiver`;

-- Exportiere Struktur von Tabelle raid_receiver.raids
CREATE TABLE IF NOT EXISTS `raids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NULL DEFAULT NULL,
  `latitude` float DEFAULT 0,
  `longitude` float DEFAULT 0,
  `level` int(11) DEFAULT NULL,
  `pokemon_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `cp` int(11) DEFAULT NULL,
  `start` int(11) DEFAULT NULL,
  `end` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `evolution` int(11) DEFAULT NULL,
  `spawn` int(11) DEFAULT NULL,
  `move_1` int(11) DEFAULT NULL,
  `move_2` int(11) DEFAULT NULL,
  `gym_id` varchar(50) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `is_ex_raid_eligible` varchar(50) DEFAULT NULL,
  `is_exclusive` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;