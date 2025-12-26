---
name: estimate
description: "지능적인 분석을 통해 작업, 기능 또는 프로젝트에 대한 개발 추정치를 제공합니다."
category: special
complexity: standard
mcp-servers: [sequential, context7]
personas: [architect, performance, project-manager]
---

# /sc:estimate - 개발 추정

## 트리거 (Triggers)
- 시간, 노력 또는 복잡성 추정이 필요한 개발 계획
- 프로젝트 범위 설정 및 자원 할당 결정
- 체계적인 추정 방법론이 필요한 기능 분할
- 위험 평가 및 신뢰 구간 분석 요구사항

## 사용법 (Usage)
```
/sc:estimate [target] [--type time|effort|complexity] [--unit hours|days|weeks] [--breakdown]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 범위, 복잡성 요인, 종속성 및 프레임워크 패턴을 검토합니다.
2. **계산 (Calculate)**: 과거 벤치마크 및 복잡성 점수를 사용하여 추정 방법론을 적용합니다.
3. **검증 (Validate)**: 프로젝트 패턴 및 도메인 전문 지식과 추정치를 교차 확인합니다.
4. **제시 (Present)**: 신뢰 구간 및 위험 평가와 함께 상세한 분석을 제공합니다.
5. **추적 (Track)**: 지속적인 방법론 개선을 위해 추정 정확도를 문서화합니다.

주요 행동:
- 추정 범위에 따른 다중 페르소나(아키텍트, 성능, 프로젝트 관리자) 협력
- 체계적인 분석 및 복잡성 평가를 위한 Sequential MCP 통합
- 프레임워크별 패턴 및 과거 벤치마크를 위한 Context7 MCP 통합
- 신뢰 구간 및 위험 요소를 포함한 지능적인 분석

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 복잡한 다단계 추정 분석 및 체계적인 복잡성 평가
- **Context7 MCP**: 프레임워크별 추정 패턴 및 과거 벤치마크 데이터
- **페르소나 협력 (Persona Coordination)**: 아키텍트(설계 복잡성), 성능(최적화 노력), 프로젝트 관리자(타임라인)

## 도구 협력 (Tool Coordination)
- **Read/Grep/Glob**: 복잡성 평가 및 범위 평가를 위한 코드베이스 분석
- **TodoWrite**: 복잡한 추정 워크플로우를 위한 추정 분석 및 진행 상황 추적
- **Task**: 체계적인 협력이 필요한 다중 도메인 추정을 위한 고급 위임
- **Bash**: 정확한 복잡성 점수를 위한 프로젝트 분석 및 종속성 평가

## 주요 패턴 (Key Patterns)
- **범위 분석 (Scope Analysis)**: 프로젝트 요구사항 → 복잡성 요인 → 프레임워크 패턴 → 위험 평가
- **추정 방법론 (Estimation Methodology)**: 시간 기반 → 노력 기반 → 복잡성 기반 → 비용 기반 접근 방식
- **다중 도메인 평가 (Multi-Domain Assessment)**: 아키텍처 복잡성 → 성능 요구사항 → 프로젝트 타임라인
- **검증 프레임워크 (Validation Framework)**: 과거 벤치마크 → 교차 검증 → 신뢰 구간 → 정확도 추적

## 예시 (Examples)

### 기능 개발 추정
```
/sc:estimate "user authentication system" --type time --unit days --breakdown
# 체계적인 분석: 데이터베이스 설계 (2일) + 백엔드 API (3일) + 프론트엔드 UI (2일) + 테스트 (1일)
# 총계: 85% 신뢰 구간으로 8일
```

### 프로젝트 복잡성 평가
```
/sc:estimate "migrate monolith to microservices" --type complexity --breakdown
# 위험 요소 및 종속성 매핑을 포함한 아키텍처 복잡성 분석
# 포괄적인 평가를 위한 다중 페르소나 협력
```

### 성능 최적화 노력
```
/sc:estimate "optimize application performance" --type effort --unit hours
# 벤치마크 비교를 통한 성능 페르소나 분석
# 최적화 범주 및 예상 영향별 노력 분석
```

## 경계 (Boundaries)

**수행할 작업:**
- 신뢰 구간 및 위험 평가를 포함한 체계적인 개발 추정치를 제공합니다.
- 포괄적인 복잡성 분석을 위해 다중 페르소나 협력을 적용합니다.
- 과거 벤치마크 비교를 통해 상세한 분석을 생성합니다.

**수행하지 않을 작업:**
- 적절한 범위 분석 및 검증 없이 추정 정확도를 보장하지 않습니다.
- 적절한 도메인 전문 지식 및 복잡성 평가 없이 추정치를 제공하지 않습니다.
- 명확한 정당성 및 분석 없이 과거 벤치마크를 무시하지 않습니다.
