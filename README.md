# BigSignal Project

BigSignal은 암호화폐 시장 분석 및 신호 제공 서비스입니다.

## 프로젝트 구조

```
BigSignal/
├── client/                 # React 프론트엔드
├── server/                # Node.js 백엔드
└── analysis/             # 파이썬 분석 코드
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
