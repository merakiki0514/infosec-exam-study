# 파트 7. 최종 총정리 — 시험 직전 핵심 암기

이 파트는 시험 전날 또는 시험 당일 아침에 빠르게 복습하기 위한 최종 정리본입니다. 모든 파트의 핵심을 압축하였습니다.

## 【 네트워크 보안 】

| 주제 | 정답 / 핵심 |
|---|---|
| Slow Read Attack | TCP Window Size = 0 조작 → 서버 연결 자원 고갈 DoS |
| 스머프 공격 3요소 | (A)Smurf / (B)Directed Broadcast / (C)ICMP Echo Request |
| NTP DDoS 대응 4가지 | ①4.2.7이상 업그레이드 ②monlist 비활성화 ③점검 ④100byte이상 차단 |
| Promiscuous Mode 로그 의미 | 스니핑 공격 의심. 최선 대응: 암호화 통신 사용 |
| ping 스니핑 탐지 | 가짜 MAC으로 ICMP Echo Request → Reply 오면 Promiscuous Mode |
| VLAN 할당 4가지 | 포트 / MAC주소 / 네트워크주소 / 프로토콜 |
| LAN 스위칭 3가지 | Store-and-Forward / Cut-Through / Fragment-Free |
| IPsec 기능 | 기밀성·무결성·원천인증·재전송방지·접근제어 |
| IPsec AH | 무결성+인증 / Sequence Number로 재전송 공격 방지 |
| IPsec 모드 2가지 | 전송모드(페이로드만) / 터널모드(전체 패킷, VPN) |
| DNS Recursive vs Authoritative | Recursive=캐시DNS(대리질의) / Authoritative=공식DNS(최종응답) |
| CSMA/CA RTS·CTS | 무선랜 충돌 회피 프레임. 연결 타임아웃 설정 |
| IDS FP / FN | FP=오탐(공격아닌데 공격) / FN=미탐(공격인데 통과) — FN이 더 위험 |
| 스텔스 스캔 3가지 | FIN / NULL / Xmas — 열린 포트는 무응답, 닫힌 포트는 RST |
| DNS 스푸핑 | MITM 공격 기법. 위조 DNS 응답으로 악성 서버 유도 |
| 세션 하이재킹 | 인증된 세션 탈취. 대응: HTTPS + HttpOnly 쿠키 |

## 【 웹 보안 】

| 주제 | 정답 / 핵심 |
|---|---|
| XSS 정의 | 악성 스크립트 삽입 → 희생자 브라우저에서 실행 |
| Stored XSS | DB 저장 → 조회 시 실행 (지속적·Persistent) |
| Reflected XSS | URL에 삽입 → 응답에 반사 즉시 실행 (비지속적·Non-Persistent) |
| DOM-based XSS | 서버 거치지 않음. 클라이언트 JS DOM 조작으로 실행 |
| XSS 대응 | 입력검증 + HTML 엔티티 인코딩 + HttpOnly + CSP |
| SQL Injection 안전 코드 | PreparedStatement + ? + setString() — SQL과 데이터 분리 |
| CSRF 정의 | 인증된 사용자 권한으로 의도치 않은 요청 전송 |
| CSRF 방어 | CSRF 토큰(UUID 매 요청 생성, 세션 비교) + POST 방식 |
| HTTP Request Smuggling | Content-Length vs Transfer-Encoding 불일치 악용 |
| HTTP 응답 분할 | (A)CR(%0D) + (B)LF(%0A) 삽입 |
| SSRF 필터링 | 화이트리스트(기본) → 블랙리스트(무작위 입력) |
| 파일 업로드 우회 | Content-Type 헤더를 image/gif 등으로 변조 |
| 파일 업로드 성공 조건 | URL 직접 접근 가능 + 서버 사이드 실행 권한 |
| 디렉터리 리스팅 차단 | Apache Options 지시자에서 Indexes 삭제 |
| 쿠키 보안 3속성 | HttpOnly(JS차단) / Secure(HTTPS만) / SameSite(CSRF방지) |
| 퍼징(Fuzzing) | 무작위 데이터 입력 → 오류·취약점 자동 발견 |
| SW 보안약점 3가지 | SQL Injection / XSS / OS Command Injection |

## 【 시스템 보안 】

| 주제 | 정답 / 핵심 |
|---|---|
| 패스워드 최소 길이 | /etc/login.defs → PASS_MIN_LEN 8 |
| /etc/passwd x 의미 | 패스워드가 /etc/shadow에 저장됨 |
| /etc/shadow $ID | $1=MD5 / $5=SHA-256 / $6=SHA-512 |
| utmp / wtmp / lastlog | 현재로그인 / 전체이력 / 마지막로그인 |
| lastb | 로그인 실패 기록 (/var/log/btmp) |
| lastcomm | 실행된 명령 이력 |
| lsof | 열려있는 파일·소켓 정보 — 악성 프로세스 포트 확인 |
| 세션 타임아웃 | export TMOUT=600 → /etc/profile |
| World-writable 파일 | find / -type f -perm -2 |
| umask 022 | 파일 기본권한 644 / 디렉터리 755 |
| HeartBleed 시스템 조치 | OpenSSL 취약하지 않은 버전으로 업데이트 |
| HeartBleed 서비스 조치 | 인증서 재발급 + 사용자 비밀번호 재설정 유도 |
| 버퍼오버플로우 위험 함수 | strcpy() → 대안: strncpy() |
| APT 정의 | 특정 대상 / 장기간 지속 / 다양한 기법 |
| 킬 체인 7단계 | 정찰→무기화→전달→익스플로잇→설치→C2→목표달성 |
| 제로데이 | 패치 공개 전(0일) 취약점 악용 |
| TEMPEST | 전자파 누설을 이용한 도청 기술·방어 분야 |
| 접근통제 DAC | 소유자가 자유롭게 접근 권한 설정 |
| 접근통제 MAC | 보안 등급(레이블) 기반 강제 접근 제어 |
| 접근통제 RBAC | 역할(Role)에 따른 접근 권한 부여 |
| NetBIOS 조치 | WINS 탭 → NetBIOS over TCP/IP 사용 안 함 |

## 【 암호화·인증 】

| 주제 | 정답 / 핵심 |
|---|---|
| SSL/TLS 비대칭키 사용 | 서버 인증 + 키 교환 단계 (Change Cipher Spec 이전) |
| SSL/TLS 대칭키 사용 | Change Cipher Spec 이후 — 실제 데이터 암호화 |
| RSA 키 교환 | 클라이언트가 Pre-Master Secret을 서버 공개키로 암호화 전달 |
| DH 키 교환 | 양측 DH 공개값 교환 → 각자 Pre-Master Secret 계산 (PFS) |
| 인증서 고정 목적 | MITM 방지. 우회: Frida 후킹 / 앱 리패키징 |
| PGP | 하이브리드 + Web of Trust — 개인간 |
| PEM | IETF 표준 + X.509 PKI 중앙 CA |
| S/MIME | MIME 확장 + PKI — 기업 이메일 표준 |
| PAM auth | 사용자 신원 확인(인증) |
| PAM account | 계정 유효성 확인(만료·시간제한) |
| PAM session | 세션 시작·종료 작업(로그·환경설정) |
| PAM password | 패스워드 변경·복잡도 검사 |
| EAM→IAM 개선 2가지 | 전체 계정 통합관리 + 생명주기 자동화 |
| MDM | 모바일 기기 원격 보호·관리 솔루션 |
| 크리덴셜 스터핑 | 유출된 ID·PW를 타 서비스에 대입 |
| Password Spray | 여러 계정에 하나의 흔한 패스워드 → 잠금 우회 |
| 해시 4특성 | 일방향성 / 충돌저항성 / 역상저항성 / 눈사태효과 |
| Deeplink 취약점 | URL 스킴 파라미터 미검증 → 비인가 화면 접근 |

## 【 위험 관리 】

| 주제 | 정답 / 핵심 |
|---|---|
| 위험 관리 3단계 | 위험분석 → 위험평가 → 정보보호대책 선정 |
| 위험 관리 6단계 빈칸 | (A)위험분석 (B)위험평가 (C)정보보호대책 구현 |
| 자산 | 조직이 보호해야 할 모든 유·무형의 대상 |
| 위협 | 자산에 손실을 초래할 잠재적 원인 또는 행위자 |
| 취약점 | 위협의 이용 대상이 되는 자산의 잠재적 약점 |
| 위험 수용 | 현재 위험을 받아들이고 잠재적 손실 감수 |
| 위험 감소 | 보호대책 채택·구현으로 위험 줄임 |
| 위험 전가 | 보험·외주 등으로 제3자에게 손실 비용 이전 |
| 위험 회피 | 위험한 프로세스·사업 포기 |
| 복합 접근법 | 고위험→상세 위험분석 / 그 외→기준선 접근법 |
| 델파이법 | 전문가 반복 익명 설문으로 합의 도출하는 정성적 방법 |
| 콜드 사이트 | RTO 최장 — IT자원 미확보, 복구에 가장 긴 시간 |
| 미러 사이트 | Active-Active 실시간 동시 서비스, RTO=0 |
| RTO | 목표 복구 시간 (짧을수록 높은 수준의 DR 필요) |
| RPO | 목표 복구 시점 (짧을수록 데이터 유실 최소화) |
| CISO 역할 4가지 | 계획수립·시행 / 감사 / 위험식별·평가 / 교육·훈련 |
| 개인정보 영향평가 5가지 | 수 / 제3자제공 / 권리침해 / 민감정보 / 보유기간 |
| 생체인식 6원칙 | 비례성·적법성·목적제한·투명성·안전성·통제권보장 |
| CIA | 기밀성(유출방지)·무결성(변조방지)·가용성(서비스보장) |

## 【 법·제도·실무 】

| 주제 | 정답 / 핵심 |
|---|---|
| iptables ICMP 차단 | -p icmp --icmp-type echo-request -j DROP |
| sendmail RELAY / DISCARD | kca.or.kr RELAY / spam.com DISCARD |
| sendmail 설정 파일 | sendmail.cf → access → access.db |
| Apache 디렉터리 리스팅 | Options 지시자에서 Indexes 삭제 |
| 네트워크 장비 암호화 확인 | show running-config → enable secret / password-encryption |
| SQL Injection 방어 핵심 | PreparedStatement + ? + setString() |
| CSRF 토큰 원리 | UUID 생성 → 세션 저장 → 히든 필드 → 요청 시 비교 |
| 피들러 HTTPS 오류 | 피들러 CA 인증서를 신뢰 저장소에 미설치 |
| 파일 업로드 우회 | Content-Type 헤더를 image/gif 등으로 변조 |
| DB 금지 권한 3가지 | DBA권한 / 계정생성삭제권한 / ALL PRIVILEGES |
| DB 최소화 방안 4가지 | 최소권한 / 기본계정삭제 / 암호화통신 / 로깅감사 |
| SIEM | 로그·이벤트 통합 수집·분석·관제 시스템 |
| 보안관제 구성요소 | 에이전트 → 정보수집 서버 → 통합관제 서버 |
| DLP | 중요 데이터 외부 유출 탐지·차단 솔루션 |
| NTFS | ACL접근제어 + EFS암호화 + 저널링 |
| E2EE | 송신자~수신자 전 구간 암호화, 서버도 복호화 불가 |
| 핫픽스 vs 업데이트 | 핫픽스=긴급 패치 / 업데이트=일반 기능 추가·개선 |
| 로그인 배너 설정 | telnet: /etc/issue.net / vsftpd: ftpd_banner |

## 회차별 신규 출제 토픽 — 연도별 트렌드

| 연도·회차 | 신규 주요 토픽 |
|---|---|
| 24년도 1회 | TEMPEST / 세션 하이재킹 / SOAR / ping 스니핑 탐지 / 자산 중요도 평가 |
| 24년도 2회 | HTTP Request Smuggling / Slow Read Attack / HeartBleed / DNS Recursive·Authoritative |
| 24년도 4회 | NTP DDoS 대응 / 복합 접근법 위험분석 / 재해복구(미러·콜드) / RARP / VLAN 4종 |
| 25년도 1회 | SSRF / 사이버 킬 체인 / Deeplink / IPsec 모드 / lsof / NetBIOS취약점 / PAM |
| 25년도 2회 | E2EE / DLP / 인증서 고정(Certificate Pinning) / ShellShock 웹쉘 / 보안관제 구성요소 |
| 25년도 4회 | 크리덴셜 스터핑 / Password Spray / EAM·IAM / MDM·BYOD / Snort 규칙 / DB 마스킹 / 전자메일 PGP·PEM·S/MIME |
| 26년도 1회 | CSRF 토큰 / 퍼징 / SIEM / 생체인식 6원칙 / SSL/TLS 비대칭·대칭키 단계 / 피들러 분석 / iptables |

!!! tip "트렌드 분석"
    최근 회차(25년도 4회, 26년도 1회)로 갈수록 **인증/계정관리(EAM·IAM, PAM), 모바일 보안(인증서 고정, Deeplink, BYOD), 전자메일 보안(PGP/PEM/S/MIME)** 등 상대적으로 지엽적인 주제가 새로 출제되는 경향이 있습니다. 다음 회차에는 아직 출제되지 않은 지엽적 주제(예: 클라우드 보안, 컨테이너 보안, API 보안, Zero Trust)가 나올 가능성에 대비하세요. [예상문제](../predicted/predicted-questions.md) 페이지 참고.

## 시험 전략 & 마지막 조언

**최우선 암기 필수 항목**

1. 위험 처리 4가지: 수용·감소·전가·회피
2. XSS 3가지 유형: Stored·Reflected·DOM-based
3. 위험 관리 3단계: 위험분석→위험평가→대책선정
4. 접근통제 3모델: DAC·MAC·RBAC
5. SQL Injection 안전 코드: PreparedStatement + ?
6. PAM 모듈 4가지: auth·account·session·password
7. IDS 오탐/미탐: FP(공격아닌데 공격) / FN(공격인데 통과)
8. IPsec 모드: 전송모드(페이로드) / 터널모드(전체)
9. SSL/TLS: 비대칭키(핸드셰이크) / 대칭키(데이터 암호화)
10. CISO 역할 4가지: 계획·감사·위험식별·교육훈련

!!! tip "서술형 답안 작성 팁"
    정의 → 원리(예시) → 대응 순서로 서술하면 감점 없이 부분 점수를 모두 받을 수 있습니다. 핵심 키워드가 포함되어 있으면 부분 점수가 인정됩니다.
