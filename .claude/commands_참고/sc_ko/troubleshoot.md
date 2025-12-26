---
name: troubleshoot
description: "코드, 빌드, 배포 및 시스템 동작의 문제를 진단하고 해결합니다."
category: utility
complexity: basic
mcp-servers: []
personas: []
---

# /sc:troubleshoot - 문제 진단 및 해결

## 트리거 (Triggers)
- 코드 결함 및 런타임 오류 조사 요청
- 빌드 실패 분석 및 해결 필요
- 성능 문제 진단 및 최적화 요구사항
- 배포 문제 분석 및 시스템 동작 디버깅

## 사용법 (Usage)
```
/sc:troubleshoot [issue] [--type bug|build|performance|deployment] [--trace] [--fix]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 문제 설명을 검토하고 관련 시스템 상태 정보를 수집합니다.
2. **조사 (Investigate)**: 체계적인 패턴 분석을 통해 잠재적인 근본 원인을 식별합니다.
3. **디버그 (Debug)**: 로그 및 상태 검사를 포함한 구조화된 디버깅 절차를 실행합니다.
4. **제안 (Propose)**: 영향 평가 및 위험 평가를 통해 해결책 접근 방식을 검증합니다.
5. **해결 (Resolve)**: 적절한 수정 사항을 적용하고 해결 효과를 확인합니다.

주요 행동:
- 가설 테스트 및 증거 수집을 통한 체계적인 근본 원인 분석
- 다중 도메인 문제 해결 (코드, 빌드, 성능, 배포)
- 포괄적인 문제 분석을 통한 구조화된 디버깅 방법론
- 검증 및 문서화를 통한 안전한 수정 적용

## 도구 협력 (Tool Coordination)
- **Read**: 로그 분석 및 시스템 상태 검사
- **Bash**: 진단 명령어 실행 및 시스템 조사
- **Grep**: 오류 패턴 감지 및 로그 분석
- **Write**: 진단 보고서 및 해결 문서화

## 주요 패턴 (Key Patterns)
- **버그 조사 (Bug Investigation)**: 오류 분석 → 스택 트레이스 검사 → 코드 검사 → 수정 검증
- **빌드 문제 해결 (Build Troubleshooting)**: 빌드 로그 분석 → 종속성 확인 → 구성 검증
- **성능 진단 (Performance Diagnosis)**: 메트릭 분석 → 병목 현상 식별 → 최적화 추천
- **배포 문제 (Deployment Issues)**: 환경 분석 → 구성 확인 → 서비스 검증

## 예시 (Examples)

### 코드 버그 조사
```
/sc:troubleshoot "Null pointer exception in user service" --type bug --trace
# 오류 컨텍스트 및 스택 트레이스의 체계적인 분석
# 근본 원인 식별 및 대상 수정 추천 사항 제공
```

### 빌드 실패 분석
```
/sc:troubleshoot "TypeScript compilation errors" --type build --fix
# 빌드 로그 및 TypeScript 구성 분석
# 일반적인 컴파일 문제에 대한 안전한 수정 자동 적용
```

### 성능 문제 진단
```
/sc:troubleshoot "API response times degraded" --type performance
# 성능 메트릭 분석 및 병목 현상 식별
# 최적화 추천 및 모니터링 가이드 제공
```

### 배포 문제 해결
```
/sc:troubleshoot "Service not starting in production" --type deployment --trace
# 환경 및 구성 분석
# 배포 요구사항 및 종속성의 체계적인 확인
```

## 경계 (Boundaries)

**수행할 작업:**
- 구조화된 디버깅 방법론을 사용하여 체계적인 문제 진단을 실행합니다.
- 포괄적인 문제 분석을 통해 검증된 해결책 접근 방식을 제공합니다.
- 검증 및 상세 해결 문서화와 함께 안전한 수정을 적용합니다.

**수행하지 않을 작업:**
- 적절한 분석 및 사용자 확인 없이 위험한 수정을 적용하지 않습니다.
- 명시적인 허가 및 안전 검증 없이 프로덕션 시스템을 수정하지 않습니다.
- 전체 시스템 영향을 이해하지 않고 아키텍처를 변경하지 않습니다.
