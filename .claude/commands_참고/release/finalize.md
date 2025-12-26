---
name: release:finalize
description: "최종 문서화 및 정리 (최적화 버전)"
category: documentation
complexity: moderate
wave-enabled: false
performance-profile: optimized
auto-flags:
  - --seq
  - --token-efficient
  - --task-manage
mcp-servers: [sequential]
personas: [technical-writer, scribe]
---

# /release:finalize - 최종 문서화 및 정리 (v1)

> **최적화된 문서화 통합**: 모든 Task 관련 문서를 통합하고 최종 문서화를 일괄 수행합니다.

## 🎯 최적화 목표
- **토큰 효율성**: 50% 토큰 절약 (단계 통합)
- **프로세스 통합**: 7단계 → 4단계 간소화
- **문서 일관성**: 모든 문서 동시 업데이트
- **자동화 극대화**: Git 통합 및 워크플로우 완성

## 트리거
- Task 구현 및 Cross Check 적용이 완료된 경우
- 모든 개발 단계를 마무리하고 최종 정리가 필요한 경우
- 유저 매뉴얼 및 코드 설명서 생성이 필요한 경우

## 사용법
```bash
/release:finalize "Task-3-1.MR0100-Backend-API-구현"
/release:finalize "Task-3-2.MR0100-Frontend-UI-구현"
/release:finalize "Task-1.개발환경구성-및-기반설정"
```

## 자동 실행 플로우 (통합 문서화 프로세스)

### 1단계: 문서 통합 및 현황 분석
**Auto-Persona**: technical-writer
**MCP**: sequential

**자동 실행 단계**:
1. **공통 문서 분석 함수 호출**: `analyze_project_context(task_name)`
   - 📋 함수 참조: `@docs/common/07.functions/analyze_project_context.md`
   - 프로젝트 정보 및 Task 상세 정보 수집
   - 모든 Task 관련 문서 자동 수집
   - 최종 정리를 위한 통합 전략 수립
2. **모든 Task 문서 일괄 수집**:
   - 상세설계서, 구현보고서, Cross Check 보고서, 테스트 결과서
   - 소스코드 현황 및 상태 분석
3. **문서 일관성 및 무결성 검증**

### 2단계: 통합 문서 업데이트
**Auto-Persona**: technical-writer
**MCP**: sequential

**자동 실행 단계**:
1. **실제 구현 결과 반영**: 상세설계서-구현보고서-테스트결과 동기화
2. **Task 상태 완료 처리**: 모든 Task 관련 문서에서 상태를 [✓] (완료)로 업데이트
3. **프로젝트 전체 문서 정리**:
   - README.md 업데이트 (새로 구현된 기능 반영)
   - API 문서 최신화 (Swagger/OpenAPI 업데이트)
   - 사용자 매뉴얼 생성 또는 업데이트 (`./docs/project/[Project]/40.finalization/41.release-notes/user-manuals/`)

### 3단계: 코드 정리 및 최종 검증
**Auto-Persona**: refactoring-expert
**MCP**: sequential

**자동 실행 단계**:
1. **코드 정리 및 최적화**:
   - 불필요한 주석 및 디버그 코드 제거
   - 코딩 표준 최종 검증 및 수정
   - 성능 최적화 마지막 점검
2. **최종 테스트 실행**:
   - 전체 테스트 스위트 실행
   - 회귀 테스트 및 통합 테스트
   - 코드 커버리지 최종 확인
3. **배포 준비**:
   - 빌드 스크립트 검증
   - 환경 설정 파일 점검
   - 배포 가이드 업데이트

### 4단계: Git 통합 및 최종 정리
**Auto-Persona**: scribe
**MCP**: sequential

**자동 실행 단계**:
1. **Git 커밋 및 태깅**:
   - 모든 변경사항 스테이징
   - 의미 있는 커밋 메시지로 커밋
   - 릴리즈 태그 생성 (v1.0.0 형태)
2. **최종 문서 패키징**:
   - 전달용 문서 패키지 생성
   - 핸드오버 가이드 작성
   - 알려진 이슈 및 향후 계획 정리
3. **작업 공간 정리**:
   - 임시 파일 및 개발 산출물 정리
   - 아카이브 디렉토리로 구 버전 이동
   - 프로젝트 상태 최종 업데이트
4. **Task 상태 업데이트**: `update_task_status(task_number, "finalize")`
   - 📋 함수 참조: `@docs/common/07.functions/update_task_status.md`
   - tasks.md에서 Task 체크박스를 [X]로 변경
   - 진행 상태를 **[d→i→c→a→X]**로 표시

**산출물**:
- 최종 문서 패키지: `./docs/project/[Project Name]/final_delivery_[날짜].zip`
- 핸드오버 가이드: `./docs/project/[Project Name]/handover_guide.md`
- Git 태그: `v1.0.0-[Task명]`

## 🎯 최적화 특징

### 📦 일괄 처리 효율성
- 모든 최종 작업을 한 번에 처리
- 중복 작업 제거 및 자동화 극대화
- 단계별 검증으로 품질 보증

### 🔄 완전한 통합
- 문서-코드-테스트 완전 동기화
- Git 워크플로우 자동 통합
- 프로젝트 상태 실시간 업데이트

### 📊 품질 보증
- 다층 검증 (문서, 코드, 테스트)
- 최종 배포 준비 상태 확인
- 핸드오버 완전성 검증

## 산출물 위치

### SDD v1 폴더 구조 기준
- **릴리즈 노트**: `./docs/project/[Project]/40.finalization/41.release-notes/`
- **전달 패키지**: `./docs/project/[Project]/40.finalization/42.delivery-package/`
- **스냅샷**: `./docs/project/[Project]/90.archive/snapshots/`

### 레거시 구조 기준 (호환성 유지)
- **최종 문서 패키지**: `./docs/project/[Project]/final_delivery_[날짜].zip`
- **핸드오버 가이드**: `./docs/project/[Project]/handover_guide.md`

## 최종 체크리스트

### ✅ 필수 완료 항목
- [ ] 모든 Task 상태가 [✓] (완료)로 업데이트됨
- [ ] 상세설계서-구현-테스트 문서 일관성 확인
- [ ] 전체 테스트 통과 (커버리지 ≥ 80%)
- [ ] 코딩 표준 준수 검증 완료
- [ ] API 문서 최신화 완료
- [ ] README.md 및 사용자 가이드 업데이트
- [ ] Git 커밋 및 태그 생성
- [ ] 최종 문서 패키지 생성

### 📋 핸드오버 준비사항
- [ ] 실행 가능한 소스코드 및 빌드 환경
- [ ] 완전한 기술 문서 세트
- [ ] 테스트 케이스 및 실행 가이드
- [ ] 알려진 이슈 및 해결방안
- [ ] 향후 개발 가이드라인

### 🚀 배포 준비사항
- [ ] 프로덕션 환경 설정 검토
- [ ] 보안 설정 및 인증 구성
- [ ] 성능 모니터링 설정
- [ ] 백업 및 복구 절차 준비

---

**완료**: Task 개발 라이프사이클 완료. 다음 Task로 진행 또는 `/qa:integration` 통합 테스트 수행