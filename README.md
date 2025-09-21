# BigSignal: 암호화폐 자동매매 시그널 성과 분석 플랫폼

BigSignal은 텔레그램으로 수신되는 암호화폐 자동매매 시그널을 실시간으로 수집하고 분석하여, 다양한 포트폴리오 구성에 따른 투자 성과를 시뮬레이션하고 시각화하는 데이터 분석 플랫폼입니다.

## 📊 현재 운영 현황 (2025-09-21 기준)

- **수집된 거래 데이터**: 814개 BigSignal 거래
- **분석 기간**: 2025-07-23 ~ 2025-09-20 (약 2개월)
- **포트폴리오 전략**: 7가지 활성화
- **최고 성과**: DOGE_Only (4.68%), BTC_Only (3.61%)
- **자산별 거래 분포**: DOGE 386개, BTC 220개, USDC 135개, USDT 73개

## 목차

- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [시스템 아키텍처](#시스템-아키텍처)
- [설치 및 실행](#설치-및-실행)
- [최근 변경사항 및 중요 안내](#최근-변경사항-및-중요-안내-핫픽스)
- [성과 분석 및 시각화](#성과-분석-및-시각화)
- [배포 가이드](#배포-가이드)
- [프로젝트 구조](#프로젝트-구조)
- [API 엔드포인트](#api-엔드포인트)
- [데이터 모델](#데이터-모델)
- [시스템 아키텍처 상세](#bigsignal-프로젝트-아키텍처)

## 주요 기능

1. **실시간 시그널 수집**
   - 텔레그램 채널에서 매수/매도 시그널을 실시간으로 수집
   - 자동화된 메시지 파싱 및 구조화된 데이터 저장
   - HOLD, BUY, SELL 시그널 자동 분류 및 처리

2. **다중 포트폴리오 시뮬레이션**
   - 7가지 포트폴리오 구성 (단일/복합 자산)
   - BTC, USDT, DOGE 기반 조합 전략 분석
   - 초기 투자금 100만원 기준 가상 투자 시뮬레이션

3. **실시간 성과 분석 & 시각화**
   - 포트폴리오별 수익률 비교 차트
   - 시간별 가치 변화 추이 분석
   - 자산별 거래 분포 및 월별 수익률 분석
   - 리스크-수익률 산점도 및 Buy & Hold 비교

4. **과거 데이터 일괄 수집**
   - 텔레그램 채널의 모든 과거 메시지 수집 기능
   - 비동기 처리를 통한 대용량 데이터 수집
   - 중복 제거 및 데이터 무결성 검증

5. **데이터 기반 투명성**
   - 모든 거래 기록의 완전한 투명성
   - 실시간 포트폴리오 가치 평가
   - 정확한 수익률 계산 공식 적용

## 기술 스택

- **백엔드**: Django 5.2.5, Django REST Framework, Pandas, NumPy, Matplotlib
- **메시지 수집**: Python Telethon, 정규표현식 파싱, 비동기 처리
- **데이터베이스**: SQLite (개발), PostgreSQL (프로덕션)
- **시각화**: Matplotlib, Seaborn, Chart.js
- **프론트엔드**: React 18, Chart.js, Material-UI (예정)
- **배포**: 
  - Django Backend: AWS EC2 / 로컬 서버
  - React Frontend: Firebase Hosting (예정)
- **인프라**: AWS RDS (PostgreSQL), AWS S3 (선택사항)

## 시스템 아키텍처

```
텔레그램 채널 → 메시지 수집기 → PostgreSQL → Django API → React 차트
     ↓              ↓              ↓          ↓           ↓
  시그널 메시지   → 파싱/필터링    → 거래 기록   → 분석 엔진   → 시각화
                                     ↓
                              포트폴리오 시뮬레이션
                                     ↓
                              성과 분석 & 리포트
```

## 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone https://github.com/your-username/bigsignal.git
cd bigsignal
```

### 2. 백엔드 설정 (Django)
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일에서 다음 설정:
# DATABASE_URL=postgresql://user:password@localhost:5432/bigsignal
# TELEGRAM_API_ID=your_api_id
# TELEGRAM_API_HASH=your_api_hash  
# TELEGRAM_PHONE=your_phone_number
# TELEGRAM_CHANNEL_ID=-1001234567890  # 또는 @channel_username
# SECRET_KEY=your_django_secret_key
```

### 4. 데이터베이스 설정
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Django 서버 실행
```bash
python manage.py runserver
```

### 6. 텔레그램 수집기 실행
```bash
# 과거 메시지 수집 (최근 90일)
python scripts/collect_history.py 90

# 실시간 수집
python scripts/telegram_collector.py
```

### 7. 성과 분석 차트 생성
```bash
# 필요한 패키지 설치
pip install matplotlib pandas seaborn numpy

# 차트 생성
python analysis/chart_generator.py
```

### 8. 데이터 검증 및 관리
```bash
# 데이터 무결성 검사
python scripts/validate_data.py

# 간단한 현황 리포트
python scripts/print_portfolio_report.py
```

## 최근 변경사항 및 중요 안내 (핫픽스)

최근 개발 과정에서 반영된 중요한 변경사항들입니다:

### 1. 메시지 파서(message_parser.py) 개선
- **문제**: 이모지 처리(📈/📉)로 정규표현식 파싱 실패
- **해결**: 이모지를 비캡처 그룹으로 변경하여 파싱 안정성 향상
- **파일**: `backend/scripts/message_parser.py`

### 2. 과거 메시지 수집기 채널 식별 강화
- **문제**: `.env`의 `TELEGRAM_CHANNEL_ID`가 Telethon에서 인식되지 않는 문제
- **해결**: 채널 식별 로직 다단계 강화 (숫자 id → username → dialogs 순회)
- **파일**: `backend/scripts/collect_history.py`
- **권장**: 채널 ID는 `-1001234567890` 형태 또는 정확한 `@username` 사용

### 3. Django ORM 비동기 호환성 개선
- **문제**: `sync_to_async` 데코레이터 누락으로 async 환경에서 DB 저장 실패
- **해결**: 모든 비동기 스크립트에 Django ORM 호환성 추가
- **영향**: 과거 메시지 수집 시 정상적인 DB 저장 가능

### 4. 포트폴리오 모델 호환성 프로퍼티 추가
- **변경**: 기존 코드 호환성을 위한 alias 프로퍼티 추가
- **추가된 프로퍼티**: `profit_loss_percentage`, `current_value_float`
- **파일**: `backend/portfolios/models.py`

### 5. 유틸리티 스크립트 추가
- **list_telegram_dialogs.py**: 올바른 채널 식별자 찾기
- **print_portfolio_report.py**: 빠른 현황 리포트 생성
- **validate_data.py**: 데이터 무결성 검사 및 수정

### 디버깅 팁
Telethon 수집 시 `Could not find the input entity` 오류 해결:
1. `.env`의 `TELEGRAM_CHANNEL_ID` 값 확인
2. `list_telegram_dialogs.py` 실행 후 정확한 식별자 사용
3. private 채널의 경우 bot/session 계정이 채널 멤버인지 확인

## 성과 분석 및 시각화

### 현재 제공되는 분석 차트

1. **포트폴리오 성과 비교 차트** (`portfolio_performance.png`)
   - 7가지 전략의 수익률 막대 차트
   - 색상별 포트폴리오 구분

2. **시간별 포트폴리오 가치 변화** (`portfolio_timeline.png`)
   - 절대 가치 변화 추이
   - 수익률 변화 추이

3. **자산별 거래 분포** (`asset_distribution.png`)
   - 파이 차트: 자산별 거래 비율
   - 막대 차트: 자산별 거래 수

4. **월별 수익률 비교** (`monthly_returns.png`)
   - 포트폴리오별 월간 성과 비교

5. **리스크-수익률 산점도** (`risk_return_scatter.png`)
   - 변동성 대비 수익률 분석

6. **Buy & Hold 비교** (`buy_hold_comparison.png`)
   - 단순 보유 전략 대비 BigSignal 성과

### API 엔드포인트 (분석용)

```
GET /api/analysis/performance/           # 포트폴리오 성과 데이터
GET /api/analysis/timeline/              # 시간별 가치 변화
GET /api/analysis/trading-stats/         # 거래 통계
GET /api/analysis/risk-metrics/          # 리스크 메트릭
GET /api/analysis/buy-hold-comparison/   # Buy & Hold 비교
GET /api/analysis/dashboard-summary/     # 대시보드 요약
GET /api/analysis/charts/<chart_name>/   # 차트 이미지
POST /api/analysis/regenerate-charts/    # 차트 재생성
```

## 배포 가이드

### 로컬 서버 운영 (권장)

**용량 분석**:
- 연간 예상 데이터: 3,200개 거래 (약 70MB)
- 로컬 서버로 충분: 8GB RAM, 256GB SSD

**장점**:
- 비용 효율성 (클라우드 서버 불필요)
- 데이터 보안 (내부 네트워크)
- 커스터마이징 용이

### AWS EC2 Django 배포 (선택사항)

1. **EC2 인스턴스 생성**
```bash
# Ubuntu 20.04 LTS 권장
# t3.micro 이상 인스턴스 타입
```

2. **서버 환경 설정**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql-client
```

3. **프로젝트 배포**
```bash
git clone https://github.com/your-username/bigsignal.git
cd bigsignal/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

4. **Gunicorn 설정**
```bash
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

5. **Nginx 설정**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/bigsignal/backend/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/bigsignal/backend/media/;
    }
}
```

### React 프론트엔드 배포 (개발 예정)

1. **빌드 생성**
```bash
cd frontend
npm run build
```

2. **Firebase 배포**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

## 프로젝트 구조

```
📦BIGSIGNAL
 ┣ 📂backend
 ┃ ┣ 📂config
 ┃ ┃ ┣ 📜settings.py
 ┃ ┃ ┣ 📜urls.py
 ┃ ┃ ┗ 📜wsgi.py
 ┃ ┣ 📂trades
 ┃ ┃ ┣ 📜models.py
 ┃ ┃ ┣ 📜views.py
 ┃ ┃ ┣ 📜serializers.py
 ┃ ┃ ┗ 📜urls.py
 ┃ ┣ 📂portfolios
 ┃ ┃ ┣ 📜models.py
 ┃ ┃ ┣ 📜views.py
 ┃ ┃ ┣ 📜serializers.py
 ┃ ┃ ┗ 📜urls.py
 ┃ ┣ 📂analysis
 ┃ ┃ ┣ 📜portfolio_engine.py
 ┃ ┃ ┣ 📜chart_generator.py      # 🆕
 ┃ ┃ ┣ 📜views.py               # 🆕
 ┃ ┃ ┗ 📜urls.py                # 🆕
 ┃ ┣ 📂scripts
 ┃ ┃ ┣ 📜telegram_collector.py
 ┃ ┃ ┣ 📜collect_history.py     # 🔄 업데이트
 ┃ ┃ ┣ 📜message_parser.py      # 🔄 업데이트
 ┃ ┃ ┣ 📜list_telegram_dialogs.py    # 🆕
 ┃ ┃ ┣ 📜print_portfolio_report.py   # 🆕
 ┃ ┃ ┗ 📜validate_data.py            # 🆕
 ┃ ┣ 📂media/charts              # 🆕 생성된 차트 저장
 ┃ ┣ 📜manage.py
 ┃ ┗ 📜requirements.txt
 ┣ 📂frontend (개발 예정)
 ┃ ┣ 📂src
 ┃ ┃ ┣ 📂components
 ┃ ┃ ┗ 📂services
 ┃ ┗ 📜package.json
 ┣ 📜.env.example
 ┗ 📜README.md
```

## API 엔드포인트

### 거래 관련
- `GET /api/trades/` - 전체 거래 기록
- `GET /api/trades/latest/` - 최근 거래 기록
- `POST /api/trades/` - 새 거래 기록 추가

### 포트폴리오 관련
- `GET /api/portfolios/` - 전체 포트폴리오 목록
- `GET /api/portfolios/{id}/performance/` - 포트폴리오 성과 데이터
- `GET /api/portfolios/comparison/` - Buy & Hold 비교 데이터

### 분석 관련
- `GET /api/analysis/performance/` - 포트폴리오 성과 비교
- `GET /api/analysis/timeline/` - 시간별 가치 변화
- `GET /api/analysis/trading-stats/` - 거래 통계
- `GET /api/analysis/risk-metrics/` - 리스크 메트릭
- `GET /api/analysis/buy-hold-comparison/` - Buy & Hold 비교
- `GET /api/analysis/`dashboard-summary/` - 대시보드 요약
- `GET /api/analysis/charts/{chart_name}/` - 차트 이미지
- `POST /api/analysis/regenerate-charts/` - 차트 재생성