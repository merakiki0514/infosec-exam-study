# 파트 1. 네트워크 보안

본 파트는 정보보안기사 실기 시험에서 매 회차 3~4문항이 출제되는 핵심 영역입니다. 네트워크 공격 기법, 프로토콜 보안, IDS/IPS, 스니핑 탐지 등이 주를 이룹니다.

## 1. DoS / DDoS 공격 기법

> 출제 이유: 실무 보안 담당자가 반드시 알아야 할 서비스 거부 공격의 원리와 대응책을 묻기 위해 출제됩니다. 특히 Slow 계열 공격은 최근 빈출입니다.

### 1-1. Slow Read Attack

| 항목 | 내용 |
|---|---|
| 정의 | TCP 수신 윈도우 크기(Window Size)를 0 또는 매우 작은 값으로 설정하여 서버가 데이터를 전송하지 못하도록 막고, 연결을 오랫동안 유지시켜 서버 자원을 고갈시키는 DoS 공격 |
| 원리 | TCP 3-way handshake 후 공격자가 Window Size = 0 을 선언 → 서버는 데이터를 보낼 수 없고 연결을 유지 → 다수 연결 반복 시 서버 소켓 자원 고갈 |
| 피해 | 웹 서버 연결 수 한계 도달 → 정상 사용자 서비스 불가 |
| 관련 기출 | 24년도 2회 — TCP Window 크기 조작(Window size=0) DoS 공격 기법 명칭 |

**대응 방안**

- 연결당 최소 전송 속도 임계값 설정 (일정 시간 내 최소 데이터 수신 없으면 연결 강제 종료)
- 웹 서버 타임아웃(Timeout) 값 적절히 설정 (Apache: TimeOut, Nginx: send_timeout)
- 동일 IP의 동시 연결 수 제한 (mod_reqtimeout, Nginx limit_conn)
- WAF(Web Application Firewall) 또는 L7 스위치를 통한 비정상 연결 탐지·차단

**추가 지식: Slow 계열 DoS 공격 비교**

| 공격 종류 | 특징 |
|---|---|
| Slow HTTP POST (Slow Body) | POST 데이터를 매우 천천히 전송하여 서버가 요청 수신 완료를 기다리게 함 |
| Slowloris | HTTP 헤더를 매우 천천히 전송하여 서버 연결을 오래 점유 |
| Slow Read Attack | TCP Window Size를 0으로 설정하여 서버가 응답을 보내지 못하게 함 |
| 공통 특징 | 소량의 트래픽으로 서버 자원 고갈 → 탐지 어려움, 방화벽 우회 가능 |

!!! important "시험 포인트"
    Slow Read Attack = TCP Window Size 0 조작 — 이 연결고리를 반드시 암기하세요. 'Slow'라는 이름처럼 소량 트래픽으로 공격한다는 점도 중요합니다.

### 1-2. 스머프(Smurf) 공격

| 항목 | 내용 |
|---|---|
| 정의 | 출발지 IP를 피해자 IP로 위조(Spoofing)한 ICMP Echo Request 패킷을 네트워크 브로드캐스트 주소(Directed Broadcast)로 전송하여, 해당 네트워크 내 모든 호스트가 피해자에게 Echo Reply를 전송하도록 유도하는 증폭 DDoS 공격 |
| 공격 요소 | (A) Smurf 공격 / (B) Directed Broadcast / (C) ICMP Echo Request |
| 관련 기출 | 25년도 1회 — 공격 명칭과 구성요소 3가지 |

**공격 절차**

1. 공격자가 출발지 IP를 피해자 IP로 위조
2. 위조된 ICMP Echo Request를 브로드캐스트 주소(예: 192.168.1.255)로 전송
3. 해당 서브넷의 모든 호스트가 피해자 IP로 ICMP Echo Reply 전송
4. 피해자는 대량의 Reply를 수신하여 네트워크 대역폭 고갈 및 시스템 마비

**대응 방안**

- 라우터에서 Directed Broadcast 패킷 차단 설정
- IP Spoofing 방지를 위해 라우터에서 ingress filtering(uRPF) 적용
- 방화벽에서 외부에서 내부로의 ICMP Echo Request 차단

!!! important "핵심"
    스머프 공격 = IP Spoofing + Directed Broadcast + ICMP 증폭 — 이 3가지 구성 요소를 정확히 서술해야 합니다.

### 1-3. NTP DDoS (Monlist 악용)

| 항목 | 내용 |
|---|---|
| 정의 | NTP(Network Time Protocol) 서버의 monlist 명령을 악용하여 소량의 요청으로 대량의 응답을 발생시키는 반사·증폭 DDoS 공격 |
| 증폭 원리 | monlist: 최근 600개의 클라이언트 목록 반환 → 소량 요청으로 대량 응답 유발 (증폭 비율 최대 ~700배) |
| 관련 기출 | 24년도 4회 — NTP 서비스 DDoS 대응 방안 4가지 |

**대응 방안 4가지 (기출 답안)**

1. 취약한 NTP 데몬을 monlist 기능이 해제된 최신 버전(4.2.7 이상)으로 업그레이드
2. 업그레이드 불가 시 설정 변경으로 monlist 기능 비활성화 (ntp.conf에 disable monitor 추가)
3. 점검 대상 NTP 서버가 monlist 명령을 허용하는지 여부를 정기적으로 점검
4. 보안장비(방화벽)를 이용하여 100byte 이상의 NTP 서버 응답 패킷을 차단

### 1-4. DRDoS (Distributed Reflection DoS)

| 항목 | 내용 |
|---|---|
| 정의 | 공격자가 출발지 IP를 공격대상 IP로 위조(IP Spoofing)하여 다수의 반사서버(Reflector)로 요청정보를 전송, 공격대상은 반사서버로부터 다수의 응답을 받아 서비스 거부 상태가 되는 공격 유형 |
| 핵심 개념 2가지 | **반사(Reflection)**: 위조된 출발지 주소로 제3의 서버(반사서버)에 요청을 보내 그 응답이 공격대상으로 향하게 하는 것 / **증폭(Amplification)**: 반사서버의 응답 크기가 요청보다 훨씬 커서 공격 트래픽이 증폭되는 것 |

**DRDoS 공격 유형 3가지**

| 유형 | 방식 |
|---|---|
| TCP 방식 | TCP의 연결설정과정(3-Way Handshake)의 취약점을 이용 — 위조된 출발지 주소의 SYN 패킷을 반사서버(TCP 서버)로 전달하여 SYN+ACK 응답 패킷이 공격대상으로 향하도록 함 |
| ICMP 방식 | ICMP 프로토콜의 Echo Request와 Echo Reply를 이용 — 위조된 주소의 Echo Request를 반사서버로 전달하여 Echo Reply가 공격대상으로 향하도록 함(Smurf 공격이 대표적) |
| UDP 방식 | UDP 프로토콜 서비스를 제공하는 서버(**DNS**, NTP, SNMP, CHARGEN 등)를 반사서버로 이용하여 그 응답이 공격대상으로 향하도록 함 — 가장 대표적인 반사서버는 DNS 서버(53/udp) |

!!! important "핵심"
    DRDoS는 NTP DDoS·DNS 증폭 공격의 상위 개념입니다. "반사(Reflection) + 증폭(Amplification)"이라는 키워드로 정의를 서술하고, UDP 기반 반사서버 종류(DNS/NTP/SNMP/CHARGEN)를 예시로 들면 좋은 답안이 됩니다.

## 2. 네트워크 스니핑 & 탐지

> 출제 이유: 스니핑은 수동적 공격으로 탐지가 어렵다는 특성 때문에 방어 방법과 탐지 방법이 함께 출제됩니다. Promiscuous Mode 개념과 탐지 방법을 반드시 숙지해야 합니다.

### 2-1. Promiscuous Mode(무차별 모드)

| 항목 | 내용 |
|---|---|
| 정의 | NIC(네트워크 인터페이스 카드)가 자신의 MAC 주소와 무관하게 네트워크 상의 모든 프레임(패킷)을 수신하는 동작 모드 |
| 기본 동작 | 일반적으로 NIC는 자신의 MAC 주소가 목적지인 패킷만 수신 (+ 브로드캐스트) |
| 스니핑과의 관계 | 공격자가 스니핑을 위해 NIC를 Promiscuous Mode로 설정 → 모든 트래픽 도청 가능 |
| 로그 예시 | `/var/log/messages`: `device ens32 entered promiscuous mode` |
| 관련 기출 | 24년도 2회 — 로그 의미, 예상 공격, 대응 방법 |

**대응 방법 (우선순위 순서)**

1. **암호화 통신 적용 (최우선)**: TLS/SSL, SSH, HTTPS 등 암호화 프로토콜 사용 → 스니핑되어도 내용 해독 불가
2. **허브(더미 허브) 대신 스위치 장비 사용**: 스위치는 MAC 테이블 기반으로 해당 포트에만 프레임 전달 → 스니핑 범위 제한
3. 스니핑 탐지 도구를 이용한 지속적 모니터링

### 2-2. ping을 이용한 스니핑 탐지

| 항목 | 내용 |
|---|---|
| 원리 | 스니핑 중인 호스트는 Promiscuous Mode이므로 목적지 MAC 주소와 상관없이 모든 패킷을 수신·처리함 |
| 방법 | 존재하지 않는 가짜 MAC 주소를 목적지로 한 ICMP Echo Request 전송 → 정상 호스트는 응답 안 함, Promiscuous Mode 호스트는 응답 |
| 판단 기준 | 응답(ICMP Echo Reply)이 오면 해당 호스트가 Promiscuous Mode로 스니핑 중 |
| 관련 기출 | 24년도 1회 — ping 명령을 이용한 스니핑 탐지 방법 |

**추가 스니핑 탐지 방법**

- ARP Watch: ARP 테이블의 비정상적인 변화를 모니터링하여 ARP 스푸핑 기반 스니핑 탐지
- DNS 역조회: 스니핑 호스트는 수집한 패킷의 IP를 역방향 DNS 조회 → 비정상적 DNS 쿼리 탐지
- 네트워크 모니터링 도구: Wireshark, tcpdump, Snort 등으로 비정상 트래픽 탐지

!!! warning "주의"
    스위치 환경에서는 ARP Spoofing을 이용한 스니핑이 가능합니다. 스위치가 있어도 ARP Spoofing 공격에는 취약할 수 있음을 기억하세요.

## 3. VLAN & LAN 스위칭

> 출제 이유: VLAN은 네트워크 보안의 핵심 구성 요소로, 할당 방식과 설정 명령어가 반복 출제됩니다.

### 3-1. VLAN 할당 방식 4가지

| 할당 방식 | 설명 |
|---|---|
| 포트 기반 VLAN | 스위치의 물리적 포트에 VLAN을 수동 지정. 가장 일반적인 방식 |
| MAC 주소 기반 VLAN | NIC의 MAC 주소를 기준으로 VLAN을 자동 할당. 이동성이 높은 환경에 적합 |
| 네트워크 주소 기반 VLAN | IP 주소 또는 서브넷을 기준으로 VLAN 할당 |
| 프로토콜 기반 VLAN | 사용하는 네트워크 프로토콜(IP, IPX 등)을 기준으로 VLAN 할당 |

### 3-2. 정적 VLAN vs 동적 VLAN

| 구분 | 설명 |
|---|---|
| 정적 VLAN (Static VLAN) | 관리자가 스위치 포트에 수동으로 VLAN을 지정. 보안성 높음, 관리 편의성 낮음 |
| 동적 VLAN (Dynamic VLAN) | VMPS(VLAN Membership Policy Server) 등을 통해 MAC 주소나 사용자 인증 정보 기반으로 자동 할당. 관리 편의성 높음 |

**VLAN 확인 명령어**: `show vlan` (전체), `show vlan brief` (요약)

### 3-3. LAN 스위칭 방식 3가지

| 방식 | 설명 / 특징 |
|---|---|
| Store-and-Forward | 프레임 전체 수신 후 오류 검사(CRC) 완료 후 전송. 신뢰성 높음, 지연 있음 |
| Cut-Through | 목적지 MAC 주소(첫 6바이트)만 확인 후 즉시 전송. 속도 빠름, 오류 포함 프레임도 전달 |
| Fragment-Free (Modified Cut-Through) | 충돌 감지를 위해 프레임의 첫 64바이트를 수신 후 전송. Cut-Through의 단점 일부 보완 |

!!! tip "TIP"
    Fragment-Free는 이더넷의 최소 프레임 크기(64byte) 기반입니다. 충돌로 인한 런트 프레임(64byte 미만)은 걸러낼 수 있습니다.

## 4. 핵심 프로토콜 정리

> 출제 이유: 각 프로토콜의 동작 원리와 보안 취약점이 실무와 직결되어 꾸준히 출제됩니다.

### 4-1. ARP / RARP

| 프로토콜 | 방향 / 설명 |
|---|---|
| ARP (Address Resolution Protocol) | IP 주소 → MAC 주소 변환. 동일 네트워크 내 통신 시 사용 |
| RARP (Reverse ARP) | MAC 주소 → IP 주소 변환. 하드디스크 없는 터미널이 부팅 시 자신의 IP 주소 할당받을 때 사용. RARP 서버 필요 |
| ARP Spoofing (스푸핑) | ARP는 인증 없이 응답 수락 → 공격자가 가짜 ARP Reply로 피해자의 ARP 테이블 오염 → 트래픽 가로채기(MITM) |

**ARP Spoofing 대응**

- Static ARP 설정: 중요 서버의 MAC-IP 바인딩을 정적으로 설정
- Dynamic ARP Inspection (DAI): 스위치에서 ARP 패킷 검증
- 암호화 통신(TLS/SSL) 사용: 트래픽이 가로채여도 내용 보호

### 4-2. IPsec

| 항목 | 내용 |
|---|---|
| 정의 | IP 계층(3계층)에서 패킷 보안 서비스를 제공하는 네트워크 계층 보안 프로토콜. VPN 구성에 주로 사용 |
| 제공 기능 | 기밀성 / 무결성 / 데이터 원천 인증 / 재전송 공격 방지 / 접근 제어 |
| 구성 프로토콜 | AH (Authentication Header): 무결성·인증 제공, 암호화 없음 / ESP (Encapsulating Security Payload): 무결성·인증·암호화 모두 제공 |

**IPsec 동작 모드 2가지**

| 모드 | 설명 |
|---|---|
| 전송 모드 (Transport Mode) | IP 헤더는 그대로, 페이로드(데이터)만 보호. 종단 간(Host-to-Host) 통신 보호에 사용 |
| 터널 모드 (Tunnel Mode) | IP 패킷 전체를 새로운 IP 헤더로 캡슐화하여 보호. 게이트웨이 간 VPN 구성에 사용 |

**AH 헤더 주요 필드 (25년도 4회)**

- Sequence Number (순서 번호): 패킷의 순서 번호로 재전송(Replay) 공격 방지
- ICV (Integrity Check Value): 무결성 검증값

### 4-3. DNS

| 항목 | 내용 |
|---|---|
| Recursive DNS 서버 | 클라이언트가 속한 지역의 DNS 서버. 정보 없으면 상위 서버에 대신 질의하여 결과를 캐싱 후 응답. (= Cache DNS) |
| Authoritative DNS 서버 | 특정 도메인의 공식 정보를 보유하고 최종 IP를 응답하는 서버 |
| DNS 캐싱 | 한 번 조회한 DNS 결과를 TTL(Time to Live) 시간 동안 캐시에 저장하여 반복 조회 방지 |
| TTL | DNS 레코드의 유효 시간. TTL이 지나면 캐시에서 삭제되고 재조회 |

**DNS 관련 공격**

- DNS 스푸핑: 위조된 DNS 응답으로 피해자를 악성 사이트로 유도 (MITM 공격 기법)
- DNS 증폭 DDoS: UDP 특성과 DNS 응답의 큰 크기를 이용한 반사 공격
- DNS 캐시 포이즈닝: DNS 캐시에 거짓 정보를 삽입

### 4-4. CSMA/CA (무선랜)

| 항목 | 내용 |
|---|---|
| CSMA/CA 개요 | 무선랜(Wi-Fi)에서 충돌을 회피(Collision Avoidance)하는 매체 접근 제어 방식. 유선의 CSMA/CD와 달리 충돌 사전 방지 |
| RTS (Request to Send) | 송신 노드가 AP에 전송 요청 프레임 전송. 연결 타임아웃(지속시간) 포함 |
| CTS (Clear to Send) | AP가 전송 허가 프레임 전송. 연결 타임아웃(지속시간) 포함 |
| 역할 | RTS/CTS 교환으로 은닉 노드 문제(Hidden Node Problem) 해결 및 충돌 방지 |

!!! important "기출"
    CSMA/CA에서 연결 타임아웃이 설정되는 프레임 = RTS와 CTS 두 가지 모두 정답입니다.

### 4-5. SNMP

| 항목 | 내용 |
|---|---|
| 정의 | Simple Network Management Protocol. 네트워크 장비(라우터, 스위치, 서버 등)를 원격으로 모니터링·관리하는 프로토콜 |
| 포트 | UDP 161 (에이전트), UDP 162 (트랩) |
| 버전별 보안 | v1/v2c: Community String(평문) 인증 → 취약 / v3: 사용자 인증 + 암호화 + 접근 제어 지원 → 권장 |
| 보안 위협 | Community String 노출 시 장비 설정 변경, 정보 유출 가능 |

### 4-6. TCP 프로토콜 심화

| 항목 | 내용 |
|---|---|
| 연결지향(Connection-Oriented) | 물리적으로 전용회선이 연결된 것처럼 가상의(논리적인) 연결 통로를 설정해서 통신하는 방식 (가상회선방식, Virtual Circuit). 논리적 연결 통로를 통해 데이터를 주고받음으로써 데이터의 전송 순서를 보장(순서제어, Sequence Control) |
| 스트림(Stream) 기반 전송 | 데이터를 정해진 크기로 전송하는 것이 아니라 임의의 크기로 나누어 연속해서 전송하는 방식 |
| 흐름제어 (Flow Control) | 상대방이 받을 수 있는 만큼만 데이터를 효율적으로 전송하는 것. **슬라이딩 윈도우(Sliding Window)** 제어방식 사용 — 상대방의 수신 가능한 크기(Window Size) 내에서 세그먼트를 전송 시마다 수신확인응답(ACK)을 기다리지 않고 연속적으로 전송해 효율을 높임 |
| 오류제어 (Error Control) | 데이터의 오류나 누락(missing) 없이 안전한 전송을 보장. 오류 판단 기준은 송신 측에서 계산한 체크섬(checksum)을 수신 측에서 검증해 판단하며, 오류·누락 발생 시 재전송(Retransmission)을 수행해 보정 |
| 혼잡제어 (Congestion Control) | 네트워크의 혼잡 정도에 따라 송신자가 데이터 전송량을 제어하는 것. 혼잡 정도 판단 기준은 데이터의 손실 발생 유무 — 전송한 데이터에 누락이 발생하면 네트워크가 혼잡한 상태로 판단해 전송량을 조절 |

**TCP vs UDP**: TCP는 Stream 기반 통신(연결지향, 신뢰성 보장), UDP는 Datagram 기반 통신(비연결지향, 신뢰성 보장 없음, 빠른 전송)

### 4-7. 무선랜(Wireless LAN) 심화

무선랜에 관한 기술 표준은 국제표준기구인 **IEEE**에서 802.11 계열 표준으로 규정하고 있으며, 무선랜 관련 장비들은 이 표준을 준수한다. 무선랜 활성화를 위해 설립된 와이파이연합(Wi-Fi Alliance)에서 무선 제품에 관한 기술 인증(Wi-Fi 인증마크)을 수행한다.

| 무선랜 표준 | 표준 제정시기 | 주파수 대역 | 데이터 속도(최대) |
|---|---|---|---|
| 802.11 | 1997 | 2.4 GHz | 2 Mbps |
| 802.11a | 1999 | 5 GHz | 54 Mbps |
| 802.11b | 1999 | 2.4 GHz | 11 Mbps |
| 802.11g | 2003 | 2.4 GHz | 54 Mbps |
| 802.11n | 2009 | 2.4~5 GHz | 300 Mbps |

**무선랜 환경 4가지 구분**

| 환경 | 특징 |
|---|---|
| 상용 무선랜 환경 | 이동통신사가 고객 서비스용으로 구축. 자사 고객 인증을 위해 USIM, MAC, ID/Password 등을 이용 |
| 공중 무선랜 환경 | 공공기관, 호텔, 카페 등 서비스 업종에서 불특정 다수 고객 편의를 위해 제공. 대부분 소규모 환경에서 별도 보안 관리자 없이 운영 → 보안에 취약 |
| 사설 무선랜 환경 | 일반 사용자가 무선 공유기를 통해 구축. 다양한 보안기술을 이용할 수 있지만 보안 설정에 대한 인식 부족 등으로 취약점 발생 가능 |
| 기업 무선랜 환경 | 기업이 내부 업무용으로 구축. 최근 스마트폰을 이용한 스마트 오피스, 스마트 워크 등 도입 확산 |

### 4-8. IP(IPv4) 프로토콜 구조

| 항목 | 내용 |
|---|---|
| 정의 | 비연결형 프로토콜(Connectionless Protocol) — 연결 상태를 유지하지 않기 때문에 패킷 전송 순서를 보장하지 않음. 비신뢰적 프로토콜(Unreliable Protocol) — 신뢰성 있는 통신을 보장하지 않음 |
| 역할 | 목적지 주소(Destination IP Address)를 기반으로 라우팅(Routing)을 담당하는 인터넷 계층의 대표 프로토콜 |
| 헤더 크기 | 기본 헤더 20byte + 옵션 헤더 최대 40byte (총 20~60byte) |

**IP 헤더 주요 필드**

| 필드 | 설명 |
|---|---|
| VER(4bit) | IP 버전 정보 (일반적으로 IPv4) |
| HLEN(4bit) | 헤더 길이 (4byte 단위로 표현) |
| Total length(16bit) | 헤더부+데이터부를 포함한 전체 IP Packet의 길이 |
| Identification(16bit) | 단편화(Fragmentation) 전 원본 IP 데이터그램을 식별하기 위한 ID |
| Flags(3bit) | 단편화·재조합 관련 필드. 2번째 비트(DF, Don't Fragment): 1이면 단편화 금지 / 3번째 비트(MF, More Fragments): 1이면 재조합할 단편이 남아있음, 0이면 마지막 단편 |
| TTL(Time To Live) | 패킷이 통과할 수 있는 최대 라우터(홉) 수. 라우터를 통과할 때마다 1씩 감소하며 0이 되면 폐기(라우팅 루프 방지) |
| Protocol(8bit) | 상위 계층 프로토콜 식별(TCP=6, UDP=17, ICMP=1 등) |
| Source/Destination IP address(32bit씩) | 출발지/목적지 IP 주소 |

**단편화(Fragmentation)와 이더넷 MTU**: 데이터그램이 네트워크의 MTU(Maximum Transmission Unit)보다 크면 여러 조각으로 분할(단편화)되어 전송되고 수신 측에서 재조합(Reassembly)된다. 이더넷의 MTU는 **1500byte**가 표준

### 4-9. ICMP 프로토콜 구조

| 항목 | 내용 |
|---|---|
| 정의 | Internet Control Message Protocol. IP 프로토콜은 신뢰할 수 없는(전송 상태 관리 없음) 프로토콜이므로, 이 단점을 보완하기 위해 에러 발생 시 원인을 알려주거나 네트워크 상태를 진단해 주는 프로토콜 |
| 기능 | Error-Reporting Message(전송 중 오류 발생 시 에러 메시지 생성·응답) / Query Message(네트워크 상태 진단을 위한 쿼리 요청·응답 메시지 생성) |

**ICMP 메시지 구조**: `Type(8bit)` + `Code(8bit)` + `Checksum(16bit)` + `Rest of the header` + `Data section`

- **Type**: 메시지의 유형/용도 (예: Type 3 = Destination Unreachable, 목적지 도달 불가)
- **Code**: Type의 세부 내용. Type과 Code가 조합되어 ICMP 메시지의 목적을 나타냄 (예: Type 3의 Code 3 = Port Unreachable, UDP 포트가 열려있지 않음)
- **Checksum**: ICMP 메시지의 오류를 검사하기 위한 값

### 4-10. VPN(가상사설망) 프로토콜 종류

| 항목 | 내용 |
|---|---|
| 정의 | 인터넷 같은 공중망(Public Network)을 이용하여 사설망(Private Network)이 요구하는 서비스를 제공할 수 있도록 구축한 망으로, 공중망 내에서 마치 전용선처럼 사용하는 기술 |
| 터널링(Tunneling) | 송신자·수신자 사이의 전송로에 외부로부터의 침입을 막기 위해 일종의 파이프를 구성하는 것. 터널링되는 데이터를 페이로드(Payload)라 하며, 터널링 구간에서 터널링 프로토콜을 통해 페이로드가 캡슐화되어 전송됨 |

**계층별 VPN 프로토콜**

| 계층 | 프로토콜 | 특징 |
|---|---|---|
| 2계층(Data Link) | PPTP (Point to Point Tunnel Protocol) | 마이크로소프트사가 설계. PPP 패킷을 IP 패킷으로 캡슐화하여 터널링. 하나의 터널에 하나의 연결만 지원 |
| 2계층(Data Link) | L2F (Layer 2 Forwarding) | 시스코(Cisco)사가 제안. 원격지 ISP 장비에서 접근 서버 측 터널 서버로 L2F 터널 생성. 하나의 터널에 여러 연결 지원(다자간 통신 가능). 인증으로 RADIUS·TACACS+ 이용 |
| 2계층(Data Link) | L2TP (Layer 2 Tunneling Protocol) | PPTP와 L2F의 장점을 결합한 프로토콜 |
| 3계층(Network) | IPsec | [4-2절](#4-2-ipsec) 참고 |
| 4계층(Transport)/응용 | SSL/TLS | 별도 클라이언트 설치 없이 웹 브라우저로 접속 가능한 SSL VPN 구성에 사용 |

### 4-11. 라우터와 접근제어(ACL)

라우터에서는 access-list를 이용해 특정 패킷에 대한 접근제어를 설정할 수 있다. 접근제어 방법은 크게 **standard(표준)**와 **extended(확장)** access-list로 나뉜다.

| 구분 | standard access-list | extended access-list |
|---|---|---|
| 번호 범위 | 1~99 | 100~199 |
| 필터링 기준 | 출발지(source) IP만으로 패킷을 허용·차단 | 출발지 IP + **목적지 IP·포트·프로토콜**까지 이용해 좀 더 세밀하게 필터링 |
| 형식 | `access-list <번호> [permit\|deny] [출발지주소 wildcard\|any]` | `access-list <번호> [permit\|deny] <프로토콜> <출발지 wildcard> <목적지 wildcard>` |
| 예시 | `access-list 5 permit host 192.168.159.131` (특정 IP 허용) / `access-list 5 deny any` (전체 차단) | `access-list 150 deny tcp 192.168.1.0 0.0.0.255 host 100.100.100.1 eq 80` (특정 대역→특정 IP의 80포트 TCP 차단) |

- `host` 키워드: 특정 IP 1개만 지정할 때 사용 / `wildcard mask`: IP 대역을 지정할 때 사용(서브넷 마스크의 비트를 반전시킨 값) / `any`: 모든 주소 / `eq`(equal): 단일 포트 지정 / `range 시작포트 끝포트`: 포트 범위 지정

**Filtering 유형**

| 유형 | 설명 |
|---|---|
| Ingress Filtering | 라우터 내부(사내 네트워크)로 유입되는 패킷의 출발지 IP·목적지 포트를 체크해 필터링. 대부분의 공격이 실재하지 않는 위조 IP를 소스로 하므로, 인터넷상에서 사용되지 않는 IP 대역(사설 IP, 루프백, 255.255.255.255 등)만 차단해도 비정상 패킷을 사전 차단하는 효과 |
| Egress Filtering | Ingress의 반대 개념. 라우터 외부로 나가는 패킷의 출발지 IP를 체크 — 외부로 나가는 패킷의 출발지 IP는 반드시 내부 네트워크 대역이어야 정상이며, 그 외는 모두 위조된 패킷 |
| Blackhole Filtering (Null Routing) | 특정 IP·IP 대역에 대해 비정상적인 시도가 감지되면 가상의 쓰레기 인터페이스(Null interface)로 보내도록 하여 패킷이 통신되지 않도록 하는 방법 |
| Unicast RPF (Reverse-Path Forwarding) Filtering | access-list나 blackhole 필터링처럼 일일이 IP를 지정하지 않고도 비정상 트래픽을 효율적으로 필터링하는 기법. 인터페이스로 들어오는 패킷의 출발지 IP에 대해 라우팅 테이블을 확인하여, 그 IP로 라우팅될 때 **같은 인터페이스로 나가는지**를 확인해 비정상 여부(출발지 IP 위조 여부)를 판단 |

!!! tip "연결 고리"
    Smurf 공격 대응 방안의 "ingress filtering(uRPF) 적용"이 바로 이 절의 내용입니다. IP Spoofing을 이용하는 모든 공격(Smurf, SYN Flooding 등)의 근본 대응책이 필터링 기법이라는 것을 기억하세요.

### 4-12. 라우터 자체 보안 — 모드와 enable 패스워드

**라우터 사용(접속) 모드 4가지**

| 모드 | 설명 | 프롬프트 |
|---|---|---|
| User EXEC 모드 | 한정된 명령어만 사용 가능. 주로 라우터의 간단한 상태 조회 | `Router>` |
| Privileged EXEC 모드 | 재부팅·라우팅 등 라우터에서의 모든 명령어 수행 가능(`enable` 명령으로 진입) | `Router#` |
| Global Configuration 모드 | Privileged EXEC 모드에서 라우터 전반적 설정을 변경 | `Router(config)#` |
| Other Configuration 모드 | 특정 인터페이스·특정 라우팅 등 세부 설정을 변경하는 모드 | `Router(config-mode)#` |

**enable password vs enable secret (실무 핵심)**

Privileged 모드로 전환할 때 사용하는 패스워드를 설정하는 명령어는 2가지이며, **안전한 운영을 위해 `enable secret` 사용을 권장**합니다.

| 명령어 | 암호화 방식 | 특징 |
|---|---|---|
| `enable password <패스워드>` | 기본은 평문(Type 0) 저장. `service password-encryption` 명령을 실행하면 Type 7(역함수가 존재하여 원래의 평문 암호를 알 수 있는 방식)로 암호화 | 상대적으로 취약(가역적) |
| `enable secret <패스워드>` | Type 5(일방향 함수로 암호화, MD5)의 암호문으로 저장되어 원래의 평문 암호를 알 수 없음 | 안전(비가역적) — **권장** |

!!! important "핵심"
    `enable password`와 `enable secret`이 함께 설정되어 있으면 **`enable secret`이 우선 적용**됩니다. [법·제도 파트](06-law-practice.md)의 "네트워크 장비 패스워드 암호화 확인(`show running-config`)" 기출 문제가 바로 이 내용과 연결됩니다 — 점검 시 `enable secret` 사용 여부, `username secret` 사용 여부, `service password-encryption` 동작 여부를 확인합니다.

### 4-13. 네트워크 관리 명령어 (ping / traceroute)

| 명령어 | 설명 |
|---|---|
| ping | 종단(End) 노드 간에 네트워크 상태를 관리하기 위한 명령어. Target 시스템에 대한 접근성, 네트워크 속도·품질(손실률)을 검사. **ICMP Echo Request(Type 8)와 ICMP Echo Reply(Type 0)** 메시지 이용 |
| traceroute(Linux·Unix) / tracert(Windows) | 종단 노드 사이에 있는 여러 중계 노드(L3 장비·라우터) 각 구간의 네트워크 상태를 관리하기 위한 명령어로, 네트워크의 라우팅 문제점을 찾아내는 목적으로 사용 |

!!! important "핵심 — traceroute와 tracert의 동작 원리 차이"
    두 명령어의 목적지 도달 원리는 동일하지만(TTL 값을 1씩 증가시키며 중계 노드를 추적), **구현 방식에 차이**가 있습니다.

    - **traceroute (Linux/Unix 계열)**: **UDP 패킷**(포트 33434 이상)을 전송하여 진단
    - **tracert (Windows)**: **ICMP Echo Request** 패킷을 전송하여 진단

**ping 명령 주요 옵션**

| 플랫폼 | 옵션 | 의미 |
|---|---|---|
| Windows | `-n` | 패킷 전송 횟수 설정(default 4회) |
| Windows | `-l` | 패킷 크기(bytes) 설정(default 32bytes) |
| Linux | `-c` | 패킷 전송 횟수 설정(default 무한) |
| Linux | `-s` | 패킷 크기(bytes) 설정(default 56bytes) |

## 5. IDS/IPS 및 보안 장비

> 출제 이유: IDS의 탐지 오류 개념(FP/FN)과 IDS의 유형·행위는 매 회차 출제 빈도가 매우 높습니다.

### 5-1. IDS 탐지 판정 오류

| 판정 | 설명 |
|---|---|
| True Positive (정탐) | 실제 공격을 공격으로 올바르게 탐지 — 정상 상태 |
| True Negative (정상 통과) | 정상 트래픽을 정상으로 올바르게 통과 — 정상 상태 |
| False Positive (오탐, FP) | 공격이 아닌 것을 공격으로 잘못 탐지 → 불필요한 알람, 정상 서비스 차단 |
| False Negative (미탐, FN) | 실제 공격을 공격으로 탐지 못함 → 가장 위험한 오류 |

!!! important "시험 포인트"
    (A) False Positive = 오탐, (B) False Negative = 미탐 을 묻는 단순 암기 문제가 자주 출제됩니다. FP는 '잘못된 긍정(공격 아닌데 공격이라고 함)', FN은 '잘못된 부정(공격인데 아니라고 함)'으로 기억하세요.

### 5-2. IDS 기반별 분류

| 종류 | 설명 |
|---|---|
| 호스트 기반 IDS (HIDS) | 시스템 내부 상태(로그, 파일 변경, 시스템 콜 등)를 분석하여 버퍼 오버플로우, 권한 상승, 루트킷 등 탐지. 에이전트 설치 필요 |
| 네트워크 기반 IDS (NIDS) | 네트워크를 통과하는 패킷을 캡처·분석하여 공격 탐지. 별도 장비로 구성. Snort가 대표적 |

### 5-3. 탐지 방법별 분류

| 방법 | 설명 |
|---|---|
| 오용 탐지 (Signature-based) | 알려진 공격 패턴(시그니처)과 비교하여 탐지. False Negative 높음, False Positive 낮음 |
| 이상 탐지 (Anomaly-based) | 정상 기준선(Baseline)에서 벗어난 행위를 탐지. 알려지지 않은 공격도 탐지 가능. False Positive 높음 |

### 5-4. 공격 탐지 시 IDS 행위 (24년도 1회)

- 알람·이메일·SMS로 관리자에게 침입 사실 즉시 통보
- 공격자 연결에 TCP Reset 패킷 전송하여 연결 강제 차단
- 공격자 IP·사이트를 라우터·방화벽과 연동하여 차단
- 공격 포트를 확인하여 라우터와 방화벽 규칙 설정
- 심각한 경우 네트워크 구조를 임시로 변경

### 5-5. Snort 규칙 관련 문제 (25년도 4회)

| 문제 상황 | 결과 |
|---|---|
| 규칙이 지나치게 일반적/광범위 | 정상 트래픽도 공격으로 판단 → 오탐(False Positive) 증가 |
| 규칙이 지나치게 구체적/좁은 범위 | 실제 공격 트래픽을 탐지 못함 → 미탐(False Negative) 증가 |
| 규칙이 비효율적으로 복잡 | Snort 시스템 처리 부하 증가 → 전체 탐지 성능 저하 |

## 6. 포트 스캔 기법

> 출제 이유: 공격 전 정찰 단계의 핵심 기법으로 각 스캔의 동작 원리와 탐지 회피 방법을 이해해야 합니다.

### 6-1. 스텔스 스캔 3종 (24년도 4회)

| 스캔 종류 | 설명 |
|---|---|
| FIN Scan | FIN 플래그만 설정. 열린 포트: 무응답 / 닫힌 포트: RST+ACK 응답 |
| NULL Scan | 모든 플래그를 0으로 설정(빈 패킷). 열린 포트: 무응답 / 닫힌 포트: RST+ACK |
| Xmas Scan | FIN+URG+PSH 플래그 동시 설정(크리스마스트리처럼 깜박임). 열린 포트: 무응답 / 닫힌 포트: RST+ACK |

**특징 및 한계**

- 공통: 방화벽 우회 및 로그 회피 목적. TCP 3-way handshake를 완성하지 않아 연결 로그 미생성
- 한계: Windows 시스템에서는 열린 포트도 RST를 응답하므로 탐지 불가
- 탐지: 패킷 필터링 방화벽에서 비정상 플래그 조합으로 탐지 가능

### 6-2. 기타 포트 스캔 종류

| 스캔 종류 | 설명 |
|---|---|
| SYN Scan (Half-Open) | SYN만 보내고 SYN-ACK 수신 시 RST 전송. 연결 미완성으로 로그 회피. 가장 일반적 스텔스 스캔 |
| TCP Connect Scan | 완전한 3-way handshake 수행. 탐지 쉬움, 특별한 권한 불필요 |
| UDP Scan | UDP 패킷 전송. 열린 포트: 무응답 / 닫힌 포트: ICMP Port Unreachable |
| Idle Scan (Zombie Scan) | 좀비 호스트를 중간에 이용하여 스캔 출발지 IP 은닉 |

## 7. MITM 공격 & 스푸핑

> 출제 이유: 중간자 공격은 다양한 형태로 출제되며 DNS 스푸핑, ARP 스푸핑이 핵심입니다.

### 7-1. DNS 스푸핑

| 항목 | 내용 |
|---|---|
| 정의 | DNS 질의에 대한 위조 응답을 먼저 전송하여 피해자를 공격자가 제어하는 악성 서버로 유도하는 MITM 공격 |
| 관련 기출 | 26년도 1회 — MITM 공격 기법으로 DNS 스푸핑 |

**DNS 스푸핑 대응**

- DNSSEC(DNS Security Extensions) 적용: DNS 응답에 전자서명 추가하여 위변조 탐지
- DNS over HTTPS (DoH) 또는 DNS over TLS (DoT) 사용
- 캐시 포이즈닝 방지를 위해 소스 포트 랜덤화 및 Transaction ID 랜덤화

### 7-2. Session Hijacking (세션 하이재킹)

| 항목 | 내용 |
|---|---|
| 정의 | 인증된(로그인된) 세션을 탈취하여 피해자인 척 서버와 통신하는 공격 |
| 방법 | 스니핑으로 세션 토큰(쿠키) 탈취, XSS를 통한 쿠키 탈취 등 |
| 관련 기출 | 24년도 1회 |

**대응 방법**

- HTTPS 사용으로 세션 토큰 암호화
- HttpOnly 쿠키 속성으로 JavaScript 접근 차단
- 세션 만료 시간 설정 및 중요 작업 시 재인증
- IP 바인딩: 세션을 특정 IP에 고정

## 8. 요약 정리 — 핵심 암기 표

| 주제 | 핵심 키워드 |
|---|---|
| Slow Read Attack | TCP Window Size = 0, 연결 자원 고갈 |
| Smurf 공격 | IP Spoofing + Directed Broadcast + ICMP 증폭 |
| NTP DDoS | monlist 명령 악용, 700배 증폭, 4.2.7 이상 업그레이드 |
| Promiscuous Mode | 모든 프레임 수신, 스니핑 의심, 암호화가 최선의 대응 |
| 스니핑 탐지 (ping) | 가짜 MAC + ICMP Echo Request → Reply 오면 Promiscuous Mode |
| VLAN 할당 4가지 | 포트 / MAC / 네트워크 주소 / 프로토콜 |
| LAN 스위칭 3가지 | Store-and-Forward / Cut-Through / Fragment-Free |
| IPsec 모드 2가지 | 전송 모드(페이로드 보호) / 터널 모드(전체 패킷 보호) |
| IDS 오탐/미탐 | FP = 공격 아닌데 공격 / FN = 공격인데 통과 |
| 스텔스 스캔 3가지 | FIN / NULL / Xmas — 열린 포트는 무응답 |
| CSMA/CA RTS·CTS | 무선랜 충돌 회피, 연결 타임아웃 설정 프레임 |
| DNS | Recursive(캐시) → Authoritative(공식) 순으로 질의 |
| TCP 3대 제어 | 흐름제어(슬라이딩윈도우) / 오류제어(재전송) / 혼잡제어(전송량 조절) |
| 무선랜 표준 | IEEE 802.11 계열, 802.11b(11Mbps)→g(54Mbps)→n(300Mbps) |
| 무선랜 환경 4가지 | 상용(이동통신사)/공중(불특정다수, 취약)/사설(개인)/기업(업무용) |
| IP 헤더 크기 | 기본 20byte + 옵션 최대 40byte, 이더넷 MTU=1500byte |
| IP Flags | DF(단편화 금지)/MF(재조합할 단편 남음) |
| ICMP 구조 | Type+Code+Checksum, Type3=목적지 도달불가/Code3=포트 도달불가 |
| VPN 계층별 프로토콜 | 2계층: PPTP(MS)/L2F(Cisco)/L2TP, 3계층: IPsec, 4계층: SSL/TLS |
| ACL 표준/확장 | standard(1~99, 출발지만) / extended(100~199, 출발지+목적지+포트) |
| 필터링 4유형 | Ingress(유입 검사)/Egress(유출 검사)/Blackhole(Null라우팅)/uRPF(왕복경로 확인) |
| DRDoS | 반사(Reflection)+증폭(Amplification), TCP/ICMP/UDP(DNS·NTP·SNMP·CHARGEN) 3방식 |
| 라우터 모드 4가지 | User EXEC(`>`) / Privileged EXEC(`#`) / Global Config / Other Config |
| enable password vs secret | password=Type7(가역, 취약) / secret=Type5(MD5, 비가역, 권장·우선적용) |
| ping | ICMP Echo Request(Type8)/Reply(Type0), Win -n/-l, Linux -c/-s |
| traceroute vs tracert | traceroute(Linux/Unix)=UDP(33434+) / tracert(Windows)=ICMP |
