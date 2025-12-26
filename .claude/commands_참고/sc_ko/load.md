---
name: load
description: "Serena MCP 통합을 통한 세션 라이프사이클 관리 및 프로젝트 컨텍스트 로딩"
category: session
complexity: standard
mcp-servers: [serena]
personas: []
---

# /sc:load - 프로젝트 컨텍스트 로딩

## 트리거 (Triggers)
- 세션 초기화 및 프로젝트 컨텍스트 로딩 요청
- 세션 간 지속성 및 메모리 검색 필요
- 프로젝트 활성화 및 컨텍스트 관리 요구사항
- 세션 라이프사이클 관리 및 체크포인트 로딩 시나리오

## 사용법 (Usage)
```
/sc:load [target] [--type project|config|deps|checkpoint] [--refresh] [--analyze]
```

## 행동 흐름 (Behavioral Flow)
1. **초기화 (Initialize)**: Serena MCP 연결 및 세션 컨텍스트 관리 설정
2. **탐색 (Discover)**: 프로젝트 구조 분석 및 컨텍스트 로딩 요구사항 식별
3. **로드 (Load)**: 프로젝트 메모리, 체크포인트 및 세션 간 지속성 데이터 검색
4. **활성화 (Activate)**: 프로젝트 컨텍스트 설정 및 개발 워크플로우 준비
5. **검증 (Validate)**: 로드된 컨텍스트 무결성 및 세션 준비 상태 확인

주요 행동:
- 메모리 관리 및 세션 간 지속성을 위한 Serena MCP 통합
- 포괄적인 컨텍스트 로딩 및 검증을 통한 프로젝트 활성화
- <500ms 초기화 목표를 가진 성능에 민감한 작업
- 체크포인트 및 메모리 조정을 통한 세션 라이프사이클 관리

## MCP 통합 (MCP Integration)
- **Serena MCP**: 프로젝트 활성화, 메모리 검색 및 세션 관리를 위한 필수 통합
- **메모리 작업 (Memory Operations)**: 세션 간 지속성, 체크포인트 로딩 및 컨텍스트 복원
- **성능 중요 (Performance Critical)**: 핵심 작업 <200ms, 체크포인트 생성 <1s

## 도구 협력 (Tool Coordination)
- **activate_project**: 핵심 프로젝트 활성화 및 컨텍스트 설정
- **list_memories/read_memory**: 메모리 검색 및 세션 컨텍스트 로딩
- **Read/Grep/Glob**: 프로젝트 구조 분석 및 구성 탐색
- **Write**: 세션 컨텍스트 문서화 및 체크포인트 생성

## 주요 패턴 (Key Patterns)
- **프로젝트 활성화 (Project Activation)**: 디렉토리 분석 → 메모리 검색 → 컨텍스트 설정
- **세션 복원 (Session Restoration)**: 체크포인트 로딩 → 컨텍스트 검증 → 워크플로우 준비
- **메모리 관리 (Memory Management)**: 세션 간 지속성 → 컨텍스트 연속성 → 개발 효율성
- **성능 중요 (Performance Critical)**: 빠른 초기화 → 즉각적인 생산성 → 세션 준비 상태

## 예시 (Examples)

### 기본 프로젝트 로딩
```
/sc:load
# Serena 메모리 통합으로 현재 디렉토리 프로젝트 컨텍스트 로드
# 세션 컨텍스트 설정 및 개발 워크플로우 준비
```

### 특정 프로젝트 로딩
```
/sc:load /path/to/project --type project --analyze
# 포괄적인 분석으로 특정 프로젝트 로드
# 프로젝트 컨텍스트 활성화 및 세션 간 메모리 검색
```

### 체크포인트 복원
```
/sc:load --type checkpoint --checkpoint session_123
# 세션 컨텍스트로 특정 체크포인트 복원
# 전체 컨텍스트 보존으로 이전 작업 세션 계속
```

### 종속성 컨텍스트 로딩
```
/sc:load --type deps --refresh
# 새로운 분석으로 종속성 컨텍스트 로드
# 프로젝트 이해도 및 종속성 매핑 업데이트
```

## 경계 (Boundaries)

**수행할 작업:**
- 메모리 관리를 위해 Serena MCP 통합을 사용하여 프로젝트 컨텍스트를 로드합니다.
- 세션 간 지속성을 통해 세션 라이프사이클 관리를 제공합니다.
- 포괄적인 컨텍스트 로딩으로 프로젝트 활성화를 설정합니다.

**수행하지 않을 작업:**
- 명시적인 허가 없이 프로젝트 구조나 구성을 수정하지 않습니다.
- 적절한 Serena MCP 통합 및 검증 없이 컨텍스트를 로드하지 않습니다.
- 체크포인트 보존 없이 기존 세션 컨텍스트를 덮어쓰지 않습니다.
