---
name: plan:doc_init
allowed-tools: [Read, Bash, Write, TodoWrite]
description: "CLAUDE.md 파일에서 프로젝트명을 추출하여 docs 폴더 구조를 생성하는 명령어"
---

# /plan:doc_init - 문서 폴더 구조 생성

## 목적
CLAUDE.md 파일에서 프로젝트명을 추출하여 docs 폴더 구조를 자동 생성합니다.
최초 생성시는 common 폴더를 만들고, 이후에는 project 폴더 밑에 프로젝트별 폴더를 생성합니다.

## 사용법
```
/plan:doc_init
```

## 실행 과정
1. CLAUDE.md 파일에서 프로젝트명 추출
2. docs 폴더 존재 여부 확인
3. 최초 생성시 common 폴더 구조 생성
4. project 폴더 밑에 프로젝트별 폴더 생성, 폴더 있으면 종료
5. 기본 문서 템플릿 파일 생성

## 생성되는 폴더 구조
```
docs/
├── common/
│   ├── 01.config/
│   ├── 04.template/
│   ├── 06.guide/
│   └── 07.functions/
└── project/
    └── {project-name}/
        ├── 00.foundation/
        │   ├── 01.project-charter/
        │   ├── 02.design-baseline/
        │   └── 03.project-governance/
        ├── 10.design/
        │   ├── 11.basic-design/
        │   └── 12.detail-design/
        ├── 20.implementation/
        ├── 30.review/
        │   ├── 33.detail/
        │   ├── 35.code/
        │   └── 35.applied-code/
        ├── 40.finalization/
        │   ├── 41.release-notes/
        │   │   └── user-manuals/
        │   └── 42.delivery-package/
        ├── 50.test/
        │   ├── 51.e2e-test-results/
        │   ├── 52.tdd-results/
        │   └── 53.integration-test/
        │       ├── evidence/
        │       └── scenarios/
        └── 90.archive/

## Claude Code 통합
- Read 도구로 CLAUDE.md 파일 분석
- Bash 도구로 폴더 생성 명령 실행
- Write 도구로 기본 템플릿 파일 생성
- TodoWrite로 진행 상황 추적
```

<!--
MES-AI 개발 프레임워크 - Command Documentation
Copyright (c) 2025 장종익 - 동국시스템즈
Command: doc_init
Category: documentation
Version: 1.0
Developer: 장종익

이 명령어는 CLAUDE.md 파일에서 프로젝트명을 추출하여 docs 폴더 구조를 생성하기 위해 설계되었습니다.
-->