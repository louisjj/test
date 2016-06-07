CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `join_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `auth_token` varchar(255) NOT NULL,
  `valid_token` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_username` (`username`),
  UNIQUE KEY `user_email` (`email`)
);

CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `synchro_id` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `distance` decimal(10,5) NOT NULL,
  `duration` decimal(10,5) NOT NULL,
  `max_speed` decimal(10,5) NOT NULL,
  `avg_speed` decimal(10,5) NOT NULL,
  `avg_bpm` decimal(10,5) NOT NULL,
  `avg_spm` decimal(10,5) NOT NULL,
  `weather` varchar(255) NOT NULL DEFAULT 'cloudy',
  `type_activity` varchar(255) NOT NULL DEFAULT 'run',
  `mood` varchar(255) NOT NULL DEFAULT 'cool',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `activity_synchro_id` (`synchro_id`),
  KEY `activity_user_id` (`user_id`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
);