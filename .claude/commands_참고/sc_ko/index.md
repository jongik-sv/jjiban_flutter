---
name: index
description: "지능적인 구성을 통해 포괄적인 프로젝트 문서 및 지식 베이스를 생성합니다."
category: special
complexity: standard
mcp-servers: [sequential, context7]
personas: [architect, scribe, quality]
---

# /sc:index - 프로젝트 문서화

## 트리거 (Triggers)
- 프로젝트 문서 생성 및 유지보수 요구사항
- 지식 베이스 생성 및 구성 필요
- API 문서 및 구조 분석 요구사항
- 상호 참조 및 탐색 향상 요청

## 사용법 (Usage)
```
/sc:index [target] [--type docs|api|structure|readme] [--format md|json|yaml]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 프로젝트 구조를 검토하고 주요 문서 구성 요소를 식별합니다.
2. **구성 (Organize)**: 지능적인 구성 패턴 및 상호 참조 전략을 적용합니다.
3. **생성 (Generate)**: 프레임워크별 패턴으로 포괄적인 문서를 만듭니다.
4. **검증 (Validate)**: 문서의 완전성과 품질 표준을 보장합니다.
5. **유지보수 (Maintain)**: 수동 추가 및 사용자 정의를 보존하면서 기존 문서를 업데이트합니다.

주요 행동:
- 문서 범위 및 복잡성에 따른 다중 페르소나(아키텍트, 서기, 품질) 협력
- 체계적인 분석 및 포괄적인 문서화 워크플로우를 위한 Sequential MCP 통합
- 프레임워크별 패턴 및 문서 표준을 위한 Context7 MCP 통합
- 상호 참조 기능 및 자동화된 유지보수를 통한 지능적인 구성

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 복잡한 다단계 프로젝트 분석 및 체계적인 문서 생성
- **Context7 MCP**: 프레임워크별 문서 패턴 및 기존 표준
- **페르소나 협력 (Persona Coordination)**: 아키텍트(구조), 서기(콘텐츠), 품질(검증)

## 도구 협력 (Tool Coordination)
- **Read/Grep/Glob**: 문서 생성을 위한 프로젝트 구조 분석 및 콘텐츠 추출
- **Write**: 지능적인 구성 및 상호 참조를 통한 문서 생성
- **TodoWrite**: 복잡한 다중 컴포넌트 문서화 워크플로우를 위한 진행 상황 추적
- **Task**: 체계적인 협력이 필요한 대규모 문서화를 위한 고급 위임

## 주요 패턴 (Key Patterns)
- **구조 분석 (Structure Analysis)**: 프로젝트 검토 → 컴포넌트 식별 → 논리적 구성 → 상호 참조
- **문서 유형 (Documentation Types)**: API 문서 → 구조 문서 → README → 지식 베이스 접근 방식
- **품질 검증 (Quality Validation)**: 완전성 평가 → 정확성 검증 → 표준 준수 → 유지보수 계획
- **프레임워크 통합 (Framework Integration)**: Context7 패턴 → 공식 표준 → 모범 사례 → 일관성 검증

## 예시 (Examples)

### 프로젝트 구조 문서화
```
/sc:index project-root --type structure --format md
# 지능적인 구성을 통한 포괄적인 프로젝트 구조 문서화
# 상호 참조 및 컴포넌트 관계로 탐색 가능한 구조 생성
```

### API 문서 생성
```
/sc:index src/api --type api --format json
# 체계적인 분석 및 검증을 통한 API 문서화
# 서기 및 품질 페르소나가 완전성과 정확성 보장
```

### 지식 베이스 생성
```
/sc:index . --type docs
# 프로젝트별 패턴을 사용한 대화형 지식 베이스 생성
# 아키텍트 페르소나가 구조적 구성 및 상호 참조 제공
```

## 경계 (Boundaries)

**수행할 작업:**
- 지능적인 구성 및 상호 참조를 통해 포괄적인 프로젝트 문서를 생성합니다.
- 체계적인 분석 및 품질 검증을 위해 다중 페르소나 협력을 적용합니다.
- 프레임워크별 패턴 및 기존 문서 표준을 제공합니다.

**수행하지 않을 작업:**
- 명시적인 업데이트 허가 없이 기존 수동 문서를 덮어쓰지 않습니다.
- 적절한 프로젝트 구조 분석 및 검증 없이 문서를 생성하지 않습니다.
- 기존 문서 표준 또는 품질 요구사항을 우회하지 않습니다.
