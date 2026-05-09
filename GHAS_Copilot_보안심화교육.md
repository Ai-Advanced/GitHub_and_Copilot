# 🔐 GHAS + Copilot 보안 심화 교육

> **Part 4 확장판** — GHAS 보안 파이프라인 구축, Security Overview 대시보드, Copilot Autofix, 보안 자동화  
> **예상 소요:** 15~20분 (데모 + 실습 포함)  
> **대상:** 보안 관리자, DevSecOps 엔지니어, 테크 리드  
> **사전 준비:** GitHub Enterprise Cloud 또는 GHAS 라이선스가 적용된 조직

---

## 📋 목차

| 순서 | 주제 | 시간 |
|------|------|------|
| 4.1 | GHAS 보안 파이프라인 전체 아키텍처 | 3분 |
| 4.2 | Code Scanning + Copilot Autofix 심화 | 4분 |
| 4.3 | Secret Scanning + Push Protection 심화 | 3분 |
| 4.4 | Dependabot 자동화 파이프라인 구축 | 3분 |
| 4.5 | 🔧 실습: 보안 자동화 파이프라인 구축 | 5분 |
| 4.6 | Security Overview 대시보드 활용 | 3분 |

---

# 4.1 GHAS 보안 파이프라인 전체 아키텍처 (3분)

## 개발 라이프사이클 전체를 커버하는 보안 체계

```
  개발자 로컬 환경                GitHub                        운영 환경
 ┌──────────────┐      ┌─────────────────────────┐      ┌──────────────┐
 │              │      │                         │      │              │
 │  Copilot이    │ push │  ① Push Protection      │      │  ⑥ Security  │
 │  보안 코드    │─────→│     시크릿 차단          │      │    Overview   │
 │  생성 지원    │      │         │                │      │    대시보드    │
 │              │      │         ▼                │      │              │
 │  pre-commit  │      │  ② Code Scanning        │      │  조직 전체    │
 │  hook으로    │      │     CodeQL 분석          │      │  보안 현황    │
 │  로컬 검증   │      │         │                │      │  모니터링     │
 │              │      │         ▼                │      │              │
 └──────────────┘      │  ③ Copilot Autofix      │      └──────────────┘
                       │     AI 자동 수정 제안     │             ▲
                       │         │                │             │
                       │         ▼                │             │
                       │  ④ Dependency Review     │        데이터 집계
                       │     의존성 취약점 검토     │             │
                       │         │                │             │
                       │         ▼                │             │
                       │  ⑤ Dependabot           │─────────────┘
                       │     자동 업데이트 PR      │
                       │                         │
                       └─────────────────────────┘
```

### 보안 도구별 동작 시점

| 도구 | 동작 시점 | 방식 |
|------|----------|------|
| **Copilot** | 코드 작성 중 | 보안 베스트 프랙티스 기반 코드 생성 |
| **Push Protection** | `git push` 시 | 시크릿 포함 커밋 차단 |
| **Code Scanning** | PR 생성/업데이트 시 | CodeQL로 정적 분석 |
| **Copilot Autofix** | Code Scanning 알림 발생 시 | AI가 수정 코드 자동 제안 |
| **Dependency Review** | PR에 의존성 변경 시 | 새 의존성의 취약점 검토 |
| **Dependabot** | 스케줄 기반 (매일/매주) | 취약 의존성 자동 업데이트 PR |
| **Security Overview** | 상시 | 조직 전체 보안 대시보드 |

---

# 4.2 Code Scanning + Copilot Autofix 심화 (4분)

## Code Scanning (CodeQL) 동작 원리

```
┌──────────────────────────────────────────────────────────┐
│                    CodeQL 분석 프로세스                     │
│                                                          │
│  소스코드 ──→ CodeQL DB 생성 ──→ 쿼리 실행 ──→ 결과 반환   │
│                                                          │
│  지원 언어:                                               │
│  JavaScript, TypeScript, Python, Java, C/C++,            │
│  C#, Go, Ruby, Swift, Kotlin                             │
│                                                          │
│  탐지 취약점:                                              │
│  • SQL Injection (CWE-89)                                │
│  • Cross-Site Scripting (CWE-79)                         │
│  • Path Traversal (CWE-22)                               │
│  • 인증 우회 (CWE-287)                                    │
│  • 안전하지 않은 역직렬화 (CWE-502)                         │
│  • 하드코딩된 자격증명 (CWE-798)                            │
│  + 수백 가지 추가 패턴                                      │
└──────────────────────────────────────────────────────────┘
```

## Copilot Autofix: AI 자동 수정

Code Scanning이 취약점을 발견하면, **Copilot Autofix**가 자동으로 수정 코드를 제안합니다.

### 동작 흐름

```
  CodeQL이 취약점 발견
         │
         ▼
  ┌─────────────────────┐
  │  Copilot Autofix     │
  │                     │
  │  1. 취약점 컨텍스트   │
  │     분석             │
  │  2. 데이터 흐름      │
  │     추적             │
  │  3. 수정 코드        │
  │     생성             │
  │  4. 자연어 설명      │
  │     첨부             │
  └──────────┬──────────┘
             │
             ▼
  PR에 수정 제안이 표시됨
  ┌─────────────────────────────────────┐
  │  ⚠️ SQL Injection (CWE-89)          │
  │                                     │
  │  Before:                            │
  │  query = "SELECT * FROM users       │
  │           WHERE name = '" + name    │
  │                                     │
  │  🤖 Copilot Autofix 제안:            │
  │  query = "SELECT * FROM users       │
  │           WHERE name = ?"           │
  │  params = [name]                    │
  │                                     │
  │  💡 설명: 사용자 입력을 직접 SQL      │
  │  문자열에 연결하면 SQL Injection      │
  │  공격에 취약합니다. 파라미터화된       │
  │  쿼리를 사용하여 방지합니다.          │
  │                                     │
  │  [✅ 수정 적용]  [❌ 무시]  [✏️ 편집] │
  └─────────────────────────────────────┘
```

### Autofix 핵심 수치

| 지표 | 수치 |
|------|------|
| 평균 수정 시간 (Autofix 없이) | 1.5시간 |
| 평균 수정 시간 (Autofix 사용) | **28분** (3배 빠름) |
| 지원 취약점 커버리지 | **90%+** (지원 언어 기준) |
| 지원 언어 | JavaScript, TypeScript, Java, Python, C#, Go, Ruby 등 |

> 💡 **핵심 가치:** "Found means Fixed" — 발견되면 곧 수정된다

---

# 4.3 Secret Scanning + Push Protection 심화 (3분)

## Secret Scanning 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                 Secret Scanning 체계                      │
├─────────────────────┬───────────────────────────────────┤
│                     │                                   │
│  🔍 탐지 계층        │  🛡️ 보호 계층                     │
│                     │                                   │
│  • 200+ 파트너 패턴   │  • Push Protection               │
│    (AWS, Azure,     │    커밋 push 시점에서              │
│     GCP, Slack,     │    시크릿 포함 코드 차단            │
│     Stripe 등)      │                                   │
│                     │  • 바이패스 정책                    │
│  • 커스텀 정규식      │    - 허용: 감사 로그 기록          │
│    패턴 정의 가능     │    - 차단: 완전 차단 (권장)        │
│                     │    - 관리자 승인: 승인 후 허용       │
│  • 커밋 히스토리      │                                   │
│    전체 스캔         │  • 알림 & 대응                     │
│                     │    - 파트너사 자동 통보             │
│                     │    - 시크릿 자동 폐기 (일부)        │
│                     │    - Slack/Teams 알림 연동         │
└─────────────────────┴───────────────────────────────────┘
```

## Push Protection 동작 예시

```bash
$ git push origin main

remote: ——————————————————————————————————————————————————
remote: ——  GitHub Push Protection  ————————————————————
remote: ——————————————————————————————————————————————————
remote:
remote:  🚨 Push blocked!
remote:
remote:  Secret detected: AWS Access Key ID
remote:  Location: src/config.js:15
remote:  Pattern: AKIA[0-9A-Z]{16}
remote:
remote:  To push this commit, you must either:
remote:   1. Remove the secret from your commits
remote:   2. Request a bypass (if org policy allows)
remote:
remote:  Learn more:
remote:  https://docs.github.com/code-security/secret-scanning
remote: ——————————————————————————————————————————————————
```

## 커스텀 시크릿 패턴 설정

조직 내부의 고유한 시크릿 형식도 탐지할 수 있습니다.

```
Organization Settings → Code security → Secret scanning

커스텀 패턴 예시:

패턴 이름: Internal API Key
정규식:   MYCOMPANY_[A-Za-z0-9]{32}
테스트:   MYCOMPANY_abcdef1234567890abcdef1234567890
```

---

# 4.4 Dependabot 자동화 파이프라인 구축 (3분)

## Dependabot 3가지 기능

```
┌─────────────────────────────────────────────────┐
│              Dependabot 기능 체계                  │
├─────────────┬──────────────┬────────────────────┤
│  Alerts     │  Security    │  Version           │
│  (알림)      │  Updates     │  Updates           │
│             │  (보안 업뎃)   │  (버전 업뎃)        │
│             │              │                    │
│ 취약 의존성  │ 보안 패치     │ 최신 버전           │
│ 알림 발생   │ PR 자동 생성  │ PR 자동 생성        │
│             │              │                    │
│ 수동 확인   │ 자동화 가능   │ 자동화 가능         │
└─────────────┴──────────────┴────────────────────┘
```

## Dependabot 설정 파일

파일: `.github/dependabot.yml`

```yaml
version: 2
updates:
  # npm 의존성 (매일 체크)
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"
    # 보안 업데이트만 자동 머지 허용
    allow:
      - dependency-type: "direct"

  # GitHub Actions 워크플로우 (매주 체크)
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"

  # Docker 이미지 (매주 체크)
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  # pip (Python) 의존성
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
```

## Dependabot 자동 머지 워크플로우

파일: `.github/workflows/dependabot-auto-merge.yml`

```yaml
name: Dependabot Auto-Merge

on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"

      # patch/minor 업데이트만 자동 머지 (major는 수동 리뷰)
      - name: Auto-merge minor/patch updates
        if: >
          steps.metadata.outputs.update-type == 'version-update:semver-patch' ||
          steps.metadata.outputs.update-type == 'version-update:semver-minor'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

> 💡 **핵심:** patch/minor 업데이트는 자동 머지, major 업데이트는 수동 리뷰 → 안전과 효율의 균형

---

# 4.5 🔧 실습: 보안 자동화 파이프라인 구축 (5분)

## 실습 목표
**GHAS 보안 도구를 활용한 CI/CD 보안 파이프라인 구축**

> ⚠️ **사전 요구사항: GHAS 라이선스 필요**
> 
> Code Scanning(CodeQL 결과 업로드), Secret Scanning API 등 GHAS 기능은  
> **GitHub Advanced Security 라이선스가 활성화된 리포지토리**에서만 동작합니다.
> 
> - **GitHub Enterprise Cloud/Server** → Organization Settings에서 GHAS 활성화
> - **Public 리포지토리** → GHAS 기능 무료 제공 (별도 설정 없이 사용 가능)
> - **Private 리포지토리 (Free/Team)** → GHAS 라이선스 필요 (없으면 CodeQL 분석은 로컬에서 실행 가능하지만 GitHub UI에 결과가 표시되지 않음)
> 
> 💡 **실습 팁:** GHAS 라이선스가 없는 환경에서는 **Public 리포지토리**로 실습하면 모든 기능을 무료로 체험할 수 있습니다.

### Step 1: CodeQL 코드 스캐닝 워크플로우 생성

파일: `.github/workflows/security-pipeline.yml`

```yaml
name: "🔐 Security Pipeline"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:  # 수동 실행 가능
  schedule:
    - cron: '0 9 * * 1'  # 매주 월요일 09:00 UTC

jobs:
  # ──────────────────────────────────────────
  # Job 1: CodeQL 코드 스캐닝
  # ──────────────────────────────────────────
  code-scanning:
    name: "🔍 Code Scanning (CodeQL)"
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: ['javascript-typescript']
        # 필요 시 추가: 'python', 'java-kotlin', 'csharp', 'go', 'ruby'

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          # 추가 쿼리팩으로 보안 검사 강화
          queries: security-extended,security-and-quality

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"

  # ──────────────────────────────────────────
  # Job 2: Secret Scanning 알림 확인
  # ──────────────────────────────────────────
  secret-check:
    name: "🔑 Secret Scanning Check"
    runs-on: ubuntu-latest
    permissions:
      security-events: read

    steps:
      - name: Check for open secret alerts
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            try {
              const alerts = await github.rest.secretScanning.listAlertsForRepo({
                owner: context.repo.owner,
                repo: context.repo.repo,
                state: 'open'
              });

              if (alerts.data.length > 0) {
                core.warning(`⚠️ ${alerts.data.length}개의 시크릿 스캐닝 알림이 있습니다.`);
                alerts.data.forEach(alert => {
                  core.warning(`  - ${alert.secret_type_display_name} (${alert.state})`);
                });
                // 필요 시 core.setFailed()로 빌드 실패 처리
              } else {
                core.info('✅ 시크릿 스캐닝 알림 없음');
              }
            } catch (error) {
              core.info('ℹ️ Secret scanning API 접근 불가 (GHAS 라이선스 필요)');
            }

  # ──────────────────────────────────────────
  # Job 3: 의존성 취약점 검토 (PR에서만)
  # ──────────────────────────────────────────
  dependency-review:
    name: "📦 Dependency Review"
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          # Critical/High 취약점이 있으면 빌드 실패
          fail-on-severity: high
          # 알려진 취약점만 검사 (라이선스 검사도 가능)
          comment-summary-in-pr: always

  # ──────────────────────────────────────────
  # Job 4: 보안 리포트 생성
  # ──────────────────────────────────────────
  security-report:
    name: "📊 Security Report"
    runs-on: ubuntu-latest
    needs: [code-scanning, secret-check, dependency-review]
    if: always()

    steps:
      - name: Generate Security Summary
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const summary = `
            ## 🔐 Security Pipeline Report

            | 검사 항목 | 상태 |
            |----------|------|
            | Code Scanning (CodeQL) | ${{ needs.code-scanning.result == 'success' && '✅ Pass' || '❌ Fail' }} |
            | Secret Scanning | ${{ needs.secret-check.result == 'success' && '✅ Pass' || '⚠️ Check' }} |
            | Dependency Review | ${{ needs.dependency-review.result == 'success' && '✅ Pass' || '❌ Fail' }} |

            > 📅 실행 시간: ${new Date().toISOString()}
            `;

            if (context.eventName === 'pull_request') {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                body: summary
              });
            }
            core.info(summary);
```

### Step 2: Dependabot 설정 추가

파일: `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"
```

### Step 3: 보안 정책 문서 생성

파일: `SECURITY.md`

```markdown
# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |
| < 1.0   | ❌        |

## Reporting a Vulnerability

보안 취약점을 발견하셨다면:

1. **공개 이슈로 등록하지 마세요**
2. Security Advisory를 통해 비공개로 보고해주세요
   - Repository → Security → Advisories → New draft advisory
3. 48시간 이내에 확인 및 초기 대응을 진행합니다

## Security Tools

이 프로젝트는 다음 보안 도구를 사용합니다:
- ✅ GitHub Code Scanning (CodeQL)
- ✅ GitHub Secret Scanning + Push Protection
- ✅ Dependabot Security Updates
- ✅ Copilot Autofix
```

### Step 4: 확인 포인트

> ✅ PR을 생성하여 다음을 확인:
> - CodeQL이 코드를 분석하고 결과가 PR의 **Checks** 탭에 표시되는지
> - Copilot Autofix가 발견된 취약점에 대해 수정 제안을 하는지
> - Dependency Review가 새로운 취약한 의존성을 차단하는지
> - Security Report 코멘트가 PR에 자동 게시되는지

### 📊 실제 파이프라인 검증 결과

이 레포지토리에서 실제로 파이프라인을 실행한 결과입니다:

| Job | 상태 | 설명 |
|-----|------|------|
| 🔑 Secret Scanning Check | ✅ 성공 | 시크릿 알림 없음 확인 |
| 🔍 Code Scanning (CodeQL) | ⚠️ 분석 성공, 업로드 실패 | CodeQL 분석 자체는 정상 동작하여 `vulnerable-sample.js`의 취약점 탐지 완료. 단, **GHAS 미활성 리포**에서는 SARIF 결과 업로드 시 `Advanced Security must be enabled` 에러 발생 |
| 📦 Dependency Review | ⏭️ Skipped | `push` 이벤트에서는 정상적으로 건너뜀 (PR에서만 동작) |
| 📊 Security Report | ✅ 성공 | 보안 요약 리포트 정상 생성 |

> 💡 **포인트:** CodeQL 분석 엔진은 GHAS 없이도 로컬/CI에서 실행 가능하지만, GitHub UI에서 결과를 보려면(Security 탭, PR 코멘트, Copilot Autofix) **반드시 GHAS 라이선스가 필요**합니다.  
> Public 리포지토리에서는 GHAS가 무료로 제공되므로, 교육 실습 시 **Public 리포로 전환**하면 전체 플로우를 체험할 수 있습니다.

---

# 4.6 Security Overview 대시보드 활용 (3분)

## 보안 관리자를 위한 Security Overview

Security Overview는 **조직 전체의 보안 현황을 한눈에 파악**할 수 있는 대시보드입니다.

### 접근 방법

```
Organization → Security 탭 → Overview

또는

Enterprise → Code Security (사이드바)
```

### 대시보드 구성 요소

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Overview                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 Overview (개요)                                          │
│  ├─ 전체 알림 수: Critical 3 / High 12 / Medium 45 / Low 89 │
│  ├─ 트렌드: 지난 30일 알림 추이 그래프                         │
│  └─ Top 10 위험 리포지토리 순위                               │
│                                                             │
│  🔍 Coverage (커버리지)                                       │
│  ├─ Code Scanning 활성화: 85/100 repos (85%)                │
│  ├─ Secret Scanning 활성화: 92/100 repos (92%)              │
│  ├─ Push Protection 활성화: 78/100 repos (78%)              │
│  └─ Dependabot 활성화: 90/100 repos (90%)                   │
│                                                             │
│  🔧 Remediation (수정 현황)                                   │
│  ├─ 평균 수정 시간: 4.2일                                     │
│  ├─ 미해결 Critical 알림: 3건                                 │
│  ├─ 이번 달 해결된 알림: 28건                                  │
│  └─ Autofix 적용률: 62%                                      │
│                                                             │
│  🛡️ Prevention (예방)                                        │
│  ├─ Push Protection 차단 횟수: 156건/월                      │
│  ├─ PR에서 차단된 취약점: 89건/월                              │
│  └─ 바이패스 요청: 12건 (승인 8, 거부 4)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 필터링 기능

| 필터 | 용도 | 예시 |
|------|------|------|
| **팀별** | 팀 단위 보안 현황 | `team:backend-team` |
| **리포지토리별** | 특정 프로젝트 집중 분석 | `repo:my-api` |
| **심각도별** | 우선순위 기반 대응 | `severity:critical,high` |
| **도구별** | 특정 보안 도구 현황 | `tool:codeql` |
| **시크릿 유형별** | 특정 시크릿 타입 추적 | `secret-type:aws_access_key` |

### CSV 내보내기

```
Security Overview → Export → CSV

활용 예:
- 경영진 보고서 자동 생성
- 외부 SIEM/SOAR 도구 연동
- 컴플라이언스 감사 자료
- 보안 KPI 대시보드 (Grafana, Datadog 등)
```

## 보안 관리자의 주간/월간 체크리스트

### 📅 주간 체크 (15분)

```markdown
## 주간 보안 점검

### Critical/High 알림 확인
- [ ] 새로운 Critical 알림 확인 및 담당자 배정
- [ ] High 알림 중 7일 이상 미해결 건 확인
- [ ] Copilot Autofix 제안 중 미적용 건 확인

### Push Protection
- [ ] 바이패스 요청 검토 및 승인/거부
- [ ] 반복적 바이패스 요청 패턴 확인

### Dependabot
- [ ] 미머지된 보안 업데이트 PR 확인
- [ ] Major 버전 업데이트 PR 리뷰
```

### 📅 월간 체크 (30분)

```markdown
## 월간 보안 리포트

### 커버리지 분석
- [ ] Code Scanning 미활성화 리포지토리 목록 → 활성화 요청
- [ ] Push Protection 미활성화 리포지토리 → 정책 적용
- [ ] 새로 생성된 리포지토리의 보안 도구 활성화 확인

### 트렌드 분석
- [ ] 지난 달 대비 알림 증감 분석
- [ ] 평균 수정 시간 (MTTR) 추이 확인
- [ ] 팀별 보안 성과 비교

### 보고서 작성
- [ ] Security Overview CSV 내보내기
- [ ] 경영진/CISO 보고서 작성
- [ ] 보안 KPI 업데이트
```

## Copilot Custom Agent: 보안 대시보드 분석 에이전트

GHAS API를 활용하여 보안 현황을 자동 분석하는 에이전트를 만들 수 있습니다.

파일: `.github/agents/security-analyst.agent.md`

```markdown
---
name: Security Analyst
description: "조직의 보안 현황을 분석하고 리포트를 생성하는 에이전트"
tools:
  - search/codebase
  - web/fetch
  - edit
---

# 당신은 시니어 보안 분석가입니다.

## 역할
GHAS 보안 데이터를 분석하고 실행 가능한 인사이트를 제공합니다.

## 분석 영역

### 1. 취약점 현황 분석
- 심각도별 알림 분포 (Critical/High/Medium/Low)
- 미해결 알림의 연령 분석 (SLA 초과 건 식별)
- 가장 취약한 리포지토리 Top 10

### 2. 수정 효율성 분석
- 평균 수정 시간 (MTTR) 계산
- Copilot Autofix 적용률 및 효과
- 팀별 수정 성과 비교

### 3. 예방 효과 분석
- Push Protection 차단 건수 및 트렌드
- PR 단계에서 차단된 취약점 수
- 바이패스 패턴 분석

### 4. 권장 사항
위 분석을 바탕으로:
- 🔴 즉시 조치 필요 사항
- 🟡 이번 스프린트 내 개선 사항
- 🟢 중장기 개선 제안

## 출력 형식
경영진 리포트 형태 (1페이지 요약 + 상세 데이터)
```

---

# 📎 부록: GHAS 활성화 Quick Guide

## 조직 레벨 일괄 활성화

```
Organization Settings
  → Code security and analysis
    → ✅ Dependency graph (Enable all)
    → ✅ Dependabot alerts (Enable all)
    → ✅ Dependabot security updates (Enable all)
    → ✅ Code scanning default setup (Enable all)
    → ✅ Secret scanning (Enable all)
    → ✅ Push protection (Enable all)
```

## GitHub API를 활용한 자동 활성화

```bash
# 조직 내 모든 리포지토리에 GHAS 활성화 (gh CLI 사용)
gh api \
  --method PATCH \
  -H "Accept: application/vnd.github+json" \
  /repos/{owner}/{repo} \
  -f security_and_analysis[advanced_security][status]=enabled \
  -f security_and_analysis[secret_scanning][status]=enabled \
  -f security_and_analysis[secret_scanning_push_protection][status]=enabled
```

## 참고 링크

| 자료 | 링크 |
|------|------|
| GHAS 공식 문서 | https://docs.github.com/en/code-security |
| Security Overview 문서 | https://docs.github.com/en/code-security/security-overview |
| Copilot Autofix 문서 | https://docs.github.com/en/code-security/code-scanning/copilot-autofix |
| CodeQL 쿼리 작성 가이드 | https://codeql.github.com/docs |
| Dependabot 설정 가이드 | https://docs.github.com/en/code-security/dependabot |
| GitHub Security Blog | https://github.blog/tag/security/ |

---

> 💡 **핵심 메시지:** GHAS는 단순한 도구가 아니라 **개발 라이프사이클 전체에 걸친 보안 체계**입니다.  
> Copilot이 안전한 코드를 작성하고, GHAS가 놓친 부분을 잡아내고, Autofix가 수정하고,  
> Security Overview가 전체 현황을 모니터링하는 **End-to-End 보안 파이프라인**을 구축하세요.
