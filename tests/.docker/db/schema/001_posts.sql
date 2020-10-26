USE optimal;

-- NOTE: this is not a generic schema
-- story SPAT-123456 in sprint N will address this spike schema limitations
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id`            SERIAL       NOT NULL COMMENT 'Primary Key',
  `post_id`       VARCHAR(64)  NOT NULL COMMENT 'distinct post id',
  `name`          VARCHAR(128) NOT NULL COMMENT 'the producer tag name',
  `post_date`     TIMESTAMP    NOT NULL COMMENT 'the time when the post was created according to the source',
  `post_body`     TEXT         NOT NULL COMMENT 'primary text content within the forum post',
  `update_date`   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_date`  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`)
)

ENGINE  = InnoDB
DEFAULT CHARSET = utf8
AUTO_INCREMENT = 1;
