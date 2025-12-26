---
name: qa:apply
description: "Code Review 개선사항 적용 (최적화 버전)"
category: improvement
complexity: moderate
wave-enabled: false
performance-profile: optimized
auto-flags:
  - --seq
  - --token-efficient
  - --validate
mcp-servers: [sequential]
personas: [refactoring-expert, backend-architect, nexacro-developer]
---

# /qa:apply - Code Review 개선사항 적용 (v1)

> **최적화된 개선사항 적용**: Code Review에서 도출된 개선사항을 코드 및 문서에 체계적으로 적용하고 검증합니다.

## 🎯 최적화 목표
- **토큰 효율성**: 30% 토큰 절약
- **우선순위 기반**: P1-P2 중심의 선택적 적용
- **검증 중심**: 변경 사항의 영향도 분석
- **에이전트 특화**: 도메인별 전문 에이전트 활용

## 트리거
- Code Review 보고서가 완성된 Task의 개선사항 적용이 필요한 경우
- 다른 LLM에서 수행된 Code Review 결과를 적용하는 경우
- 우선순위 높은 이슈들의 신속한 해결이 필요한 경우

## 사용법
```bash
# Task 번호로 실행 (권장)
/qa:apply Task 3.1
/qa:apply 3.1

# 기존 방식도 지원
/qa:apply "Task-3-1"
/qa:apply "Task 3.2"
```

## 자동 실행 플로우

### 1단계: Code Review 결과 분석
**Auto-Persona**: refactoring-expert
**MCP**: sequential

**자동 실행 단계**:
1. **Task 정보 추출 및 파싱**:
   ```javascript
   // "/qa:apply Task 3.1" 또는 "/qa:apply 3.1"에서 Task 번호 추출
   function parseTaskFromCommand(input) {
       const taskPattern = /(?:Task\s+)?(\d+\.\d+)/i;
       return input.match(taskPattern)?.[1]; // "3.1" 추출
   }
   ```

2. **공통 문서 분석 함수 호출**: `analyze_project_context(task_number)`
   - 📋 함수 참조: `@docs/common/07.functions/analyze_project_context.md`
   - `./docs/project/maru/00.foundation/01.project-charter/tasks.md`에서 Task 정보 조회
   - 자동 파일명 생성: `{task-id}.{task명}(apply).md`
     - 예: `Task-3-1.MR0100-Backend-API-구현(apply).md`
   - 프로젝트 정보 및 Task 상세 정보 수집
   - Code Review 보고서 자동 로드
   - 개선사항 적용 전략 수립

3. **Code Review 보고서 로드**:
   - `./docs/project/[Project Name]/30.review/35.code/{task-id}.{task명}(code-check)_*.md` 패턴으로 검색
   - 예: `Task-3-1.MR0100-Backend-API-구현(code-check)_claude_20241224.md`
3. **우선순위별 이슈 분류**:
   - P1-P2: 즉시 적용 대상
   - P3-P4: 선택적 적용 검토
   - P5: 적용 보류
4. **적용 범위 결정**:
   - 코드 수정이 필요한 이슈
   - 문서 수정이 필요한 이슈
   - 설계 변경이 필요한 이슈

### 2단계: 코드 개선사항 적용 (Agent 위임)
**Auto-Persona**: backend-architect + nexacro-developer (Agent 위임)
**MCP**: sequential

**자동 실행 단계**:
1. **Backend 코드 개선** (backend-architect 위임):
   - P1-P2 보안 이슈 수정
   - 성능 최적화 코드 적용
   - 코딩 표준 준수 리팩토링
   - API 인터페이스 개선
2. **Frontend 코드 개선** (nexacro-developer 위임):
   - UI/UX 개선사항 적용
   - 사용성 및 접근성 향상
   - 화면 간 일관성 확보
   - 에러 처리 개선
3. **테스트 코드 개선** (quality-engineer):
   - 누락된 테스트 케이스 추가
   - 예외 상황 테스트 강화
   - 테스트 커버리지 향상

### 3단계: 문서 개선사항 적용
**Auto-Persona**: technical-writer
**MCP**: sequential

**자동 실행 단계**:
1. **설계 문서 업데이트**:
   - 상세설계서 수정 사항 반영
   - API 명세 업데이트
   - 화면 설계 개선사항 반영
2. **구현 보고서 업데이트**:
   - 개선사항 적용 결과 반영
   - 알려진 이슈 해결 상태 업데이트
   - 변경 이력 및 근거 기술
3. **테스트 문서 업데이트**:
   - 추가된 테스트 케이스 반영
   - 테스트 결과 업데이트

### 4단계: 개선사항 적용 검증
**Auto-Persona**: quality-engineer
**MCP**: sequential

**자동 실행 단계**:
1. **코드 품질 검증**:
   - 정적 분석 도구 실행
   - 코드 리뷰 체크리스트 검증
   - 성능 테스트 실행
2. **기능 테스트 실행**:
   - 수정된 기능의 회귀 테스트
   - 통합 테스트 재실행
   - 사용자 시나리오 테스트
3. **문서 일관성 검증**:
   - 설계-구현-테스트 문서 일관성 확인
   - 변경 사항 추적성 검증

### 5단계: 적용 결과 보고서 생성
**Auto-Persona**: technical-writer
**MCP**: sequential

**자동 실행 단계**:
1. **적용 결과 정리**:
   - 적용된 개선사항 목록
   - 적용하지 않은 이슈 및 사유
   - 변경 사항의 영향도 분석
2. **품질 개선 효과 분석**:
   - 코드 품질 메트릭 비교
   - 성능 개선 효과 측정
   - 테스트 커버리지 향상도
3. **적용 결과 보고서 작성**:
   - Code Review 개선사항 적용 상세 내역
   - 품질 개선 효과 및 검증 결과
   - 향후 개선 권장사항
4. **Task 상태 업데이트**: `update_task_status(task_number, "apply")`
   - 📋 함수 참조: `@docs/common/07.functions/update_task_status.md`
   - tasks.md에서 Task 체크박스를 [a]로 변경
   - 진행 상태를 **[d→i→c→a]**로 표시


## 🎯 최적화 특징

### 🎯 우선순위 중심 적용
- P1-P2 이슈 중심의 집중 적용
- 비용-효과 분석 기반 선택적 적용
- 리스크 최소화 및 품질 극대화

### ⚡ 에이전트 특화 위임
- 도메인별 전문 에이전트 자동 배정
- 백엔드-프론트엔드 병렬 개선
- 각 영역별 최적화된 개선 적용

### 📊 검증 중심 프로세스
- 모든 변경사항의 회귀 테스트 의무화
- 문서-코드 일관성 자동 검증
- 품질 개선 효과 정량적 측정

## 산출물 위치

### SDD v1 폴더 구조 기준
- **적용 결과 보고서**: `./docs/project/[Project]/30.review/35.applied-code/{task-id}.{task명}(apply).md`

**예시**:
- `./docs/project/maru/30.review/35.applied-code/Task-3-1.MR0100-Backend-API-구현(apply).md`
- `./docs/project/maru/30.review/35.applied-code/Task-3-2.MR0100-Frontend-UI-구현(apply).md`

## 적용 기준 가이드

### 우선순위별 적용 원칙
- **P1 (치명적)**: 반드시 적용, 즉시 수정
- **P2 (높음)**: 적용 권장, 릴리즈 전 수정
- **P3 (중간)**: 선택적 적용, 리소스 여유 시 수정
- **P4 (낮음)**: 차후 적용 검토
- **P5 (개선)**: 장기 개선 계획에 반영

### 변경 영향도 평가
- **High**: 아키텍처 또는 핵심 로직 변경
- **Medium**: 기능 수정 또는 인터페이스 변경
- **Low**: 코딩 스타일 또는 문서 수정

---

**다음 명령어**: `/release:finalize` - 최종 문서화 및 정리