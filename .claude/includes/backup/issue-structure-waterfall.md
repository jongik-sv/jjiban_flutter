# 작업 분류 체계 (Work Breakdown Structure)

## 1. 개요

프로젝트 관리를 위한 작업 분류 체계(WBS)를 정의합니다.

---

## 2. 작업 분류 체계 (WBS)

### 2.1 계층 구조

| 계층 | 명칭 | 설명 | 기간 |
|------|------|------|------|
| **Level 1** | Project | 전체 프로젝트 | 6~24개월 |
| **Level 2** | Work Package | 주요 기능 단위의 작업 묶음 | 1~3개월 |
| **Level 3** | Activity | 세부 활동 단위 | 1~4주 |
| **Level 4** | Task | 실제 수행 작업 단위 | 1일~1주 |

### 2.2 계층 다이어그램

```
Project (프로젝트)
├── Work Package #1
│   ├── Activity #1.1
│   │   ├── Task #1.1.1
│   │   ├── Task #1.1.2
│   │   └── Task #1.1.3
│   └── Activity #1.2
│       └── Task #1.2.1
├── Work Package #2
│   └── Activity #2.1
│       └── Task #2.1.1
└── Work Package #3
    └── Task #3.1 (Activity 생략 가능)
```

### 2.3 Task 유형

모든 작업은 **Task**로 통합하고, `category` 필드로 구분합니다.

```
Task (작업 항목)
├── category: "development"    # 개발 작업
├── category: "defect"         # 결함 수정
└── category: "infrastructure" # 인프라/기술 작업
```

| 유형 | 설명 |
|------|------|
| **development** | 신규 기능 개발 작업 |
| **defect** | 결함 수정 작업 |
| **infrastructure** | 인프라, 리팩토링 등 기술 작업 |

---

## 3. 계층별 허용 관계

### 3.1 하위 항목 허용 매트릭스

| 상위 계층 | 허용되는 하위 계층 |
|----------|-------------------|
| **Project** | Work Package |
| **Work Package** | Activity, Task (모든 category) |
| **Activity** | Task (모든 category) |
| **Task** | Sub-Task (깊이 제한 2단계) |

### 3.2 설계 원칙

1. **Project는 최상위 고정**: 모든 프로젝트에서 Project가 최상위 계층
2. **Task 유형 통합**: Defect, Infrastructure를 Task의 category로 통합
3. **유연한 계층**: Activity는 필요에 따라 생략 가능

---

## 4. 작업 규모 기준

### 4.1 권장 규모

| 계층 | 최소 | 권장 | 최대 |
|------|------|------|------|
| Project | 3개월 | 6~12개월 | 24개월 |
| Work Package | 2주 | 1~3개월 | 6개월 |
| Activity | 3일 | 1~4주 | 2개월 |
| Task | 4시간 | 1~3일 | 1주 |

### 4.2 분할 기준

다음 경우 더 작은 단위로 분할:
- Task가 1주 이상 소요 예상
- 단일 작업에 복수 담당자 필요
- 진척률 추적 곤란
- 의존성 복잡도 증가

---

## 5. 업계 표준 비교

| 본 시스템 | PMBOK | PRINCE2 | Redmine |
|----------|-------|---------|---------|
| Project | Project | Project | Project |
| Work Package | Work Package | Work Package | Sub-Project |
| Activity | Activity | Product | Parent Issue |
| Task | Task | Team Task | Issue |
| Task [defect] | - | - | Issue (Bug) |

---

## 6. 용어 정의

| 용어 | 정의 |
|------|------|
| **WBS** | Work Breakdown Structure, 프로젝트 범위를 계층적으로 분해한 구조 |
| **Work Package** | WBS의 최하위 산출물 단위, 일정/원가 산정 기준 |
| **Activity** | Work Package를 완성하기 위한 세부 활동 |
| **Task** | 담당자가 수행하는 최소 작업 단위 |
| **Deliverable** | 프로젝트 결과물, 산출물 |
