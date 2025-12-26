---
name: design:review_detail
description: "다른 LLM을 활용한 상세설계 교차 검증 및 리뷰"
category: quality
complexity: enhanced
wave-enabled: false
performance-profile: optimized
auto-flags:
  - --seq
  - --token-efficient
mcp-servers: [sequential]
personas: [system-architect, security-engineer, quality-engineer, technical-writer]
---

# /design:review_detail - 상세설계 교차 검증 리뷰 (v1)

> **다른 LLM 활용 검증**: detail_design 완료 후 다른 LLM(Gemini, GPT-5 등)을 통한 객관적 교차 검증으로 설계 품질을 향상시킵니다.

## 🎯 최적화 목표
- **객관성 확보**: Claude 외 다른 LLM 활용으로 편향 방지
- **설계 완전성**: 요구사항 대비 설계 커버리지 검증
- **품질 보증**: 아키텍처, 보안, 성능 측면의 다층 검증
- **실행 가능성**: 구체적이고 실행 가능한 개선 제안

## 트리거
- `/design:detail` 완료 직후
- 상세설계서의 품질 검증이 필요한 경우
- 다른 LLM을 통한 객관적 검토가 필요한 경우
- 설계 승인 전 최종 검증 단계

## 사용법
```bash
# Task 번호로 실행 (권장)
/design:review_detail Task 3.1
/design:review_detail 3.1

# 기존 방식도 지원
/design:review_detail "Task-3-1"
/design:review_detail "Task 3.2"
```

## 자동 실행 플로우

### 1단계: 검증 범위 확인 및 문서 수집
**Auto-Persona**: system-architect
**MCP**: sequential
**권장 LLM**: Claude 대신 **Gemini, GPT-5, Claude Opus 등 다른 LLM 사용**

**자동 실행 단계**:
1. **Task 정보 추출 및 파싱**:
   ```javascript
   // "/design:review_detail Task 3.1" 또는 "/design:review_detail 3.1"에서 Task 번호 추출
   function parseTaskFromCommand(input) {
       const taskPattern = /(?:Task\s+)?(\d+\.\d+)/i;
       return input.match(taskPattern)?.[1]; // "3.1" 추출
   }
   ```

2. **공통 문서 분석 함수 호출**: `analyze_project_context(task_number)`
   - 📋 함수 참조: `@docs/common/07.functions/analyze_project_context.md`
   - `./docs/project/maru/00.foundation/01.project-charter/tasks.md`에서 Task 정보 조회
   - 자동 파일명 생성: `{task-id}.{task명}(상세설계리뷰)_{llm}_{date}.md`
     - 예: `Task-3-1.MR0100-Backend-API-구현(상세설계리뷰)_gemini_20241224.md`
   - 프로젝트 정보 및 Task 상세 정보 수집

3. **검증 대상 문서 수집**:
   - **상세설계서**: `./docs/project/[Project]/10.design/12.detail-design/{task-id}.{task명}(상세설계).md`
   - **기본설계서**: `./docs/project/[Project]/10.design/11.basic-design/{task-id}.{task명}(기본설계).md`
   - **요구사항 문서**: PRD, 기능 명세서
   - **참조 문서**: 아키텍처 가이드, 코딩 표준, 보안 정책

### 2단계: 설계 문서 분석 및 검증 준비
**Auto-Persona**: system-architect
**MCP**: sequential
**권장 LLM**: Gemini, GPT-5 등 Claude와 다른 LLM

**자동 실행 단계**:
1. **상세설계서 구조 분석**:
   - 설계 문서 구조 및 템플릿 준수 여부 확인
   - 필수 섹션 포함 여부 검증
   - 문서 완전성 평가

2. **요구사항 추적성 검증**:
   - 모든 요구사항이 설계에 반영되었는지 확인
   - 요구사항 ID와 설계 요소 간 매핑 검증
   - 누락된 요구사항 식별

3. **설계 일관성 확인**:
   - 기본설계서와의 일관성 검증
   - 아키텍처 원칙 준수 여부 확인
   - 명명 규칙 및 표준 준수 검증

### 3단계: 다층 품질 검증 (다른 LLM 필수)
**Auto-Persona**: system-architect + security-engineer + quality-engineer
**MCP**: sequential
**권장 LLM**: **반드시 Claude와 다른 LLM 사용 (Gemini, GPT-5, Claude Opus, Qwen Code 등)**

**자동 실행 단계**:

#### 3.1 아키텍처 검증 (system-architect)
1. **시스템 구조 분석**:
   - 아키텍처 패턴 적절성 평가
   - 컴포넌트 분할 및 책임 분리 검증
   - 확장성 및 유지보수성 평가

2. **데이터 흐름 검증**:
   - 데이터 인터페이스 설계 적절성
   - API 설계 일관성 및 REST 원칙 준수
   - 데이터 모델 정규화 및 무결성

3. **통합 전략 평가**:
   - 외부 시스템 연동 설계 적절성
   - 에러 처리 및 트랜잭션 관리
   - 동시성 제어 및 동기화 전략

#### 3.2 보안 검증 (security-engineer)
1. **보안 위협 분석**:
   - OWASP Top 10 대응 여부 확인
   - 인증/인가 메커니즘 적절성
   - 데이터 암호화 및 보호 전략

2. **취약점 식별**:
   - SQL Injection, XSS 등 취약점 가능성
   - 민감 데이터 노출 위험
   - 접근 제어 및 권한 관리

3. **보안 정책 준수**:
   - 조직 보안 정책 준수 여부
   - 규정 준수 요구사항 (GDPR, 개인정보보호법 등)
   - 보안 로깅 및 모니터링 전략

#### 3.3 성능 및 품질 검증 (quality-engineer)
1. **성능 요구사항 검증**:
   - 응답 시간 및 처리량 목표 달성 가능성
   - 병목 지점 식별 및 최적화 방안
   - 캐싱 전략 및 리소스 관리

2. **테스트 가능성 평가**:
   - 단위 테스트 가능성
   - 통합 테스트 시나리오 완전성
   - UI 테스트케이스 실행 가능성

3. **코드 품질 기준**:
   - SOLID 원칙 준수 여부
   - DRY, KISS, YAGNI 원칙 적용
   - 코딩 표준 및 네이밍 컨벤션

#### 3.4 이슈 분류 및 우선순위화
**심각도(Severity) 분류**:
- ⚠️ **Critical**: 시스템 중단, 데이터 손실, 심각한 보안 이슈
- ❗ **High**: 핵심 기능 오류, 다수 사용자 영향, 보안 취약점
- 🔧 **Medium**: 부분적 기능 제한, 성능 저하, 사용성 문제
- 📝 **Low**: 경미한 불편, UI/문구 개선, 코드 품질
- ℹ️ **Info**: 개선 제안, 모범 사례 권장

**우선순위(Priority) 할당**:
- 🔴 **P1 (즉시 해결)**: 설계 결함, 심각한 보안 위험, 구현 불가능
- 🟠 **P2 (빠른 해결)**: 아키텍처 개선, 성능 문제, 테스트 불가능
- 🟡 **P3 (보통 해결)**: 코드 품질, 표준 미준수, 문서화 부족
- 🟢 **P4 (개선 항목)**: 최적화 기회, 모범 사례 적용, 리팩토링
- 🔵 **P5 (참고 사항)**: 참고용 정보, 향후 고려 사항

### 4단계: 상세설계 리뷰 보고서 생성
**Auto-Persona**: technical-writer
**MCP**: sequential
**권장 LLM**: 3단계와 동일한 LLM 사용

**자동 실행 단계**:
1. **검증 결과 종합**:
   - 발견된 이슈 목록 정리
   - 카테고리별 분류 (아키텍처, 보안, 성능, 품질)
   - 심각도 및 우선순위 할당

2. **개선사항 제안**:
   - 구체적이고 실행 가능한 해결 방안
   - 설계 변경 제안 및 근거
   - 코드 예시 또는 참조 문서 제공

3. **리뷰 보고서 작성**:
   - 검증 범위 및 방법론 기술
   - 이슈 및 개선사항 상세 기술
   - 강점 및 우수 사례 포함
   - 다음 단계 권장사항 제시

4. **Task 상태 업데이트**: `update_task_status(task_number, "design_reviewed")`
   - 📋 함수 참조: `@docs/common/07.functions/update_task_status.md`
   - tasks.md에서 Task 체크박스를 [dr]로 변경
   - 진행 상태를 **[d→dr]**로 표시

## 🎯 최적화 특징

### 🔍 다중 LLM 교차 검증
- **Claude 외 다른 LLM 필수**: Gemini, GPT-5, Claude Opus 등 활용
- **편향 방지**: 서로 다른 LLM의 관점으로 객관성 확보
- **강점 활용**: 각 LLM의 특화 영역 활용 (예: GPT-5의 추론, Gemini의 패턴 인식)

### 📊 체계적 품질 검증
- **다층 검증**: 아키텍처, 보안, 성능, 품질 측면의 종합 검증
- **이슈 분류**: P1-P5 우선순위 및 심각도 매트릭스 적용
- **실행 가능성**: 구체적인 개선안과 코드 예시 제공

### ⚡ 토큰 효율성
- **공통 함수 재사용**: analyze_project_context 활용
- **구조화된 템플릿**: 일관된 검증 체크리스트
- **집중 분석**: 중요 이슈 중심의 상세 분석

## 산출물 위치

### SDD v1 폴더 구조 기준
- **상세설계 리뷰 보고서**: `./docs/project/[Project]/30.review/33.detail/{task-id}.{task명}(상세설계리뷰)_{llm}_{date}.md`

**예시**:
- `./docs/project/maru/30.review/33.detail/Task-3-1.MR0100-Backend-API-구현(상세설계리뷰)_gemini_20241224.md`
- `./docs/project/maru/30.review/33.detail/Task-3-2.MR0100-Frontend-UI-구현(상세설계리뷰)_gpt4_20241224.md`

## 리뷰 보고서 템플릿 구조

```markdown
# 상세설계 리뷰 보고서

## 📋 기본 정보
- **Task**: {task-id} {task명}
- **검토자**: {LLM 이름} (예: Gemini 2.5 Pro)
- **검토일**: {YYYY-MM-DD}
- **상세설계서**: {파일 경로}

## 🎯 검증 범위
- 검증 대상 문서
- 검증 방법론
- 검증 기준

## ✅ 강점 및 우수 사례
- 잘 설계된 부분
- 모범 사례 적용 사례
- 특별히 우수한 점

## ⚠️ 발견된 이슈

### 🔴 P1 - 즉시 해결 필요
**[이슈 제목]**
- **심각도**: Critical/High
- **카테고리**: 아키텍처/보안/성능/품질
- **설명**: 상세한 이슈 설명
- **영향**: 미치는 영향 분석
- **개선안**: 구체적인 해결 방법
- **참조**: 코드 예시, 문서 링크

### 🟠 P2 - 빠른 해결 권장
[동일 형식 반복]

### 🟡 P3 - 보통 우선순위
[동일 형식 반복]

### 🟢 P4 - 개선 항목
[동일 형식 반복]

### 🔵 P5 - 참고 사항
[동일 형식 반복]

## 📊 검증 결과 요약

### 요구사항 커버리지
- 전체 요구사항: {n}개
- 설계 반영: {n}개 ({percentage}%)
- 누락: {n}개

### 이슈 분류
| 우선순위 | Critical | High | Medium | Low | Info | 합계 |
|---------|----------|------|--------|-----|------|------|
| P1      | {n}      | {n}  | {n}    | {n} | {n}  | {n}  |
| P2      | {n}      | {n}  | {n}    | {n} | {n}  | {n}  |
| P3      | {n}      | {n}  | {n}    | {n} | {n}  | {n}  |
| P4      | {n}      | {n}  | {n}    | {n} | {n}  | {n}  |
| P5      | {n}      | {n}  | {n}    | {n} | {n}  | {n}  |
| **합계**| {n}      | {n}  | {n}    | {n} | {n}  | {n}  |

### 카테고리별 분류
- 🏗️ 아키텍처: {n}개
- 🛡️ 보안: {n}개
- ⚡ 성능: {n}개
- 📝 품질: {n}개

## 🎯 종합 평가
- 전반적인 설계 품질 평가
- 구현 준비도 평가
- 주요 리스크 및 우려사항

## 📋 다음 단계 권장사항
1. P1 이슈 즉시 해결
2. P2 이슈 설계 수정 반영
3. 개선안 적용 후 재검토 필요 여부
4. 구현 전 추가 검토 항목

## 📎 참조 문서
- 상세설계서
- 기본설계서
- 요구사항 문서
- 관련 표준 및 가이드
```

## 품질 기준

### 검증 품질 표준
- **커버리지**: 요구사항 95% 이상 검증
- **정확성**: 실제 설계 문서 기반 분석
- **실행 가능성**: 모든 개선안에 구체적 해결 방법 포함
- **우선순위**: P1-P2 이슈는 반드시 해결 권장

### LLM 선택 가이드
- **Gemini**: 패턴 인식, 시스템 분석에 강점
- **GPT-5**: 논리적 추론, 보안 분석에 강점
- **Claude Opus**: 코드 품질, 아키텍처 분석에 강점
- **권장**: 설계 복잡도에 따라 최신 모델 사용

---

**다음 명령어**: `/design:apply_detail_review` - 상세설계 리뷰 개선사항 적용
