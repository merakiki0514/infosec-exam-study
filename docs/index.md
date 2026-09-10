# 정보보안기사 실기 스터디

정보보안기사 실기 시험 준비를 위한 개인 학습 자료입니다. 7개년 기출문제와 주제별 핵심 개념 정리, 예상문제를 한 곳에 모았습니다.

## 이 사이트 구성

<div class="grid cards" markdown>

- :material-book-open-variant: **[개념 정리](concepts/01-network.md)**

    6개 파트(네트워크·웹·시스템·암호화인증·위험관리·법제도) + 최종 총정리

- :material-file-document-multiple: **[기출문제](past-exams/2024-1.md)**

    24년 1·2·4회, 25년 1·2·4회, 26년 1회 — 총 7개년 기출 원문과 모범답안

- :material-lightbulb-on: **[예상문제](predicted/predicted-questions.md)**

    출제 트렌드 분석을 바탕으로 한 신규 토픽 예상문제

- :material-calendar-check: **[학습 계획](study-plan.md)**

    시험일까지 주차별 학습 로드맵

</div>

## 빈출 파트 우선순위

기출 분석 결과, 매 회차 다음 순서로 출제 비중이 높습니다.

1. **위험 관리** — 매 회차 3~4문항 (위험처리 4가지, 위험분석 접근법, CIA, 재해복구)
2. **웹 보안** — 매 회차 3~4문항 (XSS, SQL Injection, CSRF는 거의 매번 출제)
3. **네트워크 보안** — 매 회차 3~4문항 (DoS/DDoS, 스니핑, IDS, 포트스캔)
4. **시스템 보안** — 리눅스/윈도우 실무 설정, 접근통제 모델, 유명 취약점
5. **암호화·인증** — SSL/TLS, PAM, 계정관리(EAM/IAM), 모바일 보안
6. **법·제도·실무** — iptables, sendmail, Apache 설정 등 실무형 문제 다수

## 매일 학습하기

Claude Code에서 이 프로젝트 디렉토리를 열고 `/study` 스킬을 실행하면, 그날의 학습 주제를 골라 주관식·실무형 문제를 출제하고 채점해 줍니다. 자세한 내용은 [학습 계획](study-plan.md) 페이지를 참고하세요.
