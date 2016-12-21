SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for answers_snapshots
-- ----------------------------
DROP TABLE IF EXISTS `answers_snapshots`;
CREATE TABLE `answers_snapshots` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answer_id` int(11) DEFAULT NULL,
  `voteup_count` int(11) DEFAULT NULL,
  `comment_count` int(11) DEFAULT NULL,
  `collapsed_counts` int(11) DEFAULT NULL,
  `excerpt` text,
  `can_comment` text,
  `comment_permission` varchar(255) DEFAULT NULL,
  `is_normal` varchar(10) DEFAULT NULL,
  `reshipment_settings` varchar(255) DEFAULT NULL,
  `author` text,
  `question` text,
  `relationship` text,
  `suggest_edit` text,
  `type` varchar(255) DEFAULT NULL,
  `created_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `updated_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `crawl_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for manage_information
-- ----------------------------
DROP TABLE IF EXISTS `manage_information`;
CREATE TABLE `manage_information` (
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `cookies` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for questions
-- ----------------------------
DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `title` text,
  `crawl_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for questions_snapshots
-- ----------------------------
DROP TABLE IF EXISTS `questions_snapshots`;
CREATE TABLE `questions_snapshots` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `question_type` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `answer_num` int(11) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  `views_num` int(11) DEFAULT NULL,
  `labels` text,
  `content` text,
  `crawl_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user_snapshots
-- ----------------------------
DROP TABLE IF EXISTS `user_snapshots`;
CREATE TABLE `user_snapshots` (
  `id` int(11) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `avatar` text,
  `answers_num` int(11) DEFAULT NULL,
  `posts_num` int(11) DEFAULT NULL,
  `asks_num` int(11) DEFAULT NULL,
  `followers_num` int(11) DEFAULT NULL,
  `followees_num` int(11) DEFAULT NULL,
  `agrees_num` int(11) DEFAULT NULL,
  `thanks_num` int(11) DEFAULT NULL,
  `be_collected_num` int(11) DEFAULT NULL,
  `edits_num` int(11) DEFAULT NULL,
  `crawl_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
