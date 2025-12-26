---
name: save
description: "Serena MCP 통합을 통한 세션 라이프사이클 관리 및 세션 컨텍스트 지속성"
category: session
complexity: standard
mcp-servers: [serena]
personas: []
---

# /sc:save - 세션 컨텍스트 지속성

## 트리거 (Triggers)
- 세션 완료 및 프로젝트 컨텍스트 지속성 필요
- 세션 간 메모리 관리 및 체크포인트 생성 요청
- 프로젝트 이해 보존 및 발견 사항 보관 시나리오
- 세션 라이프사이클 관리 및 진행 상황 추적 요구사항

## 사용법 (Usage)
```
/sc:save [--type session|learnings|context|all] [--summarize] [--checkpoint]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 세션 진행 상황을 검토하고 보존할 가치가 있는 발견 사항을 식별합니다.
2. **지속 (Persist)**: Serena MCP 메모리 관리를 사용하여 세션 컨텍스트 및 학습 내용을 저장합니다.
3. **체크포인트 (Checkpoint)**: 복잡한 세션 및 진행 상황 추적을 위한 복구 지점을 만듭니다.
4. **검증 (Validate)**: 세션 데이터 무결성 및 세션 간 호환성을 확인합니다.
5. **준비 (Prepare)**: 향후 세션에서 원활하게 계속할 수 있도록 세션 컨텍스트를 준비합니다.

주요 행동:
- 메모리 관리 및 세션 간 지속성을 위한 Serena MCP 통합
- 세션 진행 상황 및 중요 작업에 기반한 자동 체크포인트 생성
- 포괄적인 발견 및 패턴 보관을 통한 세션 컨텍스트 보존
- 누적된 프로젝트 통찰력 및 기술적 결정을 통한 세션 간 학습

## MCP 통합 (MCP Integration)
- **Serena MCP**: 세션 관리, 메모리 작업 및 세션 간 지속성을 위한 필수 통합
- **메모리 작업 (Memory Operations)**: 세션 컨텍스트 저장, 체크포인트 생성 및 발견 사항 보관
- **성능 중요 (Performance Critical)**: 메모리 작업 <200ms, 체크포인트 생성 <1s

## 도구 협력 (Tool Coordination)
- **write_memory/read_memory**: 핵심 세션 컨텍스트 지속성 및 검색
- **think_about_collected_information**: 세션 분석 및 발견 사항 식별
- **summarize_changes**: 세션 요약 생성 및 진행 상황 문서화
- **TodoRead**: 자동 체크포인트 트리거를 위한 작업 완료 추적

## 주요 패턴 (Key Patterns)
- **세션 보존 (Session Preservation)**: 발견 사항 분석 → 메모리 지속성 → 체크포인트 생성
- **세션 간 학습 (Cross-Session Learning)**: 컨텍스트 축적 → 패턴 보관 → 향상된 프로젝트 이해
- **진행 상황 추적 (Progress Tracking)**: 작업 완료 → 자동 체크포인트 → 세션 연속성
- **복구 계획 (Recovery Planning)**: 상태 보존 → 체크포인트 검증 → 복원 준비 상태

## 예시 (Examples)

### 기본 세션 저장
```
/sc:save
# 현재 세션 발견 사항 및 컨텍스트를 Serena MCP에 저장
# 세션이 30분을 초과하면 자동으로 체크포인트 생성
```

### 포괄적인 세션 체크포인트
```
/sc:save --type all --checkpoint
# 복구 체크포인트와 함께 전체 세션 보존
# 세션 복원을 위한 모든 학습 내용, 컨텍스트 및 진행 상황 포함
```

### 세션 요약 생성
```
/sc:save --summarize
# 발견 사항 문서화와 함께 세션 요약 생성
# 세션 간 학습 패턴 및 프로젝트 통찰력 업데이트
```

### 발견 사항만 지속
```
/sc:save --type learnings
# 세션 중에 발견된 새로운 패턴과 통찰력만 저장
# 전체 세션 보존 없이 프로젝트 이해도 업데이트
```

## 경계 (Boundaries)

**수행할 작업:**
- 세션 간 지속성을 위해 Serena MCP 통합을 사용하여 세션 컨텍스트를 저장합니다.
- 세션 진행 상황 및 작업 완료에 따라 자동 체크포인트를 만듭니다.
- 향상된 프로젝트 이해를 위해 발견 사항과 패턴을 보존합니다.

**수행하지 않을 작업:**
- 적절한 Serena MCP 통합 및 메모리 접근 없이 작동하지 않습니다.
- 검증 및 무결성 확인 없이 세션 데이터를 저장하지 않습니다.
- 적절한 체크포인트 보존 없이 기존 세션 컨텍스트를 덮어쓰지 않습니다.
