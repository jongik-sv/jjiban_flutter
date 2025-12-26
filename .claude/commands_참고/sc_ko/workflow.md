---
name: workflow
description: "PRD 및 기능 요구사항에서 구조화된 구현 워크플로우를 생성합니다."
category: orchestration
complexity: advanced
mcp-servers: [sequential, context7, magic, playwright, morphllm, serena]
personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
---

# /sc:workflow - 구현 워크플로우 생성기

## 트리거 (Triggers)
- 구현 계획을 위한 PRD 및 기능 명세서 분석
- 개발 프로젝트를 위한 구조화된 워크플로우 생성
- 복잡한 구현 전략을 위한 다중 페르소나 협력
- 세션 간 워크플로우 관리 및 종속성 매핑

## 사용법 (Usage)
```
/sc:workflow [prd-file|feature-description] [--strategy systematic|agile|enterprise] [--depth shallow|normal|deep] [--parallel]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: PRD 및 기능 명세서를 파싱하여 구현 요구사항 이해
2. **계획 (Plan)**: 종속성 매핑 및 작업 오케스트레이션을 통해 포괄적인 워크플로우 구조 생성
3. **협력 (Coordinate)**: 도메인 전문 지식 및 구현 전략을 위해 여러 페르소나 활성화
4. **실행 (Execute)**: 자동화된 작업 협력을 통해 구조화된 단계별 워크플로우 생성
5. **검증 (Validate)**: 품질 게이트 적용 및 여러 도메인에 걸쳐 워크플로우 완전성 보장

주요 행동:
- 아키텍처, 프론트엔드, 백엔드, 보안 및 데브옵스 도메인에 걸친 다중 페르소나 오케스트레이션
- 전문 워크플로우 분석을 위한 지능적인 라우팅을 통한 고급 MCP 협력
- 점진적인 워크플로우 향상 및 병렬 처리를 통한 체계적인 실행
- 포괄적인 종속성 추적을 통한 세션 간 워크플로우 관리

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 복잡한 다단계 워크플로우 분석 및 체계적인 구현 계획
- **Context7 MCP**: 프레임워크별 워크플로우 패턴 및 구현 모범 사례
- **Magic MCP**: UI/UX 워크플로우 생성 및 디자인 시스템 통합 전략
- **Playwright MCP**: 테스트 워크플로우 통합 및 품질 보증 자동화
- **Morphllm MCP**: 대규모 워크플로우 변환 및 패턴 기반 최적화
- **Serena MCP**: 세션 간 워크플로우 지속성, 메모리 관리 및 프로젝트 컨텍스트

## 도구 협력 (Tool Coordination)
- **Read/Write/Edit**: PRD 분석 및 워크플로우 문서 생성
- **TodoWrite**: 복잡한 다단계 워크플로우 실행을 위한 진행 상황 추적
- **Task**: 병렬 워크플로우 생성 및 다중 에이전트 협력을 위한 고급 위임
- **WebSearch**: 기술 연구, 프레임워크 검증 및 구현 전략 분석
- **sequentialthinking**: 복잡한 워크플로우 종속성 분석을 위한 구조화된 추론

## 주요 패턴 (Key Patterns)
- **PRD 분석 (PRD Analysis)**: 문서 파싱 → 요구사항 추출 → 구현 전략 개발
- **워크플로우 생성 (Workflow Generation)**: 작업 분해 → 종속성 매핑 → 구조화된 구현 계획
- **다중 도메인 협력 (Multi-Domain Coordination)**: 교차 기능 전문 지식 → 포괄적인 구현 전략
- **품질 통합 (Quality Integration)**: 워크플로우 검증 → 테스트 전략 → 배포 계획

## 예시 (Examples)

### 체계적인 PRD 워크플로우
```
/sc:workflow ClaudeDocs/PRD/feature-spec.md --strategy systematic --depth deep
# 체계적인 워크플로우 생성을 통한 포괄적인 PRD 분석
# 완전한 구현 전략을 위한 다중 페르소나 협력
```

### 애자일 기능 워크플로우
```
/sc:workflow "user authentication system" --strategy agile --parallel
# 병렬 작업 협력을 통한 애자일 워크플로우 생성
# 프레임워크 및 UI 워크플로우 패턴을 위한 Context7 및 Magic MCP
```

### 엔터프라이즈 구현 계획
```
/sc:workflow enterprise-prd.md --strategy enterprise --validate
# 포괄적인 검증을 통한 엔터프라이즈 규모 워크플로우
# 규정 준수 및 확장성을 위한 보안, 데브옵스 및 아키텍트 페르소나
```

### 세션 간 워크플로우 관리
```
/sc:workflow project-brief.md --depth normal
# Serena MCP가 세션 간 워크플로우 컨텍스트 및 지속성 관리
# 메모리 기반 통찰력을 통한 점진적인 워크플로우 향상
```

## 경계 (Boundaries)

**수행할 작업:**
- PRD 및 기능 명세서에서 포괄적인 구현 워크플로우를 생성합니다.
- 완전한 구현 전략을 위해 여러 페르소나와 MCP 서버를 조율합니다.
- 세션 간 워크플로우 관리 및 점진적 향상 기능을 제공합니다.

**수행하지 않을 작업:**
- 워크플로우 계획 및 전략을 넘어선 실제 구현 작업을 실행하지 않습니다.
- 적절한 분석 및 검증 없이 수립된 개발 프로세스를 무시하지 않습니다.
- 포괄적인 요구사항 분석 및 종속성 매핑 없이 워크플로우를 생성하지 않습니다.
