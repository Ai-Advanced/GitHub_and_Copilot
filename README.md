# 🎓 GitHub Copilot & GHAS 교육 자료

> AI 코딩 어시스턴트 **GitHub Copilot**과 보안 솔루션 **GHAS(GitHub Advanced Security)** 를 다루는 교육 자료입니다.

## 📋 교육 개요

| 항목 | 내용 |
|------|------|
| **교육 시간** | 40~50분 |
| **형태** | 이론 + Hands-on 실습 |
| **준비물** | VS Code (최신), GitHub 계정, Copilot 라이선스 |

## 📂 교육 자료 구성

| 파일 | 설명 |
|------|------|
| [GitHub_Copilot_GHAS_교육자료.md](./GitHub_Copilot_GHAS_교육자료.md) | **메인 교육자료** — 전체 커리큘럼, Copilot 소개, Cursor 비교, GHE+GHAS |
| [GitHub_Copilot_CustomAgent_심화교육.md](./GitHub_Copilot_CustomAgent_심화교육.md) | **Custom Agent 심화** — Sub-Agent 오케스트레이션, 현업 실습, 프롬프트 꿀팁 |
| [GHAS_Copilot_보안심화교육.md](./GHAS_Copilot_보안심화교육.md) | **GHAS 보안 심화** — 보안 파이프라인 구축, Security Overview, Copilot Autofix |

## 🕐 교육 아젠다

| 순서 | 주제 | 시간 | 자료 |
|------|------|------|------|
| 1 | GitHub Copilot 소개 & 핵심 기능 | 5분 | 메인 교육자료 |
| 2 | Copilot vs Cursor 기능 비교 | 5분 | 메인 교육자료 |
| 3 | **Custom Agent 심화** (아키텍처 · Sub-Agent · 실습 · 프롬프트 꿀팁) | 25~30분 | 심화 교육자료 |
| 4 | GHE + GHAS 소개 | 5분 | 메인 교육자료 |
| | **합계** | **~45~50분** | |

## 🔑 주요 학습 내용

### Part 1~2: Copilot 소개 & 경쟁 비교
- Copilot 핵심 기능 5가지 (코드 완성, Chat, Agent Mode, CLI, GitHub.com)
- Copilot vs Cursor 기능 비교표, 장단점, 선택 가이드

### Part 3: Custom Agent 심화 ⭐
- **에이전트 아키텍처** — 커스터마이징 4단계 (Instructions → Agents → Skills → MCP)
- **Sub-Agent & 오케스트레이션** — Handoff(순차 전환) vs Sub-Agent(자동 호출)
- **멀티 에이전트 실습** — Planner → Researcher → Implementer → Reviewer 파이프라인
- **현업 시나리오 실습** — PR 자동 리뷰, 레거시 코드 현대화, 온보딩 가이드
- **프롬프트 꿀팁** — "역할 부여 vs 방법론 학습" 원리, 5가지 실전 패턴

### Part 4: GHE + GHAS (→ [보안 심화 문서](./GHAS_Copilot_보안심화교육.md))
- GitHub Enterprise Cloud/Server 비교
- GHAS 3대 기능: Code Scanning, Secret Scanning, Dependabot
- **Code Scanning + Copilot Autofix** — AI 자동 취약점 수정 (평균 수정 시간 3배 단축)
- **Secret Scanning + Push Protection** — 시크릿 포함 커밋 push 차단
- **보안 자동화 파이프라인 실습** — GitHub Actions 기반 CI/CD 보안 파이프라인 구축
- **Security Overview 대시보드** — 조직 전체 보안 현황 모니터링, 주간/월간 체크리스트
- Copilot + GHAS 시너지 (End-to-End 보안 체계)

## 🚀 빠른 시작

```bash
# 실습 환경 준비
mkdir copilot-agent-lab && cd copilot-agent-lab
git init
mkdir -p .github/agents
```

## 📎 참고 링크

| 자료 | 링크 |
|------|------|
| GitHub Copilot 공식 문서 | https://docs.github.com/copilot |
| Custom Agents 공식 문서 | https://code.visualstudio.com/docs/copilot/customization/custom-agents |
| Sub-Agents 공식 문서 | https://code.visualstudio.com/docs/copilot/agents/subagents |
| GHAS 공식 문서 | https://docs.github.com/en/code-security |
| Awesome Copilot 예제 | https://github.com/github/awesome-copilot |

---

> 📝 질문이나 피드백은 이슈로 남겨주세요!
