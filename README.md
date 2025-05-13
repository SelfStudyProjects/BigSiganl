# BigSignal Project

BigSignal은 암호화폐 시장 분석 및 신호 제공 서비스입니다.

## 프로젝트 구조

```
BigSignal/
├── client/                 # React 프론트엔드
├── server/                # Node.js 백엔드
└── analysis/             # 파이썬 분석 코드
```

## 프로젝트 견적

```mermaid
graph TD
    A[텔레그램 메시지 로그] --> B{데이터 수집/가공\\(Node.js 함수)};
    C[빗썸 API/데이터] --> B;
    B --> D[수익률 계산 및 DB 저장\\(Firebase Database)];
    D --> E[시각화 데이터 준비\\(Node.js 함수)];
    E --> F[시각화 그래프 생성\\(Python 스크립트)];
    F --> G[시각화 자료 제공\\(Firebase Storage or direct)];
    G --> H[프론트엔드\\(React JS)];
    H --> I[사용자 (X 홍보 대상)];
    J[관리자 (내부 확인용)] --> H; %% 관리자에서 프론트엔드로 연결 추가

    classDef default fill:#f9f,stroke:#333,stroke-width:2px;
    classDef data fill:#ccf,stroke:#333,stroke-width:2px;
    classDef code fill:#cfc,stroke:#333,stroke-width:2px;
    class A,C data;
    class B,D,E,F code;
    class G data;
    class H code;
    class I,J data;
```

## 시작하기

### 프론트엔드 (React)
```bash
cd client
npm install
npm start
```

### 백엔드 (Node.js)
```bash
cd server
npm install
npm run dev
```

### 데이터 분석 (Python)
```bash
cd analysis
pip install -r requirements.txt
jupyter notebook
```

## 기술 스택
- 프론트엔드: React.js
- 백엔드: Node.js, Firebase Cloud Functions
- 데이터 분석: Python (pandas, matplotlib, seaborn)
- 배포: Firebase Hosting
