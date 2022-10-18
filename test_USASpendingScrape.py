import unittest
from unittest.mock import MagicMock, mock_open, patch

from awards import Contract, Grant
from USASpendingScrape import download_zips


class TestUSASpendingScrape(unittest.TestCase):
    @patch("USASpendingScrape.requests")
    def test_api_hit(self, mock_requests):
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {
            "file_name": "file name",
            "file_url": "url",
        }

        mock_requests.post.return_value = mock_post_response

        mock_get_response = MagicMock()
        mock_get_response.iter_content.return_value = b"hello world"
        mock_requests.get.return_value = mock_get_response

        award_list = [Grant("ABC123", 123)]

        with patch("USASpendingScrape.open", mock_open()) as m:
            download_zips(award_list)
            mock_requests.get.assert_called()
            m.assert_called()
            m().write.assert_called()


if __name__ == "__main__":
    unittest.main()
