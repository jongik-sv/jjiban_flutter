---
name: explain
description: "교육적인 명확성으로 코드, 개념 및 시스템 동작에 대한 명확한 설명을 제공합니다."
category: workflow
complexity: standard
mcp-servers: [sequential, context7]
personas: [educator, architect, security]
---

# /sc:explain - 코드 및 개념 설명

## 트리거 (Triggers)
- 복잡한 기능에 대한 코드 이해 및 문서화 요청
- 아키텍처 구성 요소에 대한 시스템 동작 설명 필요
- 지식 전달을 위한 교육 콘텐츠 생성
- 프레임워크별 개념 명확화 요구사항

## 사용법 (Usage)
```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 포괄적인 이해를 위해 대상 코드, 개념 또는 시스템을 검토합니다.
2. **평가 (Assess)**: 청중 수준과 적절한 설명 깊이 및 형식을 결정합니다.
3. **구조화 (Structure)**: 점진적인 복잡성과 논리적 흐름으로 설명 순서를 계획합니다.
4. **생성 (Generate)**: 예제, 다이어그램 및 대화형 요소를 사용하여 명확한 설명을 만듭니다.
5. **검증 (Validate)**: 설명의 정확성과 교육적 효과를 확인합니다.

주요 행동:
- 도메인 전문 지식(교육자, 아키텍트, 보안)을 위한 다중 페르소나 협력
- Context7 통합을 통한 프레임워크별 설명
- 복잡한 개념 분석을 위한 Sequential MCP를 통한 체계적인 분석
- 청중과 복잡성에 따른 적응형 설명 깊이

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 복잡한 다중 컴포넌트 분석 및 구조화된 추론을 위해 자동 활성화
- **Context7 MCP**: 프레임워크 문서 및 공식 패턴 설명
- **페르소나 협력 (Persona Coordination)**: 교육자(학습), 아키텍트(시스템), 보안(실무)

## 도구 협력 (Tool Coordination)
- **Read/Grep/Glob**: 설명 콘텐츠를 위한 코드 분석 및 패턴 식별
- **TodoWrite**: 복잡한 다중 파트 설명을 위한 진행 상황 추적
- **Task**: 체계적인 분석이 필요한 포괄적인 설명 워크플로우 위임

## 주요 패턴 (Key Patterns)
- **점진적 학습 (Progressive Learning)**: 기본 개념 → 중간 세부 정보 → 고급 구현
- **프레임워크 통합 (Framework Integration)**: Context7 문서 → 정확한 공식 패턴 및 실무
- **다중 도메인 분석 (Multi-Domain Analysis)**: 기술적 정확성 + 교육적 명확성 + 보안 인식
- **대화형 설명 (Interactive Explanation)**: 정적 콘텐츠 → 예제 → 대화형 탐색

## 예시 (Examples)

### 기본 코드 설명
```
/sc:explain authentication.js --level basic
# 초보자를 위한 실용적인 예제가 포함된 명확한 설명
# 교육자 페르소나가 학습에 최적화된 구조 제공
```

### 프레임워크 개념 설명
```
/sc:explain react-hooks --level intermediate --context react
# 공식 React 문서 패턴을 위한 Context7 통합
# 점진적인 복잡성을 가진 구조화된 설명
```

### 시스템 아키텍처 설명
```
/sc:explain microservices-system --level advanced --format interactive
# 아키텍트 페르소나가 시스템 설계 및 패턴 설명
# 순차적 분석 분해를 통한 대화형 탐색
```

### 보안 개념 설명
```
/sc:explain jwt-authentication --context security --level basic
# 보안 페르소나가 인증 개념 및 모범 사례 설명
# 실용적인 예제가 포함된 프레임워크에 구애받지 않는 보안 원칙
```

## 경계 (Boundaries)

**수행할 작업:**
- 교육적인 명확성으로 명확하고 포괄적인 설명을 제공합니다.
- 도메인 전문 지식과 정확한 분석을 위해 관련 페르소나를 자동 활성화합니다.
- 공식 문서 통합을 통해 프레임워크별 설명을 생성합니다.

**수행하지 않을 작업:**
- 철저한 분석 및 정확성 검증 없이 설명을 생성하지 않습니다.
- 프로젝트별 문서 표준을 무시하거나 민감한 세부 정보를 공개하지 않습니다.
- 수립된 설명 검증 또는 교육 품질 요구사항을 우회하지 않습니다.
