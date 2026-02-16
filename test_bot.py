import unittest

from chart_config import ChartRequest, parse_chart_args


class ParseChartArgsTests(unittest.TestCase):
    def test_default_values(self):
        request = parse_chart_args(["aapl"])
        self.assertEqual(request, ChartRequest(ticker="AAPL", period="1mo", interval="1d"))

    def test_custom_values(self):
        request = parse_chart_args(["nvda", "5d", "15m"])
        self.assertEqual(request, ChartRequest(ticker="NVDA", period="5d", interval="15m"))

    def test_invalid_period(self):
        with self.assertRaises(ValueError):
            parse_chart_args(["AAPL", "7d", "1d"])

    def test_invalid_interval(self):
        with self.assertRaises(ValueError):
            parse_chart_args(["AAPL", "1mo", "7m"])

    def test_intraday_period_restriction(self):
        with self.assertRaises(ValueError):
            parse_chart_args(["AAPL", "1y", "15m"])


if __name__ == "__main__":
    unittest.main()
