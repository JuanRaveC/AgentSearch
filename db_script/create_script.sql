CREATE DATABASE `agentdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `historial` (
  `id_historial` int(11) NOT NULL AUTO_INCREMENT,
  `palabra_clave` varchar(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `id_xml` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_historial`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tema` (
  `id_tema` int(11) NOT NULL,
  `tema` varchar(20) DEFAULT NULL,
  `id_xml` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_tema`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `url` (
  `id_url` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) DEFAULT NULL,
  `id_tema` int(11) DEFAULT NULL,
  `institucion` varchar(20) DEFAULT NULL,
  `crawled_ind` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id_url`),
  KEY `FK_URL_TEMA_idx` (`id_tema`),
  CONSTRAINT `FK_URL_TEMA` FOREIGN KEY (`id_tema`) REFERENCES `tema` (`id_tema`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `url_base` (
  `id_url_base` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) DEFAULT NULL,
  `institucion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_url_base`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `xml` (
  `id_xml` int(11) NOT NULL,
  `xml` blob,
  PRIMARY KEY (`id_xml`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
