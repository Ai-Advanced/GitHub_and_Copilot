# 🎓 GitHub Copilot & GHAS 교육 자료

> **교육 시간:** 40~50분  
> **대상:** 개발자, DevOps 엔지니어, 보안 담당자  
> **준비물:** VS Code (최신 버전), GitHub 계정, GitHub Copilot 라이선스

---

## 📋 교육 아젠다

| 순서 | 주제 | 시간 |
|------|------|------|
| 1 | GitHub Copilot 소개 & 핵심 기능 | 5분 |
| 2 | Copilot vs Cursor 기능 비교 | 5분 |
| 3 | Custom Agent 심화 (아키텍처 · Sub-Agent · 실습 · 프롬프트 꿀팁) (→ [심화 문서](./GitHub_Copilot_CustomAgent_심화교육.md)) | 25~30분 |
| 4 | GHE + GHAS 소개 | 5분 |
| 합계 | | **~45~50분** |

> 📖 **Part 3 Custom Agent 심화 과정**이 교육의 핵심입니다: [`GitHub_Copilot_CustomAgent_심화교육.md`](./GitHub_Copilot_CustomAgent_심화교육.md)  
> 에이전트 아키텍처, Sub-Agent 오케스트레이션, 현업 활용 시나리오 실습, 프롬프트 꿀팁을 다룹니다.

---

# 📌 Part 1. GitHub Copilot 소개 (5분)

## 1.1 GitHub Copilot이란?

GitHub Copilot은 **AI 기반 페어 프로그래머**입니다.

- 🤖 코드 자동완성, 함수 생성, 테스트 작성, 문서화까지 지원
- 💬 자연어로 대화하며 코딩 (Copilot Chat)
- 🔄 Agent Mode: 자율적으로 코드 수정, 테스트 실행, 반복 개선
- 🌐 VS Code, JetBrains, Visual Studio, Neovim, Xcode, Eclipse, CLI 지원

## 1.2 Copilot 주요 기능 5가지

### ① 코드 자동완성 (Code Completion)
```python
# 함수 시그니처만 작성하면 Copilot이 구현을 제안
def calculate_fibonacci(n):
    # Copilot이 자동으로 구현 코드를 생성합니다
```

### ② Copilot Chat
- 사이드바에서 코드에 대한 질문/설명 요청
- `/explain`, `/fix`, `/tests` 등 슬래시 커맨드 지원

### ③ Agent Mode (에이전트 모드)
- 자율적으로 코드 수정 → 테스트 실행 → 오류 수정 반복
- GitHub Issue → PR 자동 생성 가능
- 터미널 명령어 실행, 파일 생성/편집 등 전체 워크플로우 자동화

### ④ Copilot CLI
- 터미널에서 AI와 대화하며 코딩하는 CLI 도구
- 설치:
  - Mac: `brew install copilot-cli`
  - Windows: `winget install GitHub.Copilot`
- 주요 모드:
  - **기본 모드** — 질문/답변 형식으로 코드 작성, 파일 편집, 명령 실행
  - **Autopilot 모드** — AI가 자율적으로 작업 수행 (사용자 승인 최소화)
  - **Plan 모드** — 구현 전 계획서를 먼저 작성하고 검토 후 실행

### ⑤ Copilot in GitHub.com
- Pull Request 요약 자동 생성
- 코드 리뷰 지원
- Issue → PR 자동화 (Coding Agent)

## 1.3 Copilot 요금제

| 플랜 | 가격 | 주요 특징 |
|------|------|-----------|
| **Free** | $0 | 제한된 완성/채팅 |
| **Individual** | $10/월 | 무제한 완성, Chat, CLI |
| **Business** | $19/월/사용자 | 조직 관리, 감사 로그, IP 면책 |
| **Enterprise** | $39/월/사용자 | Knowledge Base, 모델 파인튜닝, SSO |

> 💡 **2026년 6월부터** Business/Enterprise에 **AI Credits 기반 사용량 과금** 도입 예정

---

# 📌 Part 2. Copilot vs Cursor 비교 분석 (5분)

## 2.1 핵심 차이점

| 비교 항목 | GitHub Copilot | Cursor |
|-----------|---------------|--------|
| **형태** | IDE 확장 프로그램 (플러그인) | 독립 AI-네이티브 IDE (VS Code 포크) |
| **지원 IDE** | VS Code, JetBrains, VS, Neovim, Xcode, Eclipse | Cursor 전용 |
| **가격** | $10~$39/월 | $20/월 (Pro) |
| **코드 완성** | 인라인, 멀티라인 | 인라인, 멀티라인, AI 네이티브 컨텍스트 |
| **멀티파일 편집** | 기본 수준 (점진적 개선 중) | ⭐ 강력 (Composer로 프로젝트 전체 편집) |
| **Agent Mode** | Preview → GA (Issue→PR 자동화) | ⭐ 성숙 (코드 실행, 브라우저 제어 포함) |
| **모델 선택** | GPT-4o, Claude, Gemini | GPT-5.2, Claude Opus, Gemini, Grok |
| **GitHub 연동** | ⭐ 네이티브 통합 (Issue, PR, Actions) | 제한적 |
| **엔터프라이즈** | ⭐ 감사 로그, SSO, IP 면책, 정책 제어 | 기본 팀 기능 |
| **커스터마이징** | copilot-instructions.md, Custom Agent | .cursorrules |

## 2.2 Copilot의 강점 💪

1. **IDE 유연성** — 기존 IDE를 바꿀 필요 없음 (6개+ IDE 지원)
2. **GitHub 네이티브 통합** — Issue, PR, Actions, Code Review와 원활한 연동
3. **엔터프라이즈 보안** — 감사 로그, SSO, IP 면책, 콘텐츠 제외 정책
4. **가격 경쟁력** — Cursor 대비 50% 저렴 ($10 vs $20)
5. **GHAS 연계** — 보안 스캐닝과 AI 코딩의 통합 생태계

## 2.3 Cursor의 강점 💪

1. **멀티파일 편집 능력** — 프로젝트 전체를 이해하고 수정하는 능력이 강력
2. **AI 네이티브 설계** — IDE 자체가 AI 중심으로 구축됨
3. **Composer 모드** — 대규모 리팩토링에서 최대 30% 빠른 결과
4. **모델 다양성** — 다양한 최신 모델 즉시 선택 가능

## 2.4 언제 무엇을 선택할까?

```
┌─────────────────────────────────────────────────┐
│  이런 경우 → Copilot                             │
│  • 여러 IDE를 사용하는 팀                          │
│  • GitHub 중심 워크플로우                          │
│  • 엔터프라이즈 보안/컴플라이언스 요구               │
│  • 비용 효율성 중시                                │
├─────────────────────────────────────────────────┤
│  이런 경우 → Cursor                              │
│  • VS Code 단독 사용팀                            │
│  • 대규모 코드베이스 리팩토링 빈번                   │
│  • AI-first 경험 원하는 개인/소규모 팀              │
└─────────────────────────────────────────────────┘
```

---

# 📌 Part 3. Custom Agent 심화 (25~30분)

> 이 파트의 상세 내용은 심화 문서를 참고하세요: **[GitHub_Copilot_CustomAgent_심화교육.md](./GitHub_Copilot_CustomAgent_심화교육.md)**
>
> | 섹션 | 내용 | 시간 |
> |------|------|------|
> | 3.1 | Agent 아키텍처 이해 (커스터마이징 5단계, `.agent.md` 필드, 도구 레퍼런스) | 5분 |
> | 3.2 | Sub-Agent & 오케스트레이션 (Handoff vs Sub-Agent) | 5분 |
> | 3.3 | 🔧 실습: 4단계 멀티 에이전트 파이프라인 구축 (Planner→Researcher→Implementer→Reviewer) | 8분 |
> | 3.4 | 현업 활용 시나리오 & 실습 (PR 리뷰, 레거시 현대화, 온보딩 가이드) | 8분 |
> | 3.5 | 에이전트 프롬프트 꿀팁 (방법론 학습, 5가지 실전 패턴, 안티패턴) | 4분 |

아래는 Part 3에서 다루는 핵심 개념의 간략한 소개입니다. 데모와 실습은 심화 문서를 따라 진행합니다.

## 3.1 Copilot 커스터마이징 5단계

```
Level 1: Custom Instructions    → 프로젝트 규칙/스타일 정의
Level 2: Custom Agents          → 전문가 AI 페르소나 생성
Level 3: Agent Skills           → 스크립트 포함 이식 가능한 능력
Level 4: MCP (Model Context Protocol) → 외부 도구 연동
```

## 3.2 Custom Instructions (커스텀 인스트럭션)

### 📁 글로벌 인스트럭션: `.github/copilot-instructions.md`
프로젝트 전체에 적용되는 규칙을 정의합니다.

```markdown
<!-- .github/copilot-instructions.md -->

## 코딩 규칙
- TypeScript를 사용하고 `any` 타입 사용 금지
- 함수명은 camelCase, 클래스명은 PascalCase 사용
- 모든 public 함수에는 JSDoc 주석 필수
- 에러 처리는 반드시 try-catch로 감싸기

## 아키텍처
- Clean Architecture 패턴 준수
- Repository 패턴으로 데이터 접근 추상화
- 비즈니스 로직은 Service 레이어에 배치

## 테스트
- 모든 함수에 단위 테스트 작성
- Jest + Testing Library 사용
- 커버리지 80% 이상 유지
```

### 📁 패턴 기반 인스트럭션: `.instructions.md`
특정 파일 패턴에 맞는 규칙을 적용합니다.

```markdown
<!-- src/components/.instructions.md -->
---
applyTo: "**/*.tsx"
---
- React 함수형 컴포넌트만 사용
- Props는 interface로 정의
- styled-components 대신 Tailwind CSS 사용
- 컴포넌트당 하나의 파일
```

## 3.3 MCP (Model Context Protocol) 연동

외부 도구와 서비스를 에이전트에 연결하는 프로토콜입니다.

```jsonc
// .vscode/mcp.json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${env:DATABASE_URL}"
      }
    }
  }
}
```

> MCP를 통해 에이전트가 GitHub API, DB, Slack 등 외부 시스템과 직접 상호작용 가능!

---

# 📌 Part 4. GHE + GHAS 소개 (5분)

> 이 파트의 상세 실습 및 보안 파이프라인 구축은 심화 문서를 참고하세요: **[GHAS_Copilot_보안심화교육.md](./GHAS_Copilot_보안심화교육.md)**
>
> | 섹션 | 내용 |
> |------|------|
> | 4.1 | GHAS 보안 파이프라인 전체 아키텍처 |
> | 4.2 | Code Scanning + Copilot Autofix 심화 |
> | 4.3 | Secret Scanning + Push Protection 심화 |
> | 4.4 | Dependabot 자동화 파이프라인 구축 |
> | 4.5 | 🔧 실습: 보안 자동화 파이프라인 구축 |
> | 4.6 | Security Overview 대시보드 활용 (보안 관리자용) |

## 4.1 GitHub Enterprise (GHE) 개요

GitHub Enterprise는 기업 환경에 최적화된 GitHub 플랫폼입니다.

### GHE Cloud vs GHE Server

| 항목 | GHE Cloud | GHE Server |
|------|-----------|------------|
| **호스팅** | GitHub 관리 (SaaS) | 자체 인프라 (On-premise) |
| **업데이트** | 자동 | 수동 |
| **규정 준수** | SOC 1/2, FedRAMP 등 | 자체 보안 정책 |
| **데이터 주권** | GitHub 인프라 | 자사 데이터센터 |
| **GHAS** | ✅ 포함 | ✅ 별도 라이선스 |

### GHE 핵심 기능
- **SAML SSO / SCIM** — 기업 ID 관리 통합
- **감사 로그** — 모든 활동 추적/감사
- **IP 허용 목록** — 네트워크 수준 접근 제어
- **리포지토리 정책** — 조직 전체 브랜치 보호, 리뷰 정책
- **내부 리포지토리** — InnerSource를 위한 사내 공개 리포지토리

## 4.2 GHAS (GitHub Advanced Security) 개요

GHAS는 **소프트웨어 공급망 전체를 보호**하는 통합 보안 솔루션입니다.

```
┌─────────────────────────────────────────────────────────┐
│                    GHAS 보안 체계                        │
├──────────────┬──────────────┬───────────────────────────┤
│  Code        │  Secret      │  Supply Chain             │
│  Scanning    │  Scanning    │  Security                 │
│              │              │                           │
│ • CodeQL     │ • 200+ 패턴   │ • Dependabot Alerts      │
│ • 자동 수정   │ • Push 보호   │ • Dependabot Updates     │
│ • PR 통합    │ • 커스텀 패턴  │ • Dependency Review      │
│ • SARIF 지원 │ • 파트너 연동  │ • SBOM 생성              │
└──────────────┴──────────────┴───────────────────────────┘
```

### 🔍 Code Scanning (코드 스캐닝)
- **CodeQL** 엔진으로 코드의 보안 취약점 자동 탐지
- SQL Injection, XSS, Path Traversal 등 탐지
- PR에서 직접 결과 확인 및 **Copilot Autofix**로 자동 수정 제안
- 지원 언어: JavaScript, TypeScript, Python, Java, C/C++, Go, Ruby, C#, Swift, Kotlin

### 🔑 Secret Scanning (시크릿 스캐닝)
- 코드에 노출된 API 키, 토큰, 비밀번호 등 자동 탐지
- **Push Protection**: 시크릿이 포함된 커밋을 **push 단계에서 차단**
- **200개+ 파트너 패턴** (AWS, Azure, GCP, Slack 등)
- 커스텀 정규식 패턴으로 사내 시크릿 형식도 탐지 가능

### 📦 Dependabot (의존성 보안)
- 알려진 취약점이 있는 의존성 자동 탐지 & 알림
- 보안 업데이트 PR 자동 생성
- 버전 업데이트 PR 자동 생성
- 다양한 생태계 지원: npm, Maven, pip, NuGet, Go, Rust 등

## 4.3 GHAS + Copilot 시너지 🤝

```
         개발자가 코드 작성
               │
    ┌──────────▼──────────┐
    │   Copilot이 보안     │
    │   베스트 프랙티스로   │
    │   코드 생성          │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   Push Protection    │ ← 시크릿 포함 시 push 차단
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   Code Scanning      │ ← PR에서 취약점 자동 탐지
    │   + Copilot Autofix  │ ← AI가 수정 코드 자동 제안
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   Dependabot         │ ← 취약한 의존성 자동 업데이트
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   Security Overview  │ ← 조직 전체 보안 현황 대시보드
    └──────────┴──────────┘
```

> 💡 **핵심 메시지:** Copilot이 안전한 코드를 작성하고, GHAS가 놓친 부분을 잡아내는 **이중 보안 체계**

---

# 📌 부록: Quick Reference

## A. 실습 환경 세팅 체크리스트

```
□ VS Code 최신 버전 설치
□ GitHub Copilot 최신 버전 설치
□ GitHub 계정 로그인 & Copilot 라이선스 활성화
□ Git 설치 & 설정
```

## B. 유용한 Copilot 단축키

| 단축키 | 기능 |
|--------|------|
| `Tab` | 제안 수락 |
| `Esc` | 제안 거부 |
| `Alt + ]` / `Alt + [` | 다음/이전 제안 |
| `Ctrl + Enter` | 모든 제안 보기 (새 탭) |
| `Ctrl + I` (Mac: `Cmd + I`) | 인라인 Chat 열기 |
| `Ctrl + Shift + I` | Copilot Chat 패널 토글 |

## C. Copilot Chat 유용한 슬래시 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/explain` | 선택한 코드 설명 |
| `/fix` | 코드 문제 수정 제안 |
| `/tests` | 단위 테스트 생성 |
| `/doc` | 문서/주석 생성 |
| `/optimize` | 성능 최적화 제안 |
| `/new` | 새 프로젝트 스캐폴딩 |

## D. 파일 구조 요약

```
.github/
├── copilot-instructions.md          # 글로벌 커스텀 인스트럭션
├── agents/
│   ├── security-reviewer.agent.md   # 보안 리뷰 에이전트
│   ├── test-generator.agent.md      # 테스트 생성 에이전트
│   └── code-reviewer.agent.md       # 코드 리뷰 에이전트

src/
├── components/
│   └── .instructions.md             # 컴포넌트 전용 인스트럭션
└── ...

.vscode/
└── mcp.json                         # MCP 서버 설정
```

## E. 추가 학습 자료

| 자료 | 링크 |
|------|------|
| GitHub Copilot 공식 문서 | https://docs.github.com/copilot |
| Custom Agents 가이드 | https://docs.github.com/en/copilot/reference/custom-agents-configuration |
| GHAS 공식 문서 | https://docs.github.com/en/code-security |
| VS Code Copilot 커스터마이징 | https://code.visualstudio.com/docs/copilot/customization |
| GitHub Roadmap | https://github.com/github/roadmap |
| Copilot Trust Center | https://copilot.github.trust.page/ |
| GHEC Trust Center | https://ghec.github.trust.page/ |

---

> 📝 **교육 후 설문/피드백을 수집하여 다음 교육에 반영하세요!**
