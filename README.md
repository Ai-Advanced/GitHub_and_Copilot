# 🎓 GitHub Copilot & GHAS 교육 자료

> AI 코딩 어시스턴트 **GitHub Copilot**과 보안 솔루션 **GHAS(GitHub Advanced Security)** 를 다루는 교육 자료입니다.

## 📋 교육 개요

| 항목 | 내용 |
|------|------|
| **교육 시간** | 40~50분 |
| **형태** | 이론 + Hands-on 실습 |
| **준비물** | VS Code (최신), GitHub 계정, Copilot 라이선스 |

## 📂 교육 자료 구성 (챕터 순서)

| 챕터 | 파일 | 소요 시간 | 설명 |
|------|------|-----------|------|
| **Ch.1** | [ch01_GitHub_Copilot_소개.md](./ch01_GitHub_Copilot_소개.md) | 10분 | Copilot 소개, 핵심 기능 5가지, 요금제, Cursor 비교 |
| **Ch.2** | [ch02_Custom_Agent_심화교육.md](./ch02_Custom_Agent_심화교육.md) | 25~30분 | 커스터마이징 기초 → Agent 아키텍처 → 오케스트레이션 → 실습 → 프롬프트 꿀팁 |
| **Ch.3** | [ch03_GHE_GHAS_보안심화.md](./ch03_GHE_GHAS_보안심화.md) | 20~25분 | GHE 개요, GHAS 3대 기능, 보안 파이프라인 구축 실습, Security Overview |
| **Ch.4** | [ch04_Agent_성능비교_보고서.md](./ch04_Agent_성능비교_보고서.md) | 참고 자료 | 역할 부여형 vs 4-Agent 파이프라인 실전 성능 비교 |

### 실습 · 데모 파일

| 파일 | 설명 |
|------|------|
| [`.github/agents/`](./.github/agents/) | 🤖 Custom Agent 8종 (Planner, Researcher, Implementer, Reviewer, Orchestrator 등) |
| [`.github/workflows/security-pipeline.yml`](./.github/workflows/security-pipeline.yml) | 🔐 보안 자동화 파이프라인 (CodeQL + Secret Scanning + Dependency Review) |
| [`.github/dependabot.yml`](./.github/dependabot.yml) | 📦 Dependabot 자동 업데이트 설정 |
| [`src/vulnerable-sample.js`](./src/vulnerable-sample.js) | ⚠️ 의도적 취약 JS 코드 (CodeQL 탐지 데모용) |
| [`src/python-api/legacy_api.py`](./src/python-api/legacy_api.py) | ⚠️ 의도적 취약 Flask API (Agent 오케스트레이션 데모용) |
| [`src/python-api/modernized/`](./src/python-api/modernized/) | ✅ 4-Agent 파이프라인이 생성한 현대화 코드 |
| [`SECURITY.md`](./SECURITY.md) | 🛡️ 보안 정책 문서 |

## 🕐 교육 아젠다

| 순서 | 주제 | 시간 | 챕터 |
|------|------|------|------|
| 1 | GitHub Copilot 소개 & 핵심 기능 | 5분 | Ch.1 |
| 2 | Copilot vs Cursor 기능 비교 | 5분 | Ch.1 |
| 3 | **Custom Agent 심화** (아키텍처 · 오케스트레이션 · 실습 · 프롬프트) | 25~30분 | Ch.2 |
| 4 | GHE + GHAS 보안 심화 | 5분+ | Ch.3 |
| | **합계** | **~45~50분** | |

## 🔑 주요 학습 내용

### Chapter 1: Copilot 소개 & Cursor 비교
- Copilot 핵심 기능 5가지 (코드 완성, Chat, Agent Mode, CLI, GitHub.com)
- Copilot vs Cursor 기능 비교표, 장단점, 선택 가이드
- 요금제 비교 (Free → Enterprise)

### Chapter 2: Custom Agent 심화 ⭐
- **커스터마이징 기초** — Instructions, MCP(Model Context Protocol) 연동
- **에이전트 아키텍처** — `.agent.md` 파일 구조, 도구 레퍼런스, 모델 선택
- **Sub-Agent & 오케스트레이션** — Handoff(순차 전환) vs Sub-Agent(자동 호출)
- **멀티 에이전트 실습** — Planner → Researcher → Implementer → Reviewer 파이프라인
- **현업 시나리오 실습** — PR 자동 리뷰, 레거시 코드 현대화, 온보딩 가이드
- **프롬프트 꿀팁** — "역할 부여 vs 방법론 학습" 원리, 5가지 실전 패턴

### Chapter 3: GHE + GHAS 보안 심화
- GitHub Enterprise Cloud/Server 비교
- GHAS 3대 기능: Code Scanning, Secret Scanning, Dependabot
- **Code Scanning + Copilot Autofix** — AI 자동 취약점 수정
- **Secret Scanning + Push Protection** — 시크릿 포함 커밋 push 차단
- **보안 자동화 파이프라인 실습** — GitHub Actions 기반 CI/CD 보안 파이프라인
- **Security Overview 대시보드** — 조직 전체 보안 현황 모니터링

### Chapter 4: Agent 성능 비교 보고서 📊
- 단순 역할 부여형 vs 4-Agent 파이프라인 비교
- 13개 취약점 탐지 결과 (CWE 매핑, CVSS 점수, 공격 시나리오)
- 에이전트별 최적 사용 타이밍 가이드
- Before / After 코드 품질 지표

## ✅ 보안 파이프라인 검증 결과

이 리포지토리에 실제로 배포된 보안 파이프라인의 실행 결과입니다.

### Pipeline Jobs

| Job | 상태 | 설명 |
|-----|------|------|
| 🔍 Code Scanning (CodeQL) | ✅ 성공 | SARIF 결과 GitHub Security 탭에 업로드 완료 |
| 🔑 Secret Scanning Check | ✅ 성공 | 시크릿 알림 없음 확인 |
| 📦 Dependency Review | ⏭️ Skipped | push 이벤트에서는 건너뜀 (PR에서만 동작) |
| 📊 Security Report | ✅ 성공 | 보안 요약 리포트 생성 |

### CodeQL 탐지 알림

`src/vulnerable-sample.js`에서 다음 취약점이 탐지되었습니다:

| 취약점 | CWE | 심각도 |
|--------|-----|--------|
| **SQL Injection** (`js/sql-injection`) | CWE-89 | 🔴 High |
| **Reflected XSS** (`js/reflected-xss`) | CWE-79 | 🔴 High |
| **Missing Rate Limiting** ×2 (`js/missing-rate-limiting`) | CWE-770 | 🔴 High |

> 🔗 [Security 탭에서 확인하기](https://github.com/Ai-Advanced/GitHub_and_Copilot/security)  
> 🔗 [Actions 탭에서 파이프라인 확인하기](https://github.com/Ai-Advanced/GitHub_and_Copilot/actions)

## 🚀 빠른 시작

```bash
# 실습 환경 준비
mkdir copilot-agent-lab && cd copilot-agent-lab
git init
mkdir -p .github/agents
```

## �� 참고 링크

| 자료 | 링크 |
|------|------|
| GitHub Copilot 공식 문서 | https://docs.github.com/copilot |
| Custom Agents 공식 문서 | https://code.visualstudio.com/docs/copilot/customization/custom-agents |
| Sub-Agents 공식 문서 | https://code.visualstudio.com/docs/copilot/agents/subagents |
| GHAS 공식 문서 | https://docs.github.com/en/code-security |
| CodeQL 쿼리 가이드 | https://codeql.github.com/docs |
| Copilot Autofix 문서 | https://docs.github.com/en/code-security/code-scanning/copilot-autofix |
| Awesome Copilot 예제 | https://github.com/github/awesome-copilot |

---

> 📝 질문이나 피드백은 이슈로 남겨주세요!
