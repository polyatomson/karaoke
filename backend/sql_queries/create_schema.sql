CREATE TABLE IF NOT EXISTS `Songs` (
  `title` varchar(500) NOT NULL,
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `artist` varchar(500) NOT NULL DEFAULT 'Unknown',
  `vocals` tinyint(1) DEFAULT NULL,
  `in_use` tinyint(1) NOT NULL DEFAULT '1',
  `origin` varchar(20) NOT NULL,
  `link` varchar(800) NOT NULL,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `Songs_UN_link` (`link`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `Views` (
  `song_id` int(11) NOT NULL,
  `n_views` int(11) NOT NULL,
  UNIQUE KEY `Views_UN` (`song_id`),
  CONSTRAINT `Views_FK` FOREIGN KEY (`song_id`) REFERENCES `Songs` (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Songs(song_id, title, artist, vocals, in_use, origin, link) 
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE song_id=song_id;

