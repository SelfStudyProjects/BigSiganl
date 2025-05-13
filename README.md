# BigSignal Project

BigSignal은 암호화폐 시장 분석 및 신호 제공 서비스입니다.

## 프로젝트 구조

```
BigSignal/
├── client/                 # React 프론트엔드
│   ├── package.json
│   └── .env
├── server/                # Node.js 백엔드
│   ├── package.json
│   └── .env
├── analysis/             # 파이썬 분석 코드
│   ├── requirements.txt
│   └── .env
├── .gitignore
└── README.md
```

## 시스템 요구사항

- Node.js >= 16.x
- Python >= 3.8
- npm >= 8.x
- pip >= 21.x

## 시작하기

### 환경 설정
1. Firebase 프로젝트 설정
   - Firebase Console에서 새 프로젝트 생성
   - Firebase CLI 설치: `npm install -g firebase-tools`
   - 프로젝트 초기화: `firebase init`

2. 환경 변수 설정
   - 각 디렉토리의 `.env.example` 파일을 `.env`로 복사
   - 필요한 환경 변수 값 설정

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
- 데이터베이스: Firebase Realtime Database
- 데이터 분석: Python (pandas, matplotlib, seaborn)
- 배포: Firebase Hosting
- 버전 관리: Git
- 테스트: Jest (프론트엔드), Mocha (백엔드), Pytest (파이썬)

## 개발 가이드라인
- 코드 스타일: ESLint (프론트엔드/백엔드), Black (파이썬)
- 커밋 메시지: Conventional Commits
- 브랜치 전략: Git Flow

## API 문서
- Swagger UI: `http://localhost:3000/api-docs`
- Postman Collection: `docs/postman_collection.json`

## 라이선스
MIT License

## 프로젝트 견적

```mermaid
graph TD
    A[텔레그램 메시지 로그] --> B{데이터 수집/가공\\(Node.js 함수)}
    C[빗썸 API/데이터] --> B
    B --> D[수익률 계산 및 DB 저장\\(Firebase Database)]
    D --> E[시각화 데이터 준비\\(Node.js 함수)]
    E --> F[시각화 그래프 생성\\(Python 스크립트)]
    F --> G[시각화 자료 제공\\(Firebase Storage or direct)]
    G --> H[프론트엔드\\(React JS)]
    H --> I[사용자 (X 홍보 대상)]
    J[관리자 (내부 확인용)] --> H

    classDef default fill:#f9f,stroke:#333,stroke-width:2px;
    classDef data fill:#ccf,stroke:#333,stroke-width:2px;
    classDef code fill:#cfc,stroke:#333,stroke-width:2px;
    class A,C data;
    class B,D,E,F code;
    class G data;
    class H code;
    class I,J data;
```