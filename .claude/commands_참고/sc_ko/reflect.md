---
name: reflect
description: "Serena MCP 분석 기능을 사용한 작업 성찰 및 검증"
category: special
complexity: standard
mcp-servers: [serena]
personas: []
---

# /sc:reflect - 작업 성찰 및 검증

## 트리거 (Triggers)
- 검증 및 품질 평가가 필요한 작업 완료
- 세션 진행 상황 분석 및 수행된 작업에 대한 성찰
- 프로젝트 개선을 위한 세션 간 학습 및 통찰력 캡처
- 포괄적인 작업 준수 확인이 필요한 품질 게이트

## 사용법 (Usage)
```
/sc:reflect [--type task|session|completion] [--analyze] [--validate]
```

## 행동 흐름 (Behavioral Flow)
1. **분석 (Analyze)**: Serena 성찰 도구를 사용하여 현재 작업 상태 및 세션 진행 상황 검토
2. **검증 (Validate)**: 작업 준수, 완료 품질 및 요구사항 이행 평가
3. **성찰 (Reflect)**: 수집된 정보 및 세션 통찰력에 대한 심층 분석 적용
4. **문서화 (Document)**: 세션 메타데이터 업데이트 및 학습 통찰력 캡처
5. **최적화 (Optimize)**: 프로세스 개선 및 품질 향상을 위한 추천 사항 제공

주요 행동:
- 포괄적인 성찰 분석 및 작업 검증을 위한 Serena MCP 통합
- TodoWrite 패턴과 고급 Serena 분석 기능 간의 다리 역할
- 세션 간 지속성 및 학습 캡처를 통한 세션 라이프사이클 통합
- 핵심 성찰 및 검증을 위한 <200ms 성능에 민감한 작업

## MCP 통합 (MCP Integration)
- **Serena MCP**: 성찰 분석, 작업 검증 및 세션 메타데이터를 위한 필수 통합
- **성찰 도구 (Reflection Tools)**: think_about_task_adherence, think_about_collected_information, think_about_whether_you_are_done
- **메모리 작업 (Memory Operations)**: read_memory, write_memory, list_memories를 사용한 세션 간 지속성
- **성능 중요 (Performance Critical)**: 핵심 성찰 작업 <200ms, 체크포인트 생성 <1s

## 도구 협력 (Tool Coordination)
- **TodoRead/TodoWrite**: 전통적인 작업 관리와 고급 성찰 분석 간의 다리 역할
- **think_about_task_adherence**: 프로젝트 목표 및 세션 목표에 대한 현재 접근 방식 검증
- **think_about_collected_information**: 세션 작업 및 정보 수집 완전성 분석
- **think_about_whether_you_are_done**: 작업 완료 기준 평가 및 남은 작업 식별
- **메모리 도구 (Memory Tools)**: 세션 메타데이터 업데이트 및 세션 간 학습 캡처

## 주요 패턴 (Key Patterns)
- **작업 검증 (Task Validation)**: 현재 접근 방식 → 목표 정렬 → 편차 식별 → 경로 수정
- **세션 분석 (Session Analysis)**: 정보 수집 → 완전성 평가 → 품질 평가 → 통찰력 캡처
- **완료 평가 (Completion Assessment)**: 진행 상황 평가 → 완료 기준 → 남은 작업 → 결정 검증
- **세션 간 학습 (Cross-Session Learning)**: 성찰 통찰력 → 메모리 지속성 → 향상된 프로젝트 이해

## 예시 (Examples)

### 작업 준수 성찰
```
/sc:reflect --type task --analyze
# 프로젝트 목표에 대한 현재 접근 방식 검증
# 편차 식별 및 경로 수정 추천 사항 제공
```

### 세션 진행 상황 분석
```
/sc:reflect --type session --validate
# 세션 작업 및 정보 수집에 대한 포괄적인 분석
# 프로젝트 개선을 위한 품질 평가 및 격차 식별
```

### 완료 검증
```
/sc:reflect --type completion
# 실제 진행 상황에 대한 작업 완료 기준 평가
# 작업 완료 준비 상태 결정 및 남은 장애물 식별
```

## 경계 (Boundaries)

**수행할 작업:**
- Serena MCP 분석 도구를 사용하여 포괄적인 작업 성찰 및 검증을 수행합니다.
- 향상된 작업 관리를 위해 TodoWrite 패턴과 고급 성찰 기능을 연결합니다.
- 세션 간 학습 캡처 및 세션 라이프사이클 통합을 제공합니다.

**수행하지 않을 작업:**
- 적절한 Serena MCP 통합 및 성찰 도구 접근 없이 작동하지 않습니다.
- 적절한 준수 및 품질 검증 없이 작업 완료 결정을 무시하지 않습니다.
- 세션 무결성 확인 및 세션 간 지속성 요구사항을 우회하지 않습니다.
