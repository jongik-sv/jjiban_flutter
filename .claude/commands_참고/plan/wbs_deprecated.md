---
name: plan:wbs
description: "설계 문서를 참조하여 상세 구현 계획을 생성하고, 구조화된 개발 로드맵과 작업 분할을 만듭니다."
category: planning
complexity: complex
wave-enabled: true
performance-profile: complex
auto-flags:
  - --seq
  - --c7
  - --token-efficient
mcp-servers: [sequential, context7]
personas: [architect, analyzer, scribe]
---

# /plan:wbs - 화면 중심 개발 구현 계획 생성

> **화면 중심 WBS 생성**: 설계 문서를 분석하여 화면 단위 Task 구조로 구현 계획을 생성합니다.

## 트리거
- 프로젝트 초기 구현 계획 수립이 필요한 경우
- 설계 문서 기반 체계적인 개발 로드맵이 필요한 경우
- 화면 단위 독립 Task로 작업 분할이 필요한 경우

## 사용법
```bash
/plan:wbs
```

## 핵심 특징
- **screen-centric**: 각 화면을 독립적인 Task로 관리
- **task-classification**: 시스템 공통/UI 없음/UI 있음 Task 분류
- **integrated-development**: Backend API + Frontend UI 통합 개발
- **breakdown**: 완료 추적이 포함된 상세 작업 분할
- **phases**: 마일스톤이 포함된 단계별 개발 구조

## Task 분류 체계

### 1. 시스템 공통 기능 Task
- **특징**: 전체 시스템의 기반이 되는 공통 기능
- **구성**: Backend 서비스, 데이터베이스, 캐시, 보안, 로깅 등
- **형식**: 기능 중심의 세부 작업 분할
- **예시**: 개발 환경 구축, 데이터베이스 스키마, 공통 API, 인증 시스템

### 2. UI 없는 기능 Task
- **특징**: Frontend UI가 필요 없는 Backend 전용 기능
- **구성**: API 서비스, 데이터 처리, 배치 작업, 통합 기능
- **형식**: Backend 중심의 기능 구현
- **예시**: 데이터 동기화, 스케줄러, 외부 연동 API, 백그라운드 처리

### 3. UI 있는 화면 Task
- **특징**: 사용자가 직접 사용하는 화면 기능
- **구성**: Backend API + Frontend UI 통합 개발
- **형식**: 화면별 독립 Task (1화면 = 1Task)
- **하위 구조**: X.1 Backend API 구현 + X.2 Frontend UI 구현
- **예시**: 마루헤더관리, 코드기본값관리, 룰실행테스트 등

## 자동 실행 플로우

### 1단계: 프로젝트 컨텍스트 및 화면 목록 분석
**Auto-Persona**: architect + analyzer
**MCP**: sequential + context7

**자동 실행 단계**:
1. **프로젝트 이름 추출**: CLAUDE.md 파일에서 프로젝트 이름 자동 읽기
   ```javascript
   // CLAUDE.md에서 "## Project Overview" 섹션의 프로젝트명 추출
   const projectName = extractProjectName("CLAUDE.md");
   ```

2. **설계 문서 스캔**:
   - `./docs/project/[project]/00.foundation/01.project-charter/` - 프로젝트 헌장
   - `./docs/project/[project]/00.foundation/02.design-baseline/` - 설계 기준선
   - `./docs/project/[project]/10.design/11.basic-design/` - 기본 설계

3. **화면 목록 추출**: 프로그램 리스트 설계서에서 화면 ID, 화면명, 우선순위 추출

4. **요구사항 추출**: 설계 문서에서 기능적/비기능적 요구사항 분석

5. **아키텍처 분석**: 시스템 아키텍처 및 기술 스택 식별

6. **종속성 매핑**: 구성 요소 간 종속성 및 통합 지점 분석

### 2단계: 화면별 Task 분류 및 단계 계획
**Auto-Persona**: architect
**MCP**: sequential

**자동 실행 단계**:
1. **Task 분류**: 시스템 공통/UI 없음/UI 있음으로 자동 분류
2. **화면 우선순위 적용**: 프로그램 리스트의 우선순위 기반 개발 순서 결정
3. **단계별 그룹핑**: 관련 화면을 기능별로 그룹화 (예: 마루관리, 코드관리, 룰관리)
4. **종속성 분석**: 화면 간 데이터 의존성 및 개발 순서 분석
5. **5단계 구조 생성**: 명확한 마일스톤이 있는 개발 단계 구조 생성
6. **리소스 추정**: 화면별 개발 시간 및 난이도 추정

### 3단계: 화면별 상세 작업 분할 및 추적 구조
**Auto-Persona**: architect + scribe
**MCP**: sequential

**자동 실행 단계**:
1. **화면별 Task 생성**: 각 화면 = 독립 Task (1화면 = 1Task)
2. **통합 개발 구조**:
   - X.1 Backend API 구현
   - X.2 Frontend UI 구현
3. **체크박스 추적**: `[ ]` (미완료), `[-]` (진행중), `[d]` (설계완료), `[i]` (구현완료), `[x]` (검증완료)
4. **요구사항 매핑**: 각 Task를 설계 요구사항에 연결
5. **구현 세부 정보**: Backend API 및 Frontend UI 구현 상세 명세
6. **완료 기준**: API + UI + 통합 완성 기준 정의

### 4단계: 화면별 마일스톤 및 품질 기준
**Auto-Persona**: quality-engineer + architect
**MCP**: sequential

**자동 실행 단계**:
1. **마일스톤 정의**: 각 단계별 화면 완료 목표 설정
2. **완성도 기준**:
   - Backend API: 엔드포인트 구현 및 테스트
   - Frontend UI: Form 구현 및 Dataset 연동
   - 통합: Frontend-Backend 연동
   - UI/UX: 사용자 시나리오 검증
   - 에러 처리: 예외 상황 처리
3. **진행률 추적**: 화면별 진행 상황 모니터링 시스템
4. **품질 게이트**: 테스트 및 검증 체크포인트
5. **위험 평가**: 화면 간 의존성 위험 및 완화 전략
6. **성능 목표**: 측정 가능한 성능/사용성 지표

### 5단계: tasks.md 구현 계획 문서 생성
**Auto-Persona**: scribe
**MCP**: sequential

**자동 실행 단계**:
1. **tasks.md 생성**: `./docs/project/[project]/00.foundation/01.project-charter/tasks.md`
2. **화면별 완료 추적**: 체크박스 기반 진행 상황 추적
3. **요구사항 추적성**: 설계 요구사항 100% 매핑 검증
4. **구현 가이드**: 각 화면별 Backend + Frontend 상세 지침
5. **성공 지표**: 측정 가능한 성공 기준 포함
6. **Task 번호 부여**: 계층적 번호 체계 (1, 1.1, 2, 2.1, 2.2 등)

## 출력 형식

### tasks.md 템플릿
```markdown
# [프로젝트명] 구현 계획 (화면 중심)

## 프로젝트 개요
[CLAUDE.md에서 추출한 프로젝트 설명]

### 핵심 아키텍처
- **3-Tier Architecture**: Frontend + Backend + Database
- **화면 중심 개발**: 각 화면 = 독립 Task (Backend + Frontend 통합)
- **기술 스택**: [프레임워크, 라이브러리, 도구]

## 1단계: 시스템 공통 기능

- [ ] 1. [공통 기능 Task명]
  - 1.1 [하위 작업]
  - 1.2 [기술 요구사항]
  - _요구사항: [REQ-ID]_
  - _참고: [설계문서명]_

## 2단계: [화면 그룹명] 화면 구현

- [ ] 2. [화면ID] - [화면명] (우선순위: N)
  - [ ] 2.1 Backend API 구현
    - API 엔드포인트 구현
    - 비즈니스 로직 구현
    - 데이터 검증 로직
    - Swagger 문서화
  - [ ] 2.2 Frontend UI 구현
    - Form/화면 생성
    - UI 컴포넌트 구현
    - Dataset 연동 및 바인딩
    - 사용자 인터페이스 최적화
  - _요구사항: [REQ-ID]_
  - _참고: [프로그램리스트.md, api-design.md, ui-design.md]_

## 화면별 완성도 기준
- [ ] **Backend API**: 엔드포인트 구현 및 테스트 완료
- [ ] **Frontend UI**: Form 구현 및 Dataset 연동 완료
- [ ] **기능 통합**: Frontend-Backend 완전 연동
- [ ] **UI/UX**: 사용자 시나리오 검증
- [ ] **에러 처리**: 예외 상황 처리 및 피드백

## 성공 지표
### 기능적 성공 기준
- [ ] 모든 화면 완성: [N]개 핵심 화면 구현 및 동작
- [ ] CRUD 완전성: 모든 화면에서 CRUD 기능 동작
- [ ] 화면별 완성도: 각 화면 100% 기능 구현

### 사용성 기준
- [ ] 응답성: 각 화면 로딩 < 2초
- [ ] 직관성: 최소 교육으로 사용 가능
- [ ] 일관성: 모든 화면 동일 UI 패턴
```

## 🎯 최적화 특징

### ✅ 화면 중심 접근
- 각 화면 = 독립 Task로 명확한 작업 단위
- Backend + Frontend 통합 개발 구조
- 화면별 진행 상황 추적 용이

### 📊 체계적 구조
- 5단계 명확한 마일스톤 구조
- 계층적 Task 번호 체계
- 요구사항 100% 추적성

### ⚡ 효율적 실행
- 설계 문서 자동 스캔 및 분석
- 프로젝트명 자동 추출
- tasks.md 자동 생성

## 산출물 위치

### SDD v1 폴더 구조 기준
- **tasks.md**: `./docs/project/[project]/00.foundation/01.project-charter/tasks.md`

**예시**:
- `./docs/project/maru/00.foundation/01.project-charter/tasks.md`

## 성공 기준
- **요구사항 커버리지**: 설계 문서 요구사항 100% 화면별 매핑
- **화면 분할 정확도**: 95% 이상 정확한 화면별 작업 식별
- **완료 추적**: 체크박스 기반 진행 상황 모니터링 시스템
- **문서 품질**: 명확한 구조의 tasks.md (화면별 독립 Task)
- **개발 준비**: 각 화면별 Backend + Frontend 즉시 실행 가능

## 성능 목표
- **설계 문서 분석**: 3분 미만 (화면 목록 추출 포함)
- **tasks.md 생성**: 5분 미만
- **요구사항 매핑**: 100% 추적성
- **단계 계획**: 명확한 5단계 구조 및 마일스톤

---

**다음 명령어**: `/design:detail` - Task별 상세설계 수행


<!--
MES-AI 개발 프레임워크 - Command Documentation
Copyright (c) 2025 장종익 - 동국시스템즈
Command: wbs
Category: planning
Version: 1.0
Developer: 장종익

이 명령어는 설계 문서를 참조하여 상세 구현 계획을 생성하고, 구조화된 개발 로드맵과 작업 분할을 위해 설계되었습니다.
-->

