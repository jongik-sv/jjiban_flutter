---
name: brainstorm
description: "소크라테스식 대화와 체계적인 탐색을 통한 상호작용적 요구사항 발굴"
category: orchestration
complexity: advanced
mcp-servers: [sequential, context7, magic, playwright, morphllm, serena]
personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
---

# /sc:brainstorm - 상호작용적 요구사항 발굴

> **컨텍스트 프레임워크 참고**: 이 파일은 Claude Code 사용자가 `/sc:brainstorm` 패턴을 입력했을 때의 행동 지침을 제공합니다. 이것은 실행 가능한 명령이 아니며, 아래에 정의된 행동 패턴을 활성화하는 컨텍스트 트리거입니다.

## 트리거 (Triggers)
- 구조화된 탐색이 필요한 모호한 프로젝트 아이디어
- 요구사항 발굴 및 명세서 개발 필요
- 컨셉 검증 및 실현 가능성 평가 요청
- 세션 간 브레인스토밍 및 반복적 개선 시나리오

## 컨텍스트 트리거 패턴 (Context Trigger Pattern)
```
/sc:brainstorm [topic/idea] [--strategy systematic|agile|enterprise] [--depth shallow|normal|deep] [--parallel]
```
**사용법**: 체계적인 탐색 및 다중 페르소나 협력을 통해 브레인스토밍 행동 모드를 활성화하려면 Claude Code 대화에 이 패턴을 입력하십시오.

## 행동 흐름 (Behavioral Flow)
1. **탐색 (Explore)**: 소크라테스식 대화와 체계적인 질문을 통해 모호한 아이디어를 구체화
2. **분석 (Analyze)**: 도메인 전문 지식과 포괄적인 분석을 위해 여러 페르소나를 조율
3. **검증 (Validate)**: 여러 도메인에 걸쳐 실현 가능성 평가 및 요구사항 검증 적용
4. **명세화 (Specify)**: 세션 간 지속성 기능을 갖춘 구체적인 명세서 생성
5. **핸드오프 (Handoff)**: 구현 또는 추가 개발 준비가 된 실행 가능한 요약본 생성

주요 행동:
- 아키텍처, 분석, 프론트엔드, 백엔드, 보안 도메인에 걸친 다중 페르소나 오케스트레이션
- 전문 분석을 위한 지능적인 라우팅을 통한 고급 MCP 협력
- 점진적인 대화 향상 및 병렬 탐색을 통한 체계적인 실행
- 포괄적인 요구사항 발굴 문서화를 통한 세션 간 지속성

## MCP 통합 (MCP Integration)
- **Sequential MCP**: 체계적인 탐색 및 검증을 위한 복잡한 다단계 추론
- **Context7 MCP**: 프레임워크별 실현 가능성 평가 및 패턴 분석
- **Magic MCP**: UI/UX 실현 가능성 및 디자인 시스템 통합 분석
- **Playwright MCP**: 사용자 경험 검증 및 상호작용 패턴 테스트
- **Morphllm MCP**: 대규모 콘텐츠 분석 및 패턴 기반 변환
- **Serena MCP**: 세션 간 지속성, 메모리 관리 및 프로젝트 컨텍스트 강화

## 도구 협력 (Tool Coordination)
- **Read/Write/Edit**: 요구사항 문서화 및 명세서 생성
- **TodoWrite**: 복잡한 다단계 탐색을 위한 진행 상황 추적
- **Task**: 병렬 탐색 경로 및 다중 에이전트 협력을 위한 고급 위임
- **WebSearch**: 시장 조사, 경쟁 분석 및 기술 검증
- **sequentialthinking**: 복잡한 요구사항 분석을 위한 구조화된 추론

## 주요 패턴 (Key Patterns)
- **소크라테스식 대화 (Socratic Dialogue)**: 질문 중심의 탐색 → 체계적인 요구사항 발굴
- **다중 도메인 분석 (Multi-Domain Analysis)**: 여러 기능 분야의 전문 지식 → 포괄적인 실현 가능성 평가
- **점진적 협력 (Progressive Coordination)**: 체계적인 탐색 → 반복적인 개선 및 검증
- **명세서 생성 (Specification Generation)**: 구체적인 요구사항 → 실행 가능한 구현 요약본

## 예시 (Examples)

### 체계적인 제품 발굴
```
/sc:brainstorm "AI-powered project management tool" --strategy systematic --depth deep
# 다중 페르소나 분석: architect (시스템 설계), analyzer (실현 가능성), project-manager (요구사항)
# Sequential MCP가 구조화된 탐색 프레임워크 제공
```

### 애자일 기능 탐색
```
/sc:brainstorm "real-time collaboration features" --strategy agile --parallel
# 프론트엔드, 백엔드, 보안 페르소나를 사용한 병렬 탐색 경로
# 프레임워크 및 UI 패턴 분석을 위한 Context7 및 Magic MCP
```

### 엔터프라이즈 솔루션 검증
```
/sc:brainstorm "enterprise data analytics platform" --strategy enterprise --validate
# 보안, 데브옵스, 아키텍트 페르소나를 사용한 포괄적인 검증
# 엔터프라이즈 요구사항 추적을 위한 Serena MCP
```

### 세션 간 개선
```
/sc:brainstorm "mobile app monetization strategy" --depth normal
# Serena MCP가 세션 간 컨텍스트 및 반복적 개선 관리
# 메모리 기반 통찰력을 통한 점진적인 대화 향상
```

## 경계 (Boundaries)

**수행할 작업:**
- 체계적인 탐색을 통해 모호한 아이디어를 구체적인 명세서로 변환
- 포괄적인 분석을 위해 여러 페르소나와 MCP 서버를 조율
- 세션 간 지속성 및 점진적인 대화 향상 제공

**수행하지 않을 작업:**
- 적절한 요구사항 발굴 없이 구현 결정
- 탐색 단계에서 규정된 솔루션으로 사용자 비전 무시
- 복잡한 다중 도메인 프로젝트에 대한 체계적인 탐색 생략
