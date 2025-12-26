---
name: improve
description: "코드 품질, 성능 및 유지보수성을 체계적으로 개선합니다."
category: workflow
complexity: standard
mcp-servers: [sequential, context7]
personas: [architect, performance, quality, security]
---

# /sc:improve - 코드 개선

## 트리거 (Triggers)
- 코드 품질 향상 및 리팩토링 요청
- 성능 최적화 및 병목 현상 해결 필요
- 유지보수성 개선 및 기술 부채 감소
- 모범 사례 적용 및 코딩 표준 강제

## 사용법 (Usage)
```
/sc:improve [target] [--type quality|performance|maintainability|style] [--safe] [--interactive]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 개선 기회 및 품질 문제를 위해 코드베이스를 검토합니다.
2. **계획 (Plan)**: 개선 접근 방식을 선택하고 전문 지식을 위해 관련 페르소나를 활성화합니다.
3. **실행 (Execute)**: 도메인별 모범 사례를 사용하여 체계적인 개선을 적용합니다.
4. **검증 (Validate)**: 개선 사항이 기능을 보존하고 품질 표준을 충족하는지 확인합니다.
5. **문서화 (Document)**: 개선 요약 및 향후 작업을 위한 추천 사항을 생성합니다.

주요 행동:
- 개선 유형에 따른 다중 페르소나(아키텍트, 성능, 품질, 보안) 협력
- 모범 사례를 위한 Context7 통합을 통한 프레임워크별 최적화
- 복잡한 다중 컴포넌트 개선을 위한 Sequential MCP를 통한 체계적인 분석
- 포괄적인 검증 및 롤백 기능을 갖춘 안전한 리팩토링

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 복잡한 다단계 개선 분석 및 계획을 위해 자동 활성화
- **Context7 MCP**: 프레임워크별 모범 사례 및 최적화 패턴
- **페르소나 협력 (Persona Coordination)**: 아키텍트(구조), 성능(속도), 품질(유지보수성), 보안(안전)

## 도구 협력 (Tool Coordination)
- **Read/Grep/Glob**: 코드 분석 및 개선 기회 식별
- **Edit/MultiEdit**: 안전한 코드 수정 및 체계적인 리팩토링
- **TodoWrite**: 복잡한 다중 파일 개선 작업을 위한 진행 상황 추적
- **Task**: 체계적인 협력이 필요한 대규모 개선 워크플로우 위임

## 주요 패턴 (Key Patterns)
- **품질 개선 (Quality Improvement)**: 코드 분석 → 기술 부채 식별 → 리팩토링 적용
- **성능 최적화 (Performance Optimization)**: 프로파일링 분석 → 병목 현상 식별 → 최적화 구현
- **유지보수성 향상 (Maintainability Enhancement)**: 구조 분석 → 복잡성 감소 → 문서 개선
- **보안 강화 (Security Hardening)**: 취약점 분석 → 보안 패턴 적용 → 검증 확인

## 예시 (Examples)

### 코드 품질 향상
```
/sc:improve src/ --type quality --safe
# 안전한 리팩토링 적용을 통한 체계적인 품질 분석
# 코드 구조 개선, 기술 부채 감소, 가독성 향상
```

### 성능 최적화
```
/sc:improve api-endpoints --type performance --interactive
# 성능 페르소나가 병목 현상 및 최적화 기회 분석
# 복잡한 성능 개선 결정을 위한 대화형 안내
```

### 유지보수성 개선
```
/sc:improve legacy-modules --type maintainability --preview
# 아키텍트 페르소나가 구조를 분석하고 유지보수성 개선 제안
# 검토를 위해 적용 전 변경 사항을 보여주는 미리보기 모드
```

### 보안 강화
```
/sc:improve auth-service --type security --validate
# 보안 페르소나가 취약점을 식별하고 보안 패턴 적용
# 포괄적인 검증으로 보안 개선 효과 보장
```

## 경계 (Boundaries)

**수행할 작업:**
- 도메인별 전문 지식과 검증을 통해 체계적인 개선을 적용합니다.
- 다중 페르소나 협력 및 모범 사례를 통해 포괄적인 분석을 제공합니다.
- 롤백 기능 및 품질 보존을 통해 안전한 리팩토링을 실행합니다.

**수행하지 않을 작업:**
- 적절한 분석 및 사용자 확인 없이 위험한 개선을 적용하지 않습니다.
- 전체 시스템 영향을 이해하지 않고 아키텍처를 변경하지 않습니다.
- 수립된 코딩 표준 또는 프로젝트별 규칙을 무시하지 않습니다.
