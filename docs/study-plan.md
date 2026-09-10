# 학습 계획 (시험까지 3~4주)

시험일에 맞춰 아래 계획을 조정하세요. 하루 2~3시간 기준이며, `/study` 명령으로 매일 진행 상황을 기록하면 [진행 기록](#진행-기록)에 자동 반영됩니다.

## 전체 로드맵

| 주차 | 목표 | 핵심 활동 |
|---|---|---|
| 1주차 | 개념 정리 1회독 | 네트워크·웹·시스템 보안 개념 학습 + 단답형 문제 풀이 |
| 2주차 | 개념 정리 마무리 + 기출 1회독 | 암호화인증·위험관리·법제도 학습 + 7개년 기출 풀이 시작 |
| 3주차 | 기출 반복 + 예상문제 | 기출 전체 2회독, 오답 위주 복습, 예상문제로 신규 토픽 보강 |
| 4주차 | 최종 총정리 | 취약 영역 집중, 전체 모의고사, 최종 암기표 반복, 시험 전날 총정리 |

## 1주차 — 개념 정리 1회독

- [ ] Day 1: [네트워크 보안](concepts/01-network.md) 1~4장 (DoS/DDoS, 스니핑, VLAN, 프로토콜)
- [ ] Day 2: [네트워크 보안](concepts/01-network.md) 5~9장 (IDS/IPS, 포트스캔, MITM, TCP·무선랜 심화) + 단답형 복습
- [ ] Day 3: [웹·애플리케이션 보안](concepts/02-web.md) 1~4장 (XSS, SQL Injection, CSRF, HTTP 취약점)
- [ ] Day 4: [웹·애플리케이션 보안](concepts/02-web.md) 5~10장 (SSRF, 파일업로드, SW 보안약점) + 복습
- [ ] Day 5: [인프라 프로토콜](concepts/09-infra-protocols.md) 1~5장 (DNS/HTTP/FTP/SNMP/DHCP)
- [ ] Day 6: [인프라 프로토콜](concepts/09-infra-protocols.md) 6~9장 (이메일/DB/클라우드 보안)
- [ ] Day 7: 주말 복습 — 1주차 오답 단답형 재시험 (`/study review`)

## 2주차 — 시스템·침해사고 + 개념 마무리

- [ ] Day 8: [시스템 보안](concepts/03-system.md) 1~3장 (리눅스/윈도우 설정, PATH·버퍼오버플로우, 주요 취약점)
- [ ] Day 9: [시스템 보안](concepts/03-system.md) 4~7장 (포렌식, 접근통제모델, 보안관제)
- [ ] Day 10: [침해사고 분석 및 대응](concepts/08-incident-response.md) 1~4장 (Snort/iptables 실무, 점검 도구)
- [ ] Day 11: [침해사고 분석 및 대응](concepts/08-incident-response.md) 5~7장 (침해사고 시나리오 5종, 주요 취약점)
- [ ] Day 12: [암호화·인증](concepts/04-crypto-auth.md) 전체
- [ ] Day 13: [위험 관리](concepts/05-risk-management.md) 1~6장 (위험처리 4가지, 접근법 4가지, BCP/DRP)
- [ ] Day 14: 주말 복습 — [위험 관리](concepts/05-risk-management.md) 7~12장 (CC, 사회공학, ISMS-P, 개인정보) + [법·제도 & 실무형](concepts/06-law-practice.md)

## 3주차 — 기출 반복 + 예상문제

- [ ] Day 15~18: 기출 7개년 전체 풀이 — [2024년 1회](past-exams/2024-1.md)~[2026년 1회](past-exams/2026-1.md) (실제 시험처럼 시간 재고 풀기, 오답만 표시)
- [ ] Day 19~20: [예상문제](predicted/predicted-questions.md) 학습 (제로트러스트, 클라우드/컨테이너 보안 등 신규 토픽)
- [ ] Day 21: 주말 — 3주차 취약 영역 재점검 (`/study weak`)

## 4주차 — 최종 총정리

- [ ] Day 22~25: [최종 총정리](concepts/07-final-summary.md) 표 암기 + 취약 영역 집중 복습
- [ ] Day 26~27: 전체 모의고사 (기출 7개년 + 교재기반·예상문제 중 랜덤 30문항, 서술형 위주)
- [ ] 시험 전날: [최종 총정리 — 시험 전략](concepts/07-final-summary.md#시험-전략--마지막-조언) 페이지만 빠르게 훑기

## 매일 학습 루틴 (`/study`)

Claude Code에서 이 프로젝트를 열고 아래처럼 실행하세요.

```
/study
```

- 오늘 진행할 주제(위 로드맵 기준)를 자동으로 제안
- 해당 주제의 단답형·서술형·실무형 문제를 섞어 출제 (기출 위주, 가끔 예상문제 포함)
- 답을 입력하면 모범답안과 비교해 채점 및 피드백
- 틀리거나 애매했던 문제는 `progress/progress.json`에 기록되어 다음에 우선 재출제

특정 주제만 복습하고 싶다면 `/study network`, `/study risk` 처럼 주제 코드를 붙이고, 오답만 다시 풀고 싶다면 `/study review`를 사용하세요.

## 진행 기록

`/study`를 실행할 때마다 `progress/progress.json`에 학습 이력이 쌓입니다. 이 표는 학습을 진행하면서 직접 채워가거나, `/study` 세션 마지막에 자동으로 요약을 받아 붙여넣으세요.

| 날짜 | 주제 | 푼 문항 수 | 정답률 | 비고 |
|---|---|---|---|---|
| | | | | |
