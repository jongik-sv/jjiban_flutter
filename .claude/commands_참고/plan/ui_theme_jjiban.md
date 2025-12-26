---
name: plan:ui_theme
description: "외부 사이트 UI/UX 테마 추출 및 jjiban 적용 가이드 생성"
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
mcp-servers: [sequential, playwright, context7]
personas: [analyzer, frontend, architect]
allowed-tools: [WebFetch, Read, Write, Glob, Grep, TodoWrite, Bash]
---

# /plan:ui_theme - jjiban UI/UX 테마 추출 시스템

> **목적**: 외부 사이트의 UI/UX 디자인 요소를 분석하여 jjiban 프로젝트(Nuxt 3 + Vue 3 + PrimeVue 4 + TailwindCSS)에 적용 가능한 테마 가이드를 생성합니다.

## 트리거
- 참고할 외부 사이트의 디자인 시스템 분석 필요
- SaaS/프로젝트 관리 도구의 UX/UI 패턴 연구
- PrimeVue 테마 커스터마이징 가이드 작성
- TailwindCSS 설정 파일 생성

## 사용법
```bash
/plan:ui_theme "https://example.com/dashboard"
/plan:ui_theme "https://linear.app" --focus "project-management"
/plan:ui_theme "https://notion.so" --analysis-depth deep
```

## 기술 스택 맵핑

| 추출 요소 | jjiban 적용 대상 |
|-----------|-----------------|
| 색상 시스템 | TailwindCSS `tailwind.config.ts`, PrimeVue preset |
| 타이포그래피 | `assets/css/main.css`, Tailwind 폰트 설정 |
| 컴포넌트 스타일 | PrimeVue 4.x 테마 커스터마이징 |
| 레이아웃 패턴 | Nuxt 3 레이아웃, Vue 컴포넌트 |
| 간격/그리드 | TailwindCSS spacing scale |

---

## Wave 자동 실행 플로우

### Wave 1: 사이트 접근 및 스크린샷 수집
**MCP**: playwright
**산출물**: 멀티 뷰포트 스크린샷, DOM 구조

**실행 단계**:
1. **사이트 접근성 검증**:
   - Playwright로 URL 접근 확인
   - 로딩 완료 대기 (networkidle)
2. **스크린샷 캡처**:
   - 데스크톱: 1920x1080
   - 태블릿: 768x1024
   - 모바일: 375x667
3. **DOM 분석**:
   - 주요 컴포넌트 식별
   - CSS 변수 추출

### Wave 2: 디자인 토큰 추출
**MCP**: playwright + sequential
**산출물**: 색상 팔레트, 타이포그래피, 간격 시스템

**실행 단계**:
1. **색상 시스템**:
   - Primary/Secondary/Accent 컬러
   - Semantic 컬러 (success, warning, error, info)
   - 중성 컬러 (gray scale)
   - Surface/Background 컬러
2. **타이포그래피**:
   - 폰트 패밀리
   - 헤딩 스케일 (H1~H6)
   - 본문 텍스트 스타일
3. **간격 시스템**:
   - Spacing scale 추출
   - 컨테이너 너비
   - Grid 시스템

### Wave 3: 컴포넌트 패턴 분석
**MCP**: playwright + context7
**산출물**: UI 컴포넌트 스타일 가이드

**실행 단계**:
1. **기본 컴포넌트**:
   - 버튼 (variants, states)
   - 입력 필드 (text, select, checkbox)
   - 카드 컴포넌트
   - 네비게이션
2. **복합 컴포넌트**:
   - 데이터 테이블
   - 모달/다이얼로그
   - 드롭다운 메뉴
3. **상태 표현**:
   - Hover/Focus/Active
   - Loading/Disabled
   - 에러 상태

### Wave 4: jjiban 적용 가이드 생성
**MCP**: sequential + context7
**산출물**: 테마 설정 파일, 적용 가이드 문서

**실행 단계**:
1. **TailwindCSS 설정 생성**:
   - `tailwind.config.ts` 확장 설정
   - 커스텀 컬러 팔레트
   - 커스텀 폰트 설정
2. **PrimeVue 테마 설정**:
   - Aura 프리셋 기반 커스터마이징
   - CSS 변수 오버라이드
3. **적용 가이드 문서 작성**

---

## 산출물 구조

### 1. JSON 디자인 토큰
**위치**: `assets/themes/{site-name}/design-tokens.json`

```json
{
  "metadata": {
    "source_url": "URL",
    "analysis_date": "YYYY-MM-DD",
    "target_stack": "nuxt3-primevue4-tailwind"
  },
  "colors": {
    "primary": {
      "50": "#hex", "100": "#hex", "500": "#hex", "900": "#hex"
    },
    "secondary": {},
    "semantic": {
      "success": "#hex",
      "warning": "#hex",
      "error": "#hex",
      "info": "#hex"
    },
    "surface": {
      "ground": "#hex",
      "card": "#hex",
      "overlay": "#hex"
    }
  },
  "typography": {
    "fontFamily": {
      "sans": "font-name, sans-serif",
      "mono": "font-name, monospace"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem"
    }
  },
  "spacing": {
    "scale": ["0.25rem", "0.5rem", "0.75rem", "1rem", "1.5rem", "2rem"],
    "container": {
      "sm": "640px",
      "md": "768px",
      "lg": "1024px",
      "xl": "1280px"
    }
  },
  "borderRadius": {
    "none": "0",
    "sm": "0.125rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "full": "9999px"
  },
  "shadows": {
    "sm": "box-shadow value",
    "md": "box-shadow value",
    "lg": "box-shadow value"
  }
}
```

### 2. TailwindCSS 확장 설정
**위치**: `assets/themes/{site-name}/tailwind.extend.ts`

```typescript
// tailwind.config.ts에 머지할 설정
export const themeExtend = {
  colors: {
    primary: {
      50: '#hex',
      // ...
    }
  },
  fontFamily: {
    sans: ['Font Name', 'sans-serif']
  }
}
```

### 3. PrimeVue 테마 프리셋
**위치**: `assets/themes/{site-name}/primevue-preset.ts`

```typescript
import { definePreset } from '@primevue/themes';
import Aura from '@primevue/themes/aura';

export const CustomPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '{primary.50}',
      // ...
    }
  }
});
```

### 4. 적용 가이드 문서
**위치**: `docs/common/06.guide/ui-theme-guide_{site-name}_{timestamp}.md`

**문서 구성**:
- 디자인 시스템 개요
- 색상 시스템 사용 가이드
- 타이포그래피 가이드
- 컴포넌트 스타일 가이드
- jjiban 적용 방법
- 코드 예시

---

## PrimeVue 4.x 컴포넌트 맵핑

| 분석 대상 | PrimeVue 컴포넌트 |
|----------|------------------|
| 버튼 | Button, SplitButton |
| 입력 필드 | InputText, InputNumber, Textarea |
| 선택 | Select, MultiSelect, Checkbox, RadioButton |
| 테이블 | DataTable |
| 카드 | Card, Panel |
| 모달 | Dialog |
| 메뉴 | Menu, Menubar, TieredMenu |
| 트리 | Tree, TreeTable |
| 태그 | Tag, Chip |
| 진행 | ProgressBar, ProgressSpinner |

---

## jjiban 특화 분석 포인트

### 프로젝트 관리 UI 패턴
```yaml
kanban_board:
  - 컬럼 스타일 (Todo, Design, Implement 등)
  - 카드 디자인 및 드래그 인터랙션
  - 상태 표시 (badge, tag)

task_detail:
  - 폼 레이아웃
  - 문서 목록 표시
  - 탭 네비게이션

wbs_tree:
  - 트리 노드 스타일
  - 확장/축소 인터랙션
  - 계층 표시 (들여쓰기, 연결선)

gantt_chart:
  - 타임라인 스타일
  - 바 컬러 (상태별)
  - 마일스톤 표시
```

### 칸반 상태별 색상 권장

| 상태 | 코드 | 권장 색상 계열 |
|------|------|---------------|
| Todo | `[ ]` | Gray |
| Design | `[bd]` | Blue |
| Detail | `[dd]` | Indigo |
| Implement | `[im]` | Purple |
| Verify | `[vf]` | Orange |
| Done | `[xx]` | Green |

---

## 품질 검증

### 자동 검증 항목
- [ ] 색상 대비율 WCAG AA 준수 (4.5:1 이상)
- [ ] 폰트 크기 최소 14px 이상
- [ ] 터치 타겟 최소 44x44px
- [ ] PrimeVue 테마 변수 유효성

### 수동 검토 권장
- [ ] 브랜드 일관성
- [ ] 가독성 확인
- [ ] 반응형 레이아웃 테스트

---

## 예상 실행 시간
- **단순 사이트** (랜딩 페이지): 10-15분
- **중간 사이트** (SaaS 대시보드): 20-30분
- **복합 사이트** (엔터프라이즈): 35-50분

---

## 성공 조건
- JSON 디자인 토큰 생성 완료
- TailwindCSS 확장 설정 생성
- PrimeVue 프리셋 생성
- 적용 가이드 문서 작성
- WCAG AA 색상 대비 준수

---

## 제한사항
- 로그인 필요 페이지는 분석 제한
- JavaScript 렌더링 콘텐츠는 로딩 후 분석
- 저작권 준수: 분석 목적으로만 사용, 디자인 복제 금지

<!--
jjiban 프로젝트 - UI Theme Extract Command
Target: Nuxt 3 + Vue 3 + PrimeVue 4 + TailwindCSS
-->
