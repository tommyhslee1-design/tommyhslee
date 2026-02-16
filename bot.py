import asyncio
import logging
import os
import tempfile

import mplfinance as mpf
import yfinance as yf
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from chart_config import ChartRequest, parse_chart_args

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

HELP_TEXT = (
    "사용법:\n"
    "/chart <TICKER> [PERIOD] [INTERVAL]\n\n"
    "예시:\n"
    "/chart AAPL\n"
    "/chart TSLA 3mo 1d\n"
    "/chart NVDA 5d 15m\n\n"
    "티커 예시: AAPL, TSLA, 005930.KS\n"
    "지원 기간: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max\n"
    "지원 간격: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo"
)


def build_chart_image(chart_request: ChartRequest) -> str:
    df = yf.download(
        chart_request.ticker,
        period=chart_request.period,
        interval=chart_request.interval,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(
            "데이터가 없습니다. "
            f"ticker={chart_request.ticker}, "
            f"period={chart_request.period}, "
            f"interval={chart_request.interval}"
        )

    df.index.name = "Date"

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_file.close()

    title = f"{chart_request.ticker} ({chart_request.period}, {chart_request.interval})"
    mpf.plot(
        df,
        type="candle",
        style="charles",
        volume=True,
        title=title,
        mav=(5, 20),
        savefig=temp_file.name,
        tight_layout=True,
    )

    return temp_file.name


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text(
        "안녕하세요! 주식 차트 봇입니다.\n"
        "`/chart AAPL` 처럼 입력하면 차트를 보내드려요.",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text(HELP_TEXT)


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    image_path = ""
    try:
        request = parse_chart_args(context.args)

        await update.message.reply_text(
            "차트를 생성 중입니다...\n"
            f"Ticker: {request.ticker}\n"
            f"Period: {request.period}\n"
            f"Interval: {request.interval}"
        )

        image_path = await asyncio.to_thread(build_chart_image, request)

        with open(image_path, "rb") as chart_file:
            await update.message.reply_photo(
                photo=chart_file,
                caption=(
                    f"{request.ticker} 차트\n"
                    f"period={request.period}, interval={request.interval}"
                ),
            )
    except ValueError as exc:
        await update.message.reply_text(f"입력 오류: {exc}")
    except Exception as exc:
        logger.exception("차트 생성 실패")
        await update.message.reply_text(
            "차트 생성에 실패했습니다. 잠시 후 다시 시도해주세요.\n"
            f"상세: {exc}"
        )
    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN 환경 변수가 필요합니다.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chart", chart))

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
