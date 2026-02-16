# 텔레그램 연동 주식 차트 봇

텔레그램에서 종목 티커를 입력하면 캔들 차트를 이미지로 돌려주는 Python 봇 예제입니다.

## 구현 개요 ("이걸 어떻게 구현해?")
1. **텔레그램 봇 생성**: BotFather에서 토큰 발급
2. **명령어 파싱**: `/chart <티커> [기간] [간격]` 형태 파싱
3. **입력 검증**: 지원 기간/간격 검증 + 분봉 제한 검증
4. **시세 데이터 수집**: `yfinance`로 OHLCV 다운로드
5. **차트 렌더링**: `mplfinance`로 캔들+거래량 PNG 생성
6. **텔레그램 전송**: 생성한 PNG를 `reply_photo`로 전송
7. **정리**: 임시 파일 삭제, 실패 시 사용자 친화 오류 메시지 반환

## 기능
- `/chart AAPL` 입력 시 기본값(`1mo`, `1d`)으로 차트 전송
- 기간(`period`)과 간격(`interval`) 사용자 지정 가능
- 잘못된 파라미터에 대한 검증/오류 메시지 제공
- 차트 생성은 백그라운드 스레드에서 실행하여 봇 응답성 개선

## 사전 준비
1. [BotFather](https://t.me/BotFather)에서 텔레그램 봇 생성
2. 봇 토큰 발급
3. Python 3.10+ 설치

## 설치
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 환경 변수 설정
프로젝트 루트에 `.env` 파일 생성:

```env
TELEGRAM_BOT_TOKEN=여기에_봇_토큰
```

## 실행
```bash
python bot.py
```

## 명령어
- `/start`: 소개 메시지
- `/help`: 도움말
- `/chart <TICKER> [PERIOD] [INTERVAL]`
  - 예: `/chart AAPL`
  - 예: `/chart TSLA 3mo 1d`
  - 예: `/chart NVDA 5d 15m`

## 지원 파라미터
- `PERIOD`: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
- `INTERVAL`: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

### 제한 사항
- 분봉/시간봉(`1m`~`1h`)은 Yahoo Finance 정책상 `period`를 짧게 설정해야 합니다.
- 본 예제에서는 `1m`~`1h` 사용 시 `period`를 `1d`, `5d`, `1mo`로 제한합니다.

## 파일 구조
- `bot.py`: 텔레그램 핸들러 + 차트 생성 로직
- `requirements.txt`: 의존성
- `.env.example`: 환경 변수 예시
