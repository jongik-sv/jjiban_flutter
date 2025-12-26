---
name: spawn
description: "지능적인 분해 및 위임을 통한 메타 시스템 작업 오케스트레이션"
category: special
complexity: high
mcp-servers: []
personas: []
---

# /sc:spawn - 메타 시스템 작업 오케스트레이션

## 트리거 (Triggers)
- 지능적인 작업 분해가 필요한 복잡한 다중 도메인 작업
- 여러 기술 영역에 걸친 대규모 시스템 작업
- 병렬 협력 및 종속성 관리가 필요한 작업
- 표준 명령어 기능을 넘어서는 메타 레벨 오케스트레이션

## 사용법 (Usage)
```
/sc:spawn [complex-task] [--strategy sequential|parallel|adaptive] [--depth normal|deep]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 복잡한 작업 요구사항을 파싱하고 여러 도메인에 걸쳐 범위 평가
2. **분해 (Decompose)**: 작업을 협력된 하위 작업 계층 구조로 분해
3. **오케스트레이션 (Orchestrate)**: 최적의 협력 전략(병렬/순차)을 사용하여 작업 실행
4. **모니터링 (Monitor)**: 종속성 관리를 통해 작업 계층 구조 전반의 진행 상황 추적
5. **통합 (Integrate)**: 결과 집계 및 포괄적인 오케스트레이션 요약 제공

주요 행동:
- 에픽 → 스토리 → 태스크 → 서브태스크 분해를 통한 메타 시스템 작업 분해
- 작업 특성에 기반한 지능적인 협력 전략 선택
- 병렬 및 순차 실행 패턴을 사용한 교차 도메인 작업 관리
- 작업 계층 구조 전반의 고급 종속성 분석 및 자원 최적화

## MCP 통합 (MCP Integration)
- **네이티브 오케스트레이션 (Native Orchestration)**: 메타 시스템 명령어는 MCP 종속성 없이 네이티브 협력을 사용
- **점진적 통합 (Progressive Integration)**: 점진적 향상을 위한 체계적인 실행과의 협력
- **프레임워크 통합 (Framework Integration)**: SuperClaude 오케스트레이션 계층과의 고급 통합

## 도구 협력 (Tool Coordination)
- **TodoWrite**: 에픽 → 스토리 → 태스크 레벨에 걸친 계층적 작업 분해 및 진행 상황 추적
- **Read/Grep/Glob**: 복잡한 작업을 위한 시스템 분석 및 종속성 매핑
- **Edit/MultiEdit/Write**: 병렬 및 순차 실행을 사용한 협력된 파일 작업
- **Bash**: 지능적인 자원 관리를 통한 시스템 레벨 작업 협력

## 주요 패턴 (Key Patterns)
- **계층적 분해 (Hierarchical Breakdown)**: 에픽 레벨 작업 → 스토리 협력 → 태스크 실행 → 서브태스크 세분화
- **전략 선택 (Strategy Selection)**: 순차(종속성 순서) → 병렬(독립적) → 적응형(동적)
- **메타 시스템 협력 (Meta-System Coordination)**: 교차 도메인 작업 → 자원 최적화 → 결과 통합
- **점진적 향상 (Progressive Enhancement)**: 체계적인 실행 → 품질 게이트 → 포괄적인 검증

## 예시 (Examples)

### 복잡한 기능 구현
```
/sc:spawn "implement user authentication system"
# 분해: 데이터베이스 설계 → 백엔드 API → 프론트엔드 UI → 테스트
# 종속성 관리를 통해 여러 도메인에 걸쳐 협력
```

### 대규모 시스템 작업
```
/sc:spawn "migrate legacy monolith to microservices" --strategy adaptive --depth deep
# 정교한 오케스트레이션을 통한 엔터프라이즈 규모 작업
# 작업 특성에 기반한 적응형 협력
```

### 교차 도메인 인프라
```
/sc:spawn "establish CI/CD pipeline with security scanning"
# DevOps, 보안, 품질 도메인에 걸친 시스템 전반의 인프라 작업
# 검증 게이트를 통한 독립적인 컴포넌트의 병렬 실행
```

## 경계 (Boundaries)

**수행할 작업:**
- 복잡한 다중 도메인 작업을 협력된 작업 계층 구조로 분해합니다.
- 병렬 및 순차 협력 전략을 통해 지능적인 오케스트레이션을 제공합니다.
- 표준 명령어 기능을 넘어서는 메타 시스템 작업을 실행합니다.

**수행하지 않을 작업:**
- 간단한 작업에 대해 도메인별 명령어를 대체하지 않습니다.
- 사용자 협력 선호도나 실행 전략을 무시하지 않습니다.
- 적절한 종속성 분석 및 검증 없이 작업을 실행하지 않습니다.
