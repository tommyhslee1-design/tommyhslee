from dataclasses import dataclass
from typing import Sequence

DEFAULT_PERIOD = "1mo"
DEFAULT_INTERVAL = "1d"

VALID_PERIODS = {
    "1d",
    "5d",
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y",
    "10y",
    "ytd",
    "max",
}
VALID_INTERVALS = {
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
}

INTRADAY_INTERVALS = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"}
INTRADAY_ALLOWED_PERIODS = {"1d", "5d", "1mo"}


@dataclass(frozen=True)
class ChartRequest:
    ticker: str
    period: str
    interval: str


def _join_sorted(values: Sequence[str]) -> str:
    return ", ".join(sorted(values))


def parse_chart_args(args: list[str]) -> ChartRequest:
    if not args:
        raise ValueError("티커를 입력해주세요. 예: /chart AAPL")

    ticker = args[0].upper().strip()
    period = args[1].strip() if len(args) >= 2 else DEFAULT_PERIOD
    interval = args[2].strip() if len(args) >= 3 else DEFAULT_INTERVAL

    if period not in VALID_PERIODS:
        raise ValueError(
            f"지원하지 않는 period입니다: {period}\n"
            f"지원 목록: {_join_sorted(VALID_PERIODS)}"
        )

    if interval not in VALID_INTERVALS:
        raise ValueError(
            f"지원하지 않는 interval입니다: {interval}\n"
            f"지원 목록: {_join_sorted(VALID_INTERVALS)}"
        )

    if interval in INTRADAY_INTERVALS and period not in INTRADAY_ALLOWED_PERIODS:
        raise ValueError(
            "분봉/시간봉 interval(1m~1h)은 period를 1d, 5d, 1mo 중 하나로 지정해주세요.\n"
            "예: /chart NVDA 5d 15m"
        )

    return ChartRequest(ticker=ticker, period=period, interval=interval)
