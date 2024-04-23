# Code by AkinoAlice@TyrantRey

from pymilvus import MilvusClient
from pymilvus import DataType

from typing import Literal, Dict
from os import getenv, listdir

import mysql.connector as connector
import logging

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
        self.cursor = self.connection.cursor(
                dictionary=True, prepared=True)

        try:
            self.connection.database = getenv("MYSQL_DATABASE")
        except connector.Error as error:
            logging.error(error)
            logging.debug("Creating database")
            self.create_database()
        finally:
            self.connection.database = getenv("MYSQL_DATABASE")
            self.cursor = self.connection.cursor(
                dictionary=True, prepared=True)

    def create_database(self) -> None:
        self.cursor.execute(f"CREATE DATABASE {self.DATABASE};")
        self.connection.connect(database=self.DATABASE)
        self.connection.commit()

        # LOGIN table
        self.cursor.execute(
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
        self.cursor.execute(
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
        self.cursor.execute(
            """
            CREATE TABLE `FCU_LLM`.`role` (
                `role_id` INT NOT NULL,
                `role_name` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`role_id`)
            );
            """
        )

        # CHAT table
        self.cursor.execute(
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
        self.cursor.execute(
            """
            CREATE TABLE `file` (
                `file_id` varchar(45) NOT NULL,
                `file_name` varchar(255) NOT NULL,
                `last_update` timestamp NOT NULL DEFAULT NOW(),
                `expired` tinyint NOT NULL DEFAULT '1',
                PRIMARY KEY (`file_id`)
            )
            """
        )

        # QA table
        self.cursor.execute(
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
        self.cursor.execute(
            """
            CREATE TABLE `FCU_LLM`.`tag` (
                `tag_id` INT NOT NULL,
                `tag_name` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`tag_id`)
            );
            """
        )

        self.connection.commit()
        logging.debug("Created database")

class SetupMilvus(object):
    def __init__(self) -> None:
        self.HOST = getenv("MILVUS_HOST")
        self.PORT = getenv("MILVUS_PORT")

        self.client = MilvusClient(
            uri=f"http://{self.HOST}:{self.PORT}"
        )

    def create_collection(
        self, collection_name: str = "",
        index_type: Literal["FLAT", "IVF_FLAT", "IVF_SQ8", "IVF_PQ", "HNSW",
                            "ANNOY", "RHNSW_FLAT", "RHNSW_PQ", "RHNSW_SQ"] = "IVF_FLAT",
        metric_type: Literal["L2", "IP"] = "L2"
    ) -> Dict:

        schema = MilvusClient.create_schema(
            auto_id=True,
            enable_dynamic_field=False,
        )

        schema.add_field(field_name="id", datatype=DataType.VARCHAR,
                         max_length=512, is_primary=True)
        schema.add_field(field_name="source",
                         datatype=DataType.VARCHAR, max_length=512)
        schema.add_field(field_name="vector",
                         datatype=DataType.FLOAT_VECTOR, dim=768)

        index_params = self.client.prepare_index_params()

        index_params.add_index(
            field_name="vector",
            index_type=index_type,
            metric_type=metric_type,
            params={
                "nlist": 128
            }
        )

        self.client.create_collection(
            collection_name=collection_name,
            schema=schema,
            metric_type=metric_type,
            index_params=index_params
        )

        collection_status = self.client.get_load_state(
            collection_name=collection_name
        )
        logging.debug(f"Creating collection: {collection_name}")
        return collection_status


class SetupRAG(object):
    def __init__(self) -> None:
        self.LLM_model = getenv("LLM_MODEL_PATH")
        self.embedded_model = getenv("EMBEDDING_MODEL_PATH")
