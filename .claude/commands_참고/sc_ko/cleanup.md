---
name: cleanup
description: "체계적으로 코드를 정리하고, 데드 코드를 제거하며, 프로젝트 구조를 최적화합니다."
category: workflow
complexity: standard
mcp-servers: [sequential, context7]
personas: [architect, quality, security]
---

# /sc:cleanup - 코드 및 프로젝트 정리

## 트리거 (Triggers)
- 코드 유지보수 및 기술 부채 감소 요청
- 데드 코드 제거 및 임포트 최적화 필요
- 프로젝트 구조 개선 및 조직화 요구사항
- 코드베이스 위생 및 품질 개선 계획

## 사용법 (Usage)
```
/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--interactive]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 대상 범위에 걸쳐 정리 기회와 안전 고려사항을 평가합니다.
2. **계획 (Plan)**: 정리 접근 방식을 선택하고 도메인 전문 지식을 위해 관련 페르소나를 활성화합니다.
3. **실행 (Execute)**: 지능적인 데드 코드 감지 및 제거를 통해 체계적인 정리를 적용합니다.
4. **검증 (Validate)**: 테스트 및 안전 검증을 통해 기능 손실이 없는지 확인합니다.
5. **보고 (Report)**: 지속적인 유지보수를 위한 추천 사항과 함께 정리 요약을 생성합니다.

주요 행동:
- 정리 유형에 따라 다중 페르소나(아키텍트, 품질, 보안) 협력
- Context7 MCP 통합을 통한 프레임워크별 정리 패턴
- 복잡한 정리 작업을 위한 Sequential MCP를 통한 체계적인 분석
- 백업 및 롤백 기능을 갖춘 안전 우선 접근 방식

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 복잡한 다단계 정리 분석 및 계획을 위해 자동 활성화
- **Context7 MCP**: 프레임워크별 정리 패턴 및 모범 사례
- **페르소나 협력 (Persona Coordination)**: 아키텍트(구조), 품질(부채), 보안(자격 증명)

## 도구 협력 (Tool Coordination)
- **Read/Grep/Glob**: 정리 기회를 위한 코드 분석 및 패턴 감지
- **Edit/MultiEdit**: 안전한 코드 수정 및 구조 최적화
- **TodoWrite**: 복잡한 다중 파일 정리 작업을 위한 진행 상황 추적
- **Task**: 체계적인 협력이 필요한 대규모 정리 워크플로우 위임

## 주요 패턴 (Key Patterns)
- **데드 코드 감지 (Dead Code Detection)**: 사용량 분석 → 종속성 검증을 통한 안전한 제거
- **임포트 최적화 (Import Optimization)**: 종속성 분석 → 사용하지 않는 임포트 제거 및 구성
- **구조 정리 (Structure Cleanup)**: 아키텍처 분석 → 파일 구성 및 모듈식 개선
- **안전 검증 (Safety Validation)**: 정리 전/중/후 확인 → 전체 정리 과정에서 기능 보존

## 예시 (Examples)

### 안전한 코드 정리
```
/sc:cleanup src/ --type code --safe
# 자동 안전 검증을 통한 보수적인 정리
# 모든 기능을 보존하면서 데드 코드 제거
```

### 임포트 최적화
```
/sc:cleanup --type imports --preview
# 실행 없이 사용하지 않는 임포트 정리 분석 및 표시
# Context7 패턴을 통한 프레임워크 인식 최적화
```

### 포괄적인 프로젝트 정리
```
/sc:cleanup --type all --interactive
# 복잡한 결정을 위한 사용자 안내가 포함된 다중 도메인 정리
# 포괄적인 분석을 위해 모든 페르소나 활성화
```

### 프레임워크별 정리
```
/sc:cleanup components/ --aggressive
# Context7 프레임워크 패턴을 사용한 철저한 정리
# 복잡한 종속성 관리를 위한 순차 분석
```

## 경계 (Boundaries)

**수행할 작업:**
- 체계적으로 코드를 정리하고, 데드 코드를 제거하며, 프로젝트 구조를 최적화합니다.
- 백업 및 롤백 기능을 포함한 포괄적인 안전 검증을 제공합니다.
- 프레임워크별 패턴 인식을 통해 지능적인 정리 알고리즘을 적용합니다.

**수행하지 않을 작업:**
- 철저한 안전 분석 및 검증 없이 코드를 제거하지 않습니다.
- 프로젝트별 정리 제외 항목이나 아키텍처 제약 조건을 무시하지 않습니다.
- 기능을 손상시키거나 버그를 유발하는 정리 작업을 적용하지 않습니다.
