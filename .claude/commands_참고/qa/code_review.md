---
name: qa:code_review
description: "Code Review 설계-구현 일관성 검증 (최적화 버전)"
category: analysis
complexity: enhanced
wave-enabled: false
performance-profile: optimized
auto-flags:
  - --seq
  - --token-efficient
mcp-servers: [sequential]
personas: [system-architect, security-engineer, quality-engineer]
---

# /qa:code_review - 코드 리뷰 분석 (v1)

> **최적화된 코드 리뷰**: 다른 LLM을 활용한 설계-구현 일관성 검증을 통해 불일치성을 분석하고 개선 제안을 제공합니다.

## 🎯 최적화 목표
- **토큰 효율성**: 30% 토큰 절약
- **다중 LLM 활용**: 다른 LLM 결과와 분리 유지
- **체계적 검증**: 우선순위 기반 이슈 분류
- **실행 가능성**: 구체적이고 실행 가능한 개선 제안

## 트리거
- Task 구현 후 설계-구현 일관성 검증이 필요한 경우
- 설계 문서와 실제 코드 간의 불일치 분석이 필요한 경우
- 다른 LLM을 통한 객관적 검증이 필요한 경우

## 사용법
```bash
# Task 번호로 실행 (권장)
/qa:code_review Task 3.1
/qa:code_review 3.1

# 기존 방식도 지원
/qa:code_review "Task-3-1"
/qa:code_review "Task 3.2"
```

## 자동 실행 플로우

### 1단계: 교차 검증 범위 확인 및 문서 수집
**Auto-Persona**: system-architect
**MCP**: sequential

**자동 실행 단계**:
1. **Task 정보 추출 및 파싱**:
   ```javascript
   // "/qa:code_review Task 3.1" 또는 "/qa:code_review 3.1"에서 Task 번호 추출
   function parseTaskFromCommand(input) {
       const taskPattern = /(?:Task\s+)?(\d+\.\d+)/i;
       return input.match(taskPattern)?.[1]; // "3.1" 추출
   }
   ```

2. **공통 문서 분석 함수 호출**: `analyze_project_context(task_number)`
   - 📋 함수 참조: `@docs/common/07.functions/analyze_project_context.md`
   - `./docs/project/maru/00.foundation/01.project-charter/tasks.md`에서 Task 정보 조회
   - 자동 파일명 생성: `{task-id}.{task명}(code-check)_{llm}_{date}.md`
     - 예: `Task-3-1.MR0100-Backend-API-구현(code-check)_claude_20241224.md`
   - 프로젝트 정보 및 Task 상세 정보 수집
   - 교차 검증 대상 문서 자동 수집
   - 검증 범위 및 기준 설정
2. **추가 코드 리뷰 참조 문서** 수집:
   - 구현 보고서: `./docs/project/[Project Name]/20.implementation/{task-id}.{task명}(implementation).md`
   - 테스트 결과서 (있는 경우)
   - 소스 코드 분석

### 2단계: 소스 코드 분석 및 매핑
**Auto-Persona**: system-architect
**MCP**: sequential

**자동 실행 단계**:
1. **구현된 소스 코드 분석**:
   - Backend API 구조 및 로직 분석
   - Frontend 화면 구성 및 연동 분석
   - 데이터베이스 스키마 및 관계 분석
2. **설계 대비 구현 매핑**:
   - 상세설계서의 요구사항 vs 실제 구현
   - API 명세 vs 구현된 엔드포인트
   - 화면 설계 vs 구현된 UI
   - 데이터 모델 vs 데이터베이스 스키마

### 3단계: 일관성 검증 및 이슈 도출 (다른 LLM 권장)
**Auto-Persona**: system-architect + security-engineer + quality-engineer
**MCP**: sequential
**권장 LLM**: Claude 대신 Gemini, GPT-5 등 다른 LLM 활용

**자동 실행 단계**:
1. **설계-구현 일관성 검증**:
   - 기능적 요구사항 충족도 검증
   - 비기능적 요구사항 (성능, 보안) 검증
   - 인터페이스 설계 일관성 검증
2. **코드 품질 및 보안 검증**:
   - 코딩 표준 및 패턴 준수 검증
   - 보안 취약점 및 리스크 분석
   - 성능 최적화 가능성 분석
3. **테스트 커버리지 및 품질 검증**:
   - 테스트 케이스 완전성 검증
   - 예외 처리 및 경계 조건 검증
   - 사용성 및 접근성 검증
4. **심각도(Severity) 분류**:
   - ⚠️ Critical: 시스템 전체 중단, 데이터 손실, 보안 이슈
   - ❗ High: 핵심 기능 오류, 다수 사용자 영향
   - 🔧 Medium: 부분적 기능 제한, 사용성 저하
   - 📝 Low: 경미한 불편, UI/문구/미관 문제
   - ℹ️ Info: 기타 문제, 경고 수준
5. **우선순위(Priority) 할당**:
   - 🔴 P1 (즉시 해결): 운영 차질, 고객 불만 폭주, 보안 위협
   - 🟠 P2 (빠른 해결): 주요 기능 저하, 다수 사용자 영향
   - 🟡 P3 (보통 해결): 단기적 우회 가능, 영향 제한적
   - 🟢 P4 (개선 항목): 장기 개선, 경미한 사항
   - 🔵 P5 (보류 항목): 보류 항목
6. **매트릭스 기반 분류**: 심각도와 우선순위를 조합한 종합 평가   

### 4단계: Code Review 보고서 생성
**Auto-Persona**: technical-writer
**MCP**: sequential

**자동 실행 단계**:
1. **검증 결과 종합**:
   - 발견된 이슈 목록 정리
   - 우선순위 분류 (P1: 치명적 → P5: 개선)
   - 영향도 및 해결 난이도 평가
2. **개선사항 제안**:
   - 구체적이고 실행 가능한 해결 방안
   - 코드 예시 또는 설계 변경사항 포함
   - 비용-효과 분석 및 일정 추정
3. **Code Review 보고서 작성**:
   - 검증 범위 및 방법론 기술
   - 이슈 및 개선사항 상세 기술
   - 다음 단계 권장사항 제시
4. **Task 상태 업데이트**: `update_task_status(task_number, "code_review")`
   - 📋 함수 참조: `@docs/common/07.functions/update_task_status.md`
   - tasks.md에서 Task 체크박스를 [c]로 변경
   - 진행 상태를 **[d→i→c]**로 표시

## 🎯 최적화 특징

### 🔍 다중 LLM 교차 검증
- Claude 외 Gemini, GPT-5 등 다른 LLM 활용 권장
- 각 LLM의 강점을 활용한 검증 관점 다양화
- 편향 방지 및 객관성 확보

### 📊 체계적 이슈 분류
- P1-P5 우선순위 기반 이슈 관리
- 영향도 및 해결 난이도 매트릭스 적용
- 실행 가능성 중심의 개선안 제시

### ⚡ 토큰 효율성
- 공통 문서 분석 함수 재사용
- 구조화된 검증 체크리스트 활용
- 중요 이슈 중심의 집중 분석

## 산출물 위치

### SDD v1 폴더 구조 기준
- **Code Review 보고서**: `./docs/project/[Project]/30.review/35.code/{task-id}.{task명}(code-check)_{llm}_{date}.md`

**예시**:
- `./docs/project/maru/30.review/35.code/Task-3-1.MR0100-Backend-API-구현(code-check)_claude_20241224.md`
- `./docs/project/maru/30.review/35.code/Task-3-2.MR0100-Frontend-UI-구현(code-check)_gemini_20241224.md`



### Code Review 품질 기준
- **커버리지**: 설계서 요구사항 90% 이상 검증
- **정확성**: 실제 소스 코드 기반 분석
- **실행 가능성**: 구체적 개선 방안 포함
- **우선순위**: P1-P2 이슈는 반드시 해결 권장

---

**다음 명령어**: `/qa:apply` - Code Review 개선사항 적용