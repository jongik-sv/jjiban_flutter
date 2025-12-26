---
name: select-tool
description: "복잡성 점수 및 작업 분석을 기반으로 한 지능적인 MCP 도구 선택"
category: special
complexity: high
mcp-servers: [serena, morphllm]
personas: []
---

# /sc:select-tool - 지능적인 MCP 도구 선택

## 트리거 (Triggers)
- Serena와 Morphllm 사이에서 최적의 MCP 도구 선택이 필요한 작업
- 복잡성 분석 및 기능 매칭이 필요한 메타 시스템 결정
- 성능 대 정확성 절충이 필요한 도구 라우팅 결정
- 지능적인 도구 기능 평가가 유익한 작업

## 사용법 (Usage)
```
/sc:select-tool [operation] [--analyze] [--explain]
```

## 행동 흐름 (Behavioral Flow)
1. **파싱 (Parse)**: 작업 유형, 범위, 파일 수 및 복잡성 지표 분석
2. **점수화 (Score)**: 다양한 작업 요인에 걸쳐 다차원 복잡성 점수 적용
3. **매칭 (Match)**: Serena 및 Morphllm 기능과 작업 요구사항 비교
4. **선택 (Select)**: 점수 매트릭스 및 성능 요구사항에 따라 최적의 도구 선택
5. **검증 (Validate)**: 선택 정확성 확인 및 신뢰도 메트릭 제공

주요 행동:
- 파일 수, 작업 유형, 언어 및 프레임워크 요구사항에 기반한 복잡성 점수화
- 최적의 선택을 위한 속도 대 정확성 절충을 평가하는 성능 평가
- 직접 매핑 및 임계값 기반 라우팅 규칙을 갖춘 결정 로직 매트릭스
- Serena(의미론적 작업) 대 Morphllm(패턴 작업)의 도구 기능 매칭

## MCP 통합 (MCP Integration)
- **Serena MCP**: 의미론적 작업, LSP 기능, 심볼 탐색 및 프로젝트 컨텍스트에 최적
- **Morphllm MCP**: 패턴 기반 편집, 대량 변환 및 속도가 중요한 작업에 최적
- **결정 매트릭스 (Decision Matrix)**: 복잡성 점수 및 작업 특성에 기반한 지능적인 라우팅

## 도구 협력 (Tool Coordination)
- **get_current_config**: 도구 기능 평가를 위한 시스템 구성 분석
- **execute_sketched_edit**: 선택 정확성을 위한 작업 테스트 및 검증
- **Read/Grep**: 작업 컨텍스트 분석 및 복잡성 요인 식별
- **통합 (Integration)**: refactor, edit, implement, improve 명령어에서 사용되는 자동 선택 로직

## 주요 패턴 (Key Patterns)
- **직접 매핑 (Direct Mapping)**: 심볼 작업 → Serena, 패턴 편집 → Morphllm, 메모리 작업 → Serena
- **복잡성 임계값 (Complexity Thresholds)**: 점수 >0.6 → Serena, 점수 <0.4 → Morphllm, 0.4-0.6 → 기능 기반
- **성능 절충 (Performance Trade-offs)**: 속도 요구사항 → Morphllm, 정확성 요구사항 → Serena
- **대체 전략 (Fallback Strategy)**: Serena → Morphllm → 네이티브 도구로 이어지는 성능 저하 체인

## 예시 (Examples)

### 복잡한 리팩토링 작업
```
/sc:select-tool "rename function across 10 files" --analyze
# 분석: 높은 복잡성 (다중 파일, 심볼 작업)
# 선택: Serena MCP (LSP 기능, 의미론적 이해)
```

### 패턴 기반 대량 편집
```
/sc:select-tool "update console.log to logger.info across project" --explain
# 분석: 패턴 기반 변환, 속도 우선
# 선택: Morphllm MCP (패턴 매칭, 대량 작업)
```

### 메모리 관리 작업
```
/sc:select-tool "save project context and discoveries"
# 직접 매핑: 메모리 작업 → Serena MCP
# 근거: 프로젝트 컨텍스트 및 세션 간 지속성
```

## 경계 (Boundaries)

**수행할 작업:**
- 작업을 분석하고 Serena와 Morphllm 사이에서 최적의 도구 선택을 제공합니다.
- 파일 수, 작업 유형 및 요구사항에 따라 복잡성 점수를 적용합니다.
- 95% 이상의 선택 정확도로 100ms 미만의 결정 시간을 제공합니다.

**수행하지 않을 작업:**
- 사용자가 명확한 선호도를 가질 때 명시적인 도구 명세를 무시하지 않습니다.
- 적절한 복잡성 분석 및 기능 매칭 없이 도구를 선택하지 않습니다.
- 편의성이나 속도를 위해 성능 요구사항을 타협하지 않습니다.
