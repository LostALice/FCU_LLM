# Code by AkinoAlice@TyrantRey

from os import getenv

import mysql.connector as connector

class SetupMYSQL(object):
    def __init__(self) -> None:
        self.HOST = getenv("MYSQL_HOST")
        self.USER = getenv("MYSQL_USER_NAME")
        self.PASSWORD = getenv("MYSQL_PASSWORD")
        self.DATABASE = getenv("MYSQL_DATABASE")

        self.connection = connector.connect(
            host=getenv("MYSQL_HOST"),
            user=getenv("MYSQL_USER_NAME"),
            password=getenv("MYSQL_PASSWORD"),
            port=getenv("MYSQL_PORT"),
        )
        self.curser = self.connection.cursor(dictionary=True, prepared=True)

        self.curser.execute(f"CREATE DATABASE {self.DATABASE};")
        self.connection.connect(database=self.DATABASE)
        self.connection.commit()

        # LOGIN table
        self.curser.execute(
            """
            CREATE TABLE `FCU_LLM`.`login` (
                `user_id` VARCHAR(45) NOT NULL,
                `password` VARCHAR(45) NOT NULL,
                `jwt` VARCHAR(45) NOT NULL,
                `last_login` TIMESTAMP NOT NULL,
                PRIMARY KEY (`user_id`)
            );
            """
        )

        # USER table
        self.curser.execute(
            """
            CREATE TABLE `FCU_LLM`.`user` (
                `user_id` INT NOT NULL,
                `username` VARCHAR(45) NOT NULL,
                `role_id` INT NOT NULL,
                PRIMARY KEY (`user_id`)
            );
            """
        )

        # ROLE table
        self.curser.execute(
            """
            CREATE TABLE `FCU_LLM`.`role` (
                `role_id` INT NOT NULL,
                `role_name` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`role_id`)
            );
            """
        )

        # CHAT table
        self.curser.execute(
            """
            CREATE TABLE `FCU_LLM`.`chat` (
                `chat_id` VARCHAR(45) NOT NULL,
                `user_id` VARCHAR(45) NOT NULL,
                `chat_name` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`chat_id`)
            );
            """
        )

        # FILE table
        self.curser.execute(
            """
            CREATE TABLE `file` (
                `file_id` varchar(45) NOT NULL,
                `file_path` int NOT NULL,
                `last_update` timestamp NOT NULL,
                `expired` tinyint NOT NULL DEFAULT '1',
                PRIMARY KEY (`file_id`)
            )
            """
        )

        # QA table
        self.curser.execute(
            """
            CREATE TABLE `FCU_LLM`.`qa` (
                `chat_id` VARCHAR(45) NOT NULL,
                `content` LONGTEXT NOT NULL,
                `sent_time` TIMESTAMP NOT NULL,
                `sent_by` VARCHAR(45) NOT NULL,
                `file_id` VARCHAR(45) NULL DEFAULT NULL,
                PRIMARY KEY (`chat_id`)
            );
            """
        )

        # TAG table
        self.curser.execute(
            """
            CREATE TABLE `FCU_LLM`.`tag` (
                `tag_id` INT NOT NULL,
                `tag_name` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`tag_id`)
            );
            """
        )

        self.connection.commit()

class SetupMilvus(object):
    def __init__(self) -> None:
        self.HOST = getenv("MILVUS_HOST")
        self.PORT = getenv("MILVUS_PORT")