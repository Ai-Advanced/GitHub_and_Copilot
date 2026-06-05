# 🚀 [/Fleet] 활용 Custom Agent 테스트 가이드

## 📁 현재 에이전트 구조

```
.github/agents/
├── feature-builder.agent.md   ← 🎯 오케스트레이터 (메인)
├── planner.agent.md           ← Phase 1: 계획 수립
├── researcher.agent.md        ← Phase 2: 기술 조사
├── implementer.agent.md       ← Phase 3: 구현
├── reviewer.agent.md          ← Phase 4: 리뷰
├── modernizer.agent.md        ← (독립) 레거시 코드 현대화
├── onboarding-guide.agent.md  ← (독립) 온보딩 가이드
└── pr-reviewer.agent.md       ← (독립) PR 리뷰
```

### 에이전트 관계도
```
Feature Builder (오케스트레이터)
    │
    ├─➀─→ Planner (계획)
    │         ├── handoff → Researcher
    │         └── handoff → Implementer
    │
    ├─➁─→ Researcher (조사)
    │         └── handoff → Implementer
    │
    ├─➂─→ Implementer (구현)
    │         └── handoff → Reviewer
    │
    └─➃─→ Reviewer (리뷰)
              └── handoff → Implementer (수정 필요 시)
```

---

## 🧪 테스트 방법 (초보자 가이드)

### 방법 1: Copilot Chat에서 직접 호출

VS Code의 Copilot Chat 패널에서 `@` 기호로 에이전트를 호출합니다:

```
@feature-builder demo-todo-app에 우선순위(priority) 기능을 추가해줘.
high/medium/low 3단계로 설정할 수 있어야 해.
```

### 방법 2: /fleet 모드로 병렬 실행

Copilot CLI(터미널)에서 `/fleet` 명령으로 여러 서브에이전트를 동시에 실행합니다:

```
/fleet demo-todo-app에 태그(tag) 기능을 추가해줘.
Todo에 여러 태그를 붙일 수 있고, 태그별로 필터링이 가능해야 해.
```

### 방법 3: 개별 서브에이전트 직접 호출

특정 단계만 실행하고 싶을 때:

```
@planner demo-todo-app에 마감일(dueDate) 기능을 추가하려면 어떻게 해야 할까?

@researcher Node.js에서 날짜 처리 라이브러리 비교해줘 (date-fns vs dayjs vs luxon)

@implementer demo-todo-app/src/index.js에 dueDate 필드를 추가하고 테스트도 작성해줘

@reviewer demo-todo-app/src/index.js 코드를 리뷰해줘
```

---

## 📋 추천 테스트 시나리오 (난이도별)

### ⭐ 초급: 단순 필드 추가
```
@feature-builder demo-todo-app에 메모(description) 필드를 추가해줘
```

### ⭐⭐ 중급: 새 기능 추가
```
@feature-builder demo-todo-app에 카테고리 기능을 추가해줘.
- 카테고리 CRUD
- Todo를 카테고리에 할당
- 카테고리별 Todo 조회
```

### ⭐⭐⭐ 고급: 아키텍처 변경
```
@feature-builder demo-todo-app을 REST API 서버로 변환해줘.
- Express.js 사용
- GET/POST/PUT/DELETE 엔드포인트
- 에러 핸들링 미들웨어
- 입력 유효성 검증
```

---

## ⚙️ 커스텀 에이전트 만드는 방법

### 1단계: `.github/agents/` 폴더에 마크다운 파일 생성

파일명 규칙: `에이전트이름.agent.md`

### 2단계: Front Matter (YAML 헤더) 작성

```yaml
---
name: My Agent              # 에이전트 이름 (필수)
description: "설명"          # 한줄 설명 (필수)
tools:                       # 사용할 도구 목록
  - search/codebase          #   코드 검색
  - edit                     #   파일 편집
  - web/fetch                #   웹 검색
  - read/terminalLastCommand #   터미널 출력 읽기
  - search/usages            #   심볼 사용처 검색
  - agent                    #   다른 에이전트 호출(오케스트레이터용)
agents:                      # 호출할 서브에이전트 (오케스트레이터용)
  - Planner
  - Implementer
model:                       # 사용할 AI 모델
  - 'Claude Sonnet 4.5'
  - 'GPT-5.2'
user-invocable: true         # 사용자가 직접 @로 호출 가능 여부
handoffs:                    # 다음 에이전트로 넘기기 (버튼)
  - label: "🚀 다음 단계"
    agent: NextAgent
    prompt: "이어서 작업해줘"
    send: false
---
```

### 3단계: 본문에 시스템 프롬프트 작성

```markdown
# 에이전트의 역할을 설명합니다.

## 워크플로우
1. 첫 번째 단계
2. 두 번째 단계

## 출력 형식
[원하는 출력 템플릿]

## ⚠️ 제약 사항
- 하면 안 되는 것
```

### 4단계: 커밋 & 푸시

```bash
git add .github/agents/my-agent.agent.md
git commit -m "feat: add my-agent custom agent"
git push
```

---

## 💡 핵심 개념 정리

| 개념 | 설명 |
|------|------|
| **오케스트레이터** | 여러 서브에이전트를 조율하는 상위 에이전트 (feature-builder) |
| **서브에이전트** | 특정 역할만 수행하는 전문 에이전트 (planner, implementer 등) |
| **Handoff** | 한 에이전트가 다른 에이전트에게 작업을 넘기는 것 |
| **tools** | 에이전트가 사용할 수 있는 도구 (코드검색, 편집, 웹검색 등) |
| **/fleet** | 여러 에이전트를 병렬로 실행하는 모드 |
| **@에이전트명** | Chat에서 특정 에이전트를 직접 호출하는 문법 |

---

## 🎯 테스트 체크리스트

- [ ] VS Code에서 Copilot Chat 패널 열기
- [ ] `@feature-builder` 입력 시 자동완성 되는지 확인
- [ ] 초급 시나리오로 테스트 실행
- [ ] 에이전트가 4단계(계획→조사→구현→리뷰) 순서로 동작하는지 확인
- [ ] 생성된 코드가 실제로 동작하는지 `npm test`로 검증

---

## ⚠️ 트러블슈팅

| 증상 | 해결 |
|------|------|
| @에이전트명이 인식 안됨 | `.github/agents/` 경로 확인, 파일명에 `.agent.md` 확인 |
| 에이전트가 도구를 못 씀 | front matter의 `tools:` 목록에 해당 도구 추가 |
| 서브에이전트 호출 안됨 | 오케스트레이터의 `agents:` 목록에 이름 추가 |
| handoff 버튼 안 보임 | `handoffs:` 설정의 agent 이름이 실제 에이전트 name과 일치하는지 확인 |
