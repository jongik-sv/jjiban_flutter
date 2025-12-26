---
name: git
description: "지능적인 커밋 메시지 및 워크플로우 최적화를 통한 Git 작업"
category: utility
complexity: basic
mcp-servers: []
personas: []
---

# /sc:git - Git 작업

## 트리거 (Triggers)
- Git 저장소 작업: status, add, commit, push, pull, branch
- 지능적인 커밋 메시지 생성 필요
- 저장소 워크플로우 최적화 요청
- 브랜치 관리 및 병합 작업

## 사용법 (Usage)
```
/sc:git [operation] [args] [--smart-commit] [--interactive]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: 저장소 상태 및 작업 디렉토리 변경 사항 확인
2. **검증 (Validate)**: 현재 Git 컨텍스트에 작업이 적절한지 확인
3. **실행 (Execute)**: 지능적인 자동화로 Git 명령어 실행
4. **최적화 (Optimize)**: 스마트 커밋 메시지 및 워크플로우 패턴 적용
5. **보고 (Report)**: 상태 및 다음 단계 가이드 제공

주요 행동:
- 변경 분석을 기반으로 한 규약적 커밋 메시지 생성
- 일관된 브랜치 이름 규칙 적용
- 안내에 따른 병합 충돌 처리
- 명확한 상태 요약 및 워크플로우 추천 제공

## 도구 협력 (Tool Coordination)
- **Bash**: Git 명령어 실행 및 저장소 작업
- **Read**: 저장소 상태 분석 및 구성 검토
- **Grep**: 로그 파싱 및 상태 분석
- **Write**: 커밋 메시지 생성 및 문서화

## 주요 패턴 (Key Patterns)
- **스마트 커밋 (Smart Commits)**: 변경 사항 분석 → 규약적 커밋 메시지 생성
- **상태 분석 (Status Analysis)**: 저장소 상태 → 실행 가능한 추천 사항
- **브랜치 전략 (Branch Strategy)**: 일관된 이름 지정 및 워크플로우 강제
- **오류 복구 (Error Recovery)**: 충돌 해결 및 상태 복원 가이드

## 예시 (Examples)

### 스마트 상태 분석
```
/sc:git status
# 변경 요약과 함께 저장소 상태 분석
# 다음 단계 및 워크플로우 추천 제공
```

### 지능적인 커밋
```
/sc:git commit --smart-commit
# 변경 분석에서 규약적 커밋 메시지 생성
# 모범 사례 및 일관된 서식 적용
```

### 대화형 작업
```
/sc:git merge feature-branch --interactive
# 충돌 해결 지원을 통한 안내된 병합
```

## 경계 (Boundaries)

**수행할 작업:**
- 지능적인 자동화로 Git 작업을 실행합니다.
- 변경 분석에서 규약적 커밋 메시지를 생성합니다.
- 워크플로우 최적화 및 모범 사례 가이드를 제공합니다.

**수행하지 않을 작업:**
- 명시적인 승인 없이 저장소 구성을 수정하지 않습니다.
- 확인 없이 파괴적인 작업을 실행하지 않습니다.
- 수동 개입이 필요한 복잡한 병합을 처리하지 않습니다.
