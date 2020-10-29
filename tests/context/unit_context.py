import sys
from box import Box

sys.path.append("./tests/mock")

from mock.rds import Rds
from mock.s3 import VoidS3
from mock import extract


class UnitContext:
    def __init__(self):
        self.var = Box({"insert_statement": "...", "delimiter": ",", "newline": "\n"})

        self.s3 = VoidS3()

        self.extract = extract

        self.rds = Rds()
