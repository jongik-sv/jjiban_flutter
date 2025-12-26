---
name: design:ui_theme
description: "외부 사이트 UI/UX 테마 자동 추출 및 가이드 문서 생성"
category: analysis
complexity: complex
wave-enabled: true
performance-profile: optimization
auto-flags:
  - --wave-mode force
  - --wave-strategy systematic
  - --seq
  - --play
  - --c7
  - --validate
  - --uc
mcp-servers: [sequential, playwright, context7]
personas: [analyzer, frontend, architect, scribe]
allowed-tools: [WebFetch, Read, Write, Glob, Grep, TodoWrite]
---

# /plan:ui_theme - 지능형 UI/UX 테마 추출 시스템

> **Wave 시스템 활용**: 외부 사이트의 UI/UX 디자인 원칙을 체계적으로 분석하고 JSON 형태로 정리하여 UI/UX 가이드 문서를 자동 생성합니다.

## 트리거
- 기존 사이트의 디자인 시스템 분석이 필요한 경우
- SaaS/ERP 시스템의 UX/UI 패턴 연구가 필요한 경우
- 디자인 원칙 및 컴포넌트 표준화 가이드 작성이 필요한 경우
- 경쟁사 분석 및 벤치마킹이 필요한 경우

## 사용법
```bash
/plan:ui_theme "https://example.com/dashboard"
/plan:ui_theme "https://app.salesforce.com" --focus "saas-erp"
/plan:ui_theme "https://notion.so" --analysis-depth deep
```

## Wave 자동 실행 플로우

### Wave 1: 사이트 접근 및 기본 분석
**Auto-Persona**: analyzer + frontend
**MCP**: playwright + sequential
**산출물**:
- 사이트 접근성 확인
- 초기 페이지 구조 분석
- 스크린샷 및 DOM 구조 수집

**자동 실행 단계**:
1. **사이트 접근성 검증**:
   - Playwright로 URL 접근 확인
   - 로딩 시간 및 응답성 측정
   - 에러 페이지 여부 확인
2. **초기 화면 캡처**:
   - 데스크톱 뷰포트 스크린샷 (1920x1080)
   - 모바일 뷰포트 스크린샷 (375x667)
   - 태블릿 뷰포트 스크린샷 (768x1024)
3. **DOM 구조 수집**:
   - HTML 구조 분석
   - CSS 스타일시트 추출
   - JavaScript 상호작용 요소 식별

### Wave 2: 디자인 요소 상세 분석
**Auto-Persona**: frontend + analyzer
**MCP**: playwright + sequential + context7
**산출물**:
- 컬러 팔레트 추출
- 타이포그래피 분석
- 레이아웃 패턴 식별
- 컴포넌트 카탈로그 생성

**자동 실행 단계**:
1. **색상 시스템 분석**:
   - 주요 브랜드 컬러 추출 (Primary, Secondary, Accent)
   - 상태별 컬러 (Success, Warning, Error, Info)
   - 중성 컬러 (배경, 텍스트, 경계선)
   - 컬러 접근성 대비율 분석
2. **타이포그래피 시스템**:
   - 폰트 패밀리 및 웨이트 분석
   - 헤딩 계층 구조 (H1~H6)
   - 본문 텍스트 스타일
   - 라인 높이 및 간격 패턴
3. **레이아웃 패턴**:
   - 그리드 시스템 분석
   - 컨테이너 최대 너비
   - 간격 시스템 (Spacing Scale)
   - 반응형 브레이크포인트

### Wave 3: 컴포넌트 패턴 분석
**Auto-Persona**: frontend + architect
**MCP**: playwright + sequential
**산출물**:
- UI 컴포넌트 인벤토리
- 상호작용 패턴 분석
- 상태 관리 패턴
- 접근성 기능 평가

**자동 실행 단계**:
1. **기본 컴포넌트 분석**:
   - 버튼 (Primary, Secondary, Tertiary)
   - 입력 필드 (Text, Select, Checkbox, Radio)
   - 카드 및 컨테이너
   - 내비게이션 (헤더, 사이드바, 브레드크럼)
2. **복합 컴포넌트 분석**:
   - 데이터 테이블
   - 폼 레이아웃
   - 모달 및 오버레이
   - 대시보드 위젯
3. **상호작용 패턴**:
   - 호버 및 포커스 상태
   - 로딩 상태 표시
   - 피드백 메시지
   - 애니메이션 및 전환 효과

### Wave 4: UX 패턴 및 사용성 분석
**Auto-Persona**: frontend + analyzer
**MCP**: playwright + sequential
**산출물**:
- 사용자 흐름 분석
- 정보 아키텍처
- 사용성 원칙 추출
- 접근성 평가

**자동 실행 단계**:
1. **정보 아키텍처 분석**:
   - 주요 내비게이션 구조
   - 정보 계층 및 그룹핑
   - 검색 및 필터링 패턴
   - 사용자 맥락별 정보 우선순위
2. **사용자 경험 패턴**:
   - 태스크 플로우 분석
   - 오류 처리 방식
   - 피드백 및 확인 패턴
   - 개인화 및 커스터마이징
3. **접근성 기능**:
   - 키보드 내비게이션
   - 스크린 리더 호환성
   - 색상 대비 및 가독성
   - ARIA 라벨 및 역할

### Wave 5: JSON 구조화 및 가이드 문서 생성
**Auto-Persona**: scribe + architect
**MCP**: sequential + context7
**산출물**:
- JSON 형태의 디자인 토큰
- UI/UX 가이드 문서
- 구현 가이드라인
- 맥락적 사용 권장사항

**자동 실행 단계**:
1. **JSON 디자인 토큰 생성**:
```json
{
  "metadata": {
    "site_url": "URL",
    "analysis_date": "YYYY-MM-DD",
    "viewport_analyzed": ["desktop", "tablet", "mobile"],
    "claude_model": "claude-sonnet-4-20250514"
  },
  "colors": {
    "brand": {
      "primary": "#hex",
      "secondary": "#hex",
      "accent": "#hex"
    },
    "semantic": {
      "success": "#hex",
      "warning": "#hex",
      "error": "#hex",
      "info": "#hex"
    },
    "neutral": {
      "gray-50": "#hex",
      "gray-100": "#hex"
    }
  },
  "typography": {
    "font_families": {
      "primary": "font-name",
      "secondary": "font-name"
    },
    "scale": {
      "h1": { "size": "px", "weight": "weight", "line_height": "ratio" },
      "h2": { "size": "px", "weight": "weight", "line_height": "ratio" }
    }
  },
  "spacing": {
    "scale": ["4px", "8px", "16px", "24px", "32px"],
    "grid": {
      "container_max_width": "1200px",
      "columns": 12,
      "gutter": "24px"
    }
  },
  "components": {
    "button": {
      "primary": {
        "background": "#hex",
        "text": "#hex",
        "border_radius": "px",
        "padding": "vertical horizontal",
        "states": {
          "hover": { "background": "#hex" },
          "focus": { "outline": "style" },
          "disabled": { "opacity": "value" }
        }
      }
    },
    "card": {
      "background": "#hex",
      "border": "style",
      "border_radius": "px",
      "shadow": "box-shadow value",
      "padding": "value"
    }
  },
  "patterns": {
    "navigation": {
      "type": "horizontal|vertical|mixed",
      "hierarchy": ["primary", "secondary", "tertiary"],
      "active_state": "style description"
    },
    "layout": {
      "header_height": "px",
      "sidebar_width": "px",
      "content_max_width": "px"
    }
  },
  "interactions": {
    "animations": {
      "duration": "ms",
      "easing": "function",
      "common_transitions": ["fade", "slide", "scale"]
    },
    "feedback": {
      "success_message": "style description",
      "error_message": "style description",
      "loading_indicator": "style description"
    }
  },
  "accessibility": {
    "color_contrast": {
      "aa_compliant": "boolean",
      "aaa_compliant": "boolean"
    },
    "keyboard_navigation": "present|absent",
    "screen_reader": "optimized|basic|poor"
  },
  "context_insights": {
    "industry": "saas|erp|e-commerce|etc",
    "user_type": "enterprise|consumer|mixed",
    "complexity_level": "simple|moderate|complex",
    "primary_tasks": ["task1", "task2", "task3"],
    "design_philosophy": "description"
  }
}
```

2. **UI/UX 가이드 문서 생성**:
   - 위치: `./docs/common/06.guide/`
   - 파일명: `ui-ux_guide_202509151203.md`
   - 모델명 상단 표시: `claude-sonnet-4-20250514`

**가이드 문서 구성**:
- 디자인 시스템 개요
- 색상 시스템 및 사용 가이드
- 타이포그래피 가이드라인
- 컴포넌트 라이브러리
- 레이아웃 패턴 및 그리드 시스템
- 상호작용 및 애니메이션 가이드
- 접근성 가이드라인
- 반응형 디자인 원칙
- 구현 예시 및 코드 스니펫
- 맥락별 사용 권장사항

## 컨텍스트 인사이트 분석

### 산업별 특화 분석
```yaml
saas_erp_focus:
  key_elements: ["데이터 밀도", "워크플로우 효율성", "계층적 정보 구조"]
  ui_priorities: ["스캔 가능성", "액션 명확성", "상태 피드백"]
  ux_patterns: ["대시보드 레이아웃", "드릴다운 내비게이션", "배치 작업"]

e_commerce_focus:
  key_elements: ["제품 표시", "구매 전환", "신뢰성 신호"]
  ui_priorities: ["시각적 계층", "CTA 명확성", "브랜드 일관성"]
  ux_patterns: ["제품 브라우징", "장바구니 플로우", "체크아웃 프로세스"]

content_platform_focus:
  key_elements: ["콘텐츠 가독성", "개인화", "소셜 상호작용"]
  ui_priorities: ["타이포그래피", "미디어 처리", "피드 레이아웃"]
  ux_patterns: ["콘텐츠 발견", "소셜 피드", "검색 및 필터"]
```

### 맥락적 연결 분석
- **컨텐츠-디자인 관계**: 정보 유형에 따른 시각적 처리 방식
- **사용자 행동-UI 패턴**: 주요 태스크와 연결된 인터페이스 설계
- **비즈니스 목표-UX 전략**: 수익 모델과 연결된 사용자 경험 설계

## 주요 특징

### 🎨 포괄적 디자인 분석
- **시각적 요소**: 색상, 타이포그래피, 간격, 형태
- **상호작용 요소**: 애니메이션, 전환, 피드백
- **구조적 요소**: 레이아웃, 정보 아키텍처, 내비게이션

### 📱 반응형 및 접근성 중심
- **다중 뷰포트**: 데스크톱, 태블릿, 모바일 분석
- **접근성 평가**: WCAG 가이드라인 기준 평가
- **브라우저 호환성**: 크로스 브라우저 렌더링 확인

### 🧩 컨텍스트 인식 분석
- **산업별 특화**: 도메인별 UI/UX 패턴 인식
- **사용자 중심**: 타겟 사용자에 따른 디자인 원칙 추출
- **비즈니스 연계**: 사업 목표와 연결된 디자인 결정

### 📋 구조화된 문서화
- **JSON 토큰**: 개발자 친화적 구조화된 데이터
- **가이드 문서**: 디자이너/개발자용 실용적 가이드
- **구현 예시**: 실제 코드 스니펫 포함

## 예상 실행 시간
- **단순 사이트** (랜딩 페이지): 15-20분
- **중간 사이트** (SaaS 대시보드): 25-35분
- **복합 사이트** (엔터프라이즈 플랫폼): 40-60분

## 자동 산출물 목록
1. **JSON 디자인 토큰**
   - 색상 시스템
   - 타이포그래피 스케일
   - 간격 및 그리드 시스템
   - 컴포넌트 스타일

2. **스크린샷 컬렉션**
   - 다중 뷰포트 캡처
   - 컴포넌트별 상세 캡처
   - 상태별 UI 캡처

3. **UI/UX 가이드 문서**
   - 디자인 원칙 및 철학
   - 컴포넌트 사용 가이드
   - 구현 가이드라인
   - 접근성 권장사항

4. **컨텍스트 인사이트**
   - 산업별 특화 분석
   - 사용자 경험 패턴
   - 비즈니스 목표 연계 분석

## 품질 보장 기능

### 🔍 다층 검증 시스템
- **자동 스크린샷 비교**: 다중 뷰포트 일관성 확인
- **CSS 추출 검증**: 실제 적용된 스타일 vs 추출된 토큰
- **접근성 자동 검사**: aXe 엔진 기반 자동 평가

### 📊 데이터 품질 관리
- **중복 제거**: 유사한 색상/크기 값 통합
- **계층화**: 우선순위 기반 토큰 구조화
- **표준화**: 일관된 명명 규칙 적용

## 제한사항 및 주의사항
- **사이트 접근성**: 로그인이 필요한 페이지는 분석 제한
- **동적 콘텐츠**: JavaScript 렌더링 콘텐츠는 로딩 후 분석
- **저작권 준수**: 분석 목적으로만 사용, 디자인 복제 금지
- **데이터 정확성**: 자동 추출이므로 일부 수동 검토 권장

## 성공 조건
- ✅ 완전한 JSON 디자인 토큰 생성
- ✅ 다중 뷰포트 스크린샷 캡처
- ✅ 포괄적 UI/UX 가이드 문서 완성
- ✅ 접근성 평가 및 권장사항 제시
- ✅ 컨텍스트 인사이트 및 실무 적용 가이드 제공

---

**핵심 장점**: 수동 분석 대비 10배 빠른 속도로 체계적이고 재사용 가능한 디자인 시스템 문서를 생성하여, 팀의 디자인 일관성과 개발 효율성을 크게 향상시킵니다.

<!--
MES-AI 개발 프레임워크 - Command Documentation
Copyright (c) 2025 장종익 - 동국시스템즈
Command: ui_theme_extract
Category: analysis
Version: 1.0
Developer: 장종익

이 명령어는 외부 사이트 UI/UX 테마 자동 추출 및 가이드 문서 생성을 위해 설계되었습니다.
-->
