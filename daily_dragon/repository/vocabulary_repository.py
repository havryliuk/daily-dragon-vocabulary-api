import json
import logging
import os
import time
from typing import Dict

import boto3
from botocore.exceptions import ClientError

from daily_dragon.exceptions import WordAlreadyExistsError

logger = logging.getLogger(__name__)


class VocabularyRepository:

    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv("S3_BUCKET")
        self.vocabulary_file_key = os.getenv("S3_FILE_PATH")

    def get_vocabulary(self) -> Dict[str, Dict]:
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.vocabulary_file_key)
            return json.loads(response['Body'].read().decode())
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.info("Vocabulary file not found, creating a new one.")
                return dict()
            else:
                logger.error("Error fetching vocabulary file: %s", e)
                raise

    def save_vocabulary(self, vocabulary: Dict[str, Dict]):
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=self.vocabulary_file_key,
            Body=json.dumps(vocabulary, ensure_ascii=False).encode('utf-8')
        )

    def add_word(self, word: str) -> None:
        vocabulary = self.get_vocabulary()

        if word in vocabulary:
            logger.info("Word already exists in vocabulary: %s", word)
            raise WordAlreadyExistsError()

        word_details = {
            'adoption': 0,
            'created_on': int(time.time())
        }

        vocabulary[word] = word_details

        self.save_vocabulary(vocabulary)

        logger.info("Word added to vocabulary: %s", word)
