---
name: design
description: "포괄적인 명세서를 통해 시스템 아키텍처, API 및 컴포넌트 인터페이스를 설계합니다."
category: utility
complexity: basic
mcp-servers: []
personas: []
---

# /sc:design - 시스템 및 컴포넌트 설계

## 트리거 (Triggers)
- 아키텍처 기획 및 시스템 설계 요청
- API 명세서 및 인터페이스 설계 필요
- 컴포넌트 설계 및 기술 명세서 요구사항
- 데이터베이스 스키마 및 데이터 모델 설계 요청

## 사용법 (Usage)
```
/sc:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 대상 요구사항과 기존 시스템 컨텍스트를 검토합니다.
2. **계획 (Plan)**: 유형 및 형식에 따라 설계 접근 방식과 구조를 정의합니다.
3. **설계 (Design)**: 업계 모범 사례를 바탕으로 포괄적인 명세서를 작성합니다.
4. **검증 (Validate)**: 설계가 요구사항과 유지보수성 표준을 충족하는지 확인합니다.
5. **문서화 (Document)**: 다이어그램과 명세서로 명확한 설계 문서를 생성합니다.

주요 행동:
- 확장성을 고려한 요구사항 기반 설계 접근 방식
- 유지보수 가능한 솔루션을 위한 업계 모범 사례 통합
- 필요에 따른 다중 형식 출력 (다이어그램, 명세서, 코드)
- 기존 시스템 아키텍처 및 제약 조건에 대한 검증

## 도구 협력 (Tool Coordination)
- **Read**: 요구사항 분석 및 기존 시스템 검토
- **Grep/Glob**: 패턴 분석 및 시스템 구조 조사
- **Write**: 설계 문서 및 명세서 생성
- **Bash**: 필요 시 외부 설계 도구 통합

## 주요 패턴 (Key Patterns)
- **아키텍처 설계 (Architecture Design)**: 요구사항 → 시스템 구조 → 확장성 기획
- **API 설계 (API Design)**: 인터페이스 명세서 → RESTful/GraphQL 패턴 → 문서화
- **컴포넌트 설계 (Component Design)**: 기능적 요구사항 → 인터페이스 설계 → 구현 가이드
- **데이터베이스 설계 (Database Design)**: 데이터 요구사항 → 스키마 설계 → 관계 모델링

## 예시 (Examples)

### 시스템 아키텍처 설계
```
/sc:design user-management-system --type architecture --format diagram
# 컴포넌트 관계를 포함한 포괄적인 시스템 아키텍처 생성
# 확장성 고려사항 및 모범 사례 포함
```

### API 명세서 설계
```
/sc:design payment-api --type api --format spec
# 엔드포인트와 데이터 모델을 포함한 상세 API 명세서 생성
# RESTful 설계 원칙 및 업계 표준 준수
```

### 컴포넌트 인터페이스 설계
```
/sc:design notification-service --type component --format code
# 명확한 계약과 종속성을 가진 컴포넌트 인터페이스 설계
# 구현 가이드 및 통합 패턴 제공
```

### 데이터베이스 스키마 설계
```
/sc:design e-commerce-db --type database --format diagram
# 엔티티 관계와 제약 조건을 포함한 데이터베이스 스키마 생성
# 정규화 및 성능 고려사항 포함
```

## 경계 (Boundaries)

**수행할 작업:**
- 업계 모범 사례를 바탕으로 포괄적인 설계 명세서를 작성합니다.
- 요구사항에 따라 여러 형식의 출력(다이어그램, 명세서, 코드)을 생성합니다.
- 유지보수성 및 확장성 표준에 대해 설계를 검증합니다.

**수행하지 않을 작업:**
- 실제 구현 코드를 생성하지 않습니다 (구현은 /sc:implement 사용).
- 명시적인 설계 승인 없이 기존 시스템 아키텍처를 수정하지 않습니다.
- 기존에 수립된 아키텍처 제약 조건을 위반하는 설계를 생성하지 않습니다.
