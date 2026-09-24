# 추가 컨텍스트 기능

> 📖 **사전 학습**: 이 부록을 읽기 전에 [2장: 컨텍스트와 대화](../02-context-conversations/README.md)를 먼저 마칩니다.

이 부록에서는 두 가지 추가 컨텍스트 기능을 다룹니다. 이미지 다루기와 여러 디렉터리에 대한 권한 관리입니다.

---

## 이미지로 작업하기

`@` 문법을 사용해 대화에 이미지를 포함할 수 있습니다. Copilot은 스크린샷, 목업, 다이어그램을 비롯한 다양한 시각 자료를 분석할 수 있습니다.

### 기본 이미지 참조

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot이 이미지를 분석하고 응답합니다

> @mockup.png @current-design.png Compare these two designs

# 이미지를 끌어다 놓거나 클립보드에서 붙여넣을 수도 있습니다
```

### 지원되는 이미지 형식

| 형식 | 가장 잘 어울리는 용도 |
|--------|----------|
| PNG | 스크린샷, UI 목업, 다이어그램 |
| JPG/JPEG | 사진, 복잡한 이미지 |
| GIF | 단순한 다이어그램(첫 프레임만 사용) |
| WebP | 웹 스크린샷 |

### 실용적인 이미지 활용 사례

**1. UI 디버깅**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. 디자인 구현**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. 에러 분석**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. 아키텍처 리뷰**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. 변경 전/후 비교**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### 이미지와 코드 결합하기

이미지는 코드 컨텍스트와 결합될 때 더욱 강력해집니다:

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### 이미지 사용 팁

- **스크린샷은 잘라냅니다** - 관련 부분만 남기면 컨텍스트 토큰을 아낄 수 있습니다.
- **고대비를 사용합니다** - 분석할 UI 요소가 잘 보이도록 합니다.
- **필요하면 표시를 추가합니다** - 업로드 전에 문제 영역에 동그라미를 치거나 강조 표시를 해 둡니다.
- **개념 하나당 이미지 한 장** - 여러 장도 가능하지만 초점을 분명히 합니다.

---

## 권한 패턴

기본적으로 Copilot은 현재 디렉터리의 파일에 접근할 수 있습니다. 그 외 위치의 파일을 다루려면 권한을 부여해야 합니다.

### 디렉터리 추가하기

```bash
# 허용 목록에 디렉터리를 추가합니다
copilot --add-dir /path/to/other/project

# 여러 디렉터리를 추가합니다
copilot --add-dir ~/workspace --add-dir /tmp
```

### 모든 경로 허용하기

```bash
# 경로 제한을 완전히 비활성화합니다(주의해서 사용)
copilot --allow-all-paths
```

### 세션 안에서

```bash
copilot

> /add-dir /path/to/other/project
# 이제 해당 디렉터리의 파일을 참조할 수 있습니다

> /list-dirs
# 허용된 모든 디렉터리를 확인합니다

> /yolo
# /allow-all on의 빠른 별칭입니다 — 모든 권한 프롬프트를 자동 승인합니다
```

### 자동화 환경에서

```bash
# 비대화형 스크립트에 모든 권한을 허용합니다
copilot -p "Review @src/" --allow-all

# 기억하기 쉬운 별칭을 사용합니다
copilot -p "Review @src/" --yolo
```

### 다중 디렉터리 접근이 필요한 상황

이러한 권한이 필요한 대표적인 시나리오들입니다:

1. **모노레포 작업** - 여러 패키지에 걸친 코드 비교
2. **프로젝트 간 리팩터링** - 공유 라이브러리 업데이트
3. **문서 프로젝트** - 여러 코드베이스를 함께 참조
4. **마이그레이션 작업** - 기존 구현과 새 구현 비교

---

[**← 2장으로 돌아가기**](../02-context-conversations/README.md) | [**부록 목록으로 돌아가기**](README.md)
