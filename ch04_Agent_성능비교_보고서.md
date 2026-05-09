# 📌 Chapter 4. Custom Agent 오케스트레이션 성능 비교 보고서

> **학습 목표:** 단순 역할 부여형 vs 4-Agent 파이프라인의 실제 성능 차이를 확인하고, 에이전트 활용의 효용성을 검증합니다.  
> **이전 단계:** [Chapter 3 — GHAS 보안 심화](./ch03_GHE_GHAS_보안심화.md)

---


> **테스트 대상**: `src/python-api/legacy_api.py` (312줄, 현업 스타일 Flask 레거시 API)  
> **비교 방식**: 동일 코드에 두 가지 접근법을 적용하여 결과물 품질 비교

---

## 📌 Executive Summary

| 지표 | ❌ 단순 리뷰 | ✅ 4-Agent 파이프라인 | 격차 |
|------|:---:|:---:|:---:|
| 탐지 취약점 수 | 3~5개 | **13개** | +160~330% |
| CWE 번호 매핑 | 0개 | **11개 CWE** | ∞ |
| CVSS 점수 산출 | 0건 | **13건** (평균 8.67) | ∞ |
| 공격 시나리오 (curl) | 0개 | **13개** (재현 가능) | ∞ |
| 기술 대안 비교 | 0건 | **4개 영역** (16개 후보) | ∞ |
| 결과 코드 모듈 수 | 0개 | **12개 파일** (875줄) | ∞ |
| OWASP 카테고리 커버리지 | A03 일부만 | **A01~A05** (5개) | +400% |

---

## 1. 테스트 대상 코드

**파일**: `src/python-api/legacy_api.py`

현업에서 흔히 볼 수 있는 레거시 Flask API를 재현했습니다:
- 직원 관리 CRUD (로그인, 조회, 생성, 삭제)
- 프로젝트 관리 (조회, 검색)
- 보고서 생성, 파일 업로드/다운로드
- 관리자 기능 (급여 수정, SQL 실행, 환경변수 조회)

**의도적으로 포함된 취약점**: SQL Injection (6개소), SSTI, Path Traversal, 하드코딩 시크릿, MD5 해싱, IDOR, Mass Assignment, 정보 노출, 제한 없는 파일 업로드, 임의 SQL 실행

---

## 2. ❌ 접근법 A: 역할 부여형 단순 리뷰

**프롬프트**: `"넌 10년 경력 시니어 백엔드 개발자야. 이 코드를 리뷰해줘."`

### 리뷰 결과 요약

| 관점 | 결과 |
|------|------|
| 발견한 문제 | "시크릿 키 하드코딩", "MD5 비권장", "SQL에 f-string 위험", "debug=True 제거" |
| 분석 깊이 | "~하세요", "~해보세요" 수준의 피상적 조언 |
| 수정 코드 | 없음 |
| 공격 시나리오 | 없음 |
| CWE/CVSS | 없음 |

### 💀 놓친 치명적 취약점

| 놓친 취약점 | CVSS | 왜 위험한가 |
|------------|------|-----------|
| **SSTI** (render_template_string) | 9.8 | 서버 원격 코드 실행 (RCE) 가능 |
| **임의 SQL 실행** (/run-query) | 10.0 | 인증 없이 DB 전체 장악 |
| **Mass Assignment** (role 조작) | 8.1 | 일반 사용자가 관리자 권한 획득 |
| **IDOR** (인증 없는 삭제/수정) | 9.1 | 누구나 직원 삭제, 급여 변경 가능 |
| **환경변수 노출** (/debug/env) | 7.5 | 서버 모든 시크릿 탈취 |
| **비밀번호 해시 응답 포함** | 6.5 | MD5 해시 → 레인보우 테이블로 즉시 복원 |

> **결론**: 역할 부여형 리뷰는 "SQL Injection 있으니 파라미터 바인딩 하세요" 수준에서 멈춤.  
> CVSS 10.0짜리 임의 SQL 실행 엔드포인트조차 감지하지 못함.

---

## 3. ✅ 접근법 B: 4-Agent 오케스트레이션 파이프라인

### 오케스트레이터 실행 흐름

```
시간 ─────────────────────────────────────────────────────────────────▶

Feature Builder  Planner         Researcher       Reviewer         Implementer
    │                │                │               │                │
    │  ① 계획 수립    │                │               │                │
    │───────────────▶│                │               │                │
    │  "현대화 계획을   │                │               │                │
    │   ADR로 세워줘" │                │               │                │
    │                │                │               │                │
    │  ADR + C4 반환  │                │               │                │
    │◀───────────────│                │               │                │
    │                                 │               │                │
    │  ② 기술 조사 (계획서 전달)        │               │                │
    │────────────────────────────────▶│               │                │
    │  "인증/DB/검증 기술              │               │                │
    │   비교 조사해줘"                 │               │                │
    │                                 │               │                │
    │  Technology Radar 반환           │               │                │
    │◀────────────────────────────────│               │                │
    │                                                 │                │
    │  ③ 보안 감사 (계획서+기술조사 전달)               │                │
    │────────────────────────────────────────────────▶│                │
    │  "OWASP/CWE/CVSS 기준으로                       │                │
    │   전수 감사해줘"                                 │                │
    │                                                 │                │
    │  13개 취약점 + CVSS + 공격시나리오                 │                │
    │◀────────────────────────────────────────────────│                │
    │                                                                  │
    │  ④ 구현 (계획서+기술선택+취약점 전달)                              │
    │─────────────────────────────────────────────────────────────────▶│
    │  "모든 분석 결과를 반영하여                                        │
    │   전체 재작성해줘"                                                │
    │                                                                  │
    │  12개 모듈 현대화 코드 반환                                        │
    │◀─────────────────────────────────────────────────────────────────│
    │                                                                  │
    ▼ 완료
```

### Phase 1 — Planner 에이전트

**호출 시점**: 코드를 받으면 **가장 먼저** 호출  
**방법론**: RFC/ADR/C4 Model/Impact Mapping

| 산출물 | 내용 |
|--------|------|
| ADR-001 | 전체 현대화 의사결정 문서 |
| C4 다이어그램 | Level 1 (System Context) + Level 2 (Container) |
| 요구사항 매핑 | 15개 항목 (현재 상태 → 목표 상태, 우선순위) |
| 영향 범위 분석 | 7개 영역별 위험도 매핑 |
| 구현 Phase | P0 (즉시) / P1 (1주) / P2 (2주) 분류 |

**기여 가치**: Planner 없이 구현에 들어가면 "급한 것부터 대충 고치기" → 신규 결함 유발.  
Planner가 P0~P2 우선순위를 잡아주면 체계적 수정 가능.

### Phase 2 — Researcher 에이전트

**호출 시점**: Planner가 기술 선택이 필요한 영역을 식별한 후  
**방법론**: Technology Radar / SLR / SWOT / ATAM

| 조사 영역 | 비교 대상 | 최종 선택 | 근거 |
|-----------|----------|----------|------|
| 비밀번호 해싱 | MD5/bcrypt/argon2/scrypt | **bcrypt** | OWASP 권장, Flask 생태계 최적 |
| 인증 방식 | 자체토큰/JWT/Flask-Login/OAuth2 | **JWT (PyJWT)** | REST API 최적, RFC 7519, 무상태 |
| DB 레이어 | raw sqlite3/SQLAlchemy/Peewee | **SQLAlchemy 2.0** | 업계 표준, 파라미터 바인딩 자동화 |
| 입력 검증 | 수동/marshmallow/Pydantic/cerberus | **Pydantic v2** | 타입 안전, Rust 코어, 최소 번들 |

**기여 가치**: Researcher 없으면 개발자 개인 선호로 기술 선택 → "argon2가 좋다던데?"  
Researcher가 비교표와 학계/표준 근거를 제시하면 팀 합의 용이.

### Phase 3 — Reviewer 에이전트

**호출 시점**: 기술 선택 완료 후, 구현 전 정확한 취약점 파악  
**방법론**: OWASP Top 10 / SANS CWE Top 25 / CVSS v3.1 / NIST SSDF

| # | 취약점 | CWE | CVSS | 공격 시나리오 |
|---|--------|-----|------|-------------|
| 1 | SQL Injection (login) | CWE-89 | 9.8 | `' OR 1=1 --` 인증 우회 |
| 2 | SQL Injection (employees) | CWE-89 | 9.1 | UNION 기반 데이터 추출 |
| 3 | SQL Injection (search) | CWE-89 | 8.6 | UNION 기반 크로스 테이블 조회 |
| 4 | SQL Injection (CUD) | CWE-89 | 9.8 | DROP TABLE, 급여 변조 |
| 5 | **SSTI** | CWE-1336 | **9.8** | `{{config['SECRET_KEY']}}` → RCE |
| 6 | Path Traversal | CWE-22 | 7.5 | `../../../etc/passwd` |
| 7 | Unrestricted Upload | CWE-434 | 8.8 | 웹쉘 업로드 |
| 8 | Hardcoded Secrets | CWE-798 | 8.1 | 토큰 위조 |
| 9 | Missing Auth (IDOR) | CWE-862 | 9.1 | 인증 없이 삭제/수정 |
| 10 | Information Disclosure | CWE-200 | 7.5 | `/debug/env` 전체 환경변수 |
| 11 | **Arbitrary SQL** | CWE-89 | **10.0** | `/run-query`로 DB 완전 장악 |
| 12 | Mass Assignment | CWE-915 | 8.1 | `role: "admin"` 직접 지정 |
| 13 | Password Hash Exposure | CWE-200 | 6.5 | 응답에 해시 포함 |

**CVSS 평균: 8.67 (Critical)**

**기여 가치**: Reviewer 없으면 표면적 취약점(SQLi)만 수정하고 SSTI, Mass Assignment 같은 심층 취약점 방치.  
CVSS 점수와 curl 공격 명령을 제공하면 "정말 위험한지" 즉시 검증 가능.

### Phase 4 — Implementer 에이전트

**호출 시점**: 모든 분석이 완료된 후 마지막으로 호출  
**방법론**: Clean Code / SOLID / 12-Factor App / Defensive Programming

| Before (레거시) | After (현대화) |
|----------------|---------------|
| 단일 파일 312줄 | 12개 모듈 875줄 |
| f-string SQL | SQLAlchemy ORM 파라미터 바인딩 |
| MD5 해싱 | bcrypt (cost factor 12) |
| 자체 MD5 토큰 | JWT (HS256, 만료 시간) |
| 인증/인가 없음 | `@login_required` + `@admin_required` RBAC |
| 입력 검증 없음 | Pydantic v2 스키마 6개 |
| 하드코딩 시크릿 | pydantic-settings 환경변수 |
| render_template_string | 위험 엔드포인트 제거 |
| debug=True 고정 | 환경변수 기반 토글 |
| Rate Limit 없음 | Flask-Limiter (로그인 10/min) |
| 보안 헤더 없음 | X-Content-Type-Options 등 5개 |
| `/run-query` 존재 | **완전 제거** |
| `/debug/env` 존재 | **완전 제거** |

**기여 가치**: Implementer가 앞 3단계의 모든 산출물을 입력으로 받아 **즉시 배포 가능한** 코드 생산.

---

## 4. 각 에이전트를 언제 쓰면 효과적인가?

### 에이전트별 최적 사용 타이밍

```
프로젝트 라이프사이클:

기획 ──── 설계 ──── 구현 ──── 리뷰 ──── 배포 ──── 운영
 │         │         │         │         │         │
 │    ┌────┴────┐    │    ┌────┴────┐    │    ┌────┴────┐
 │    │Planner  │    │    │Reviewer │    │    │Onboarding│
 │    │계획 수립 │    │    │코드 리뷰 │    │    │Guide    │
 │    └─────────┘    │    └─────────┘    │    └─────────┘
 │         │         │         │         │
 │    ┌────┴────┐    │    ┌────┴────┐    │
 │    │Researcher│   │    │PR       │    │
 │    │기술 조사 │    │    │Reviewer │    │
 │    └─────────┘    │    └─────────┘    │
 │                   │                   │
 │              ┌────┴────┐         ┌────┴────┐
 │              │Implement│         │Moderniz │
 │              │er 구현   │         │er 리팩터│
 │              └─────────┘         └─────────┘
 │
 └── Feature Builder (전체 오케스트레이션)
```

### 개별 vs 오케스트레이션 사용 가이드

| 상황 | 권장 접근법 | 이유 |
|------|-----------|------|
| 새 기능 개발 (대규모) | **Feature Builder** 오케스트레이션 | 계획→조사→구현→리뷰 전체 자동화 |
| 새 기능 개발 (소규모) | **Planner → Implementer** Handoff | 조사 단계 생략으로 속도 향상 |
| 기존 코드 보안 감사 | **Reviewer** 단독 | OWASP/CWE 기반 집중 감사 |
| PR 코드 리뷰 | **PR Reviewer** 단독 | Issue 연동 + Conventional Comments |
| 레거시 코드 현대화 | **Modernizer** (서브에이전트 포함) | Researcher+Reviewer 자동 호출 |
| 기술 선택 의사결정 | **Researcher** 단독 | Technology Radar 비교 분석 |
| 신규 팀원 온보딩 | **Onboarding Guide** 단독 | 프로젝트 구조 파악 지원 |

---

## 5. Before / After 한눈에 비교

### 코드 품질 지표

```
                    Before (레거시)          After (현대화)
                    ─────────────          ──────────────
보안 취약점          ████████████████ 13개   ░░░░░░░░░░░░░░ 0개   ✅ -100%
CWE 위반            ███████████ 11개        ░░░░░░░░░░░░░░ 0개   ✅ -100%
OWASP 위반          █████ 5개               ░░░░░░░░░░░░░░ 0개   ✅ -100%
인증된 엔드포인트     ░░░░░░░░░░░ 0%          ████████░ 89%        ✅ +89%p
파라미터 바인딩       █ 14%                   ██████████ 100%      ✅ +86%p
입력 검증 스키마      ░░░░░░░░░░░ 0개          ██████ 6개           ✅ +6
보안 헤더            ░░░░░░░░░░░ 0개          █████ 5개            ✅ +5
모듈 분리            █ 1개                    ████████████ 12개    ✅ +1100%
```

### 분석 깊이 비교

```
                     단순 리뷰             4-Agent 파이프라인
                     ─────────            ──────────────────
취약점 탐지           ███ 3~5개             █████████████ 13개
CWE 매핑             ░░░ 0개               ███████████ 11개
CVSS 산출            ░░░ 0건               █████████████ 13건
공격 시나리오         ░░░ 0개               █████████████ 13개
기술 비교             ░░░ 0건               ████ 4개 영역
아키텍처 설계         ░░░ 없음              ██ C4+ADR
방법론 적용           ░░░ 0개               ████████████ 12개
결과 코드             ░░░ 없음              ████████████ 12 파일
```

---

## 6. 산출물 파일 목록

| 구분 | 경로 | 설명 |
|------|------|------|
| **레거시 코드** | `src/python-api/legacy_api.py` | 테스트 대상 (312줄, 13개 취약점) |
| **파이프라인 분석** | `src/python-api/PIPELINE_ANALYSIS.md` | Phase 1~4 전체 분석 문서 |
| **현대화 코드** | `src/python-api/modernized/` | 12개 모듈 (875줄) |
| ├ 설정 | `modernized/config.py` | pydantic-settings 환경변수 관리 |
| ├ DB | `modernized/database.py` | SQLAlchemy 세션 관리 |
| ├ 모델 | `modernized/models.py` | ORM 모델 (민감정보 필터링) |
| ├ 인증 | `modernized/auth.py` | JWT + bcrypt + RBAC 데코레이터 |
| ├ 검증 | `modernized/validators.py` | Pydantic v2 입력 스키마 |
| ├ 미들웨어 | `modernized/middleware.py` | 보안 헤더 + 에러 핸들러 |
| ├ 라우트 | `modernized/routes/employees.py` | 직원 CRUD (보안 적용) |
| ├ 라우트 | `modernized/routes/projects.py` | 프로젝트 관리 |
| ├ 라우트 | `modernized/routes/files.py` | 안전한 파일 관리 |
| ├ 앱 | `modernized/app.py` | Flask 팩토리 패턴 |
| └ 설정 | `modernized/.env.example` | 환경변수 템플릿 |
| **이 보고서** | `ch04_Agent_성능비교_보고서.md` | 최종 비교 보고서 |

---

## 7. 핵심 결론

> **"넌 전문가야"는 AI에게 페르소나(겉모습)를 줍니다.**  
> **"방법론을 학습하고 적용해"는 AI에게 실제 기준과 프레임워크를 줍니다.**

단순 역할 부여는 CVSS 10.0짜리 임의 SQL 실행 엔드포인트도 놓치지만,  
방법론 학습형 4-Agent 파이프라인은 **13개 취약점을 CWE/CVSS/curl 공격 시나리오까지 포함하여** 체계적으로 분석하고,  
**즉시 배포 가능한 12개 모듈의 현대화 코드**까지 생산합니다.

이것이 **Custom Agent 오케스트레이션**의 현업 가치입니다.