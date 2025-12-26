---
name: analyze
description: "품질, 보안, 성능, 아키텍처 도메인에 걸친 포괄적인 코드 분석"
category: utility
complexity: basic
mcp-servers: []
personas: []
---

# /sc:analyze - 코드 분석 및 품질 평가

## 트리거 (Triggers)
- 프로젝트 또는 특정 컴포넌트에 대한 코드 품질 평가 요청
- 보안 취약점 스캐닝 및 규정 준수 검증 필요
- 성능 병목 현상 식별 및 최적화 계획 요구사항
- 아키텍처 검토 및 기술 부채 평가 요구사항

## 사용법 (Usage)
```
/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]
```

## 행동 흐름 (Behavioral Flow)
1. **탐색 (Discover)**: 언어 감지 및 프로젝트 분석을 사용하여 소스 파일 분류
2. **스캔 (Scan)**: 도메인별 분석 기술 및 패턴 매칭 적용
3. **평가 (Evaluate)**: 심각도 등급 및 영향 평가와 함께 우선순위가 지정된 결과 생성
4. **추천 (Recommend)**: 구현 가이드와 함께 실행 가능한 추천 사항 생성
5. **보고 (Report)**: 메트릭 및 개선 로드맵과 함께 포괄적인 분석 결과 제시

주요 행동:
- 정적 분석과 휴리스틱 평가를 결합한 다중 도메인 분석
- 지능적인 파일 탐색 및 언어별 패턴 인식
- 결과 및 추천 사항의 심각도 기반 우선순위 지정
- 메트릭, 추세 및 실행 가능한 통찰력을 포함한 포괄적인 보고

## 도구 협력 (Tool Coordination)
- **Glob**: 파일 탐색 및 프로젝트 구조 분석
- **Grep**: 패턴 분석 및 코드 검색 작업
- **Read**: 소스 코드 검사 및 구성 분석
- **Bash**: 외부 분석 도구 실행 및 검증
- **Write**: 보고서 생성 및 메트릭 문서화

## 주요 패턴 (Key Patterns)
- **도메인 분석 (Domain Analysis)**: 품질/보안/성능/아키텍처 → 전문화된 평가
- **패턴 인식 (Pattern Recognition)**: 언어 감지 → 적절한 분석 기술
- **심각도 평가 (Severity Assessment)**: 이슈 분류 → 우선순위가 지정된 추천 사항
- **보고서 생성 (Report Generation)**: 분석 결과 → 구조화된 문서

## 예시 (Examples)

### 포괄적인 프로젝트 분석
```
/sc:analyze
# 전체 프로젝트의 다중 도메인 분석
# 주요 결과 및 로드맵이 포함된 포괄적인 보고서 생성
```

### 집중적인 보안 평가
```
/sc:analyze src/auth --focus security --depth deep
# 인증 컴포넌트에 대한 심층 보안 분석
# 상세한 해결 가이드와 함께 취약점 평가
```

### 성능 최적화 분석
```
/sc:analyze --focus performance --format report
# 성능 병목 현상 식별
# 최적화 추천 사항이 포함된 HTML 보고서 생성
```

### 빠른 품질 검사
```
/sc:analyze src/components --focus quality --depth quick
# 컴포넌트 디렉토리에 대한 빠른 품질 평가
# 코드 스멜 및 유지보수성 이슈 식별
```

## 경계 (Boundaries)

**수행할 작업:**
- 여러 도메인에 걸쳐 포괄적인 정적 코드 분석 수행
- 실행 가능한 추천 사항과 함께 심각도 등급이 매겨진 결과 생성
- 메트릭 및 개선 가이드가 포함된 상세 보고서 제공

**수행하지 않을 작업:**
- 코드 컴파일 또는 런타임이 필요한 동적 분석 실행
- 명시적인 사용자 동의 없이 소스 코드 수정 또는 수정 사항 적용
- 가져오기 및 사용 패턴을 넘어선 외부 종속성 분석
