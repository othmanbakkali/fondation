-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 07 août 2026 à 04:31
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `django_fondation`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `auth_permission`
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
(25, 'Can add contact message', 7, 'add_contactmessage'),
(26, 'Can change contact message', 7, 'change_contactmessage'),
(27, 'Can delete contact message', 7, 'delete_contactmessage'),
(28, 'Can view contact message', 7, 'view_contactmessage'),
(29, 'Can add content item', 8, 'add_contentitem'),
(30, 'Can change content item', 8, 'change_contentitem'),
(31, 'Can delete content item', 8, 'delete_contentitem'),
(32, 'Can view content item', 8, 'view_contentitem'),
(33, 'Can add page content', 9, 'add_pagecontent'),
(34, 'Can change page content', 9, 'change_pagecontent'),
(35, 'Can delete page content', 9, 'delete_pagecontent'),
(36, 'Can view page content', 9, 'view_pagecontent'),
(37, 'Can add partner', 10, 'add_partner'),
(38, 'Can change partner', 10, 'change_partner'),
(39, 'Can delete partner', 10, 'delete_partner'),
(40, 'Can view partner', 10, 'view_partner'),
(41, 'Can add site setting', 11, 'add_sitesetting'),
(42, 'Can change site setting', 11, 'change_sitesetting'),
(43, 'Can delete site setting', 11, 'delete_sitesetting'),
(44, 'Can view site setting', 11, 'view_sitesetting'),
(45, 'Can add volunteer application', 12, 'add_volunteerapplication'),
(46, 'Can change volunteer application', 12, 'change_volunteerapplication'),
(47, 'Can delete volunteer application', 12, 'delete_volunteerapplication'),
(48, 'Can view volunteer application', 12, 'view_volunteerapplication'),
(49, 'Can add formation registration', 13, 'add_formationregistration'),
(50, 'Can change formation registration', 13, 'change_formationregistration'),
(51, 'Can delete formation registration', 13, 'delete_formationregistration'),
(52, 'Can view formation registration', 13, 'view_formationregistration'),
(53, 'Can add Inscription activité', 14, 'add_activityregistration'),
(54, 'Can change Inscription activité', 14, 'change_activityregistration'),
(55, 'Can delete Inscription activité', 14, 'delete_activityregistration'),
(56, 'Can view Inscription activité', 14, 'view_activityregistration'),
(57, 'Can add user profile', 15, 'add_userprofile'),
(58, 'Can change user profile', 15, 'change_userprofile'),
(59, 'Can delete user profile', 15, 'delete_userprofile'),
(60, 'Can view user profile', 15, 'view_userprofile');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(3, 'pbkdf2_sha256$600000$NNfFKvzuSV8htYYgqnkPDv$GC4tsDD4+r19ANdH/gXQ2h0LOYz7c10NY/TW5F1x9Oo=', '2026-08-07 02:12:58.801668', 1, 'hp', '', '', 'abdelmajid@gmail.com', 1, 1, '2026-08-04 12:38:51.637783');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_activityregistration`
--

CREATE TABLE `core_activityregistration` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(160) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(40) NOT NULL,
  `city` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `activity_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_contactmessage`
--

CREATE TABLE `core_contactmessage` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(160) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(40) NOT NULL,
  `subject` varchar(180) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `attachment_url` varchar(255) NOT NULL,
  `city` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_contentitem`
--

CREATE TABLE `core_contentitem` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `module` varchar(30) NOT NULL,
  `title` varchar(220) NOT NULL,
  `slug` varchar(240) NOT NULL,
  `category` varchar(80) NOT NULL,
  `summary` longtext NOT NULL,
  `body` longtext NOT NULL,
  `image_url` varchar(200) NOT NULL,
  `gallery` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`gallery`)),
  `video_url` varchar(200) NOT NULL,
  `facebook_url` varchar(200) NOT NULL,
  `instagram_url` varchar(200) NOT NULL,
  `youtube_url` varchar(200) NOT NULL,
  `author` varchar(120) NOT NULL,
  `date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `start_time` time(6) DEFAULT NULL,
  `end_time` time(6) DEFAULT NULL,
  `location` varchar(180) NOT NULL,
  `instructor_name` varchar(120) NOT NULL,
  `total_seats` int(10) UNSIGNED NOT NULL CHECK (`total_seats` >= 0),
  `registered_seats` int(10) UNSIGNED NOT NULL CHECK (`registered_seats` >= 0),
  `participants` int(10) UNSIGNED NOT NULL CHECK (`participants` >= 0),
  `reports_count` int(10) UNSIGNED NOT NULL CHECK (`reports_count` >= 0),
  `reading_time` int(10) UNSIGNED NOT NULL CHECK (`reading_time` >= 0),
  `status` varchar(20) NOT NULL,
  `order` int(10) UNSIGNED NOT NULL CHECK (`order` >= 0),
  `featured` tinyint(1) NOT NULL,
  `meta_title` varchar(180) NOT NULL,
  `meta_description` longtext NOT NULL,
  `keywords` varchar(255) NOT NULL,
  `canonical_url` varchar(200) NOT NULL,
  `og_image_url` varchar(200) NOT NULL,
  `title_ar` varchar(220) DEFAULT NULL,
  `title_en` varchar(220) DEFAULT NULL,
  `category_ar` varchar(80) DEFAULT NULL,
  `category_en` varchar(80) DEFAULT NULL,
  `summary_ar` longtext DEFAULT NULL,
  `summary_en` longtext DEFAULT NULL,
  `body_ar` longtext DEFAULT NULL,
  `body_en` longtext DEFAULT NULL,
  `meta_title_ar` varchar(180) DEFAULT NULL,
  `meta_title_en` varchar(180) DEFAULT NULL,
  `meta_description_ar` longtext DEFAULT NULL,
  `meta_description_en` longtext DEFAULT NULL,
  `keywords_ar` varchar(255) DEFAULT NULL,
  `keywords_en` varchar(255) DEFAULT NULL,
  `body_fr` longtext DEFAULT NULL,
  `category_fr` varchar(80) DEFAULT NULL,
  `instructor_name_ar` varchar(120) DEFAULT NULL,
  `instructor_name_en` varchar(120) DEFAULT NULL,
  `instructor_name_fr` varchar(120) DEFAULT NULL,
  `keywords_fr` varchar(255) DEFAULT NULL,
  `location_ar` varchar(180) DEFAULT NULL,
  `location_en` varchar(180) DEFAULT NULL,
  `location_fr` varchar(180) DEFAULT NULL,
  `meta_description_fr` longtext DEFAULT NULL,
  `meta_title_fr` varchar(180) DEFAULT NULL,
  `summary_fr` longtext DEFAULT NULL,
  `title_fr` varchar(220) DEFAULT NULL,
  `linkedin_url` varchar(200) NOT NULL,
  `tiktok_url` varchar(200) NOT NULL,
  `twitter_url` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_contentitem`
--

INSERT INTO `core_contentitem` (`id`, `created_at`, `updated_at`, `module`, `title`, `slug`, `category`, `summary`, `body`, `image_url`, `gallery`, `video_url`, `facebook_url`, `instagram_url`, `youtube_url`, `author`, `date`, `start_date`, `end_date`, `start_time`, `end_time`, `location`, `instructor_name`, `total_seats`, `registered_seats`, `participants`, `reports_count`, `reading_time`, `status`, `order`, `featured`, `meta_title`, `meta_description`, `keywords`, `canonical_url`, `og_image_url`, `title_ar`, `title_en`, `category_ar`, `category_en`, `summary_ar`, `summary_en`, `body_ar`, `body_en`, `meta_title_ar`, `meta_title_en`, `meta_description_ar`, `meta_description_en`, `keywords_ar`, `keywords_en`, `body_fr`, `category_fr`, `instructor_name_ar`, `instructor_name_en`, `instructor_name_fr`, `keywords_fr`, `location_ar`, `location_en`, `location_fr`, `meta_description_fr`, `meta_title_fr`, `summary_fr`, `title_fr`, `linkedin_url`, `tiktok_url`, `twitter_url`) VALUES
(9, '2026-08-02 23:47:29.469080', '2026-08-06 02:53:51.637905', 'program', 'Éducation et réussite', 'education-et-reussite', 'Éducation', 'Soutien scolaire, bourses et orientation pour les jeunes.', 'Soutien scolaire, bourses et orientation pour les jeunes.', 'https://placehold.co/700x450/062B4F/FFFFFF?text=Fondation', '[]', '', '', '', '', '', NULL, NULL, NULL, NULL, NULL, '', '', 0, 0, 0, 0, 3, 'publie', 1, 0, '', '', '', '', '', 'التعليم والنجاح', 'Education and success', 'تعليم', 'Education', 'الدعم الأكاديمي والمنح الدراسية والتوجيه للشباب.', 'Academic support, scholarships and guidance for young people.', 'الدعم الأكاديمي والمنح الدراسية والتوجيه للشباب.', 'Academic support, scholarships and guidance for young people.', '', '', '', '', '', '', 'Soutien scolaire, bourses et orientation pour les jeunes.', 'Éducation', NULL, NULL, '', '', NULL, NULL, '', '', '', 'Soutien scolaire, bourses et orientation pour les jeunes.', 'Éducation et réussite', '', '', ''),
(10, '2026-08-02 23:47:29.476058', '2026-08-06 02:53:58.205747', 'program', 'Culture et patrimoine', 'culture-et-patrimoine', 'Culture', 'Valorisation du patrimoine tangérois et soutien aux artistes.', 'Valorisation du patrimoine tangérois et soutien aux artistes.', 'https://placehold.co/700x450/062B4F/FFFFFF?text=Fondation', '[]', '', '', '', '', 'Fondation Tanger Métropole', NULL, NULL, NULL, NULL, NULL, 'Tanger', '', 0, 0, 0, 0, 3, 'publie', 2, 0, '', '', '', '', '', 'الثقافة والتراث', 'Culture and heritage', 'ثقافة', 'Culture', 'الترويج لتراث طنجة ودعم الفنانين.', 'Promotion of Tangiers heritage and support for artists.', 'الترويج لتراث طنجة ودعم الفنانين.', 'Promotion of Tangiers heritage and support for artists.', '', '', '', '', '', '', 'Valorisation du patrimoine tangérois et soutien aux artistes.', 'Culture', NULL, NULL, '', '', 'طنجة', 'Tangier', 'Tanger', '', '', 'Valorisation du patrimoine tangérois et soutien aux artistes.', 'Culture et patrimoine', '', '', ''),
(11, '2026-08-02 23:47:29.484636', '2026-08-06 02:54:13.255359', 'program', 'Solidarité sociale', 'solidarite-sociale', 'Social', 'Actions de proximité pour les familles et quartiers prioritaires.', 'Actions de proximité pour les familles et quartiers prioritaires.', 'https://placehold.co/700x450/062B4F/FFFFFF?text=Fondation', '[]', '', '', '', '', 'Fondation Tanger Métropole', NULL, NULL, NULL, NULL, NULL, 'Tanger', '', 0, 0, 0, 0, 3, 'publie', 3, 0, '', '', '', '', '', 'التضامن الاجتماعي', 'Social solidarity', 'اجتماعي', 'Social', 'الإجراءات المحلية للعائلات والأحياء ذات الأولوية.', 'Local actions for priority families and neighborhoods.', 'الإجراءات المحلية للعائلات والأحياء ذات الأولوية.', 'Local actions for priority families and neighborhoods.', '', '', '', '', '', '', 'Actions de proximité pour les familles et quartiers prioritaires.', 'Social', NULL, NULL, '', '', 'طنجة', 'Tangier', 'Tanger', '', '', 'Actions de proximité pour les familles et quartiers prioritaires.', 'Solidarité sociale', '', '', ''),
(12, '2026-08-02 23:47:29.491613', '2026-08-06 02:54:20.241782', 'program', 'Sport pour tous', 'sport-pour-tous', 'Sport', 'Événements et encadrement sportif pour les jeunes.', 'Événements et encadrement sportif pour les jeunes.', 'https://placehold.co/700x450/062B4F/FFFFFF?text=Fondation', '[]', '', '', '', '', 'Fondation Tanger Métropole', NULL, NULL, NULL, NULL, NULL, 'Tanger', '', 0, 0, 0, 0, 3, 'publie', 4, 0, '', '', '', '', '', 'الرياضة للجميع', 'Sport for all', 'رياضة', 'Sport', 'الفعاليات والدعم الرياضي للشباب.', 'Events and sports support for young people.', 'الفعاليات والدعم الرياضي للشباب.', 'Events and sports support for young people.', '', '', '', '', '', '', 'Événements et encadrement sportif pour les jeunes.', 'Sport', NULL, NULL, '', '', 'طنجة', 'Tangier', 'Tanger', '', '', 'Événements et encadrement sportif pour les jeunes.', 'Sport pour tous', '', '', '');

-- --------------------------------------------------------

--
-- Structure de la table `core_formationregistration`
--

CREATE TABLE `core_formationregistration` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(160) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(40) NOT NULL,
  `city` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `formation_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_pagecontent`
--

CREATE TABLE `core_pagecontent` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `slug` varchar(80) NOT NULL,
  `title` varchar(180) NOT NULL,
  `subtitle` longtext NOT NULL,
  `hero_image_url` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `sections` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`sections`)),
  `meta_title` varchar(180) NOT NULL,
  `meta_description` longtext NOT NULL,
  `keywords` varchar(255) NOT NULL,
  `canonical_url` varchar(200) NOT NULL,
  `og_image_url` varchar(200) NOT NULL,
  `status` varchar(20) NOT NULL,
  `title_ar` varchar(180) DEFAULT NULL,
  `title_en` varchar(180) DEFAULT NULL,
  `subtitle_ar` longtext DEFAULT NULL,
  `subtitle_en` longtext DEFAULT NULL,
  `content_ar` longtext DEFAULT NULL,
  `content_en` longtext DEFAULT NULL,
  `meta_title_ar` varchar(180) DEFAULT NULL,
  `meta_title_en` varchar(180) DEFAULT NULL,
  `meta_description_ar` longtext DEFAULT NULL,
  `meta_description_en` longtext DEFAULT NULL,
  `keywords_ar` varchar(255) DEFAULT NULL,
  `keywords_en` varchar(255) DEFAULT NULL,
  `content_fr` longtext DEFAULT NULL,
  `keywords_fr` varchar(255) DEFAULT NULL,
  `meta_description_fr` longtext DEFAULT NULL,
  `meta_title_fr` varchar(180) DEFAULT NULL,
  `subtitle_fr` longtext DEFAULT NULL,
  `title_fr` varchar(180) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_pagecontent`
--

INSERT INTO `core_pagecontent` (`id`, `created_at`, `updated_at`, `slug`, `title`, `subtitle`, `hero_image_url`, `content`, `sections`, `meta_title`, `meta_description`, `keywords`, `canonical_url`, `og_image_url`, `status`, `title_ar`, `title_en`, `subtitle_ar`, `subtitle_en`, `content_ar`, `content_en`, `meta_title_ar`, `meta_title_en`, `meta_description_ar`, `meta_description_en`, `keywords_ar`, `keywords_en`, `content_fr`, `keywords_fr`, `meta_description_fr`, `meta_title_fr`, `subtitle_fr`, `title_fr`) VALUES
(1, '2026-08-02 23:47:29.306927', '2026-08-07 02:30:10.078866', 'accueil', 'Fondation Tanger Métropole', '', '', 'La Fondation Tanger Métropole s\'engage à promouvoir l\'inclusion sociale et le développement local à travers le sport, la culture et l\'éducation.', '{\"texts\": {\"hero_btn1\": \"D\\u00e9couvrir la Fondation\", \"hero_btn1_ar\": \"\\u0627\\u0643\\u062a\\u0634\\u0641 \\u0627\\u0644\\u0645\\u0624\\u0633\\u0633\\u0629\", \"hero_btn1_en\": \"Discover the Foundation\", \"hero_btn2\": \"Devenir B\\u00e9n\\u00e9vole\", \"hero_btn2_ar\": \"\\u0643\\u0646 \\u0645\\u062a\\u0637\\u0648\\u0639\\u064b\\u0627\", \"hero_btn2_en\": \"Become a Volunteer\", \"hero_scroll\": \"D\\u00e9filer\", \"hero_scroll_ar\": \"\\u0642\\u0645 \\u0628\\u0627\\u0644\\u062a\\u0645\\u0631\\u064a\\u0631\", \"hero_scroll_en\": \"Scroll\", \"annonces_title\": \"Actualit\\u00e9s & Annonces\", \"annonces_title_ar\": \"\\u0627\\u0644\\u0623\\u062e\\u0628\\u0627\\u0631 \\u0648\\u0627\\u0644\\u0625\\u0639\\u0644\\u0627\\u0646\\u0627\\u062a\", \"annonces_title_en\": \"News & Announcements\", \"stats_beneficiaries_label\": \"B\\u00e9n\\u00e9ficiaires\", \"stats_beneficiaries_label_ar\": \"\\u0627\\u0644\\u0645\\u0633\\u062a\\u0641\\u064a\\u062f\\u0648\\u0646\", \"stats_beneficiaries_label_en\": \"Beneficiaries\", \"stats_beneficiaries_sub\": \"directs et indirects\", \"stats_beneficiaries_sub_ar\": \"\\u0627\\u0644\\u0645\\u0628\\u0627\\u0634\\u0631\\u0629 \\u0648\\u063a\\u064a\\u0631 \\u0627\\u0644\\u0645\\u0628\\u0627\\u0634\\u0631\\u0629\", \"stats_beneficiaries_sub_en\": \"direct and indirect\", \"stats_programs_label\": \"Programmes\", \"stats_programs_label_ar\": \"\\u0627\\u0644\\u0628\\u0631\\u0627\\u0645\\u062c\", \"stats_programs_label_en\": \"Programs\", \"stats_programs_sub\": \"publi\\u00e9s\", \"stats_programs_sub_ar\": \"\\u0646\\u0634\\u0631\\u062a\", \"stats_programs_sub_en\": \"published\", \"stats_formations_label\": \"Formations\", \"stats_formations_label_ar\": \"\\u062a\\u0645\\u0631\\u064a\\u0646\", \"stats_formations_label_en\": \"Training\", \"stats_formations_sub\": \"publi\\u00e9es\", \"stats_formations_sub_ar\": \"\\u0646\\u0634\\u0631\\u062a\", \"stats_formations_sub_en\": \"published\", \"stats_partners_label\": \"Partenaires\", \"stats_partners_label_ar\": \"\\u0627\\u0644\\u0634\\u0631\\u0643\\u0627\\u0621\", \"stats_partners_label_en\": \"Partners\", \"stats_partners_sub\": \"actifs\", \"stats_partners_sub_ar\": \"\\u0623\\u0635\\u0648\\u0644\", \"stats_partners_sub_en\": \"assets\", \"stats_volunteers_label\": \"B\\u00e9n\\u00e9voles\", \"stats_volunteers_label_ar\": \"\\u0627\\u0644\\u0645\\u062a\\u0637\\u0648\\u0639\\u064a\\u0646\", \"stats_volunteers_label_en\": \"Volunteers\", \"stats_volunteers_sub\": \"candidatures\", \"stats_volunteers_sub_ar\": \"\\u0627\\u0644\\u062a\\u0637\\u0628\\u064a\\u0642\\u0627\\u062a\", \"stats_volunteers_sub_en\": \"applications\", \"stats_years_label\": \"Ann\\u00e9es\", \"stats_years_label_ar\": \"\\u0633\\u0646\\u064a\\u0646\", \"stats_years_label_en\": \"Years\", \"stats_years_sub\": \"d\'exp\\u00e9rience\", \"stats_years_sub_ar\": \"\\u0645\\u0646 \\u0627\\u0644\\u062e\\u0628\\u0631\\u0629\", \"stats_years_sub_en\": \"of experience\", \"domains_title\": \"Nos Domaines d\'Intervention\", \"domains_title_ar\": \"\\u0645\\u062c\\u0627\\u0644\\u0627\\u062a \\u0627\\u0644\\u062a\\u062f\\u062e\\u0644 \\u0644\\u062f\\u064a\\u0646\\u0627\", \"domains_title_en\": \"Our Areas of Intervention\", \"domains_btn\": \"D\\u00e9couvrir\", \"domains_btn_ar\": \"\\u064a\\u0643\\u062a\\u0634\\u0641\", \"domains_btn_en\": \"Discover\", \"activities_title\": \"Activit\\u00e9s de la Fondation\", \"activities_title_ar\": \"\\u0623\\u0646\\u0634\\u0637\\u0629 \\u0627\\u0644\\u0645\\u0624\\u0633\\u0633\\u0629\", \"activities_title_en\": \"Foundation activities\", \"activities_btn\": \"Voir toutes les activit\\u00e9s\", \"activities_btn_ar\": \"\\u0634\\u0627\\u0647\\u062f \\u062c\\u0645\\u064a\\u0639 \\u0627\\u0644\\u0623\\u0646\\u0634\\u0637\\u0629\", \"activities_btn_en\": \"See all activities\", \"partners_title\": \"Nos Partenaires\", \"partners_title_ar\": \"\\u0634\\u0631\\u0643\\u0627\\u0624\\u0646\\u0627\", \"partners_title_en\": \"Our Partners\", \"benevolat_title\": \"Devenir B\\u00e9n\\u00e9vole\", \"benevolat_title_ar\": \"\\u0643\\u0646 \\u0645\\u062a\\u0637\\u0648\\u0639\\u064b\\u0627\", \"benevolat_title_en\": \"Become a Volunteer\", \"benevolat_text\": \"Rejoignez une communaut\\u00e9 dynamique qui transforme Tanger. Chaque geste compte pour construire un avenir meilleur.\", \"benevolat_text_ar\": \"\\u0627\\u0646\\u0636\\u0645 \\u0625\\u0644\\u0649 \\u0645\\u062c\\u062a\\u0645\\u0639 \\u062f\\u064a\\u0646\\u0627\\u0645\\u064a\\u0643\\u064a \\u064a\\u0639\\u0645\\u0644 \\u0639\\u0644\\u0649 \\u062a\\u062d\\u0648\\u064a\\u0644 \\u0637\\u0646\\u062c\\u0629. \\u0643\\u0644 \\u0628\\u0627\\u062f\\u0631\\u0629 \\u0645\\u0647\\u0645\\u0629 \\u0644\\u0628\\u0646\\u0627\\u0621 \\u0645\\u0633\\u062a\\u0642\\u0628\\u0644 \\u0623\\u0641\\u0636\\u0644.\", \"benevolat_text_en\": \"Join a dynamic community that is transforming Tangier. Every gesture counts to build a better future.\", \"benevolat_point1\": \"Missions flexibles adapt\\u00e9es \\u00e0 votre disponibilit\\u00e9\", \"benevolat_point1_ar\": \"\\u0645\\u0647\\u0645\\u0627\\u062a \\u0645\\u0631\\u0646\\u0629 \\u062a\\u062a\\u0643\\u064a\\u0641 \\u0645\\u0639 \\u0645\\u062f\\u0649 \\u062a\\u0648\\u0641\\u0631\\u0643\", \"benevolat_point1_en\": \"Flexible missions adapted to your availability\", \"benevolat_point2\": \"Formations offertes pour d\\u00e9velopper vos comp\\u00e9tences\", \"benevolat_point2_ar\": \"\\u0627\\u0644\\u062a\\u062f\\u0631\\u064a\\u0628 \\u0627\\u0644\\u0645\\u0642\\u062f\\u0645 \\u0644\\u062a\\u0637\\u0648\\u064a\\u0631 \\u0645\\u0647\\u0627\\u0631\\u0627\\u062a\\u0643\", \"benevolat_point2_en\": \"Training offered to develop your skills\", \"benevolat_point3\": \"Impact mesurable sur la communaut\\u00e9\", \"benevolat_point3_ar\": \"\\u062a\\u0623\\u062b\\u064a\\u0631 \\u064a\\u0645\\u0643\\u0646 \\u0642\\u064a\\u0627\\u0633\\u0647 \\u0639\\u0644\\u0649 \\u0627\\u0644\\u0645\\u062c\\u062a\\u0645\\u0639\", \"benevolat_point3_en\": \"Measurable impact on the community\", \"benevolat_btn\": \"S\'inscrire maintenant\", \"benevolat_btn_ar\": \"\\u0633\\u062c\\u0644 \\u0627\\u0644\\u0622\\u0646\", \"benevolat_btn_en\": \"Register now\", \"contact_title\": \"Contactez-nous\", \"contact_title_ar\": \"\\u0627\\u062a\\u0635\\u0644 \\u0628\\u0646\\u0627\", \"contact_title_en\": \"Contact us\", \"contact_name_ph\": \"Nom complet\", \"contact_name_ph_ar\": \"\\u0627\\u0644\\u0627\\u0633\\u0645 \\u0627\\u0644\\u0643\\u0627\\u0645\\u0644\", \"contact_name_ph_en\": \"Full name\", \"contact_email_ph\": \"Email\", \"contact_email_ph_ar\": \"\\u0628\\u0631\\u064a\\u062f \\u0625\\u0644\\u0643\\u062a\\u0631\\u0648\\u0646\\u064a\", \"contact_email_ph_en\": \"E-mail\", \"contact_msg_ph\": \"Votre message\", \"contact_msg_ph_ar\": \"\\u0631\\u0633\\u0627\\u0644\\u062a\\u0643\", \"contact_msg_ph_en\": \"Your message\", \"contact_btn\": \"Envoyer\", \"contact_btn_ar\": \"\\u064a\\u0631\\u0633\\u0644\", \"contact_btn_en\": \"Send\"}}', 'Accueil FTM', 'Description SEO', 'fondation,tanger', '', '', 'publie', 'مؤسسة طنجة الكبرى', 'Tanger Metropolis Foundation', '', '', 'تلتزم مؤسسة طنجة الكبرى بتعزيز الإدماج الاجتماعي والتنمية المحلية من خلال الرياضة والثقافة والتعليم.', 'The Tanger Metropole Foundation is committed to promoting social inclusion and local development through sports, culture, and education.', 'الصفحة الرئيسية اف تي ام', 'FTM Home', 'وصف كبار المسئولين الاقتصاديين', 'SEO description', 'مؤسسة طنجة', 'foundation, tangier', '', 'fondation,tanger', 'Description SEO', 'Accueil FTM', '', 'Fondation Tanger Métropole'),
(2, '2026-08-02 23:47:29.314016', '2026-08-06 03:11:17.006883', 'a-propos', 'À propos', 'Une fondation engagée pour l\'éducation, la culture, le social et le sport dans le Grand Tanger.', '/media/pages/WhatsApp%20Image%202026-07-27%20at%2021.29.09.jpeg', 'Une fondation engagée pour l\'éducation, la culture, le social et le sport dans le Grand Tanger.', '{\"texts\": {\"presentation_title\": \"\\u00c0 propos de la Fondation Tanger M\\u00e9tropole\", \"mission_label\": \"Notre raison d\'\\u00eatre\", \"mission_title\": \"Notre mission\", \"mission_button_text\": \"D\\u00e9couvrir nos programmes\", \"objectives_title\": \"Nos objectifs\", \"values_title\": \"Nos valeurs\", \"bureau_title\": \"Notre bureau dirigeant\", \"bureau_intro\": \"Une \\u00e9quipe engag\\u00e9e qui \\u0153uvre pour la r\\u00e9alisation des objectifs de la Fondation et le d\\u00e9veloppement de ses actions.\", \"members_title\": \"Liste des membres du bureau dirigeant\", \"members_intro\": \"Consultez la liste compl\\u00e8te des membres de notre bureau dirigeant avec leurs fonctions et statuts.\", \"members_search_placeholder\": \"Rechercher un membre par nom ou fonction...\", \"members_filter_all\": \"Toutes les fonctions\", \"members_export\": \"Exporter\", \"members_empty_title\": \"Aucun membre trouv\\u00e9\", \"members_empty_text\": \"Essayez de modifier vos crit\\u00e8res de recherche.\", \"zone_title\": \"Notre zone d\'intervention\", \"zone_name\": \"Grand Tanger\", \"zone_text\": \"La Fondation Tanger M\\u00e9tropole intervient principalement dans le Grand Tanger et ses environs, en d\\u00e9veloppant des projets sociaux, \\u00e9ducatifs, culturels, professionnels et citoyens.\", \"cta_title\": \"Construisons ensemble l\'avenir du Grand Tanger\", \"cta_text\": \"Rejoignez nos programmes, devenez b\\u00e9n\\u00e9vole ou contactez-nous pour proposer une initiative au service de la communaut\\u00e9.\", \"cta_primary_text\": \"Devenir b\\u00e9n\\u00e9vole\", \"cta_secondary_text\": \"Nous contacter\", \"presentation_title_ar\": \"\\u0639\\u0646 \\u0645\\u0624\\u0633\\u0633\\u0629 \\u0637\\u0646\\u062c\\u0629 \\u0645\\u062a\\u0631\\u0648\\u0628\\u0648\\u0644\", \"presentation_title_en\": \"About the Tanger M\\u00e9tropole Foundation\", \"mission_label_ar\": \"\\u0633\\u0628\\u0628 \\u0648\\u062c\\u0648\\u062f\\u0646\\u0627\", \"mission_label_en\": \"Our reason for being\", \"mission_title_ar\": \"\\u0645\\u0647\\u0645\\u062a\\u0646\\u0627\", \"mission_title_en\": \"Our mission\", \"mission_button_text_ar\": \"\\u0627\\u0643\\u062a\\u0634\\u0641 \\u0628\\u0631\\u0627\\u0645\\u062c\\u0646\\u0627\", \"mission_button_text_en\": \"Discover our programs\", \"objectives_title_ar\": \"\\u0623\\u0647\\u062f\\u0627\\u0641\\u0646\\u0627\", \"objectives_title_en\": \"Our objectives\", \"values_title_ar\": \"\\u0642\\u064a\\u0645\\u0646\\u0627\", \"values_title_en\": \"Our values\", \"bureau_title_ar\": \"\\u0645\\u0643\\u062a\\u0628 \\u0625\\u062f\\u0627\\u0631\\u062a\\u0646\\u0627\", \"bureau_title_en\": \"Our management office\", \"bureau_intro_ar\": \"\\u0641\\u0631\\u064a\\u0642 \\u0645\\u0644\\u062a\\u0632\\u0645 \\u064a\\u0639\\u0645\\u0644 \\u0639\\u0644\\u0649 \\u062a\\u062d\\u0642\\u064a\\u0642 \\u0623\\u0647\\u062f\\u0627\\u0641 \\u0627\\u0644\\u0645\\u0624\\u0633\\u0633\\u0629 \\u0648\\u062a\\u0637\\u0648\\u064a\\u0631 \\u0623\\u0639\\u0645\\u0627\\u0644\\u0647\\u0627.\", \"bureau_intro_en\": \"A committed team that works to achieve the Foundation\'s objectives and develop its actions.\", \"members_title_ar\": \"\\u0642\\u0627\\u0626\\u0645\\u0629 \\u0623\\u0639\\u0636\\u0627\\u0621 \\u0645\\u062c\\u0644\\u0633 \\u0627\\u0644\\u0625\\u062f\\u0627\\u0631\\u0629\", \"members_title_en\": \"List of members of the governing board\", \"members_intro_ar\": \"\\u0631\\u0627\\u062c\\u0639 \\u0627\\u0644\\u0642\\u0627\\u0626\\u0645\\u0629 \\u0627\\u0644\\u0643\\u0627\\u0645\\u0644\\u0629 \\u0644\\u0623\\u0639\\u0636\\u0627\\u0621 \\u0647\\u064a\\u0626\\u062a\\u0646\\u0627 \\u0627\\u0644\\u0625\\u062f\\u0627\\u0631\\u064a\\u0629 \\u0645\\u0639 \\u0648\\u0638\\u0627\\u0626\\u0641\\u0647\\u0645 \\u0648\\u062d\\u0627\\u0644\\u0627\\u062a\\u0647\\u0645.\", \"members_intro_en\": \"Consult the complete list of members of our governing body with their functions and statuses.\", \"members_search_placeholder_ar\": \"\\u0627\\u0644\\u0628\\u062d\\u062b \\u0639\\u0646 \\u0639\\u0636\\u0648 \\u0628\\u0627\\u0644\\u0627\\u0633\\u0645 \\u0623\\u0648 \\u0627\\u0644\\u0645\\u0646\\u0635\\u0628...\", \"members_search_placeholder_en\": \"Search for a member by name or position...\", \"members_filter_all_ar\": \"\\u062c\\u0645\\u064a\\u0639 \\u0627\\u0644\\u0648\\u0638\\u0627\\u0626\\u0641\", \"members_filter_all_en\": \"All functions\", \"members_export_ar\": \"\\u064a\\u0635\\u062f\\u0651\\u0631\", \"members_export_en\": \"Export\", \"members_empty_title_ar\": \"\\u0644\\u0645 \\u064a\\u062a\\u0645 \\u0627\\u0644\\u0639\\u062b\\u0648\\u0631 \\u0639\\u0644\\u0649 \\u0623\\u0639\\u0636\\u0627\\u0621\", \"members_empty_title_en\": \"No members found\", \"members_empty_text_ar\": \"\\u062d\\u0627\\u0648\\u0644 \\u062a\\u063a\\u064a\\u064a\\u0631 \\u0645\\u0639\\u0627\\u064a\\u064a\\u0631 \\u0627\\u0644\\u0628\\u062d\\u062b \\u0627\\u0644\\u062e\\u0627\\u0635\\u0629 \\u0628\\u0643.\", \"members_empty_text_en\": \"Try changing your search criteria.\", \"zone_title_ar\": \"\\u0645\\u062c\\u0627\\u0644 \\u062a\\u062f\\u062e\\u0644\\u0646\\u0627\", \"zone_title_en\": \"Our area of \\u200b\\u200bintervention\", \"zone_name_ar\": \"\\u0637\\u0646\\u062c\\u0629 \\u0627\\u0644\\u0643\\u0628\\u0631\\u0649\", \"zone_name_en\": \"Greater Tangier\", \"zone_text_ar\": \"\\u062a\\u0639\\u0645\\u0644 \\u0645\\u0624\\u0633\\u0633\\u0629 \\u0637\\u0646\\u062c\\u0629 \\u0645\\u062a\\u0631\\u0648\\u0628\\u0648\\u0644 \\u0623\\u0633\\u0627\\u0633\\u0627 \\u0641\\u064a \\u0645\\u062f\\u064a\\u0646\\u0629 \\u0637\\u0646\\u062c\\u0629 \\u0627\\u0644\\u0643\\u0628\\u0631\\u0649 \\u0648\\u0636\\u0648\\u0627\\u062d\\u064a\\u0647\\u0627\\u060c \\u0645\\u0646 \\u062e\\u0644\\u0627\\u0644 \\u062a\\u0637\\u0648\\u064a\\u0631 \\u0627\\u0644\\u0645\\u0634\\u0627\\u0631\\u064a\\u0639 \\u0627\\u0644\\u0627\\u062c\\u062a\\u0645\\u0627\\u0639\\u064a\\u0629 \\u0648\\u0627\\u0644\\u062a\\u0639\\u0644\\u064a\\u0645\\u064a\\u0629 \\u0648\\u0627\\u0644\\u062b\\u0642\\u0627\\u0641\\u064a\\u0629 \\u0648\\u0627\\u0644\\u0645\\u0647\\u0646\\u064a\\u0629 \\u0648\\u0627\\u0644\\u0645\\u062f\\u0646\\u064a\\u0629.\", \"zone_text_en\": \"The Tangier M\\u00e9tropole Foundation operates mainly in Greater Tangier and its surroundings, by developing social, educational, cultural, professional and civic projects.\", \"cta_title_ar\": \"\\u062f\\u0639\\u0648\\u0646\\u0627 \\u0646\\u0628\\u0646\\u064a \\u0645\\u0633\\u062a\\u0642\\u0628\\u0644 \\u0637\\u0646\\u062c\\u0629 \\u0627\\u0644\\u0643\\u0628\\u0631\\u0649 \\u0645\\u0639\\u0627\", \"cta_title_en\": \"Let\'s build the future of Greater Tangier together\", \"cta_text_ar\": \"\\u0627\\u0646\\u0636\\u0645 \\u0625\\u0644\\u0649 \\u0628\\u0631\\u0627\\u0645\\u062c\\u0646\\u0627 \\u0648\\u0643\\u0646 \\u0645\\u062a\\u0637\\u0648\\u0639\\u0627\\u064b \\u0623\\u0648 \\u062a\\u0648\\u0627\\u0635\\u0644 \\u0645\\u0639\\u0646\\u0627 \\u0644\\u0627\\u0642\\u062a\\u0631\\u0627\\u062d \\u0645\\u0628\\u0627\\u062f\\u0631\\u0629 \\u0644\\u062e\\u062f\\u0645\\u0629 \\u0627\\u0644\\u0645\\u062c\\u062a\\u0645\\u0639.\", \"cta_text_en\": \"Join our programs, become a volunteer or contact us to propose an initiative to serve the community.\", \"cta_primary_text_ar\": \"\\u0643\\u0646 \\u0645\\u062a\\u0637\\u0648\\u0639\\u0627\", \"cta_primary_text_en\": \"Become a volunteer\", \"cta_secondary_text_ar\": \"\\u0627\\u062a\\u0635\\u0644 \\u0628\\u0646\\u0627\", \"cta_secondary_text_en\": \"Contact us\"}, \"presentation_cards\": [{\"icon\": \"fa-calendar-alt\", \"title\": \"Date de cr\\u00e9ation\", \"text\": \"27 mars 2018\", \"title_ar\": \"\\u062a\\u0627\\u0631\\u064a\\u062e \\u0627\\u0644\\u0625\\u0646\\u0634\\u0627\\u0621\", \"title_en\": \"Creation date\", \"text_ar\": \"27 \\u0645\\u0627\\u0631\\u0633 2018\", \"text_en\": \"March 27, 2018\"}, {\"icon\": \"fa-eye\", \"title\": \"Vision\", \"text\": \"Devenir une r\\u00e9f\\u00e9rence dans l\'accompagnement et la qualification des jeunes et des femmes, ainsi qu\'un mod\\u00e8le de travail associatif structur\\u00e9, innovant et engag\\u00e9 dans le d\\u00e9veloppement humain et territorial.\", \"title_ar\": \"\\u0631\\u0624\\u064a\\u0629\", \"title_en\": \"Vision\", \"text_ar\": \"\\u0623\\u0646 \\u0646\\u0635\\u0628\\u062d \\u0645\\u0631\\u062c\\u0639\\u064b\\u0627 \\u0641\\u064a \\u062f\\u0639\\u0645 \\u0648\\u062a\\u0623\\u0647\\u064a\\u0644 \\u0627\\u0644\\u0634\\u0628\\u0627\\u0628 \\u0648\\u0627\\u0644\\u0646\\u0633\\u0627\\u0621\\u060c \\u0648\\u0646\\u0645\\u0648\\u0630\\u062c\\u064b\\u0627 \\u0644\\u0644\\u0639\\u0645\\u0644 \\u0627\\u0644\\u062c\\u0645\\u0639\\u0648\\u064a \\u0627\\u0644\\u0645\\u0646\\u0638\\u0645 \\u0648\\u0627\\u0644\\u0645\\u0628\\u062a\\u0643\\u0631 \\u0627\\u0644\\u0645\\u0644\\u062a\\u0632\\u0645 \\u0628\\u0627\\u0644\\u062a\\u0646\\u0645\\u064a\\u0629 \\u0627\\u0644\\u0628\\u0634\\u0631\\u064a\\u0629 \\u0648\\u0627\\u0644\\u062a\\u0631\\u0627\\u0628\\u064a\\u0629.\", \"text_en\": \"Become a reference in the support and qualification of young people and women, as well as a model of structured, innovative associative work committed to human and territorial development.\"}, {\"icon\": \"fa-rocket\", \"title\": \"Mission\", \"text\": \"Autonomiser les jeunes et les femmes du Grand Tanger \\u00e0 travers des programmes de formation, d\'accompagnement et d\'encadrement.\", \"title_ar\": \"\\u062a\\u0643\\u0644\\u064a\\u0641\", \"title_en\": \"Assignment\", \"text_ar\": \"\\u062a\\u0645\\u0643\\u064a\\u0646 \\u0627\\u0644\\u0634\\u0628\\u0627\\u0628 \\u0648\\u0627\\u0644\\u0646\\u0633\\u0627\\u0621 \\u0628\\u0645\\u062f\\u064a\\u0646\\u0629 \\u0637\\u0646\\u062c\\u0629 \\u0627\\u0644\\u0643\\u0628\\u0631\\u0649 \\u0645\\u0646 \\u062e\\u0644\\u0627\\u0644 \\u0628\\u0631\\u0627\\u0645\\u062c \\u0627\\u0644\\u062a\\u062f\\u0631\\u064a\\u0628 \\u0648\\u0627\\u0644\\u062f\\u0639\\u0645 \\u0648\\u0627\\u0644\\u0625\\u0634\\u0631\\u0627\\u0641.\", \"text_en\": \"Empower young people and women in Greater Tangier through training, support and supervision programs.\"}, {\"icon\": \"fa-map-marker-alt\", \"title\": \"Zone d\'intervention\", \"text\": \"Le Grand Tanger et ses environs\", \"title_ar\": \"\\u0645\\u0646\\u0637\\u0642\\u0629 \\u0627\\u0644\\u062a\\u062f\\u062e\\u0644\", \"title_en\": \"Intervention area\", \"text_ar\": \"\\u0637\\u0646\\u062c\\u0629 \\u0627\\u0644\\u0643\\u0628\\u0631\\u0649 \\u0648\\u0636\\u0648\\u0627\\u062d\\u064a\\u0647\\u0627\", \"text_en\": \"Greater Tangier and its surroundings\"}, {\"icon\": \"fa-users\", \"title\": \"Publics cibl\\u00e9s\", \"text\": \"Les jeunes, les femmes, les porteurs de projets, les associations locales et les acteurs de la soci\\u00e9t\\u00e9 civile.\", \"title_ar\": \"\\u0627\\u0644\\u062c\\u0645\\u0627\\u0647\\u064a\\u0631 \\u0627\\u0644\\u0645\\u0633\\u062a\\u0647\\u062f\\u0641\\u0629\", \"title_en\": \"Target audiences\", \"text_ar\": \"\\u0627\\u0644\\u0634\\u0628\\u0627\\u0628 \\u0648\\u0627\\u0644\\u0646\\u0633\\u0627\\u0621 \\u0648\\u0642\\u0627\\u062f\\u0629 \\u0627\\u0644\\u0645\\u0634\\u0627\\u0631\\u064a\\u0639 \\u0648\\u0627\\u0644\\u062c\\u0645\\u0639\\u064a\\u0627\\u062a \\u0627\\u0644\\u0645\\u062d\\u0644\\u064a\\u0629 \\u0648\\u0641\\u0627\\u0639\\u0644\\u064a \\u0627\\u0644\\u0645\\u062c\\u062a\\u0645\\u0639 \\u0627\\u0644\\u0645\\u062f\\u0646\\u064a.\", \"text_en\": \"Young people, women, project leaders, local associations and civil society actors.\"}], \"mission_features\": [{\"feature\": \"Formation professionnelle\", \"feature_ar\": \"\\u0627\\u0644\\u062a\\u062f\\u0631\\u064a\\u0628 \\u0627\\u0644\\u0645\\u0647\\u0646\\u064a\", \"feature_en\": \"Vocational training\"}, {\"feature\": \"Insertion sociale\", \"feature_ar\": \"\\u0627\\u0644\\u062a\\u0643\\u0627\\u0645\\u0644 \\u0627\\u0644\\u0627\\u062c\\u062a\\u0645\\u0627\\u0639\\u064a\", \"feature_en\": \"Social integration\"}, {\"feature\": \"Citoyennet\\u00e9 active\", \"feature_ar\": \"\\u0627\\u0644\\u0645\\u0648\\u0627\\u0637\\u0646\\u0629 \\u0627\\u0644\\u0646\\u0634\\u0637\\u0629\", \"feature_en\": \"Active citizenship\"}, {\"feature\": \"Autonomisation\", \"feature_ar\": \"\\u0627\\u0644\\u062a\\u0645\\u0643\\u064a\\u0646\", \"feature_en\": \"Empowerment\"}], \"objectives\": [{\"icon\": \"fa-hand-holding-heart\", \"title\": \"Solidarit\\u00e9 sociale\", \"text\": \"Cr\\u00e9er un cadre permettant de renforcer et d\'enraciner les valeurs de solidarit\\u00e9 et d\'entraide sociale.\", \"title_ar\": \"\\u0627\\u0644\\u062a\\u0636\\u0627\\u0645\\u0646 \\u0627\\u0644\\u0627\\u062c\\u062a\\u0645\\u0627\\u0639\\u064a\", \"title_en\": \"Social solidarity\", \"text_ar\": \"\\u062e\\u0644\\u0642 \\u0625\\u0637\\u0627\\u0631 \\u0644\\u062a\\u0639\\u0632\\u064a\\u0632 \\u0648\\u062a\\u062c\\u0630\\u064a\\u0631 \\u0642\\u064a\\u0645 \\u0627\\u0644\\u062a\\u0636\\u0627\\u0645\\u0646 \\u0648\\u0627\\u0644\\u0645\\u0633\\u0627\\u0639\\u062f\\u0629 \\u0627\\u0644\\u0627\\u062c\\u062a\\u0645\\u0627\\u0639\\u064a\\u0629.\", \"text_en\": \"Create a framework to strengthen and take root the values \\u200b\\u200bof solidarity and social assistance.\"}, {\"icon\": \"fa-handshake\", \"title\": \"Partenariats\", \"text\": \"D\\u00e9velopper des partenariats durables avec des organismes, institutions et acteurs nationaux et internationaux.\", \"title_ar\": \"\\u0627\\u0644\\u0634\\u0631\\u0627\\u0643\\u0627\\u062a\", \"title_en\": \"Partnerships\", \"text_ar\": \"\\u062a\\u0637\\u0648\\u064a\\u0631 \\u0634\\u0631\\u0627\\u0643\\u0627\\u062a \\u062f\\u0627\\u0626\\u0645\\u0629 \\u0645\\u0639 \\u0627\\u0644\\u0645\\u0646\\u0638\\u0645\\u0627\\u062a \\u0648\\u0627\\u0644\\u0645\\u0624\\u0633\\u0633\\u0627\\u062a \\u0648\\u0623\\u0635\\u062d\\u0627\\u0628 \\u0627\\u0644\\u0645\\u0635\\u0644\\u062d\\u0629 \\u0627\\u0644\\u0648\\u0637\\u0646\\u064a\\u064a\\u0646 \\u0648\\u0627\\u0644\\u062f\\u0648\\u0644\\u064a\\u064a\\u0646.\", \"text_en\": \"Develop lasting partnerships with national and international organizations, institutions and stakeholders.\"}, {\"icon\": \"fa-globe-africa\", \"title\": \"Diplomatie parall\\u00e8le\", \"text\": \"Jouer un r\\u00f4le dans la diplomatie parall\\u00e8le et favoriser l\'\\u00e9change d\'exp\\u00e9riences.\", \"title_ar\": \"\\u0627\\u0644\\u062f\\u0628\\u0644\\u0648\\u0645\\u0627\\u0633\\u064a\\u0629 \\u0627\\u0644\\u0645\\u0648\\u0627\\u0632\\u064a\\u0629\", \"title_en\": \"Parallel diplomacy\", \"text_ar\": \"\\u0627\\u0644\\u0642\\u064a\\u0627\\u0645 \\u0628\\u062f\\u0648\\u0631 \\u0641\\u064a \\u0627\\u0644\\u062f\\u0628\\u0644\\u0648\\u0645\\u0627\\u0633\\u064a\\u0629 \\u0627\\u0644\\u0645\\u0648\\u0627\\u0632\\u064a\\u0629 \\u0648\\u062a\\u0634\\u062c\\u064a\\u0639 \\u062a\\u0628\\u0627\\u062f\\u0644 \\u0627\\u0644\\u062e\\u0628\\u0631\\u0627\\u062a.\", \"text_en\": \"Play a role in parallel diplomacy and encourage the exchange of experiences.\"}, {\"icon\": \"fa-palette\", \"title\": \"Industrie culturelle\", \"text\": \"Promouvoir le concept d\'industrie culturelle \\u00e0 travers des projets, \\u00e9v\\u00e9nements et initiatives artistiques.\", \"title_ar\": \"\\u0635\\u0646\\u0627\\u0639\\u0629 \\u062b\\u0642\\u0627\\u0641\\u064a\\u0629\", \"title_en\": \"Cultural industry\", \"text_ar\": \"\\u062a\\u0639\\u0632\\u064a\\u0632 \\u0645\\u0641\\u0647\\u0648\\u0645 \\u0627\\u0644\\u0635\\u0646\\u0627\\u0639\\u0629 \\u0627\\u0644\\u062b\\u0642\\u0627\\u0641\\u064a\\u0629 \\u0645\\u0646 \\u062e\\u0644\\u0627\\u0644 \\u0627\\u0644\\u0645\\u0634\\u0627\\u0631\\u064a\\u0639 \\u0648\\u0627\\u0644\\u0641\\u0639\\u0627\\u0644\\u064a\\u0627\\u062a \\u0648\\u0627\\u0644\\u0645\\u0628\\u0627\\u062f\\u0631\\u0627\\u062a \\u0627\\u0644\\u0641\\u0646\\u064a\\u0629.\", \"text_en\": \"Promote the concept of cultural industry through artistic projects, events and initiatives.\"}, {\"icon\": \"fa-lightbulb\", \"title\": \"Cr\\u00e9ativit\\u00e9 et innovation\", \"text\": \"Encourager la cr\\u00e9ativit\\u00e9, l\'innovation et la participation active des jeunes et des femmes.\", \"title_ar\": \"\\u0627\\u0644\\u0625\\u0628\\u062f\\u0627\\u0639 \\u0648\\u0627\\u0644\\u0627\\u0628\\u062a\\u0643\\u0627\\u0631\", \"title_en\": \"Creativity and innovation\", \"text_ar\": \"\\u062a\\u0634\\u062c\\u064a\\u0639 \\u0627\\u0644\\u0625\\u0628\\u062f\\u0627\\u0639 \\u0648\\u0627\\u0644\\u0627\\u0628\\u062a\\u0643\\u0627\\u0631 \\u0648\\u0627\\u0644\\u0645\\u0634\\u0627\\u0631\\u0643\\u0629 \\u0627\\u0644\\u0641\\u0639\\u0627\\u0644\\u0629 \\u0644\\u0644\\u0634\\u0628\\u0627\\u0628 \\u0648\\u0627\\u0644\\u0646\\u0633\\u0627\\u0621.\", \"text_en\": \"Encourage creativity, innovation and active participation of young people and women.\"}, {\"icon\": \"fa-chalkboard-teacher\", \"title\": \"Formation et accompagnement\", \"text\": \"Organiser des programmes de formation, d\'encadrement et d\'accompagnement adapt\\u00e9s.\", \"title_ar\": \"\\u0627\\u0644\\u062a\\u062f\\u0631\\u064a\\u0628 \\u0648\\u0627\\u0644\\u062f\\u0639\\u0645\", \"title_en\": \"Training and support\", \"text_ar\": \"\\u062a\\u0646\\u0638\\u064a\\u0645 \\u0628\\u0631\\u0627\\u0645\\u062c \\u0627\\u0644\\u062a\\u062f\\u0631\\u064a\\u0628 \\u0648\\u0627\\u0644\\u0625\\u0634\\u0631\\u0627\\u0641 \\u0648\\u0627\\u0644\\u062f\\u0639\\u0645 \\u0627\\u0644\\u0645\\u0646\\u0627\\u0633\\u0628\\u0629.\", \"text_en\": \"Organize appropriate training, supervision and support programs.\"}], \"values\": [{\"icon\": \"fa-flag\", \"title\": \"Citoyennet\\u00e9\", \"title_ar\": \"\\u0627\\u0644\\u0645\\u0648\\u0627\\u0637\\u0646\\u0629\", \"title_en\": \"Citizenship\"}, {\"icon\": \"fa-heart\", \"title\": \"Solidarit\\u00e9\", \"title_ar\": \"\\u062a\\u0643\\u0627\\u0641\\u0644\", \"title_en\": \"Solidarity\"}, {\"icon\": \"fa-fist-raised\", \"title\": \"Engagement\", \"title_ar\": \"\\u0627\\u0644\\u062a\\u0632\\u0627\\u0645\", \"title_en\": \"Commitment\"}, {\"icon\": \"fa-people-arrows\", \"title\": \"Inclusion\", \"title_ar\": \"\\u0627\\u0644\\u0634\\u0645\\u0648\\u0644\", \"title_en\": \"Inclusion\"}, {\"icon\": \"fa-lightbulb\", \"title\": \"Innovation\", \"title_ar\": \"\\u0627\\u0628\\u062a\\u0643\\u0627\\u0631\", \"title_en\": \"Innovation\"}, {\"icon\": \"fa-balance-scale\", \"title\": \"Responsabilit\\u00e9\", \"title_ar\": \"\\u0645\\u0633\\u0624\\u0648\\u0644\\u064a\\u0629\", \"title_en\": \"Responsibility\"}], \"zone_stats\": [{\"icon\": \"fa-city\", \"title\": \"Tanger Ville\", \"title_ar\": \"\\u0645\\u062f\\u064a\\u0646\\u0629 \\u0637\\u0646\\u062c\\u0629\", \"title_en\": \"Tangier City\"}, {\"icon\": \"fa-map\", \"title\": \"Tanger-Med\", \"title_ar\": \"\\u0637\\u0646\\u062c\\u0629 \\u0627\\u0644\\u0645\\u062a\\u0648\\u0633\\u0637\", \"title_en\": \"Tangier-Med\"}, {\"icon\": \"fa-building\", \"title\": \"Zones industrielles\", \"title_ar\": \"\\u0627\\u0644\\u0645\\u0646\\u0627\\u0637\\u0642 \\u0627\\u0644\\u0635\\u0646\\u0627\\u0639\\u064a\\u0629\", \"title_en\": \"Industrial areas\"}]}', '', '', '', '', '/media/pages/WhatsApp%20Image%202026-07-17%20at%2020.33.47%20(1).jpeg', 'publie', 'عن', 'about', 'مؤسسة تعنى بالتعليم والثقافة والاجتماعية والرياضة بطنجة الكبرى.', 'A foundation committed to education, culture, social and sport in Greater Tangier.', 'مؤسسة تعنى بالتعليم والثقافة والاجتماعية والرياضة بطنجة الكبرى.', 'A foundation committed to education, culture, social and sport in Greater Tangier.', '', '', '', '', '', '', 'Une fondation engagée pour l\'éducation, la culture, le social et le sport dans le Grand Tanger.', '', '', '', 'Une fondation engagée pour l\'éducation, la culture, le social et le sport dans le Grand Tanger.', 'À propos'),
(3, '2026-08-02 23:47:29.320619', '2026-08-06 03:06:06.514821', 'activites', 'Activités', 'Toutes les actions terrain portées par la Fondation Tanger Métropole.', '', 'Toutes les actions terrain portées par la Fondation Tanger Métropole.', '[]', '', '', '', '', '', 'publie', 'أنشطة', 'Activities', 'جميع الأعمال الميدانية التي قامت بها مؤسسة طنجة متروبول.', 'All field actions carried out by the Tanger Métropole Foundation.', 'جميع الأعمال الميدانية التي قامت بها مؤسسة طنجة متروبول.', 'All field actions carried out by the Tanger Métropole Foundation.', '', '', '', '', '', '', 'Toutes les actions terrain portées par la Fondation Tanger Métropole.', '', '', '', 'Toutes les actions terrain portées par la Fondation Tanger Métropole.', 'Activités'),
(4, '2026-08-02 23:47:29.325596', '2026-08-06 03:06:09.653750', 'actualites', 'Actualités', 'Dernières nouvelles, communiqués, formations et concours.', '', 'Dernières nouvelles, communiqués, formations et concours.', '[]', '', '', '', '', '', 'publie', 'أخبار', 'News', 'آخر الأخبار والبيانات الصحفية والتدريبات والمسابقات.', 'Latest news, press releases, training and competitions.', 'آخر الأخبار والبيانات الصحفية والتدريبات والمسابقات.', 'Latest news, press releases, training and competitions.', '', '', '', '', '', '', 'Dernières nouvelles, communiqués, formations et concours.', '', '', '', 'Dernières nouvelles, communiqués, formations et concours.', 'Actualités'),
(5, '2026-08-02 23:47:29.332290', '2026-08-06 03:06:19.191226', 'formations', 'Nos formations', 'Développez vos compétences grâce aux formations proposées par la Fondation.', '', 'Développez vos compétences grâce aux formations proposées par la Fondation.', '[]', '', '', '', '', '', 'publie', 'التدريب لدينا', 'Our training', 'طور مهاراتك بفضل التدريب الذي تقدمه المؤسسة.', 'Develop your skills thanks to the training offered by the Foundation.', 'طور مهاراتك بفضل التدريب الذي تقدمه المؤسسة.', 'Develop your skills thanks to the training offered by the Foundation.', '', '', '', '', '', '', 'Développez vos compétences grâce aux formations proposées par la Fondation.', '', '', '', 'Développez vos compétences grâce aux formations proposées par la Fondation.', 'Nos formations'),
(6, '2026-08-02 23:47:29.338120', '2026-08-06 03:06:22.539667', 'medias', 'Médias', 'Photos, vidéos, albums et documents de la Fondation.', '', 'Photos, vidéos, albums et documents de la Fondation.', '[]', '', '', '', '', '', 'publie', 'وسائط', 'Media', 'الصور ومقاطع الفيديو والألبومات والوثائق الخاصة بالمؤسسة.', 'Photos, videos, albums and documents of the Foundation.', 'الصور ومقاطع الفيديو والألبومات والوثائق الخاصة بالمؤسسة.', 'Photos, videos, albums and documents of the Foundation.', '', '', '', '', '', '', 'Photos, vidéos, albums et documents de la Fondation.', '', '', '', 'Photos, vidéos, albums et documents de la Fondation.', 'Médias'),
(7, '2026-08-02 23:47:29.343617', '2026-08-06 03:06:12.508227', 'benevolat', 'Bénévolat', 'Rejoignez les bénévoles qui transforment Tanger par l\'action.', '', 'Rejoignez les bénévoles qui transforment Tanger par l\'action.', '[]', '', '', '', '', '', 'publie', 'التطوع', 'Volunteering', 'انضم إلى المتطوعين الذين يغيرون طنجة من خلال العمل.', 'Join the volunteers who are transforming Tangier through action.', 'انضم إلى المتطوعين الذين يغيرون طنجة من خلال العمل.', 'Join the volunteers who are transforming Tangier through action.', '', '', '', '', '', '', 'Rejoignez les bénévoles qui transforment Tanger par l\'action.', '', '', '', 'Rejoignez les bénévoles qui transforment Tanger par l\'action.', 'Bénévolat'),
(8, '2026-08-02 23:47:29.348117', '2026-08-06 03:06:16.088350', 'contact', 'Contact', 'Contactez la Fondation Tanger Métropole.', '', 'Contactez la Fondation Tanger Métropole.', '[]', '', '', '', '', '', 'publie', 'اتصال', 'Contact', 'اتصل بمؤسسة طنجة متروبول.', 'Contact the Tanger Métropole Foundation.', 'اتصل بمؤسسة طنجة متروبول.', 'Contact the Tanger Métropole Foundation.', '', '', '', '', '', '', 'Contactez la Fondation Tanger Métropole.', '', '', '', 'Contactez la Fondation Tanger Métropole.', 'Contact');

-- --------------------------------------------------------

--
-- Structure de la table `core_partner`
--

CREATE TABLE `core_partner` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(180) NOT NULL,
  `partner_type` varchar(100) NOT NULL,
  `url` varchar(200) NOT NULL,
  `logo_url` varchar(500) NOT NULL,
  `description` longtext NOT NULL,
  `order` int(10) UNSIGNED NOT NULL CHECK (`order` >= 0),
  `status` varchar(20) NOT NULL,
  `featured_home` tinyint(1) NOT NULL,
  `name_ar` varchar(180) DEFAULT NULL,
  `name_en` varchar(180) DEFAULT NULL,
  `partner_type_ar` varchar(100) DEFAULT NULL,
  `partner_type_en` varchar(100) DEFAULT NULL,
  `description_ar` longtext DEFAULT NULL,
  `description_en` longtext DEFAULT NULL,
  `description_fr` longtext DEFAULT NULL,
  `name_fr` varchar(180) DEFAULT NULL,
  `partner_type_fr` varchar(100) DEFAULT NULL,
  `facebook_url` varchar(200) NOT NULL,
  `instagram_url` varchar(200) NOT NULL,
  `start_date` date DEFAULT NULL,
  `youtube_url` varchar(200) NOT NULL,
  `linkedin_url` varchar(200) NOT NULL,
  `tiktok_url` varchar(200) NOT NULL,
  `twitter_url` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_sitesetting`
--

CREATE TABLE `core_sitesetting` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `key` varchar(120) NOT NULL,
  `value` longtext NOT NULL,
  `group` varchar(80) NOT NULL,
  `value_ar` longtext DEFAULT NULL,
  `value_en` longtext DEFAULT NULL,
  `value_fr` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_sitesetting`
--

INSERT INTO `core_sitesetting` (`id`, `created_at`, `updated_at`, `key`, `value`, `group`, `value_ar`, `value_en`, `value_fr`) VALUES
(1, '2026-08-02 23:47:29.354006', '2026-08-06 02:54:21.226711', 'stats_beneficiaires', '12500', 'general', '12500', '12500', '12500'),
(2, '2026-08-02 23:47:29.359712', '2026-08-06 02:54:22.691936', 'site_phone', '+212 5 39 00 00 00', 'general', '+212 5 39 00 00 00', '+212 5 39 00 00 00', '+212 5 39 00 00 00'),
(3, '2026-08-02 23:47:29.365713', '2026-08-06 02:54:24.186365', 'site_email', 'contact@tangermetropole.ma', 'general', 'contact@tangermetropole.ma', 'contact@tangermetropole.ma', 'contact@tangermetropole.ma'),
(4, '2026-08-06 01:26:07.417771', '2026-08-06 02:54:25.114478', 'stats_annees', '7', 'general', '7', '7', '7'),
(5, '2026-08-06 02:46:54.447546', '2026-08-06 02:54:27.620982', 'phone', '+212 5 39 94 00 00', 'contact', '+212 5 39 94 00 00', '+212 5 39 94 00 00', '+212 5 39 94 00 00'),
(6, '2026-08-06 02:46:54.452792', '2026-08-06 02:54:30.656381', 'email', 'contactest@tangermetropole.ma', 'contact', 'contactest@tangermetropole.ma', 'contactest@tangermetropole.ma', 'contactest@tangermetropole.ma'),
(7, '2026-08-06 02:46:54.457942', '2026-08-06 02:54:32.158093', 'address', '23 Rue de la Liberté, Tanger 90000', 'contact', '23 شارع الحرية، طنجة 90000', '23 Rue de la Liberté, Tangier 90000', '23 Rue de la Liberté, Tanger 90000'),
(8, '2026-08-06 02:46:54.460516', '2026-08-06 02:54:33.935164', 'hours', 'Lun - Ven : 09h00 - 17h00', 'contact', 'الإثنين - الجمعة: 9:00 صباحًا - 5:00 مساءً', 'Mon - Fri: 9:00 a.m. - 5:00 p.m.', 'Lun - Ven : 09h00 - 17h00'),
(9, '2026-08-06 02:46:54.463131', '2026-08-06 02:54:35.285749', 'hours_extra', 'Fermé le samedi et le dimanche', 'contact', 'مغلق يومي السبت والأحد', 'Closed Saturday and Sunday', 'Fermé le samedi et le dimanche'),
(10, '2026-08-06 02:46:54.465428', '2026-08-06 02:54:35.296082', 'facebook_url', 'https://facebook.com/...', 'social', 'https://facebook.com/...', 'https://facebook.com/...', 'https://facebook.com/...'),
(11, '2026-08-06 02:46:54.467941', '2026-08-06 02:54:35.300039', 'instagram_url', 'https://instagram.com/...', 'social', 'https://instagram.com/...', 'https://instagram.com/...', 'https://instagram.com/...'),
(12, '2026-08-06 02:46:54.473849', '2026-08-06 02:54:35.303412', 'youtube_url', 'https://youtube.com/...', 'social', 'https://youtube.com/...', 'https://youtube.com/...', 'https://youtube.com/...'),
(13, '2026-08-06 02:46:54.476995', '2026-08-06 02:54:35.306349', 'linkedin_url', 'https://linkedin.com/...', 'social', 'https://linkedin.com/...', 'https://linkedin.com/...', 'https://linkedin.com/...'),
(14, '2026-08-06 02:46:54.479974', '2026-08-06 02:54:35.309160', 'map_link', 'https://maps.google.com/?q=Tanger,Maroc', 'map', 'https://maps.google.com/?q=Tanger,Maroc', 'https://maps.google.com/?q=Tanger,Maroc', 'https://maps.google.com/?q=Tanger,Maroc'),
(15, '2026-08-06 02:46:54.485510', '2026-08-06 02:54:35.311893', 'map_embed', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d103531.824278963!2d-5.866666684509277!3d35.76666668450928!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd0b2655c0e0e0e1%3A0x5e5c5e5e5e5e5e5e!2sTanger%2C%20Maroc!5e0!3m2!1sfr!2sma!4v1690000000000', 'map', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d103531.824278963!2d-5.866666684509277!3d35.76666668450928!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd0b2655c0e0e0e1%3A0x5e5c5e5e5e5e5e5e!2sTanger%2C%20Maroc!5e0!3m2!1sfr!2sma!4v1690000000000', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d103531.824278963!2d-5.866666684509277!3d35.76666668450928!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd0b2655c0e0e0e1%3A0x5e5c5e5e5e5e5e5e!2sTanger%2C%20Maroc!5e0!3m2!1sfr!2sma!4v1690000000000', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d103531.824278963!2d-5.866666684509277!3d35.76666668450928!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd0b2655c0e0e0e1%3A0x5e5c5e5e5e5e5e5e!2sTanger%2C%20Maroc!5e0!3m2!1sfr!2sma!4v1690000000000'),
(16, '2026-08-06 02:48:34.913109', '2026-08-06 02:54:35.316520', 'whatsapp_url', 'https://wa.me/212600000000', 'contact', 'https://wa.me/212600000000', 'https://wa.me/212600000000', 'https://wa.me/212600000000');

-- --------------------------------------------------------

--
-- Structure de la table `core_userprofile`
--

CREATE TABLE `core_userprofile` (
  `id` bigint(20) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_volunteerapplication`
--

CREATE TABLE `core_volunteerapplication` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(160) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(40) NOT NULL,
  `city` varchar(100) NOT NULL,
  `skills` varchar(255) NOT NULL,
  `motivation` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `cv_url` varchar(255) NOT NULL,
  `availability` varchar(255) NOT NULL,
  `desired_fields` varchar(255) NOT NULL,
  `experience` longtext NOT NULL,
  `skills_description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(14, 'core', 'activityregistration'),
(7, 'core', 'contactmessage'),
(8, 'core', 'contentitem'),
(13, 'core', 'formationregistration'),
(9, 'core', 'pagecontent'),
(10, 'core', 'partner'),
(11, 'core', 'sitesetting'),
(15, 'core', 'userprofile'),
(12, 'core', 'volunteerapplication'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-08-02 23:47:17.196002'),
(2, 'auth', '0001_initial', '2026-08-02 23:47:18.231356'),
(3, 'admin', '0001_initial', '2026-08-02 23:47:18.483355'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-08-02 23:47:18.503839'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-08-02 23:47:18.533948'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-08-02 23:47:18.667028'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-08-02 23:47:18.768508'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-08-02 23:47:18.796206'),
(9, 'auth', '0004_alter_user_username_opts', '2026-08-02 23:47:18.812976'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-08-02 23:47:18.908005'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-08-02 23:47:18.913156'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-08-02 23:47:18.930193'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-08-02 23:47:18.955860'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-08-02 23:47:18.976301'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-08-02 23:47:19.000765'),
(16, 'auth', '0011_update_proxy_permissions', '2026-08-02 23:47:19.015914'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-08-02 23:47:19.040165'),
(18, 'core', '0001_initial', '2026-08-02 23:47:19.320079'),
(19, 'sessions', '0001_initial', '2026-08-02 23:47:19.388853'),
(20, 'core', '0002_multilingual_fields', '2026-08-04 01:10:05.706662'),
(21, 'core', '0003_alter_contactmessage_options_and_more', '2026-08-04 02:13:54.125477'),
(22, 'core', '0004_populate_fr_translation_fields', '2026-08-04 02:13:54.231911'),
(23, 'core', '0005_activityregistration', '2026-08-04 18:20:21.648887'),
(24, 'core', '0006_partner_facebook_url_partner_instagram_url_and_more', '2026-08-06 01:38:32.066184'),
(25, 'core', '0007_partner_linkedin_url_partner_tiktok_url_and_more', '2026-08-06 02:05:08.889191'),
(26, 'core', '0008_alter_partner_logo_url', '2026-08-06 02:09:25.750165'),
(27, 'core', '0009_contentitem_linkedin_url_contentitem_tiktok_url_and_more', '2026-08-06 02:33:10.505079'),
(28, 'core', '0010_volunteerapplication_cv_url', '2026-08-06 15:22:33.810155'),
(29, 'core', '0011_volunteerapplication_availability_and_more', '2026-08-06 15:26:13.180179'),
(30, 'core', '0012_contactmessage_attachment_url_contactmessage_city', '2026-08-06 15:31:33.126982'),
(31, 'core', '0013_userprofile', '2026-08-07 02:06:48.662839');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('73b9weqhi28pmupq1isx6vugtzedcxua', 'e30:1wrF7k:F7A2LDB-EG3UoAb_ao_mIoMm51-BtHnoHHM6Db112mI', '2026-08-18 13:24:04.835317'),
('9m3q6tk37asdybhr4hp5ue63mhsoxa7o', 'e30:1wrF7D:DNbOwNyRwrZiM_MHR6J8w3Jhjyagaq0J1IcIlzL8KSM', '2026-08-18 13:23:31.250652'),
('9sza44287ybcs50yr3v8dfwe48w0b141', '.eJxVjEEOwiAQRe_C2pAZJ2Val-49AwEGLGrAlDbRGO-uTbrQ7X_vv5eybplHu7Q42SzqoEjtfjfvwjWWFcjFlXPVoZZ5yl6vit5o06cq8Xbc3L_A6Nr4fQO45IEBJLKQN35gpF6QOo-GaUhB-h7JAJuOOYIE2qMRMi4lHADXaIut5VpsfNzz9FQHeH8AZMs-Rg:1wsA4w:5FtgPCi66crwzeXwko_k2dW8Y4-UJmHuVeMmHgswnGs', '2026-08-21 02:12:58.804635'),
('i7kh63rcp9ps3jo4wkxsiarh1b0xykd2', '.eJxVjEEOwiAQRe_C2pAZJ2XApXvPQIABqRqalHbVeHdt0oVu_3vvb8qHdal-7Xn2o6iLInX63WJIz9x2II_Q7pNOU1vmMepd0Qft-jZJfl0P9--ghl6_NUAoERhAMgtFEx0jWUEaIhomV5JYi2SAzcCcQRKd0QiZUAo6QPX-AM3BNwk:1wrnAd:4kpVGhcgvZztE8zFrmhUQ2TnXfp8koUYevbTNCmuBYE', '2026-08-20 01:45:19.915489'),
('ij0z8enlji6q5qh2hlzotmq6ny4gzgxr', '.eJxVjEEOgyAQRe_CuiFDJ4K67L5nIMAMSmukAU3aNL17NXHj9r_3_lfUtLCd3DysbmDRC1fERVi3LqNdKxebaBvxvHkXnjzvgB5bmWXI81KSl7siD1rlPRNPt8M9HYyujlsN4KIHA0BsCL32nVHYksLGK22wi4HaVqEGoxtjGCjgVWlC7WJUHaj9tHKtKc-W369UPqKH3x8IH0Vf:1wrEQT:2jHmO0S4Qdplp7OuB_RDTk8kFCkBTOWssyqjZHr3dIw', '2026-08-18 12:39:21.405110'),
('ua6y7fahq5wtq9hqvsqtek3fi3c7hd3r', '.eJxVjEEOwiAQRe_C2pAZJ2Val-49AwEGLGrAlDbRGO-uTbrQ7X_vv5eybplHu7Q42SzqoEjtfjfvwjWWFcjFlXPVoZZ5yl6vit5o06cq8Xbc3L_A6Nr4fQO45IEBJLKQN35gpF6QOo-GaUhB-h7JAJuOOYIE2qMRMi4lHADXaIut5VpsfNzz9FQHeH8AZMs-Rg:1wrzbn:qg_DiWB4B1qi__VwDCj2kuWxJOR0_QJzNdvNQWVAtb0', '2026-08-20 15:02:11.448471'),
('usbc1dfw5v23lchzngn90091ymu7h479', '.eJxVjEEOwiAQRe_C2pAZJ2XApXvPQIABqRqalHbVeHdt0oVu_3vvb8qHdal-7Xn2o6iLInX63WJIz9x2II_Q7pNOU1vmMepd0Qft-jZJfl0P9--ghl6_NUAoERhAMgtFEx0jWUEaIhomV5JYi2SAzcCcQRKd0QiZUAo6QPX-AM3BNwk:1wrnAl:dcC3l8plathjFn7oeC7lsrzFe5BwkX2ugavVWVu9Z_U', '2026-08-20 01:45:27.624309'),
('wyb9vud8edkeom9k13v17xmmg1j3him1', '.eJxVjEEOwiAQRe_C2pAZJ2Val-49AwEGLGrAlDbRGO-uTbrQ7X_vv5eybplHu7Q42SzqoEjtfjfvwjWWFcjFlXPVoZZ5yl6vit5o06cq8Xbc3L_A6Nr4fQO45IEBJLKQN35gpF6QOo-GaUhB-h7JAJuOOYIE2qMRMi4lHADXaIut5VpsfNzz9FQHeH8AZMs-Rg:1wrIlr:BiOf2UANLWnu5EhuDirsQlxW_UrspAj-5m7FSHIu4Ko', '2026-08-18 17:17:43.594584'),
('zehm3u0pws19nwwzln0cqppunj1ym3vy', '.eJxVjEEOwiAQRe_C2pAZJ2Val-49AwEGLGrAlDbRGO-uTbrQ7X_vv5eybplHu7Q42SzqoEjtfjfvwjWWFcjFlXPVoZZ5yl6vit5o06cq8Xbc3L_A6Nr4fQO45IEBJLKQN35gpF6QOo-GaUhB-h7JAJuOOYIE2qMRMi4lHADXaIut5VpsfNzz9FQHeH8AZMs-Rg:1wrmON:2fdB4tusLteDleqT_S6OkR3W7y_Hz-WBb6Pr2fQxWFg', '2026-08-20 00:55:27.644998');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `core_activityregistration`
--
ALTER TABLE `core_activityregistration`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_activityregistr_activity_id_64f2cb38_fk_core_cont` (`activity_id`);

--
-- Index pour la table `core_contactmessage`
--
ALTER TABLE `core_contactmessage`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_contentitem`
--
ALTER TABLE `core_contentitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_contentitem_slug_ab8ec599` (`slug`);

--
-- Index pour la table `core_formationregistration`
--
ALTER TABLE `core_formationregistration`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_formationregist_formation_id_3b7f7f2b_fk_core_cont` (`formation_id`);

--
-- Index pour la table `core_pagecontent`
--
ALTER TABLE `core_pagecontent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Index pour la table `core_partner`
--
ALTER TABLE `core_partner`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_sitesetting`
--
ALTER TABLE `core_sitesetting`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key` (`key`);

--
-- Index pour la table `core_userprofile`
--
ALTER TABLE `core_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Index pour la table `core_volunteerapplication`
--
ALTER TABLE `core_volunteerapplication`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `core_activityregistration`
--
ALTER TABLE `core_activityregistration`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `core_contactmessage`
--
ALTER TABLE `core_contactmessage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `core_contentitem`
--
ALTER TABLE `core_contentitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT pour la table `core_formationregistration`
--
ALTER TABLE `core_formationregistration`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `core_pagecontent`
--
ALTER TABLE `core_pagecontent`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `core_partner`
--
ALTER TABLE `core_partner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `core_sitesetting`
--
ALTER TABLE `core_sitesetting`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT pour la table `core_userprofile`
--
ALTER TABLE `core_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `core_volunteerapplication`
--
ALTER TABLE `core_volunteerapplication`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `core_activityregistration`
--
ALTER TABLE `core_activityregistration`
  ADD CONSTRAINT `core_activityregistr_activity_id_64f2cb38_fk_core_cont` FOREIGN KEY (`activity_id`) REFERENCES `core_contentitem` (`id`);

--
-- Contraintes pour la table `core_formationregistration`
--
ALTER TABLE `core_formationregistration`
  ADD CONSTRAINT `core_formationregist_formation_id_3b7f7f2b_fk_core_cont` FOREIGN KEY (`formation_id`) REFERENCES `core_contentitem` (`id`);

--
-- Contraintes pour la table `core_userprofile`
--
ALTER TABLE `core_userprofile`
  ADD CONSTRAINT `core_userprofile_user_id_5141ad90_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
