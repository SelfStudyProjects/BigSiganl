# BigSignal: 암호화폐 자동매매 시그널 성과 분석 플랫폼

BigSignal은 텔레그램으로 수신되는 암호화폐 자동매매 시그널을 실시간으로 수집하고 분석하여, 다양한 포트폴리오 구성에 따른 투자 성과를 시뮬레이션하고 시각화하는 데이터 분석 플랫폼입니다.

## 목차

- [BigSignal - 암호화폐 시그널 성과 분석 플랫폼](#bigsignal---암호화폐-시그널-성과-분석-플랫폼)
  - [주요 기능](#주요-기능)
  - [기술 스택](#기술-스택)
  - [시스템 아키텍처](#시스템-아키텍처)
  - [설치 및 실행](#설치-및-실행)
  - [배포 가이드](#배포-가이드)
  - [프로젝트 구조](#프로젝트-구조)
  - [API 엔드포인트](#api-엔드포인트)
  - [데이터 모델](#데이터-모델)
- [BigSignal 프로젝트 아키텍처](#bigsignal-프로젝트-아키텍처)
  - [1. 시스템 구성요소](#1-시스템-구성요소)
    - [1.1 텔레그램 수집기](#11-텔레그램-수집기)
    - [1.2 포트폴리오 분석 엔진](#12-포트폴리오-분석-엔진)
    - [1.3 Django 백엔드](#13-django-백엔드)
    - [1.4 React 프론트엔드](#14-react-프론트엔드)
  - [2. 데이터 흐름](#2-데이터-흐름)
  - [성능 및 모니터링](#성능-및-모니터링)
  - [라이선스](#라이선스)

# BigSignal - 암호화폐 시그널 성과 분석 플랫폼

BigSignal은 텔레그램 채널을 통해 제공되는 암호화폐 자동매매 시그널의 실제 성과를 객관적으로 분석하고 시각화하여, 투자자들이 시그널의 효과를 데이터 기반으로 판단할 수 있도록 돕는 플랫폼입니다.

## 주요 기능

1. **실시간 시그널 수집**
   - 텔레그램 채널에서 매수/매도 시그널을 실시간으로 수집
   - 자동화된 메시지 파싱 및 구조화된 데이터 저장
   - HOLD, BUY, SELL 시그널 자동 분류 및 처리

2. **다중 포트폴리오 시뮬레이션**
   - 7가지 포트폴리오 구성 (단일/복합 자산)
   - BTC, USDT, DOGE 기반 조합 전략 분석
   - 초기 투자금 100만원 기준 가상 투자 시뮬레이션

3. **Buy & Hold 전략 비교**
   - 시그널 기반 투자 vs 단순 보유 전략 비교
   - 각 자산별 100% 보유 시나리오 분석
   - 상대적 성과 지표 제공

4. **실시간 성과 시각화**
   - Chart.js 기반 인터랙티브 차트
   - 포트폴리오별 수익률 추이 비교
   - 사용자 선택형 차트 업데이트 기능

5. **데이터 기반 투명성**
   - 모든 거래 기록의 완전한 투명성
   - 실시간 포트폴리오 가치 평가
   - 정확한 수익률 계산 공식 적용

## 기술 스택

- **백엔드**: Django, Django REST Framework, Pandas, NumPy
- **프론트엔드**: React, Chart.js, Node.js
- **데이터베이스**: PostgreSQL (AWS RDS)
- **메시지 수집**: Python Telethon, 정규표현식 파싱
- **배포**: 
  - Django Backend: AWS EC2
  - React Frontend: Firebase Hosting
- **인프라**: AWS RDS (PostgreSQL), AWS S3 (선택사항)

## 시스템 아키텍처

```
텔레그램 채널 → 메시지 수집기 → PostgreSQL → Django API → React 차트
     ↓              ↓              ↓          ↓           ↓
  시그널 메시지   → 파싱/필터링    → 거래 기록   → 분석 엔진   → 시각화
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
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
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

### 6. 프론트엔드 설정 (React)
```bash
cd frontend
npm install
```

### 7. React 개발 서버 실행
```bash
npm start
```

### 8. 텔레그램 수집기 실행
```bash
cd scripts
python telegram_collector.py
```

## 최근 변경사항 및 중요 안내 (핫픽스)

아래는 최근 개발 진행 중에 반영된 변경사항과 운영 시 주의할 점입니다. 개발/운영 환경에서 바로 적용 가능하도록 사용법과 원인, 해결 방법을 함께 정리합니다.

1) 메시지 파서(message_parser.py) 개선
- 문제: 일부 텔레그램 메시지의 이모지 처리(📈/📉)로 정규표현식이 잘못 캡처되어 파싱 실패가 발생했습니다.
- 해결: 이모지 부분을 비캡처 그룹으로 변경하여 캡처 그룹이 항상 action/asset을 올바르게 반환하도록 수정했습니다.
- 스크립트 경로: `backend/scripts/message_parser.py`

2) 스크립트 독립 실행성 개선
- 문제: 테스트 스크립트가 `django.utils.timezone.now()`를 사용해 Django 설정이 필요했습니다(ImproperlyConfigured 오류).
- 해결: 테스트용 스크립트에서 `datetime.now()`로 대체하여 단독 실행이 가능하도록 수정했습니다.
- 테스트 스크립트: `backend/scripts/message_parser.py` (로컬에서 바로 실행 가능)

3) 과거 메시지 수집기(collect_history.py)에서 채널 식별 문제 해결
- 문제: `.env`의 `TELEGRAM_CHANNEL_ID` 값이 Telethon의 `get_entity()`에서 바로 해석되지 않아 `Could not find the input entity for PeerUser(...)` 오류 발생.
- 해결: 채널 식별 로직을 강화했습니다. (숫자 id 시도 → 문자열(username) 시도 → dialogs 순회 탐색)
- 스크립트 경로: `backend/scripts/collect_history.py`
- 권장: `.env`에 채널 식별자는 가능하면 `-1001234567890` 형태(채널 id) 혹은 정확한 username(`@BigSignalChannel`)을 사용하세요.

4) 대화 목록 도움 스크립트 추가
- 목적: 올바른 채널 식별자(id 또는 username)를 찾기 위한 유틸
- 스크립트: `backend/scripts/list_telegram_dialogs.py`
- 사용법:
    ```powershell
    cd c:\BIGSIGNAL\backend
    .\.venv\Scripts\python.exe scripts\list_telegram_dialogs.py
    ```
    출력에서 원하는 채널의 `id`, `username`, `title`을 복사해 `.env`의 `TELEGRAM_CHANNEL_ID`에 넣으세요.

5) 포트폴리오 모델 호환성 (필드 alias)
- 변경: 기존 코드가 기대하던 `profit_loss_percentage` 같은 이름이 모델에 없어서 오류가 발생하던 것을 호환성 프로퍼티로 보완했습니다.
    - 모델 필드(데이터베이스)는 `pnl_percentage`, `current_value` 등 DecimalField로 유지합니다.
    - 편의용 프로퍼티: `profit_loss_percentage`(float 반환), `current_value_float`(float 반환)을 추가했습니다.
- 참고: 모델 파일 경로 `backend/portfolios/models.py`

6) 리포트 편의 스크립트 추가
- 목적: 인터랙티브 셸에서 들여쓰기나 복사/붙여넣기 오류 없이 동일한 정보를 출력하기 위한 스크립트입니다.
- 스크립트: `backend/scripts/print_portfolio_report.py`
- 사용법:
    ```powershell
    cd c:\BIGSIGNAL\backend
    .\.venv\Scripts\python.exe scripts\print_portfolio_report.py
    ```
    출력: 총 거래 수, 첫/마지막 거래 시각, 포트폴리오별 현황, 자산별 거래 수

## 디버깅 팁
- Telethon으로 수집 시 `Could not find the input entity` 오류가 나면:
    1. `.env`의 `TELEGRAM_CHANNEL_ID` 값을 확인 (username인지 numeric id인지)
    2. `list_telegram_dialogs.py` 실행 후 정확한 식별자 사용
    3. private 채널의 경우 bot/session 계정이 채널의 멤버여야 함

## 변경된 파일 목록 (요약)
- `backend/scripts/message_parser.py`  — 파서 안정화 (emoji 정규식, timezone 제거)
- `backend/scripts/collect_history.py` — 채널 탐색 로직 보강 (id/username/iter_dialogs)
- `backend/scripts/list_telegram_dialogs.py` — 대화 목록 유틸(새 파일)
- `backend/scripts/print_portfolio_report.py` — 리포트 유틸(새 파일)
- `backend/portfolios/models.py` — 호환성 프로퍼티 추가 (`profit_loss_percentage`, `current_value_float`)

---

위 변경사항은 개발 편의성과 안정성 향상을 위한 핫픽스입니다. 원하면 이 내용을 README 상단에 더 눈에 띄게 노출시키거나, 별도의 CHANGELOG.md로 관리하도록 정리해드릴게요.

## 배포 가이드

### AWS EC2 Django 배포

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
python3 -m venv venv
source venv/bin/activate
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
}
```

### Firebase React 배포

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

### AWS RDS PostgreSQL 설정

1. **RDS 인스턴스 생성**
   - PostgreSQL 엔진 선택
   - db.t3.micro (프리티어)
   - 퍼블릭 액세스 허용

2. **보안 그룹 설정**
   - 포트 5432 오픈
   - EC2에서 접근 가능하도록 설정

## 프로젝트 구조

```
📦bigsignal
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
 ┃ ┃ ┣ 📜views.py
 ┃ ┃ ┗ 📜urls.py
 ┃ ┣ 📜manage.py
 ┃ ┗ 📜requirements.txt
 ┣ 📂frontend
 ┃ ┣ 📂src
 ┃ ┃ ┣ 📂components
 ┃ ┃ ┃ ┣ 📜Dashboard.jsx
 ┃ ┃ ┃ ┣ 📜PortfolioChart.jsx
 ┃ ┃ ┃ ┣ 📜PortfolioSelector.jsx
 ┃ ┃ ┃ ┗ 📜ComparisonTable.jsx
 ┃ ┃ ┣ 📂services
 ┃ ┃ ┃ ┗ 📜api.js
 ┃ ┃ ┣ 📜App.js
 ┃ ┃ ┗ 📜index.js
 ┃ ┣ 📜package.json
 ┃ ┗ 📜firebase.json
 ┣ 📂scripts
 ┃ ┣ 📜telegram_collector.py
 ┃ ┣ 📜portfolio_analyzer.py
 ┃ ┗ 📜message_parser.py
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
- `GET /api/analysis/summary/` - 전체 성과 요약
- `GET /api/analysis/chart-data/` - 차트용 시계열 데이터

## 데이터 모델

### Trade 모델
```python
class Trade(models.Model):
    timestamp = models.DateTimeField()
    asset = models.CharField(max_length=10)  # BTC, USDT, DOGE
    action = models.CharField(max_length=4, choices=[
        ('BUY', 'Buy'),
        ('SELL', 'Sell')
    ])
    price = models.DecimalField(max_digits=15, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    base_currency = models.CharField(max_length=3, default='KRW')
    created_at = models.DateTimeField(auto_now_add=True)
```

### Portfolio 모델
```python
class Portfolio(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    assets = models.JSONField()  # ['BTC', 'USDT'] 등
    initial_budget = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    pnl_absolute = models.DecimalField(max_digits=15, decimal_places=2)
    pnl_percentage = models.DecimalField(max_digits=8, decimal_places=4)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### PortfolioSnapshot 모델
```python
class PortfolioSnapshot(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    portfolio_value = models.DecimalField(max_digits=15, decimal_places=2)
    pnl_percentage = models.DecimalField(max_digits=8, decimal_places=4)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2)
    holdings = models.JSONField()  # {'BTC': 0.1, 'USDT': 1000}
```

# BigSignal 프로젝트 아키텍처

## 1. 시스템 구성요소

### 1.1 텔레그램 수집기

**기능**:
- 텔레그램 API를 통한 실시간 메시지 모니터링
- BigSignal 채널 메시지 자동 파싱
- BUY/SELL/HOLD 시그널 분류 및 필터링

**구현** (`scripts/telegram_collector.py`):
```python
class BigSignalCollector:
    def __init__(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.client = TelegramClient('bigsignal', self.api_id, self.api_hash)
    
    async def handle_message(self, event):
        message = event.message.message
        parsed_trade = self.parser.parse_message(message, datetime.now())
        if parsed_trade:
            await self.save_to_database(parsed_trade)
```

### 1.2 포트폴리오 분석 엔진

**핵심 로직** (`analysis/portfolio_engine.py`):
```python
class PortfolioEngine:
    def __init__(self, initial_budget=1000000):
        self.initial_budget = initial_budget
        self.portfolios = self.initialize_portfolios()
    
    def simulate_trade(self, portfolio, trade):
        if trade.action == 'BUY':
            amount = portfolio.cash * (trade.percentage / 100)
            quantity = amount / trade.price
            portfolio.add_asset(trade.asset, quantity)
            portfolio.cash -= amount
        elif trade.action == 'SELL':
            current_holding = portfolio.get_asset(trade.asset)
            sell_quantity = current_holding * (trade.percentage / 100)
            sell_amount = sell_quantity * trade.price
            portfolio.remove_asset(trade.asset, sell_quantity)
            portfolio.cash += sell_amount
```

**포트폴리오 구성**:
1. `BTC_Only` - BTC 단일 자산
2. `USDT_Only` - USDT 단일 자산  
3. `DOGE_Only` - DOGE 단일 자산
4. `BTC_USDT` - BTC + USDT 조합
5. `BTC_DOGE` - BTC + DOGE 조합
6. `USDT_DOGE` - USDT + DOGE 조합
7. `BTC_USDT_DOGE` - 3자산 모두 조합

### 1.3 Django 백엔드

**주요 앱 구조**:
- `trades`: 거래 데이터 관리 및 API
- `portfolios`: 포트폴리오 성과 관리
- `analysis`: 실시간 분석 및 계산 엔진

**핵심 API 뷰** (`portfolios/views.py`):
```python
class PortfolioPerformanceView(APIView):
    def get(self, request, portfolio_id):
        portfolio = Portfolio.objects.get(id=portfolio_id)
        trades = Trade.objects.all().order_by('timestamp')
        
        engine = PortfolioEngine()
        performance_data = engine.calculate_performance(portfolio, trades)
        
        return Response({
            'portfolio': PortfolioSerializer(portfolio).data,
            'performance': performance_data,
            'chart_data': self.format_chart_data(performance_data)
        })
```

### 1.4 React 프론트엔드

**핵심 컴포넌트**:

**Dashboard** (`components/Dashboard.jsx`):
```javascript
const Dashboard = () => {
    const [portfolios, setPortfolios] = useState([]);
    const [selectedPortfolios, setSelectedPortfolios] = useState([]);
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        fetchPortfolioData();
        const interval = setInterval(fetchPortfolioData, 30000);
        return () => clearInterval(interval);
    }, []);

    const fetchPortfolioData = async () => {
        const response = await api.get('/analysis/summary/');
        setPortfolios(response.data.portfolios);
        updateChartData(response.data);
    };

    return (
        <div className="dashboard">
            <PortfolioSelector 
                portfolios={portfolios}
                onSelectionChange={setSelectedPortfolios}
            />
            <PortfolioChart 
                data={chartData}
                selectedPortfolios={selectedPortfolios}
            />
            <ComparisonTable portfolios={portfolios} />
        </div>
    );
};
```

**PortfolioChart** (`components/PortfolioChart.jsx`):
```javascript
const PortfolioChart = ({ data, selectedPortfolios }) => {
    const chartRef = useRef(null);

    useEffect(() => {
        if (chartRef.current) {
            const ctx = chartRef.current.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: formatChartData(data, selectedPortfolios),
                options: {
                    responsive: true,
                    scales: {
                        x: { type: 'time' },
                        y: { 
                            title: { display: true, text: '수익률 (%)' }
                        }
                    }
                }
            });
        }
    }, [data, selectedPortfolios]);

    return <canvas ref={chartRef} />;
};
```

## 2. 데이터 흐름

```
텔레그램 메시지 → 파싱 → PostgreSQL → Django ORM → 분석 엔진 → API 응답 → React 차트
      ↓             ↓         ↓            ↓           ↓            ↓           ↓
  실시간 수신    → 구조화   → 영구 저장   → 객체화   → 성과 계산  → JSON     → 시각화
```

**실시간 처리 주기**:
- 텔레그램 수집: 실시간 (메시지 발생 즉시)
- 포트폴리오 분석: API 요청 시 실시간 계산
- 웹 차트 업데이트: 30초 주기 자동 갱신

**데이터 저장 전략**:
- 거래 데이터: PostgreSQL에 영구 저장
- 포트폴리오 스냅샷: 성능 최적화를 위해 주기적 저장
- 실시간 계산: 매 API 호출 시 최신 데이터로 계산

## 성능 및 모니터링

**성능 최적화**:
- PostgreSQL 인덱스: `timestamp`, `asset`, `action` 컬럼
- Django 쿼리 최적화: `select_related()`, `prefetch_related()`
- React 상태 관리: 불필요한 리렌더링 방지

**모니터링**:
- Django 로깅: 거래 수집 및 계산 오류 추적
- AWS CloudWatch: EC2 인스턴스 모니터링
- 프론트엔드: API 응답 시간 추적

## 라이선스

MIT License

---

BigSignal 프로젝트는 암호화폐 시그널의 투명한 성과 분석을 통해 투자자들의 현명한 의사결정을 지원합니다. 모든 기술 스택이 검증된 기존 기술을 활용하여 빠른 개발과 안정적인 운영을 보장합니다.