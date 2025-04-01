import json
from unittest import TestCase

from sqlalchemy.engine import Engine

from bageltushare.download import download
from bageltushare import get_engine, create_log_table


class TestDownload(TestCase):

    def setUp(self):
        # connect to database
        with open("test_config.json") as f:
            config = json.load(f)
            self.config = config["database"]
            self.token = config["token"]
        self.engine: Engine = get_engine(**self.config)

        self.download_api_name = "trade_cal"
        self.update_by_date_api_name = "daily"
        self.update_by_ts_code_api_name = "balancesheet"

        # create log table
        create_log_table(self.engine)

    def test_download(self):
        download(self.engine, self.token, self.download_api_name)

    def test_download_failed(self):
        download(self.engine, self.token, "INVALID_API_NAME", retry=1)

