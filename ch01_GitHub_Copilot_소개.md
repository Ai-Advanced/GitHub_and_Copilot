# 📌 Chapter 1. GitHub Copilot 소개 & 비교 분석

> **소요 시간:** 10분  
> **학습 목표:** GitHub Copilot의 핵심 기능을 이해하고, Cursor와의 차이점을 파악합니다.  
> **다음 단계:** [Chapter 2 — Custom Agent 심화 교육](./ch02_Custom_Agent_심화교육.md)

---

## 📋 목차

| 순서 | 주제 | 시간 |
|------|------|------|
| 1.1 | GitHub Copilot이란? | 2분 |
| 1.2 | Copilot 주요 기능 5가지 | 3분 |
| 1.3 | Copilot 요금제 | 1분 |
| 2.1 | Copilot vs Cursor 핵심 차이점 | 2분 |
| 2.2~2.4 | 각각의 강점 & 선택 가이드 | 2분 |

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
