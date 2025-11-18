import logging
import random

from fastapi import Depends

from daily_dragon.repository.vocabulary_repository import VocabularyRepository

logger = logging.getLogger(__name__)


class VocabularyService:

    def __init__(self, vocabulary_repository: VocabularyRepository = Depends()):
        self.vocabulary_repository = vocabulary_repository

    def add_word(self, word):
        return self.vocabulary_repository.add_word(word)

    def get_vocabulary(self):
        return self.vocabulary_repository.get_vocabulary()

    def delete_word(self, word):
        vocabulary = self.vocabulary_repository.get_vocabulary()
        if word in vocabulary:
            del vocabulary[word]
            self.vocabulary_repository.save_vocabulary(vocabulary)
        logger.info(f"Deleted word {word}")

    def get_random_vocabulary(self, count):
        all_vocabulary = self.vocabulary_repository.get_vocabulary()
        random_words = random.sample(list(all_vocabulary.keys()), min(count, len(all_vocabulary)))
        return {word: all_vocabulary[word] for word in random_words}
