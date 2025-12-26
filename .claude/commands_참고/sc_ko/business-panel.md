# /sc:business-panel - 비즈니스 패널 분석 시스템

```yaml
---
command: "/sc:business-panel"
category: "분석 및 전략 기획"
purpose: "적응형 상호작용 모드를 사용한 다중 전문가 비즈니스 분석"
wave-enabled: true
performance-profile: "complex"
---
```

## 개요 (Overview)

저명한 비즈니스 사상가들 간의 AI 촉진 패널 토론으로, 그들의 독특한 프레임워크와 방법론을 통해 문서를 분석합니다.

## 전문가 패널 (Expert Panel)

### 참여 가능 전문가 (Available Experts)
- **클레이튼 크리스텐슨 (Clayton Christensen)**: 파괴적 혁신 이론, 해야 할 일 (Jobs-to-be-Done)
- **마이클 포터 (Michael Porter)**: 경쟁 전략, 5가지 힘 (Five Forces)
- **피터 드러커 (Peter Drucker)**: 경영 철학, 목표에 의한 관리 (MBO)
- **세스 고딘 (Seth Godin)**: 마케팅 혁신, 부족 구축 (Tribe Building)
- **김위찬 & 르네 마보안 (W. Chan Kim & Renée Mauborgne)**: 블루오션 전략
- **짐 콜린스 (Jim Collins)**: 조직적 탁월함, 좋은 기업을 넘어 위대한 기업으로 (Good to Great)
- **나심 니콜라스 탈레브 (Nassim Nicholas Taleb)**: 리스크 관리, 안티프래질 (Antifragility)
- **도넬라 메도즈 (Donella Meadows)**: 시스템 사고, 레버리지 포인트
- **장뤽 두몽 (Jean-luc Doumont)**: 커뮤니케이션 시스템, 구조화된 명확성

## 분석 모드 (Analysis Modes)

### 1단계: 토론 (DISCUSSION) (기본)
전문가들이 각자의 프레임워크를 통해 서로의 통찰력을 기반으로 협력하여 분석합니다.

### 2단계: 토론 (DEBATE)
전문가들 간 의견이 다르거나 논쟁적인 주제에 대해 활성화되는 대립적 분석입니다.

### 3단계: 소크라테스식 질문법 (SOCRATIC INQUIRY)
심층 학습 및 전략적 사고 개발을 위한 질문 중심의 탐색입니다.

## 사용법 (Usage)

### 기본 사용법
```bash
/sc:business-panel [document_path_or_content]
```

### 고급 옵션
```bash
/sc:business-panel [content] --experts "porter,christensen,meadows"
/sc:business-panel [content] --mode debate
/sc:business-panel [content] --focus "competitive-analysis"
/sc:business-panel [content] --synthesis-only
```

### 모드 명령어 (Mode Commands)
- `--mode discussion` - 협력적 분석 (기본)
- `--mode debate` - 아이디어에 도전하고 스트레스 테스트
- `--mode socratic` - 질문 중심의 탐색
- `--mode adaptive` - 내용에 따라 시스템이 선택

### 전문가 선택 (Expert Selection)
- `--experts "name1,name2,name3"` - 특정 전문가 선택
- `--focus domain` - 도메인에 맞춰 전문가 자동 선택
- `--all-experts` - 9명의 모든 전문가 포함

### 출력 옵션 (Output Options)
- `--synthesis-only` - 상세 분석을 건너뛰고 종합 결과만 표시
- `--structured` - 효율성을 위해 심볼 시스템 사용
- `--verbose` - 전체 상세 분석
- `--questions` - 전략적 질문에 집중

## 자동 페르소나 활성화 (Auto-Persona Activation)
- **자동 활성화**: 분석가, 아키텍트, 멘토 페르소나
- **MCP 통합**: Sequential (주요), Context7 (비즈니스 패턴)
- **도구 오케스트레이션**: Read, Grep, Write, MultiEdit, TodoWrite

## 통합 참고사항 (Integration Notes)
- 모든 사고 플래그와 호환됨 (--think, --think-hard, --ultrathink)
- 포괄적인 비즈니스 분석을 위한 웨이브 오케스트레이션 지원
- 전문적인 비즈니스 커뮤니케이션을 위해 서기 페르소나와 통합됨
