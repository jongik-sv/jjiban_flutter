---
name: implement
description: "지능적인 페르소나 활성화 및 MCP 통합을 통한 기능 및 코드 구현"
category: workflow
complexity: standard
mcp-servers: [context7, sequential, magic, playwright]
personas: [architect, frontend, backend, security, qa-specialist]
---

# /sc:implement - 기능 구현

> **컨텍스트 프레임워크 참고**: 이 행동 지침은 Claude Code 사용자가 `/sc:implement` 패턴을 입력할 때 활성화됩니다. 이는 Claude가 포괄적인 구현을 위해 전문가 페르소나와 MCP 도구를 조율하도록 안내합니다.

## 트리거 (Triggers)
- 컴포넌트, API 또는 전체 기능에 대한 기능 개발 요청
- 프레임워크별 요구사항이 있는 코드 구현 필요
- 조율된 전문 지식이 필요한 다중 도메인 개발
- 테스트 및 검증 통합이 필요한 구현 프로젝트

## 컨텍스트 트리거 패턴 (Context Trigger Pattern)
```
/sc:implement [feature-description] [--type component|api|service|feature] [--framework react|vue|express] [--safe] [--with-tests]
```
**사용법**: 조율된 전문 지식과 체계적인 개발 접근 방식으로 구현 행동 모드를 활성화하려면 Claude Code 대화에 이 패턴을 입력하십시오.

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 구현 요구사항을 검토하고 기술 컨텍스트를 감지합니다.
2. **계획 (Plan)**: 접근 방식을 선택하고 도메인 전문 지식을 위해 관련 페르소나를 활성화합니다.
3. **생성 (Generate)**: 프레임워크별 모범 사례를 사용하여 구현 코드를 작성합니다.
4. **검증 (Validate)**: 개발 전반에 걸쳐 보안 및 품질 검증을 적용합니다.
5. **통합 (Integrate)**: 문서를 업데이트하고 테스트 추천 사항을 제공합니다.

주요 행동:
- 컨텍스트 기반 페르소나 활성화 (아키텍트, 프론트엔드, 백엔드, 보안, QA)
- Context7 및 Magic MCP 통합을 통한 프레임워크별 구현
- Sequential MCP를 통한 체계적인 다중 컴포넌트 협력
- 검증을 위한 Playwright와의 포괄적인 테스트 통합

## MCP 통합 (MCP Integration)
- **Context7 MCP**: React, Vue, Angular, Express를 위한 프레임워크 패턴 및 공식 문서
- **Magic MCP**: UI 컴포넌트 생성 및 디자인 시스템 통합을 위해 자동 활성화
- **Sequential MCP**: 복잡한 다단계 분석 및 구현 계획
- **Playwright MCP**: 테스트 검증 및 품질 보증 통합

## 도구 협력 (Tool Coordination)
- **Write/Edit/MultiEdit**: 구현을 위한 코드 생성 및 수정
- **Read/Grep/Glob**: 일관성을 위한 프로젝트 분석 및 패턴 감지
- **TodoWrite**: 복잡한 다중 파일 구현을 위한 진행 상황 추적
- **Task**: 체계적인 협력이 필요한 대규모 기능 개발 위임

## 주요 패턴 (Key Patterns)
- **컨텍스트 감지 (Context Detection)**: 프레임워크/기술 스택 → 적절한 페르소나 및 MCP 활성화
- **구현 흐름 (Implementation Flow)**: 요구사항 → 코드 생성 → 검증 → 통합
- **다중 페르소나 협력 (Multi-Persona Coordination)**: 프론트엔드 + 백엔드 + 보안 → 포괄적인 솔루션
- **품질 통합 (Quality Integration)**: 구현 → 테스트 → 문서화 → 검증

## 예시 (Examples)

### React 컴포넌트 구현
```
/sc:implement user profile component --type component --framework react
# Magic MCP가 디자인 시스템 통합으로 UI 컴포넌트 생성
# 프론트엔드 페르소나가 모범 사례 및 접근성 보장
```

### API 서비스 구현
```
/sc:implement user authentication API --type api --safe --with-tests
# 백엔드 페르소나가 서버 측 로직 및 데이터 처리 담당
# 보안 페르소나가 인증 모범 사례 보장
```

### 풀스택 기능
```
/sc:implement payment processing system --type feature --with-tests
# 다중 페르소나 협력: 아키텍트, 프론트엔드, 백엔드, 보안
# Sequential MCP가 복잡한 구현 단계를 분해
```

### 프레임워크별 구현
```
/sc:implement dashboard widget --framework vue
# Context7 MCP가 Vue 관련 패턴 및 문서 제공
# 공식 모범 사례를 사용한 프레임워크에 적합한 구현
```

## 경계 (Boundaries)

**수행할 작업:**
- 지능적인 페르소나 활성화 및 MCP 협력을 통해 기능을 구현합니다.
- 프레임워크별 모범 사례 및 보안 검증을 적용합니다.
- 테스트 및 문서 통합을 포함한 포괄적인 구현을 제공합니다.

**수행하지 않을 작업:**
- 적절한 페르소나 협의 없이 아키텍처 결정을 내리지 않습니다.
- 보안 정책 또는 아키텍처 제약 조건과 충돌하는 기능을 구현하지 않습니다.
- 사용자가 지정한 안전 제약 조건을 무시하거나 품질 게이트를 우회하지 않습니다.
