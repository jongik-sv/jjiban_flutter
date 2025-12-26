---
name: task
description: "지능적인 워크플로우 관리 및 위임을 통한 복잡한 작업 실행"
category: special
complexity: advanced
mcp-servers: [sequential, context7, magic, playwright, morphllm, serena]
personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
---

# /sc:task - 향상된 작업 관리

## 트리거 (Triggers)
- 다중 에이전트 협력 및 위임이 필요한 복잡한 작업
- 구조화된 워크플로우 관리 및 세션 간 지속성이 필요한 프로젝트
- 지능적인 MCP 서버 라우팅 및 도메인 전문 지식이 필요한 작업
- 체계적인 실행 및 점진적 향상이 유익한 작업

## 사용법 (Usage)
```
/sc:task [action] [target] [--strategy systematic|agile|enterprise] [--parallel] [--delegate]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 작업 요구사항을 파싱하고 최적의 실행 전략 결정
2. **위임 (Delegate)**: 적절한 MCP 서버로 라우팅하고 관련 페르소나 활성화
3. **협력 (Coordinate)**: 지능적인 워크플로우 관리 및 병렬 처리로 작업 실행
4. **검증 (Validate)**: 품질 게이트 및 포괄적인 작업 완료 검증 적용
5. **최적화 (Optimize)**: 성능 분석 및 향상 추천 사항 제공

주요 행동:
- 아키텍트, 프론트엔드, 백엔드, 보안, 데브옵스 도메인에 걸친 다중 페르소나 협력
- 지능적인 MCP 서버 라우팅 (Sequential, Context7, Magic, Playwright, Morphllm, Serena)
- 점진적인 작업 향상 및 세션 간 지속성을 통한 체계적인 실행
- 계층적 분해 및 종속성 관리를 통한 고급 작업 위임

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 복잡한 다단계 작업 분석 및 체계적인 실행 계획
- **Context7 MCP**: 프레임워크별 패턴 및 구현 모범 사례
- **Magic MCP**: UI/UX 작업 협력 및 디자인 시스템 통합
- **Playwright MCP**: 테스트 워크플로우 통합 및 검증 자동화
- **Morphllm MCP**: 대규모 작업 변환 및 패턴 기반 최적화
- **Serena MCP**: 세션 간 작업 지속성 및 프로젝트 메모리 관리

## 도구 협력 (Tool Coordination)
- **TodoWrite**: 에픽 → 스토리 → 태스크 레벨에 걸친 계층적 작업 분해 및 진행 상황 추적
- **Task**: 복잡한 다중 에이전트 협력 및 하위 작업 관리를 위한 고급 위임
- **Read/Write/Edit**: 작업 문서화 및 구현 협력
- **sequentialthinking**: 복잡한 작업 종속성 분석을 위한 구조화된 추론

## 주요 패턴 (Key Patterns)
- **작업 계층 (Task Hierarchy)**: 에픽 레벨 목표 → 스토리 협력 → 태스크 실행 → 서브태스크 세분화
- **전략 선택 (Strategy Selection)**: 체계적(포괄적) → 애자일(반복적) → 엔터프라이즈(거버넌스)
- **다중 에이전트 협력 (Multi-Agent Coordination)**: 페르소나 활성화 → MCP 라우팅 → 병렬 실행 → 결과 통합
- **세션 간 관리 (Cross-Session Management)**: 작업 지속성 → 컨텍스트 연속성 → 점진적 향상

## 예시 (Examples)

### 복잡한 기능 개발
```
/sc:task create "enterprise authentication system" --strategy systematic --parallel
# 다중 도메인 협력을 통한 포괄적인 작업 분해
# 아키텍트, 보안, 백엔드, 프론트엔드 페르소나 활성화
```

### 애자일 스프린트 협력
```
/sc:task execute "feature backlog" --strategy agile --delegate
# 지능적인 위임을 통한 반복적인 작업 실행
# 스프린트 연속성을 위한 세션 간 지속성
```

### 다중 도메인 통합
```
/sc:task execute "microservices platform" --strategy enterprise --parallel
# 규정 준수 검증을 통한 엔터프라이즈 규모 협력
# 여러 기술 도메인에 걸친 병렬 실행
```

## 경계 (Boundaries)

**수행할 작업:**
- 다중 에이전트 협력 및 지능적인 위임을 통해 복잡한 작업을 실행합니다.
- 세션 간 지속성을 통해 계층적 작업 분해를 제공합니다.
- 최적의 작업 결과를 위해 여러 MCP 서버와 페르소나를 조율합니다.

**수행하지 않을 작업:**
- 고급 오케스트레이션이 필요 없는 간단한 작업을 실행하지 않습니다.
- 속도나 편의를 위해 품질 표준을 타협하지 않습니다.
- 적절한 검증 및 품질 게이트 없이 작동하지 않습니다.
