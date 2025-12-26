---
name: document
description: "컴포넌트, 함수, API 및 기능에 대한 집중적인 문서를 생성합니다."
category: utility
complexity: basic
mcp-servers: []
personas: []
---

# /sc:document - 집중적인 문서 생성

## 트리거 (Triggers)
- 특정 컴포넌트, 함수 또는 기능에 대한 문서 요청
- API 문서 및 참고 자료 생성 필요
- 코드 주석 및 인라인 문서 요구사항
- 사용자 가이드 및 기술 문서 작성 요청

## 사용법 (Usage)
```
/sc:document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 대상 컴포넌트 구조, 인터페이스 및 기능 검토
2. **식별 (Identify)**: 문서 요구사항 및 대상 독자 컨텍스트 결정
3. **생성 (Generate)**: 유형 및 스타일에 따라 적절한 문서 콘텐츠 생성
4. **형식화 (Format)**: 일관된 구조 및 조직 패턴 적용
5. **통합 (Integrate)**: 기존 프로젝트 문서 생태계와의 호환성 보장

주요 행동:
- API 추출 및 사용 패턴 식별을 통한 코드 구조 분석
- 다중 형식 문서 생성 (인라인, 외부, API 참조, 가이드)
- 일관된 서식 및 상호 참조 통합
- 언어별 문서 패턴 및 규칙

## 도구 협력 (Tool Coordination)
- **Read**: 컴포넌트 분석 및 기존 문서 검토
- **Grep**: 참조 추출 및 패턴 식별
- **Write**: 적절한 서식으로 문서 파일 생성
- **Glob**: 다중 파일 문서 프로젝트 및 구성

## 주요 패턴 (Key Patterns)
- **인라인 문서 (Inline Documentation)**: 코드 분석 → JSDoc/docstring 생성 → 인라인 주석
- **API 문서 (API Documentation)**: 인터페이스 추출 → 참고 자료 → 사용 예시
- **사용자 가이드 (User Guides)**: 기능 분석 → 튜토리얼 콘텐츠 → 구현 가이드
- **외부 문서 (External Docs)**: 컴포넌트 개요 → 상세 명세서 → 통합 지침

## 예시 (Examples)

### 인라인 코드 문서화
```
/sc:document src/auth/login.js --type inline
# 매개변수 및 반환 값 설명이 포함된 JSDoc 주석 생성
# 함수 및 클래스에 대한 포괄적인 인라인 문서 추가
```

### API 참조 생성
```
/sc:document src/api --type api --style detailed
# 엔드포인트 및 스키마가 포함된 포괄적인 API 문서 생성
# 사용 예시 및 통합 가이드라인 생성
```

### 사용자 가이드 작성
```
/sc:document payment-module --type guide --style brief
# 실용적인 예시가 포함된 사용자 중심 문서 생성
# 구현 패턴 및 일반적인 사용 사례에 집중
```

### 컴포넌트 문서화
```
/sc:document components/ --type external
# 컴포넌트 라이브러리에 대한 외부 문서 파일 생성
# props, 사용 예시 및 통합 패턴 포함
```

## 경계 (Boundaries)

**수행할 작업:**
- 특정 컴포넌트 및 기능에 대한 집중적인 문서를 생성합니다.
- 대상 독자의 필요에 따라 여러 문서 형식을 만듭니다.
- 기존 문서 생태계와 통합하고 일관성을 유지합니다.

**수행하지 않을 작업:**
- 적절한 코드 분석 및 컨텍스트 이해 없이 문서를 생성하지 않습니다.
- 기존 문서 표준 또는 프로젝트별 규칙을 무시하지 않습니다.
- 민감한 구현 세부 정보를 노출하는 문서를 만들지 않습니다.
