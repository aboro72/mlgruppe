-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Erstellungszeit: 15. Feb 2024 um 13:37
-- Server-Version: 8.0.30
-- PHP-Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `c1_ml`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(2, 'orga'),
(1, 'pit');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(1, 1, 5),
(2, 1, 6),
(3, 1, 7),
(4, 1, 8),
(5, 1, 9),
(6, 1, 10),
(7, 1, 11),
(8, 1, 12),
(9, 1, 13),
(10, 1, 14),
(11, 1, 15),
(12, 1, 16),
(13, 1, 25),
(14, 1, 26),
(15, 1, 27),
(16, 1, 28),
(17, 1, 29),
(18, 1, 30),
(19, 1, 31),
(20, 1, 32),
(21, 1, 33),
(22, 1, 34),
(23, 1, 35),
(24, 1, 36),
(25, 1, 37),
(26, 1, 38),
(27, 1, 39),
(28, 1, 40),
(29, 1, 41),
(30, 1, 42),
(31, 1, 43),
(32, 1, 44),
(33, 1, 45),
(34, 1, 46),
(35, 1, 47),
(36, 1, 48),
(37, 1, 49),
(38, 1, 50),
(39, 1, 51),
(40, 1, 52),
(41, 1, 53),
(42, 1, 54),
(43, 1, 55),
(44, 1, 56),
(45, 1, 57),
(46, 1, 58),
(47, 1, 59),
(48, 1, 60),
(49, 1, 61),
(50, 1, 62),
(51, 1, 63),
(52, 1, 64),
(53, 1, 65),
(54, 1, 66),
(55, 1, 67),
(56, 1, 68),
(57, 1, 69),
(58, 1, 70),
(59, 1, 71),
(60, 1, 72),
(61, 1, 73),
(62, 1, 74),
(63, 1, 75),
(64, 1, 76),
(65, 2, 25),
(66, 2, 26),
(67, 2, 27),
(68, 2, 28),
(69, 2, 61),
(70, 2, 62),
(71, 2, 63),
(72, 2, 64),
(73, 2, 65),
(74, 2, 66),
(75, 2, 67),
(76, 2, 68),
(77, 2, 69),
(78, 2, 70),
(79, 2, 71),
(80, 2, 72),
(81, 2, 73),
(82, 2, 74),
(83, 2, 75),
(84, 2, 76);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add adresse', 7, 'add_adresse'),
(26, 'Can change adresse', 7, 'change_adresse'),
(27, 'Can delete adresse', 7, 'delete_adresse'),
(28, 'Can view adresse', 7, 'view_adresse'),
(29, 'Can add festplatten image notebook', 8, 'add_festplattenimagenotebook'),
(30, 'Can change festplatten image notebook', 8, 'change_festplattenimagenotebook'),
(31, 'Can delete festplatten image notebook', 8, 'delete_festplattenimagenotebook'),
(32, 'Can view festplatten image notebook', 8, 'view_festplattenimagenotebook'),
(33, 'Can add festplatten image server', 9, 'add_festplattenimageserver'),
(34, 'Can change festplatten image server', 9, 'change_festplattenimageserver'),
(35, 'Can delete festplatten image server', 9, 'delete_festplattenimageserver'),
(36, 'Can view festplatten image server', 9, 'view_festplattenimageserver'),
(37, 'Can add schiene', 10, 'add_schiene'),
(38, 'Can change schiene', 10, 'change_schiene'),
(39, 'Can delete schiene', 10, 'delete_schiene'),
(40, 'Can view schiene', 10, 'view_schiene'),
(41, 'Can add server', 11, 'add_server'),
(42, 'Can change server', 11, 'change_server'),
(43, 'Can delete server', 11, 'delete_server'),
(44, 'Can view server', 11, 'view_server'),
(45, 'Can add rueckholung', 12, 'add_rueckholung'),
(46, 'Can change rueckholung', 12, 'change_rueckholung'),
(47, 'Can delete rueckholung', 12, 'delete_rueckholung'),
(48, 'Can view rueckholung', 12, 'view_rueckholung'),
(49, 'Can add abholung', 13, 'add_abholung'),
(50, 'Can change abholung', 13, 'change_abholung'),
(51, 'Can delete abholung', 13, 'delete_abholung'),
(52, 'Can view abholung', 13, 'view_abholung'),
(53, 'Can add versand', 14, 'add_versand'),
(54, 'Can change versand', 14, 'change_versand'),
(55, 'Can delete versand', 14, 'delete_versand'),
(56, 'Can view versand', 14, 'view_versand'),
(57, 'Can add post it', 15, 'add_postit'),
(58, 'Can change post it', 15, 'change_postit'),
(59, 'Can delete post it', 15, 'delete_postit'),
(60, 'Can view post it', 15, 'view_postit'),
(61, 'Can add kunde', 16, 'add_kunde'),
(62, 'Can change kunde', 16, 'change_kunde'),
(63, 'Can delete kunde', 16, 'delete_kunde'),
(64, 'Can view kunde', 16, 'view_kunde'),
(65, 'Can add ansprechpartner', 17, 'add_ansprechpartner'),
(66, 'Can change ansprechpartner', 17, 'change_ansprechpartner'),
(67, 'Can delete ansprechpartner', 17, 'delete_ansprechpartner'),
(68, 'Can view ansprechpartner', 17, 'view_ansprechpartner'),
(69, 'Can add kurs', 18, 'add_kurs'),
(70, 'Can change kurs', 18, 'change_kurs'),
(71, 'Can delete kurs', 18, 'delete_kurs'),
(72, 'Can view kurs', 18, 'view_kurs'),
(73, 'Can add trainer', 19, 'add_trainer'),
(74, 'Can change trainer', 19, 'change_trainer'),
(75, 'Can delete trainer', 19, 'delete_trainer'),
(76, 'Can view trainer', 19, 'view_trainer');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$720000$F124uyUiSDXE0fKPGxdOBZ$SIBkiFSQSrYXxcfXRntab6Q3l95VKuBdPBvISphQhrw=', '2024-02-15 11:10:27.000000', 1, 'admin', '', '', '', 1, 1, '2024-02-06 17:14:05.000000'),
(2, 'pbkdf2_sha256$720000$VczO8RLn7gzzY9Q7vsp1Lm$Xvx/Bd401YfdkEqPEZJFsy+966zSJZqEsXLLELrrqG4=', NULL, 0, 'rpanske', 'Rainer', 'Panske', 'r.panske@mlgruppe.de', 1, 1, '2024-02-07 08:16:52.000000'),
(3, 'pbkdf2_sha256$720000$5FIa8LNRxa4UVuSAzOTdQN$vtLGPrlytuwPHSWbSVIs2WAXnRS8tIsjwWIsjcBUeqs=', NULL, 0, 'mukarram', 'Mukarram-Ali', 'Mehar', 'm.mehar@mlgruppe.de', 1, 1, '2024-02-07 08:18:18.000000'),
(4, 'pbkdf2_sha256$720000$IZZq7zl3KdVk8zQtrYtlNV$DxaVYdUBUGSsgGCijPyS7XE8KDgJYuBjlcZAHVHv6CM=', NULL, 0, 'aborowczak', 'Andreas', 'Borowczak', 'a.borowczak@mlgruppe.de', 1, 1, '2024-02-07 08:20:46.000000');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(4, 1, 1),
(5, 1, 2),
(1, 2, 1),
(2, 3, 1),
(3, 4, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

--
-- Daten für Tabelle `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-02-06 17:16:15.537369', '1', 'All-in', 1, '[{\"added\": {}}]', 9, 1),
(2, '2024-02-06 17:16:25.806338', '2', 'unbekannt', 1, '[{\"added\": {}}]', 9, 1),
(3, '2024-02-06 17:16:30.301920', '1', 'SWS 01', 1, '[{\"added\": {}}]', 11, 1),
(4, '2024-02-06 17:16:37.908588', '2', 'SWS 02', 1, '[{\"added\": {}}]', 11, 1),
(5, '2024-02-06 17:16:52.007578', '3', 'SWS 03', 1, '[{\"added\": {}}]', 11, 1),
(6, '2024-02-06 17:17:11.260629', '4', 'SWS 04', 1, '[{\"added\": {}}]', 11, 1),
(7, '2024-02-06 17:17:17.568965', '5', 'SWS 05', 1, '[{\"added\": {}}]', 11, 1),
(8, '2024-02-06 17:17:40.177104', '6', 'SWS 06', 1, '[{\"added\": {}}]', 11, 1),
(9, '2024-02-06 17:17:53.247363', '7', 'SWS 07', 1, '[{\"added\": {}}]', 11, 1),
(10, '2024-02-06 17:18:04.661990', '8', 'SWS 08', 1, '[{\"added\": {}}]', 11, 1),
(11, '2024-02-06 17:18:15.666742', '9', 'SWS 09', 1, '[{\"added\": {}}]', 11, 1),
(12, '2024-02-06 17:18:24.552432', '10', 'SWS 10', 1, '[{\"added\": {}}]', 11, 1),
(13, '2024-02-06 17:19:42.884632', '1', 'Win11+Office2019 V1', 1, '[{\"added\": {}}]', 8, 1),
(14, '2024-02-06 17:19:50.719205', '1', 'AC 01', 1, '[{\"added\": {}}]', 10, 1),
(15, '2024-02-06 17:20:13.951368', '2', 'AC 02', 1, '[{\"added\": {}}]', 10, 1),
(16, '2024-02-06 17:20:43.745451', '3', 'AC 03', 1, '[{\"added\": {}}]', 10, 1),
(17, '2024-02-06 17:21:03.817593', '4', 'AC 04', 1, '[{\"added\": {}}]', 10, 1),
(18, '2024-02-06 17:21:29.355683', '5', 'AC 05', 1, '[{\"added\": {}}]', 10, 1),
(19, '2024-02-06 17:21:47.093117', '6', 'AC 06', 1, '[{\"added\": {}}]', 10, 1),
(20, '2024-02-06 17:22:06.141407', '7', 'AC 07', 1, '[{\"added\": {}}]', 10, 1),
(21, '2024-02-06 17:22:30.304291', '8', 'AC 08', 1, '[{\"added\": {}}]', 10, 1),
(22, '2024-02-06 17:22:56.112648', '9', 'AC  09', 1, '[{\"added\": {}}]', 10, 1),
(23, '2024-02-06 17:23:20.868207', '10', 'AC 10', 1, '[{\"added\": {}}]', 10, 1),
(24, '2024-02-06 17:23:41.043556', '11', 'AC 11', 1, '[{\"added\": {}}]', 10, 1),
(25, '2024-02-06 17:24:02.648890', '12', 'AC 12', 1, '[{\"added\": {}}]', 10, 1),
(26, '2024-02-06 17:24:30.474921', '13', 'AC 13', 1, '[{\"added\": {}}]', 10, 1),
(27, '2024-02-06 17:24:49.968564', '14', 'AC 14', 1, '[{\"added\": {}}]', 10, 1),
(28, '2024-02-06 17:25:07.750075', '15', 'AC 15', 1, '[{\"added\": {}}]', 10, 1),
(29, '2024-02-06 17:28:29.074562', '1', 'An der Trift 13 - 15, 76149 Karlsruhe', 1, '[{\"added\": {}}]', 7, 1),
(30, '2024-02-06 17:28:31.299614', '1', 'Landeskommando Baden-Württemberg (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(31, '2024-02-06 17:29:35.238733', '1', '52413 Word Aufbau None Landeskommando Baden-Württemberg (Behörde)', 1, '[{\"added\": {}}]', 18, 1),
(32, '2024-02-06 17:32:06.555940', '11', 'Keiner', 1, '[{\"added\": {}}]', 11, 1),
(33, '2024-02-06 17:43:08.731804', '3', 'SWS 03', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(34, '2024-02-06 17:43:38.308628', '5', 'SWS 05', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(35, '2024-02-06 17:43:48.702160', '7', 'SWS 07', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(36, '2024-02-06 17:44:11.075309', '2', 'SWS 02', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(37, '2024-02-06 17:44:21.509623', '9', 'SWS 09', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(38, '2024-02-06 17:44:35.995143', '10', 'SWS 10', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(39, '2024-02-06 17:45:36.259373', '2', 'AC 02', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(40, '2024-02-06 17:48:39.977709', '9', 'Versand object (9)', 1, '[{\"added\": {}}]', 14, 1),
(41, '2024-02-07 05:58:29.564732', '2', 'Thomas-Müntzner-Straße 5b, 39288 Burg', 1, '[{\"added\": {}}]', 7, 1),
(42, '2024-02-07 05:58:33.161726', '2', 'Logistikbataillon 171- Burg (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(43, '2024-02-07 05:59:35.785549', '2', 'Kurs object (2)', 1, '[{\"added\": {}}]', 18, 1),
(44, '2024-02-07 06:00:05.919028', '3', 'Logistikbataillon 171- Burg (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(45, '2024-02-07 06:01:25.915238', '10', 'Versand object (10)', 1, '[{\"added\": {}}]', 14, 1),
(46, '2024-02-07 06:02:56.655577', '3', 'Kurs object (3)', 1, '[{\"added\": {}}]', 18, 1),
(47, '2024-02-07 06:04:42.421621', '3', 'Pascalstraße 10s, 53123 Bonn', 1, '[{\"added\": {}}]', 7, 1),
(48, '2024-02-07 06:04:46.655334', '4', 'Kommando IT-Services der Bw - Bonn (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(49, '2024-02-07 06:05:15.516417', '11', 'Versand object (11)', 1, '[{\"added\": {}}]', 14, 1),
(50, '2024-02-07 06:17:09.026392', '4', 'Hohe Düne 30, 18119 Rostock', 1, '[{\"added\": {}}]', 7, 1),
(51, '2024-02-07 06:17:12.367990', '5', 'ZBrdSchBw Feuerwache Warnemünde (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(52, '2024-02-07 06:18:02.149868', '4', 'Kurs object (4)', 1, '[{\"added\": {}}]', 18, 1),
(53, '2024-02-07 06:18:38.076387', '12', 'Versand object (12)', 1, '[{\"added\": {}}]', 14, 1),
(54, '2024-02-07 06:18:53.036107', '5', 'AC 05', 2, '[{\"changed\": {\"fields\": [\"DruckerFuellstand\"]}}]', 10, 1),
(55, '2024-02-07 06:19:28.798328', '12', 'Versand object (12)', 2, '[{\"changed\": {\"fields\": [\"Kunde\"]}}]', 14, 1),
(56, '2024-02-07 06:22:02.829575', '5', 'Nürnberger Str. 184, 70374 Stuttgart', 1, '[{\"added\": {}}]', 7, 1),
(57, '2024-02-07 06:22:04.860214', '6', 'Landeskommando Baden-Württemberg Stuttgart (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(58, '2024-02-07 06:23:05.439402', '5', 'Kurs object (5)', 1, '[{\"added\": {}}]', 18, 1),
(59, '2024-02-07 06:24:14.014298', '13', 'Versand object (13)', 1, '[{\"added\": {}}]', 14, 1),
(60, '2024-02-07 07:26:52.140977', '10', 'Versand object (10)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(61, '2024-02-07 08:16:16.372321', '1', 'pit', 1, '[{\"added\": {}}]', 3, 1),
(62, '2024-02-07 08:16:53.091909', '2', 'rpanske', 1, '[{\"added\": {}}]', 4, 1),
(63, '2024-02-07 08:17:48.974799', '2', 'rpanske', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Groups\"]}}]', 4, 1),
(64, '2024-02-07 08:18:19.107913', '3', 'mukarram', 1, '[{\"added\": {}}]', 4, 1),
(65, '2024-02-07 08:20:14.901838', '3', 'mukarram', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Groups\"]}}]', 4, 1),
(66, '2024-02-07 08:20:47.225767', '4', 'aborowczak', 1, '[{\"added\": {}}]', 4, 1),
(67, '2024-02-07 08:21:24.806588', '4', 'aborowczak', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Groups\"]}}]', 4, 1),
(68, '2024-02-07 14:01:24.520799', '1', 'AC Win11+Office2019 V1', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 8, 1),
(69, '2024-02-07 14:02:22.208254', '2', 'AC Win11+Office2019 V2', 1, '[{\"added\": {}}]', 8, 1),
(70, '2024-02-07 14:02:38.293053', '4', 'AC 04', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(71, '2024-02-07 14:02:47.835763', '5', 'AC 05', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(72, '2024-02-07 14:02:56.029937', '6', 'AC 06', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(73, '2024-02-07 14:03:03.913100', '7', 'AC 07', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(74, '2024-02-07 14:14:03.274968', '1', 'AC 01', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(75, '2024-02-07 14:14:18.446357', '2', 'AC 02', 2, '[]', 10, 1),
(76, '2024-02-07 14:14:53.125897', '7', 'SWS 07', 2, '[]', 11, 1),
(77, '2024-02-07 14:16:46.617766', '11', 'Keiner', 3, '', 11, 1),
(78, '2024-02-07 18:11:09.372898', '2', 'AC 02', 2, '[]', 10, 1),
(79, '2024-02-09 08:32:36.664356', '3', 'AC_LOS2_V2', 1, '[{\"added\": {}}]', 8, 1),
(80, '2024-02-09 08:32:46.232425', '13', 'AC 13', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(81, '2024-02-09 08:32:55.549547', '13', 'AC 13', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(82, '2024-02-09 08:33:10.030497', '14', 'AC 14', 2, '[{\"changed\": {\"fields\": [\"Status\", \"Image\"]}}]', 10, 1),
(83, '2024-02-09 08:33:19.506544', '15', 'AC 15', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(84, '2024-02-09 08:33:30.957998', '4', 'AC 04', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(85, '2024-02-09 08:33:39.009542', '5', 'AC 05', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(86, '2024-02-09 08:33:47.737427', '5', 'AC 05', 2, '[]', 10, 1),
(87, '2024-02-09 08:33:56.835964', '6', 'AC 06', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(88, '2024-02-09 08:34:05.050214', '1', 'AC 01', 2, '[]', 10, 1),
(89, '2024-02-09 08:34:10.712147', '2', 'AC 02', 2, '[]', 10, 1),
(90, '2024-02-09 08:34:39.428964', '15', 'AC 15', 2, '[]', 10, 1),
(91, '2024-02-09 08:34:48.628640', '14', 'AC 14', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(92, '2024-02-09 08:34:55.090988', '13', 'AC 13', 2, '[]', 10, 1),
(93, '2024-02-09 08:35:50.523768', '10', 'SWS 10', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(94, '2024-02-09 08:35:58.567406', '5', 'SWS 05', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(95, '2024-02-09 08:36:13.336538', '6', 'SWS 06', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(96, '2024-02-09 09:08:43.634421', '6', 'Landsberger Str. 133, 04157 Leipzig', 1, '[{\"added\": {}}]', 7, 1),
(97, '2024-02-09 09:08:46.483702', '7', '9. Kompanie Feldjägerregiment 1 (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(98, '2024-02-09 09:09:01.535708', '7', '9. Kompanie Feldjägerregiment 1 Leibzig (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 16, 1),
(99, '2024-02-09 09:11:32.659870', '6', 'Kurs object (6)', 1, '[{\"added\": {}}]', 18, 1),
(100, '2024-02-09 09:11:47.477137', '14', 'Versand object (14)', 1, '[{\"added\": {}}]', 14, 1),
(101, '2024-02-09 09:13:27.933302', '7', 'Kugelfangtrift 1, 30179 Hannover', 1, '[{\"added\": {}}]', 7, 1),
(102, '2024-02-09 09:13:41.218044', '8', 'Schule für Feldjäger und Stabsdienst der Bundeswehr Hannover (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(103, '2024-02-09 09:14:42.474244', '7', 'Kurs object (7)', 1, '[{\"added\": {}}]', 18, 1),
(104, '2024-02-09 09:14:57.830209', '15', 'Versand object (15)', 1, '[{\"added\": {}}]', 14, 1),
(105, '2024-02-09 09:15:41.692167', '15', 'Versand object (15)', 2, '[{\"changed\": {\"fields\": [\"Kunde\", \"Schiene\", \"Server\"]}}]', 14, 1),
(106, '2024-02-09 09:24:26.691904', '15', 'Versand object (15)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(107, '2024-02-09 09:28:03.518194', '1', 'SWS 01', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(108, '2024-02-09 09:28:25.461050', '2', 'SWS 02', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(109, '2024-02-09 09:28:39.841332', '8', 'SWS 08', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(110, '2024-02-09 09:28:54.901399', '3', 'SWS 03', 2, '[]', 11, 1),
(111, '2024-02-09 09:29:01.164513', '4', 'SWS 04', 2, '[]', 11, 1),
(112, '2024-02-09 09:29:07.351142', '6', 'SWS 06', 2, '[]', 11, 1),
(113, '2024-02-09 09:29:29.099311', '7', 'SWS 07', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(114, '2024-02-09 09:29:36.093917', '8', 'SWS 08', 2, '[]', 11, 1),
(115, '2024-02-09 09:29:44.979014', '9', 'SWS 09', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(116, '2024-02-09 09:31:20.145006', '7', 'AC 07', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(117, '2024-02-09 09:31:48.571128', '13', 'AC 13', 2, '[]', 10, 1),
(118, '2024-02-09 09:31:56.082284', '12', 'AC 12', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(119, '2024-02-09 09:32:03.935455', '11', 'AC 11', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(120, '2024-02-09 09:32:14.846468', '10', 'AC 10', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(121, '2024-02-09 09:32:23.616697', '7', 'AC 07', 2, '[]', 10, 1),
(122, '2024-02-09 09:32:37.658066', '6', 'AC 06', 2, '[]', 10, 1),
(123, '2024-02-09 09:33:27.773843', '8', 'AC 08', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(124, '2024-02-09 09:33:37.552605', '9', 'AC  09', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 10, 1),
(125, '2024-02-09 10:02:31.241817', '8', 'Berliner Str. 100, 34560 Fritzlar', 1, '[{\"added\": {}}]', 7, 1),
(126, '2024-02-09 10:02:35.370320', '9', 'Zentrum Brandschutz der Bundeswehr Feuerwache Fritzlar (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(127, '2024-02-09 10:03:14.714854', '8', 'Kurs object (8)', 1, '[{\"added\": {}}]', 18, 1),
(128, '2024-02-09 10:03:21.887948', '16', 'Versand object (16)', 1, '[{\"added\": {}}]', 14, 1),
(129, '2024-02-09 10:03:32.213115', '16', 'Versand object (16)', 2, '[{\"changed\": {\"fields\": [\"Kunde\"]}}]', 14, 1),
(130, '2024-02-09 11:52:41.505457', '10', 'AC 10', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(131, '2024-02-09 12:40:18.963846', '14', 'Versand object (14)', 2, '[{\"changed\": {\"fields\": [\"Schiene\"]}}]', 14, 1),
(132, '2024-02-13 09:40:20.970744', '4', 'HP-Win11PRO-TN & HP-Win11PRO-DOZ V1', 1, '[{\"added\": {}}]', 8, 1),
(133, '2024-02-13 09:40:36.517565', '16', 'HP 01', 1, '[{\"added\": {}}]', 10, 1),
(134, '2024-02-13 09:41:52.868293', '2', 'AC 02', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(135, '2024-02-13 09:42:09.764937', '5', 'SWS 05', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(136, '2024-02-13 09:47:56.253230', '6', 'SWS 06', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(137, '2024-02-13 09:48:03.910437', '10', 'SWS 10', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(138, '2024-02-13 09:48:29.752004', '5', 'AC 05', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(139, '2024-02-13 09:48:37.035864', '6', 'AC 06', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(140, '2024-02-13 10:26:11.441577', '9', 'Maxhofstraße 1, 82343 Pöcking', 1, '[{\"added\": {}}]', 7, 1),
(141, '2024-02-13 10:26:25.381142', '10', 'Informationsschule der Bundeswehr - Pöcking (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(142, '2024-02-13 10:27:29.850509', '9', '51982', 1, '[{\"added\": {}}]', 18, 1),
(143, '2024-02-13 10:28:31.802919', '1', 'Rueckholung object (1)', 1, '[{\"added\": {}}]', 12, 1),
(144, '2024-02-13 11:49:40.764772', '16', 'HP 01', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(145, '2024-02-14 10:38:22.577157', '2', 'orga', 1, '[{\"added\": {}}]', 3, 1),
(146, '2024-02-14 11:14:47.786336', '17', '52413 Landeskommando Baden-Württemberg (Behörde)', 1, '[{\"added\": {}}]', 14, 1),
(147, '2024-02-14 11:17:50.202211', '2', '51910 ZBrdSchBw Feuerwache Warnemünde (Behörde)', 1, '[{\"added\": {}}]', 12, 1),
(148, '2024-02-14 11:18:32.337366', '3', '52428 Landeskommando Baden-Württemberg Stuttgart (Behörde)', 1, '[{\"added\": {}}]', 12, 1),
(149, '2024-02-14 11:20:26.499014', '6', 'SWS 06', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(150, '2024-02-14 11:21:07.627018', '10', 'SWS 10', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(151, '2024-02-15 07:15:52.459314', '10', 'Marburger Str. 75, 35066 Frankenberg/Eder', 1, '[{\"added\": {}}]', 7, 1),
(152, '2024-02-15 07:15:54.404666', '11', 'Bataillon Elektronische Kampfführung 932 (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(153, '2024-02-15 07:16:08.196239', '10', '52562', 1, '[{\"added\": {}}]', 18, 1),
(154, '2024-02-15 07:18:42.509472', '18', '52562 Bataillon Elektronische Kampfführung 932 (Behörde)', 1, '[{\"added\": {}}]', 14, 1),
(155, '2024-02-15 07:19:13.250534', '11', 'Bataillon Elektronische Kampfführung 932 - Frankenberg (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 16, 1),
(156, '2024-02-15 07:19:25.900798', '18', '52562 Bataillon Elektronische Kampfführung 932 - Frankenberg (Behörde)', 2, '[]', 14, 1),
(157, '2024-02-15 07:21:43.176680', '11', 'Zeppelinstr. 18, 99096 Erfurt', 1, '[{\"added\": {}}]', 7, 1),
(158, '2024-02-15 07:21:47.124783', '12', 'Logistikkommando der Bundeswehr Erfurt (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(159, '2024-02-15 07:22:22.708421', '19', 'None Logistikkommando der Bundeswehr Erfurt (Behörde)', 1, '[{\"added\": {}}]', 14, 1),
(160, '2024-02-15 07:23:39.218232', '11', '52585', 1, '[{\"added\": {}}]', 18, 1),
(161, '2024-02-15 07:23:45.603389', '19', '52585 Logistikkommando der Bundeswehr Erfurt (Behörde)', 2, '[{\"changed\": {\"fields\": [\"VA Nummer\"]}}]', 14, 1),
(162, '2024-02-15 07:26:06.540400', '12', 'Gnoiener Chaussee, 18334 Bad Sülze', 1, '[{\"added\": {}}]', 7, 1),
(163, '2024-02-15 07:26:10.321360', '13', 'Flugabwehrraketengruppe 24 - Bad Sülze (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(164, '2024-02-15 07:26:45.717617', '12', '52665', 1, '[{\"added\": {}}]', 18, 1),
(165, '2024-02-15 07:27:01.222168', '20', '52665 None', 1, '[{\"added\": {}}]', 14, 1),
(166, '2024-02-15 07:27:43.584764', '12', 'noch ungeplant', 1, '[{\"added\": {}}]', 11, 1),
(167, '2024-02-15 07:27:55.304621', '20', '52665 Flugabwehrraketengruppe 24 - Bad Sülze (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Kunde\", \"Schiene\", \"Server\"]}}]', 14, 1),
(168, '2024-02-15 07:32:38.322239', '13', 'Peter-Strasser-Platz 1, 27639 Wurster Nordseeküste', 1, '[{\"added\": {}}]', 7, 1),
(169, '2024-02-15 07:32:51.293853', '14', 'Marinefliegergeschwader 5 -Wurster Nordseeküste (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(170, '2024-02-15 07:33:43.464163', '13', '52744', 1, '[{\"added\": {}}]', 18, 1),
(171, '2024-02-15 07:33:55.072410', '21', '52744 None', 1, '[{\"added\": {}}]', 14, 1),
(172, '2024-02-15 07:34:33.499480', '21', '52744 Marinefliegergeschwader 5 -Wurster Nordseeküste (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Kunde\", \"Schiene\", \"Server\"]}}]', 14, 1),
(173, '2024-02-15 07:37:08.279663', '14', 'Fliegerhorst 1, 04916 Schönewalde OT Brandis', 1, '[{\"added\": {}}]', 7, 1),
(174, '2024-02-15 07:37:10.477176', '15', 'Einsatzführungsbereich 3 - Schönewalde (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(175, '2024-02-15 07:37:49.128362', '14', '52676', 1, '[{\"added\": {}}]', 18, 1),
(176, '2024-02-15 07:37:52.057458', '22', '52676 None', 1, '[{\"added\": {}}]', 14, 1),
(177, '2024-02-15 07:38:20.452087', '22', '52676 Einsatzführungsbereich 3 - Schönewalde (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Kunde\", \"Schiene\", \"Server\"]}}]', 14, 1),
(178, '2024-02-15 07:39:39.515611', '15', 'Kurt-Schumacher-Damm 41, 13405 Berlin', 1, '[{\"added\": {}}]', 7, 1),
(179, '2024-02-15 07:39:41.897204', '16', 'Territoriales Führungskommando der Bundeswehr (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(180, '2024-02-15 07:39:47.731595', '23', 'None Territoriales Führungskommando der Bundeswehr (Behörde)', 1, '[{\"added\": {}}]', 14, 1),
(181, '2024-02-15 07:40:25.769985', '16', 'Territoriales Führungskommando der Bundeswehr - Berlin (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 16, 1),
(182, '2024-02-15 07:40:54.795071', '15', '52695', 1, '[{\"added\": {}}]', 18, 1),
(183, '2024-02-15 07:41:12.465618', '23', '52695 Territoriales Führungskommando der Bundeswehr - Berlin (Behörde)', 2, '[{\"changed\": {\"fields\": [\"VA Nummer\", \"Schiene\", \"Server\"]}}]', 14, 1),
(184, '2024-02-15 07:45:40.584221', '1', 'Landeskommando Baden-Württemberg - Karlsruhe (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 16, 1),
(185, '2024-02-15 07:46:10.166200', '4', '52413 Landeskommando Baden-Württemberg - Karlsruhe (Behörde)', 1, '[{\"added\": {}}]', 12, 1),
(186, '2024-02-15 07:47:51.482384', '5', '51916 Zentrum Brandschutz der Bundeswehr Feuerwache Fritzlar (Behörde)', 1, '[{\"added\": {}}]', 12, 1),
(187, '2024-02-15 07:49:21.663643', '6', '52430 9. Kompanie Feldjägerregiment 1 Leibzig (Behörde)', 1, '[{\"added\": {}}]', 12, 1),
(188, '2024-02-15 08:57:00.407679', '17', '52413 Landeskommando Baden-Württemberg - Karlsruhe (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(189, '2024-02-15 08:57:52.331750', '15', '52420 Schule für Feldjäger und Stabsdienst der Bundeswehr Hannover (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(190, '2024-02-15 08:58:39.029621', '5', 'SWS 05', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(191, '2024-02-15 08:58:52.501652', '2', 'AC 02', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(192, '2024-02-15 10:42:04.434814', '13', 'SWS 11', 1, '[{\"added\": {}}]', 11, 1),
(193, '2024-02-15 10:42:14.924041', '14', 'SWS 12', 1, '[{\"added\": {}}]', 11, 1),
(194, '2024-02-15 10:42:46.012932', '15', 'SWS 13', 1, '[{\"added\": {}}]', 11, 1),
(195, '2024-02-15 10:42:58.546197', '16', 'SWS 14', 1, '[{\"added\": {}}]', 11, 1),
(196, '2024-02-15 10:43:18.928519', '17', 'SWS 15', 1, '[{\"added\": {}}]', 11, 1),
(197, '2024-02-15 10:43:38.656911', '22', '52676 Einsatzführungsbereich 3 - Schönewalde (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(198, '2024-02-15 10:43:45.350546', '21', '52744 Marinefliegergeschwader 5 -Wurster Nordseeküste (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(199, '2024-02-15 10:43:55.185712', '20', '52665 Flugabwehrraketengruppe 24 - Bad Sülze (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(200, '2024-02-15 10:44:06.115934', '19', '52585 Logistikkommando der Bundeswehr Erfurt (Behörde)', 2, '[]', 14, 1),
(201, '2024-02-15 10:44:10.614136', '18', '52562 Bataillon Elektronische Kampfführung 932 - Frankenberg (Behörde)', 2, '[]', 14, 1),
(202, '2024-02-15 10:44:15.218188', '17', '52413 Landeskommando Baden-Württemberg - Karlsruhe (Behörde)', 2, '[]', 14, 1),
(203, '2024-02-15 10:44:28.573788', '16', '51916 Zentrum Brandschutz der Bundeswehr Feuerwache Fritzlar (Behörde)', 2, '[]', 14, 1),
(204, '2024-02-15 10:44:36.062214', '15', '52420 Schule für Feldjäger und Stabsdienst der Bundeswehr Hannover (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(205, '2024-02-15 10:44:44.380205', '14', '52430 9. Kompanie Feldjägerregiment 1 Leibzig (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(206, '2024-02-15 10:48:37.004199', '12', 'AC 12', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(207, '2024-02-15 10:48:57.142613', '11', 'AC 11', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(208, '2024-02-15 10:49:11.312156', '4', 'AC 04', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(209, '2024-02-15 10:49:49.241973', '2', 'AC 02', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(210, '2024-02-15 10:50:08.553448', '14', 'SWS 12', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(211, '2024-02-15 10:50:15.398162', '14', 'SWS 12', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(212, '2024-02-15 10:50:28.028031', '4', 'SWS 04', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(213, '2024-02-15 10:50:34.149215', '13', 'SWS 11', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(214, '2024-02-15 10:51:08.349660', '2', 'SWS 02', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(215, '2024-02-15 10:51:30.175891', '15', 'SWS 13', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(216, '2024-02-15 10:51:34.365056', '15', 'SWS 13', 2, '[]', 11, 1),
(217, '2024-02-15 10:51:43.733726', '16', 'SWS 14', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(218, '2024-02-15 10:51:54.633388', '17', 'SWS 15', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(219, '2024-02-15 10:52:23.145597', '7', 'AC 07', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(220, '2024-02-15 10:53:04.441481', '10', 'AC 10', 2, '[]', 10, 1),
(221, '2024-02-15 10:53:17.692556', '13', 'AC 13', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(222, '2024-02-15 10:53:26.806741', '14', 'AC 14', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(223, '2024-02-15 10:53:33.010562', '15', 'AC 15', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 10, 1),
(224, '2024-02-15 10:54:11.481405', '6', '52430 9. Kompanie Feldjägerregiment 1 Leibzig (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 12, 1),
(225, '2024-02-15 10:54:15.447806', '5', '51916 Zentrum Brandschutz der Bundeswehr Feuerwache Fritzlar (Behörde)', 2, '[]', 12, 1),
(226, '2024-02-15 10:54:34.550642', '4', '52413 Landeskommando Baden-Württemberg - Karlsruhe (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 12, 1),
(227, '2024-02-15 10:54:45.576823', '2', '51910 ZBrdSchBw Feuerwache Warnemünde (Behörde)', 2, '[]', 12, 1),
(228, '2024-02-15 10:54:58.505004', '1', '51982 Informationsschule der Bundeswehr - Pöcking (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 12, 1),
(229, '2024-02-15 10:55:26.014645', '1', '51982 Informationsschule der Bundeswehr - Pöcking (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 12, 1),
(230, '2024-02-15 10:56:49.475272', '18', '52562 Bataillon Elektronische Kampfführung 932 - Frankenberg (Behörde)', 2, '[{\"changed\": {\"fields\": [\"Server\"]}}]', 14, 1),
(231, '2024-02-15 10:58:37.781159', '5', 'SWS 05', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(232, '2024-02-15 11:11:02.458270', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(233, '2024-02-15 13:12:18.710268', '16', 'Philipp-Reis-Str. 2, 54568 Gerolstein', 1, '[{\"added\": {}}]', 7, 1),
(234, '2024-02-15 13:12:21.496604', '17', 'Informationstechnikbatallion 281 (Behörde)', 1, '[{\"added\": {}}]', 16, 1),
(235, '2024-02-15 13:15:36.265627', '16', '52110', 1, '[{\"added\": {}}]', 18, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(17, 'kunden', 'ansprechpartner'),
(16, 'kunden', 'kunde'),
(18, 'kurse', 'kurs'),
(13, 'pit', 'abholung'),
(8, 'pit', 'festplattenimagenotebook'),
(9, 'pit', 'festplattenimageserver'),
(12, 'pit', 'rueckholung'),
(10, 'pit', 'schiene'),
(11, 'pit', 'server'),
(14, 'pit', 'versand'),
(15, 'postits', 'postit'),
(6, 'sessions', 'session'),
(7, 'start', 'adresse'),
(19, 'trainer', 'trainer');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-02-06 17:13:39.897946'),
(2, 'auth', '0001_initial', '2024-02-06 17:13:40.004528'),
(3, 'admin', '0001_initial', '2024-02-06 17:13:40.028899'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-02-06 17:13:40.036174'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-02-06 17:13:40.043370'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-02-06 17:13:40.070371'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-02-06 17:13:40.083581'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-02-06 17:13:40.097508'),
(9, 'auth', '0004_alter_user_username_opts', '2024-02-06 17:13:40.105922'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-02-06 17:13:40.119533'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-02-06 17:13:40.120597'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-02-06 17:13:40.127674'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-02-06 17:13:40.137711'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-02-06 17:13:40.148005'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-02-06 17:13:40.161133'),
(16, 'auth', '0011_update_proxy_permissions', '2024-02-06 17:13:40.169131'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-02-06 17:13:40.180724'),
(18, 'start', '0001_initial', '2024-02-06 17:13:40.185919'),
(19, 'start', '0002_remove_adresse_land', '2024-02-06 17:13:40.192564'),
(20, 'kunden', '0001_initial', '2024-02-06 17:13:40.216105'),
(21, 'trainer', '0001_initial', '2024-02-06 17:13:40.221383'),
(22, 'kurse', '0001_initial', '2024-02-06 17:13:40.244595'),
(23, 'pit', '0001_initial', '2024-02-06 17:13:40.396972'),
(24, 'postits', '0001_initial', '2024-02-06 17:13:40.414944'),
(25, 'sessions', '0001_initial', '2024-02-06 17:13:40.425451'),
(26, 'kunden', '0002_alter_kunde_adresse', '2024-02-14 09:38:02.675549'),
(27, 'kurse', '0002_kurs_hardware_status', '2024-02-15 11:45:53.271765'),
(28, 'pit', '0002_alter_schiene_status_alter_server_status', '2024-02-15 11:45:53.279392');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('6u2ff165z1dx9zelj1ixuy9ns2kz5tj6', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1ra88D:ImPaeIHoSKqXXZXIvnmPQzYZ1oo3_qD9EUs_cXENuw4', '2024-02-28 05:48:29.470068'),
('9viuq9dy1zqr5rtdajx75k4yqbwwf5zj', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1rYVLn:qV9SKsM4jIKMqYssEzaMKdvW9-YjuiP-95o4cwSYj_k', '2024-02-23 18:11:47.105505'),
('e9ajjgiitkdcjq6hzyvw7k6vj9yv2qdu', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1rXP2V:jKd_-BfgHKnilXr_yHV9-fv8w7POmgeRYeZadMFnhyc', '2024-02-20 17:15:19.264590'),
('erb5fu6m5p7vx83leyomq4f4vbccmosg', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1rZouy:esF_NsDjwykKRz3rvVAlMKI8xR2ukQzF4djorLEL8iQ', '2024-02-27 09:17:32.638356'),
('kbx24o7rvvpkvaz23p51wj1z3sx51jc5', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1rXatd:yjCqCmbCuRrMd_x1a1JpZDkWLCsoSNH7LbNZNSOdw5E', '2024-02-21 05:54:57.517227'),
('p70wwj5xn4r3lntatgevcz2mm7ck819f', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1raZdL:WVX5GmqoIQyYp_YXvG8XBFaUvS3yMI8kJZwt2AAb5Io', '2024-02-29 11:10:27.014598'),
('sdrx9od58je8u4tkfez76ew9c63h12sk', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1rXiQk:b7LUfahY15JJMUrL6e3W_8wv2P8ETTC5qjTV0jrfHS8', '2024-02-21 13:57:38.708521'),
('vvrtp1ildh1u0rexu7nw1pjb0hv96b6l', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1rYMBJ:Zo_m8f90fHJ3oi9dJD3V3deQbD24S6t95EoIvP31sXo', '2024-02-23 08:24:21.835305'),
('zsv7mtab5miijsa3tfump5djzuce2av4', '.eJxVjDsOwjAQBe_iGlmO_0tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV3ZwC6_G8b0pHaA_IjtPvM0t3WZkB8KP2nn45zpdTvdv4Mae91rGAjAGpuNKmAFaa8NlmSFx0xSYczSKWkgFW18FNopS1C8Ra0c7DL7fAHOODcQ:1rXdHE:RYLOr35zWY3JszDwIxONCFxwCDNExdyHLw_RTs9bWVY', '2024-02-21 08:27:28.872487');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `kunden_ansprechpartner`
--

CREATE TABLE `kunden_ansprechpartner` (
  `id` bigint NOT NULL,
  `Anrede` varchar(255) NOT NULL,
  `vorname` varchar(255) DEFAULT NULL,
  `nachname` varchar(255) NOT NULL,
  `Telefon` varchar(17) DEFAULT NULL,
  `kunde_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `kunden_kunde`
--

CREATE TABLE `kunden_kunde` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `typ` varchar(255) NOT NULL,
  `adresse_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `kunden_kunde`
--

INSERT INTO `kunden_kunde` (`id`, `name`, `typ`, `adresse_id`) VALUES
(1, 'Landeskommando Baden-Württemberg - Karlsruhe', 'Behörde', 1),
(2, 'Logistikbataillon 171- Burg', 'Behörde', 2),
(4, 'Kommando IT-Services der Bw - Bonn', 'Behörde', 3),
(5, 'ZBrdSchBw Feuerwache Warnemünde', 'Behörde', 4),
(6, 'Landeskommando Baden-Württemberg Stuttgart', 'Behörde', 5),
(7, '9. Kompanie Feldjägerregiment 1 Leibzig', 'Behörde', 6),
(8, 'Schule für Feldjäger und Stabsdienst der Bundeswehr Hannover', 'Behörde', 7),
(9, 'Zentrum Brandschutz der Bundeswehr Feuerwache Fritzlar', 'Behörde', 8),
(10, 'Informationsschule der Bundeswehr - Pöcking', 'Behörde', 9),
(11, 'Bataillon Elektronische Kampfführung 932 - Frankenberg', 'Behörde', 10),
(12, 'Logistikkommando der Bundeswehr Erfurt', 'Behörde', 11),
(13, 'Flugabwehrraketengruppe 24 - Bad Sülze', 'Behörde', 12),
(14, 'Marinefliegergeschwader 5 -Wurster Nordseeküste', 'Behörde', 13),
(15, 'Einsatzführungsbereich 3 - Schönewalde', 'Behörde', 14),
(16, 'Territoriales Führungskommando der Bundeswehr - Berlin', 'Behörde', 15),
(17, 'Informationstechnikbatallion 281', 'Behörde', 16);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `kurse_kurs`
--

CREATE TABLE `kurse_kurs` (
  `id` bigint NOT NULL,
  `va_nummer` int NOT NULL,
  `thema` varchar(50) NOT NULL,
  `kurs_start` datetime(6) DEFAULT NULL,
  `kurs_ende` datetime(6) DEFAULT NULL,
  `kunde_id` bigint DEFAULT NULL,
  `trainer_id` bigint DEFAULT NULL,
  `Hardware_Status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `kurse_kurs`
--

INSERT INTO `kurse_kurs` (`id`, `va_nummer`, `thema`, `kurs_start`, `kurs_ende`, `kunde_id`, `trainer_id`, `Hardware_Status`) VALUES
(1, 52413, 'Word Aufbau', '2024-03-04 06:30:00.000000', '2024-03-06 15:00:00.000000', 1, NULL, 'mit HW'),
(2, 52470, 'Word GL', '2024-02-19 06:30:00.000000', '2024-02-20 15:00:00.000000', 2, NULL, 'mit HW'),
(3, 52303, 'Excel GL', '2024-02-19 06:30:00.000000', '2024-02-20 15:00:00.000000', NULL, NULL, 'mit HW'),
(4, 51910, 'Outlook', '2024-02-26 06:30:00.000000', '2024-02-28 15:00:00.000000', 5, NULL, 'mit HW'),
(5, 52428, 'SharePoint', '2024-02-26 06:30:00.000000', '2024-02-28 15:00:00.000000', 6, NULL, 'mit HW'),
(6, 52430, 'Kombi', '2024-03-04 06:30:00.000000', '2024-03-08 10:30:00.000000', 7, NULL, 'mit HW'),
(7, 52420, 'Word GL', '2024-03-04 06:30:00.000000', '2024-02-05 15:00:00.000000', 8, NULL, 'mit HW'),
(8, 51916, 'Outlook', '2024-03-04 06:30:00.000000', '2024-03-06 15:00:00.000000', 9, NULL, 'mit HW'),
(9, 51982, 'Word GL', '2024-02-29 06:30:00.000000', '2024-03-01 10:30:00.000000', 10, NULL, 'mit HW'),
(10, 52562, 'Word GL', '2024-03-11 06:30:00.000000', '2024-03-12 15:00:00.000000', 11, NULL, 'mit HW'),
(11, 52585, 'Kombi', '2024-03-11 06:30:00.000000', '2024-03-15 10:30:00.000000', 12, NULL, 'mit HW'),
(12, 52665, 'Kombi', '2024-03-11 06:30:00.000000', '2024-03-15 10:30:00.000000', 13, NULL, 'mit HW'),
(13, 52744, 'Word GL', '2024-03-11 06:30:00.000000', '2024-03-12 15:00:00.000000', 14, NULL, 'mit HW'),
(14, 52676, 'SharePoint GL', '2024-03-12 06:30:00.000000', '2024-03-14 15:00:00.000000', 15, NULL, 'mit HW'),
(15, 52695, 'Kombi', '2024-03-11 06:30:00.000000', '2024-03-15 10:30:00.000000', 16, NULL, 'mit HW'),
(16, 52110, 'Excel GL', '2024-04-08 05:30:00.000000', '2024-04-09 14:00:00.000000', 17, NULL, 'mit HW');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pit_abholung`
--

CREATE TABLE `pit_abholung` (
  `id` bigint NOT NULL,
  `VA_Nummer` int NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Vorname` varchar(255) NOT NULL,
  `Name2` varchar(255) DEFAULT NULL,
  `Vorname2` varchar(255) DEFAULT NULL,
  `Mobile1` varchar(17) NOT NULL,
  `Mobile2` varchar(17) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Firmenwagen` varchar(255) NOT NULL,
  `Fahrzeugvermieter` varchar(255) DEFAULT NULL,
  `Fahrzeug_Type` varchar(255) DEFAULT NULL,
  `Kennzeichen` varchar(255) NOT NULL,
  `Datum` date DEFAULT NULL,
  `Tourdaten` longtext,
  `status` varchar(255) NOT NULL,
  `Kunde_id` bigint DEFAULT NULL,
  `Schiene_id` bigint DEFAULT NULL,
  `Server_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pit_festplattenimagenotebook`
--

CREATE TABLE `pit_festplattenimagenotebook` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `beschreibung` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `pit_festplattenimagenotebook`
--

INSERT INTO `pit_festplattenimagenotebook` (`id`, `name`, `beschreibung`) VALUES
(1, 'AC Win11+Office2019 V1', ''),
(2, 'AC Win11+Office2019 V2', ''),
(3, 'AC_LOS2_V2', ''),
(4, 'HP-Win11PRO-TN & HP-Win11PRO-DOZ V1', '');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pit_festplattenimageserver`
--

CREATE TABLE `pit_festplattenimageserver` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `beschreibung` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `pit_festplattenimageserver`
--

INSERT INTO `pit_festplattenimageserver` (`id`, `name`, `beschreibung`) VALUES
(1, 'All-in', ''),
(2, 'unbekannt', '');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pit_rueckholung`
--

CREATE TABLE `pit_rueckholung` (
  `id` bigint NOT NULL,
  `RueckDatum` date DEFAULT NULL,
  `Kunde_id` bigint DEFAULT NULL,
  `VA_Nummer_id` bigint DEFAULT NULL,
  `Schiene_id` bigint DEFAULT NULL,
  `Server_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `pit_rueckholung`
--

INSERT INTO `pit_rueckholung` (`id`, `RueckDatum`, `Kunde_id`, `VA_Nummer_id`, `Schiene_id`, `Server_id`) VALUES
(1, '2024-03-04', 10, 9, 1, 7),
(2, '2024-03-04', 5, 4, 8, 8),
(3, '2024-03-04', 6, 5, 9, 9),
(4, '2024-03-11', 1, 1, 2, 2),
(5, '2024-03-11', 9, 8, 4, 4),
(6, '2024-03-11', 7, 6, 12, 14);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pit_schiene`
--

CREATE TABLE `pit_schiene` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `DruckerFuellstand` int NOT NULL,
  `Nighthawk` varchar(10) NOT NULL,
  `Bemerkung` longtext NOT NULL,
  `image_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `pit_schiene`
--

INSERT INTO `pit_schiene` (`id`, `name`, `status`, `DruckerFuellstand`, `Nighthawk`, `Bemerkung`, `image_id`) VALUES
(1, 'AC 01', 'Standort', 100, 'NH 01', 'Fehler/Bemerkung', 1),
(2, 'AC 02', 'Reserviert', 100, 'NH 02', 'Fehler/Bemerkung', 1),
(3, 'AC 03', 'Standort', 100, 'NH 03', 'Fehler/Bemerkung', 1),
(4, 'AC 04', 'Reserviert', 100, 'NH 04', 'Fehler/Bemerkung', 3),
(5, 'AC 05', 'Standort', 41, 'NH 05', 'Fehler/Bemerkung', 3),
(6, 'AC 06', 'Standort', 100, 'NH 06', 'Fehler/Bemerkung', 3),
(7, 'AC 07', 'Reserviert', 100, 'NH 07', 'Fehler/Bemerkung', 3),
(8, 'AC 08', 'Versand', 100, 'NH 08', 'Fehler/Bemerkung', 3),
(9, 'AC  09', 'Versand', 100, 'NH 01', 'Fehler/Bemerkung', 3),
(10, 'AC 10', 'Standort', 100, 'NH 10', 'Fehler/Bemerkung', 3),
(11, 'AC 11', 'Reserviert', 100, 'NH 11', 'Fehler/Bemerkung', 3),
(12, 'AC 12', 'Reserviert', 100, 'NH 12', 'Fehler/Bemerkung', 3),
(13, 'AC 13', 'Reserviert', 100, 'NH 13', 'Fehler/Bemerkung', 3),
(14, 'AC 14', 'Reserviert', 100, 'NH 14', 'Fehler/Bemerkung', 3),
(15, 'AC 15', 'Reserviert', 100, 'NH 15', 'Fehler/Bemerkung', 3),
(16, 'HP 01', 'Lager', 100, 'HP 01', 'Fehler/Bemerkung', 4),
(17, 'HP 02', 'Lager', 100, 'NH 16', 'Fehler/Bemerkung', 4);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pit_server`
--

CREATE TABLE `pit_server` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `Bemerkung` longtext NOT NULL,
  `image_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `pit_server`
--

INSERT INTO `pit_server` (`id`, `name`, `status`, `Bemerkung`, `image_id`) VALUES
(1, 'SWS 01', 'Lager', 'Fehler/Bemerkung', 1),
(2, 'SWS 02', 'Reserviert', 'Fehler/Bemerkung', 1),
(3, 'SWS 03', 'Standort', 'Fehler/Bemerkung', 1),
(4, 'SWS 04', 'Reserviert', 'Fehler/Bemerkung', 1),
(5, 'SWS 05', 'Reserviert', 'Fehler/Bemerkung', 1),
(6, 'SWS 06', 'Standort', 'Fehler/Bemerkung', 1),
(7, 'SWS 07', 'Standort', 'Fehler/Bemerkung', 1),
(8, 'SWS 08', 'Versand', 'Fehler/Bemerkung', 1),
(9, 'SWS 09', 'Versand', 'Fehler/Bemerkung', 1),
(10, 'SWS 10', 'Standort', 'Fehler/Bemerkung', 1),
(12, 'noch ungeplant', 'Lager', 'Fehler/Bemerkung', NULL),
(13, 'SWS 11', 'Reserviert', 'Fehler/Bemerkung', 1),
(14, 'SWS 12', 'Reserviert', 'Fehler/Bemerkung', 1),
(15, 'SWS 13', 'Reserviert', 'Fehler/Bemerkung', 1),
(16, 'SWS 14', 'Reserviert', 'Fehler/Bemerkung', 1),
(17, 'SWS 15', 'Reserviert', 'Fehler/Bemerkung', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pit_versand`
--

CREATE TABLE `pit_versand` (
  `id` bigint NOT NULL,
  `Datum` date DEFAULT NULL,
  `Kunde_id` bigint DEFAULT NULL,
  `Schiene_id` bigint DEFAULT NULL,
  `Server_id` bigint DEFAULT NULL,
  `VA_Nummer_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `pit_versand`
--

INSERT INTO `pit_versand` (`id`, `Datum`, `Kunde_id`, `Schiene_id`, `Server_id`, `VA_Nummer_id`) VALUES
(14, '2024-02-26', 7, 12, 14, 6),
(15, '2024-02-26', 8, 11, 13, 7),
(16, '2024-02-26', 9, 4, 4, 8),
(17, '2024-02-26', 1, 2, 2, 1),
(18, '2024-03-04', 11, 7, 5, 10),
(19, '2024-03-04', 12, 10, 10, 11),
(20, '2024-03-04', 13, 13, 15, 12),
(21, '2024-03-04', 14, 14, 16, 13),
(22, '2024-02-04', 15, 15, 17, 14),
(23, '2024-03-04', 16, 16, 12, 15),
(24, '2024-04-01', 17, NULL, NULL, 16);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `postits_postit`
--

CREATE TABLE `postits_postit` (
  `id` bigint NOT NULL,
  `title` varchar(100) NOT NULL,
  `text` longtext NOT NULL,
  `position_x` int DEFAULT NULL,
  `position_y` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `postits_postit`
--

INSERT INTO `postits_postit` (`id`, `title`, `text`, `position_x`, `position_y`, `created_at`, `user_id`) VALUES
(1, 'DOKMBw Präsens', '<p>AnwdgAss 19.02.-23.02.2024 und 26.02.-01.03.2024 bei USH in 04509 Delitzsch Storniert</p>\r\n\r\n<ol>\r\n	<li>AnwdgMgr 08.04.-19.04.2024 bei ML in K&ouml;ln</li>\r\n	<li>F&uuml;r die zwei AwndgAss-Trainings 15.-26.04. Ort noch offen (wahrscheinlich Hannover oder Hamburg)</li>\r\n	<li>AnwdgAss 03.06.-07.06.2024 und 10.06.-14.06.2024 bei SanAkBw in 80937 M&uuml;nchen</li>\r\n</ol>\r\n\r\n<p>&nbsp;</p>', NULL, NULL, '2024-02-07 06:51:32.423340', 1),
(2, 'DPD Reklamieren auf Rechnung Feb.', '<ol>\r\n	<li>01505190221093</li>\r\n	<li>01505190221092</li>\r\n	<li>01505190221091</li>\r\n	<li>01505190221090</li>\r\n</ol>\r\n\r\n<p>Geh&ouml;rt zu EXP0150519022109020240131</p>', NULL, NULL, '2024-02-07 14:11:50.066477', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `start_adresse`
--

CREATE TABLE `start_adresse` (
  `id` bigint NOT NULL,
  `strasse` varchar(255) NOT NULL,
  `plz` varchar(10) NOT NULL,
  `stadt` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Daten für Tabelle `start_adresse`
--

INSERT INTO `start_adresse` (`id`, `strasse`, `plz`, `stadt`) VALUES
(1, 'An der Trift 13 - 15', '76149', 'Karlsruhe'),
(2, 'Thomas-Müntzner-Straße 5b', '39288', 'Burg'),
(3, 'Pascalstraße 10s', '53123', 'Bonn'),
(4, 'Hohe Düne 30', '18119', 'Rostock'),
(5, 'Nürnberger Str. 184', '70374', 'Stuttgart'),
(6, 'Landsberger Str. 133', '04157', 'Leipzig'),
(7, 'Kugelfangtrift 1', '30179', 'Hannover'),
(8, 'Berliner Str. 100', '34560', 'Fritzlar'),
(9, 'Maxhofstraße 1', '82343', 'Pöcking'),
(10, 'Marburger Str. 75', '35066', 'Frankenberg/Eder'),
(11, 'Zeppelinstr. 18', '99096', 'Erfurt'),
(12, 'Gnoiener Chaussee', '18334', 'Bad Sülze'),
(13, 'Peter-Strasser-Platz 1', '27639', 'Wurster Nordseeküste'),
(14, 'Fliegerhorst 1', '04916', 'Schönewalde OT Brandis'),
(15, 'Kurt-Schumacher-Damm 41', '13405', 'Berlin'),
(16, 'Philipp-Reis-Str. 2', '54568', 'Gerolstein');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `trainer_trainer`
--

CREATE TABLE `trainer_trainer` (
  `id` bigint NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Vorname` varchar(100) DEFAULT NULL,
  `Outlook` tinyint(1) NOT NULL,
  `SharePoint` tinyint(1) NOT NULL,
  `SMS` tinyint(1) NOT NULL,
  `Mobil` varchar(17) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indizes für die Tabelle `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indizes für die Tabelle `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indizes für die Tabelle `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indizes für die Tabelle `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indizes für die Tabelle `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indizes für die Tabelle `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indizes für die Tabelle `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indizes für die Tabelle `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indizes für die Tabelle `kunden_ansprechpartner`
--
ALTER TABLE `kunden_ansprechpartner`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kunden_ansprechpartner_kunde_id_e2fe9f22_fk_kunden_kunde_id` (`kunde_id`);

--
-- Indizes für die Tabelle `kunden_kunde`
--
ALTER TABLE `kunden_kunde`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `kunden_kunde_adresse_id_68ab835a_uniq` (`adresse_id`);

--
-- Indizes für die Tabelle `kurse_kurs`
--
ALTER TABLE `kurse_kurs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `va_nummer` (`va_nummer`),
  ADD KEY `kurse_kurs_kunde_id_9e5d7da8_fk_kunden_kunde_id` (`kunde_id`),
  ADD KEY `kurse_kurs_trainer_id_a3c9239c_fk_trainer_trainer_id` (`trainer_id`);

--
-- Indizes für die Tabelle `pit_abholung`
--
ALTER TABLE `pit_abholung`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `VA_Nummer` (`VA_Nummer`),
  ADD KEY `pit_abholung_Kunde_id_b52ac68a_fk_kunden_kunde_id` (`Kunde_id`),
  ADD KEY `pit_abholung_Schiene_id_cafb23f6_fk_pit_schiene_id` (`Schiene_id`),
  ADD KEY `pit_abholung_Server_id_76f8277d_fk_pit_server_id` (`Server_id`);

--
-- Indizes für die Tabelle `pit_festplattenimagenotebook`
--
ALTER TABLE `pit_festplattenimagenotebook`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indizes für die Tabelle `pit_festplattenimageserver`
--
ALTER TABLE `pit_festplattenimageserver`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indizes für die Tabelle `pit_rueckholung`
--
ALTER TABLE `pit_rueckholung`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pit_rueckholung_Kunde_id_6fb737b0_fk_kunden_kunde_id` (`Kunde_id`),
  ADD KEY `pit_rueckholung_VA_Nummer_id_13638458_fk_kurse_kurs_id` (`VA_Nummer_id`),
  ADD KEY `pit_rueckholung_Schiene_id_772d10be_fk_pit_schiene_id` (`Schiene_id`),
  ADD KEY `pit_rueckholung_Server_id_d8a28ff5_fk_pit_server_id` (`Server_id`);

--
-- Indizes für die Tabelle `pit_schiene`
--
ALTER TABLE `pit_schiene`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `pit_schiene_image_id_85a08b1a_fk_pit_festplattenimagenotebook_id` (`image_id`);

--
-- Indizes für die Tabelle `pit_server`
--
ALTER TABLE `pit_server`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `pit_server_image_id_fbb61e92_fk_pit_festplattenimageserver_id` (`image_id`);

--
-- Indizes für die Tabelle `pit_versand`
--
ALTER TABLE `pit_versand`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pit_versand_Kunde_id_ce7ca2cb_fk_kunden_kunde_id` (`Kunde_id`),
  ADD KEY `pit_versand_Schiene_id_2d84bc72_fk_pit_schiene_id` (`Schiene_id`),
  ADD KEY `pit_versand_Server_id_77f2ccc8_fk_pit_server_id` (`Server_id`),
  ADD KEY `pit_versand_VA_Nummer_id_79388f03_fk_kurse_kurs_id` (`VA_Nummer_id`);

--
-- Indizes für die Tabelle `postits_postit`
--
ALTER TABLE `postits_postit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `postits_postit_user_id_70bad05d_fk_auth_user_id` (`user_id`);

--
-- Indizes für die Tabelle `start_adresse`
--
ALTER TABLE `start_adresse`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `trainer_trainer`
--
ALTER TABLE `trainer_trainer`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT für Tabelle `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT für Tabelle `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT für Tabelle `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT für Tabelle `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT für Tabelle `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT für Tabelle `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT für Tabelle `kunden_ansprechpartner`
--
ALTER TABLE `kunden_ansprechpartner`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `kunden_kunde`
--
ALTER TABLE `kunden_kunde`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT für Tabelle `kurse_kurs`
--
ALTER TABLE `kurse_kurs`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT für Tabelle `pit_abholung`
--
ALTER TABLE `pit_abholung`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `pit_festplattenimagenotebook`
--
ALTER TABLE `pit_festplattenimagenotebook`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT für Tabelle `pit_festplattenimageserver`
--
ALTER TABLE `pit_festplattenimageserver`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT für Tabelle `pit_rueckholung`
--
ALTER TABLE `pit_rueckholung`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT für Tabelle `pit_schiene`
--
ALTER TABLE `pit_schiene`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT für Tabelle `pit_server`
--
ALTER TABLE `pit_server`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT für Tabelle `pit_versand`
--
ALTER TABLE `pit_versand`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT für Tabelle `postits_postit`
--
ALTER TABLE `postits_postit`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT für Tabelle `start_adresse`
--
ALTER TABLE `start_adresse`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT für Tabelle `trainer_trainer`
--
ALTER TABLE `trainer_trainer`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints der Tabelle `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints der Tabelle `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints der Tabelle `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints der Tabelle `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints der Tabelle `kunden_ansprechpartner`
--
ALTER TABLE `kunden_ansprechpartner`
  ADD CONSTRAINT `kunden_ansprechpartner_kunde_id_e2fe9f22_fk_kunden_kunde_id` FOREIGN KEY (`kunde_id`) REFERENCES `kunden_kunde` (`id`);

--
-- Constraints der Tabelle `kurse_kurs`
--
ALTER TABLE `kurse_kurs`
  ADD CONSTRAINT `kurse_kurs_kunde_id_9e5d7da8_fk_kunden_kunde_id` FOREIGN KEY (`kunde_id`) REFERENCES `kunden_kunde` (`id`),
  ADD CONSTRAINT `kurse_kurs_trainer_id_a3c9239c_fk_trainer_trainer_id` FOREIGN KEY (`trainer_id`) REFERENCES `trainer_trainer` (`id`);

--
-- Constraints der Tabelle `pit_abholung`
--
ALTER TABLE `pit_abholung`
  ADD CONSTRAINT `pit_abholung_Kunde_id_b52ac68a_fk_kunden_kunde_id` FOREIGN KEY (`Kunde_id`) REFERENCES `kunden_kunde` (`id`),
  ADD CONSTRAINT `pit_abholung_Schiene_id_cafb23f6_fk_pit_schiene_id` FOREIGN KEY (`Schiene_id`) REFERENCES `pit_schiene` (`id`),
  ADD CONSTRAINT `pit_abholung_Server_id_76f8277d_fk_pit_server_id` FOREIGN KEY (`Server_id`) REFERENCES `pit_server` (`id`);

--
-- Constraints der Tabelle `pit_rueckholung`
--
ALTER TABLE `pit_rueckholung`
  ADD CONSTRAINT `pit_rueckholung_Kunde_id_6fb737b0_fk_kunden_kunde_id` FOREIGN KEY (`Kunde_id`) REFERENCES `kunden_kunde` (`id`),
  ADD CONSTRAINT `pit_rueckholung_Schiene_id_772d10be_fk_pit_schiene_id` FOREIGN KEY (`Schiene_id`) REFERENCES `pit_schiene` (`id`),
  ADD CONSTRAINT `pit_rueckholung_Server_id_d8a28ff5_fk_pit_server_id` FOREIGN KEY (`Server_id`) REFERENCES `pit_server` (`id`),
  ADD CONSTRAINT `pit_rueckholung_VA_Nummer_id_13638458_fk_kurse_kurs_id` FOREIGN KEY (`VA_Nummer_id`) REFERENCES `kurse_kurs` (`id`);

--
-- Constraints der Tabelle `pit_schiene`
--
ALTER TABLE `pit_schiene`
  ADD CONSTRAINT `pit_schiene_image_id_85a08b1a_fk_pit_festplattenimagenotebook_id` FOREIGN KEY (`image_id`) REFERENCES `pit_festplattenimagenotebook` (`id`);

--
-- Constraints der Tabelle `pit_server`
--
ALTER TABLE `pit_server`
  ADD CONSTRAINT `pit_server_image_id_fbb61e92_fk_pit_festplattenimageserver_id` FOREIGN KEY (`image_id`) REFERENCES `pit_festplattenimageserver` (`id`);

--
-- Constraints der Tabelle `pit_versand`
--
ALTER TABLE `pit_versand`
  ADD CONSTRAINT `pit_versand_Kunde_id_ce7ca2cb_fk_kunden_kunde_id` FOREIGN KEY (`Kunde_id`) REFERENCES `kunden_kunde` (`id`),
  ADD CONSTRAINT `pit_versand_Schiene_id_2d84bc72_fk_pit_schiene_id` FOREIGN KEY (`Schiene_id`) REFERENCES `pit_schiene` (`id`),
  ADD CONSTRAINT `pit_versand_Server_id_77f2ccc8_fk_pit_server_id` FOREIGN KEY (`Server_id`) REFERENCES `pit_server` (`id`),
  ADD CONSTRAINT `pit_versand_VA_Nummer_id_79388f03_fk_kurse_kurs_id` FOREIGN KEY (`VA_Nummer_id`) REFERENCES `kurse_kurs` (`id`);

--
-- Constraints der Tabelle `postits_postit`
--
ALTER TABLE `postits_postit`
  ADD CONSTRAINT `postits_postit_user_id_70bad05d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
