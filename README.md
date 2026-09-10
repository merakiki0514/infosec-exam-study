# 정보보안기사 실기 스터디

🔗 **사이트**: https://merakiki0514.github.io/infosec-exam-study/

정보보안기사 실기 시험 대비 개인 학습 저장소입니다. 7개년 기출문제, 시중 교재("정보보안기사 실기 이론편") 목차를 커버리지 기준으로 재구성한 개념 정리, 예상문제를 구조화하여 웹사이트로 보고, Claude Code의 `/study` 스킬로 매일 학습 세션을 진행할 수 있습니다.

## 구성

```
docs/                   # MkDocs Material 사이트 콘텐츠
  concepts/              # 파트 1~9 개념 정리
    01-network.md          # 네트워크 보안
    02-web.md               # 웹·애플리케이션 보안
    03-system.md             # 시스템 보안
    04-crypto-auth.md         # 암호화·인증
    05-risk-management.md      # 위험 관리
    06-law-practice.md          # 법·제도 & 실무
    09-infra-protocols.md        # 인프라 프로토콜 & 서비스(DNS/HTTP/이메일/DB/클라우드)
    08-incident-response.md       # 침해사고 분석 및 대응
    07-final-summary.md            # 최종 총정리
  past-exams/             # 24~26년 기출문제 7개년 원문 + 모범답안
  predicted/               # 출제 트렌드 기반 예상문제
  study-plan.md             # 4주 학습 로드맵
data/questions.json      # 구조화된 문제 데이터베이스 (기출 120 + 교재기반 120 + 예상 30, 총 270문항)
scripts/quiz.py           # 문제 선택 / 채점 기록 / 통계 CLI (daily 학습 스킬이 사용)
progress/progress.json    # 학습 이력 (문제별 정답률, 세션 기록)
.claude/skills/study/      # Claude Code용 `/study` 일일 학습 스킬
mkdocs.yml                 # 사이트 설정
.github/workflows/deploy.yml  # GitHub Pages 자동 배포
```

## 사이트 로컬 미리보기

```bash
pip install mkdocs-material
mkdocs serve
```

`http://127.0.0.1:8000` 에서 확인할 수 있습니다.

## 매일 학습하기

이 프로젝트 디렉토리에서 Claude Code를 실행하고 다음과 같이 입력하세요.

```
/study
/study network      # 특정 주제만
/study review        # 오답만 복습
/study weak           # 취약 주제 자동 선별
```

## 배포

`main` 브랜치에 push하면 GitHub Actions가 자동으로 MkDocs 사이트를 빌드해 GitHub Pages에 배포합니다. 저장소 설정의 **Settings → Pages → Source**를 "GitHub Actions"로 지정해야 합니다.
