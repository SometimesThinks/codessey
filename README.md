# 클라우드 환경에서 웹 서비스 인프라 구축

## 프로젝트 개요

클라우드 환경에서 외부 접속 가능한 웹 서비스 인프라를 직접 구축하는 프로젝트

## 실행환경

- 클라우드 플랫폼: Amazon Web Services
- 리전: 서울 리전 `ap-northeast-2`
- 인스턴스: 온디맨드 `t3.micro` 1대, 무료 혜택 없는 유료 실습
- 운영체제: Ubuntu 26.04 LTS, x86_64
- 스토리지: EBS gp3 8GiB
- 네트워크:
  - VPC 1개
  - Public Subnet 1개
  - Internet Gateway 1개
  - Route Table에 `0.0.0.0/0 -> Internet Gateway` 경로 설정
- 웹 서버: Docker `nginx:stable-alpine`, HTTP·HTTPS 직접 서비스
- 접근 방식:
  - SSH: 개인 IP 또는 지정 IP 대역에서만 허용
  - HTTP: `0.0.0.0/0`에서 80번 포트 접근 허용
  - HTTPS: `0.0.0.0/0`에서 443번 포트 접근 허용

## 프로젝트 구조

```text
B3-1/
├── README.md
├── docs/
│   ├── 01_기본_구축/                 # 아키텍처·구축 흐름·IAM 설명
│   ├── 02_접속_검증/                 # HTTP·HTTPS 검증
│   ├── 03_HTTPS/                 # HTTPS 보너스
│   ├── 04_Docker/                # Docker 보너스
│   ├── 05_트러블_슈팅/                # 오류 해결 보고서
│   └── 06_리소스_정리/                # 리소스 정리 체크리스트
├── configs/                      # 캡처에서 전사한 실습 설정
└── outputs/                      # 01_계정 ~ 13_리소스_정리 섹션별 캡처
```

## 수행 항목 체크리스트

### 네트워크 구성

- [x] VPC 1개 생성
- [x] Public Subnet 1개 생성
- [x] Internet Gateway VPC 연결
- [x] Public Subnet Route Table에 `0.0.0.0/0 -> Internet Gateway` 경로 추가
- [x] Public Subnet 인스턴스의 인터넷 아웃바운드 통신 확인
  - [x] 예: `curl https://example.com` 성공

### 컴퓨트 및 웹 서버 배포

- [x] Public Subnet 내 EC2 인스턴스 1대 생성 — 최종 서브넷·SG 연결 및 인스턴스 ID 확인
- [x] SSH 인스턴스 접속
- [x] Nginx 등 웹 서버 설치
- [x] 웹 서버 실행 상태 확인
- [x] 인스턴스 내부 `curl http://localhost` 200 응답 확인

### 접근 제어

- [x] Security Group 인바운드 필요 포트만 허용
- [x] HTTP 80번 포트 `0.0.0.0/0` 접근 허용
- [x] SSH 22번 포트 개인 IP 또는 지정 IP 대역 접근 허용
- [x] `0.0.0.0/0` 대상 전체 포트 `0-65535` 허용 규칙 미생성

### IAM 최소 권한

- [x] 실습용 IAM 사용자 또는 Role 1개 사용
- [x] EC2, VPC, Security Group 구성 필요 권한 제한 — 최종 정책·연결 목록 확인
- [x] 생성, 조회, 태그, 연결 등 실습 필요 권한 구성 — [사용자 제공 최종 정책](configs/iam-policy.json) 확인
- [x] 실습 무관 S3, RDS 등 서비스 권한 미부여 — 최종 정책·연결 목록 확인
- [x] 관리자 권한(`AdministratorAccess`) 권한 미부여 — 최종 정책·연결 목록 확인

### 외부 접속 검증

- [x] A 또는 B 중 외부 접속 검증 방식 선택
- [x] A 선택 시 브라우저 `http://<퍼블릭 IP>` 페이지 정상 표시 — B 선택 및 브라우저 추가 검증 완료
- [x] B 선택 시 `GET http://<퍼블릭 IP>/health` 200 응답
- [x] 고정 응답 문구 확인
  - [x] 예: `OK`, `Hello Cloud`, `Welcome to nginx!`
- [x] 선택한 검증 방식 README 명시

### 운영 안정성 및 과금 방지

- [x] 실습 종료 후 생성 리소스 정리
- [x] EC2 종료 또는 삭제 상태 확인
- [x] EBS 볼륨 삭제 여부 확인
- [x] Elastic IP 사용 시 Release 여부 확인 — 기존 기록상 미생성, 목록 확인 후 해당 없음 기록
- [x] Internet Gateway Detach 및 삭제 여부 확인
- [x] VPC, Subnet, Route Table 삭제 여부 확인
- [x] 정리 결과 `docs/06_리소스_정리/cleanup-checklist.md` 기록

### 보너스 과제

#### HTTPS 적용

- [x] 무료 서브도메인, 보유 도메인 또는 구매 도메인 연결
- [x] Let’s Encrypt 등 HTTPS 인증서 적용
- [x] HTTPS 접속 정상 동작 확인
- [x] 인증서 적용 방식과 검증 결과 문서화

#### Docker 컨테이너 웹 서비스 배포

- [x] EC2 인스턴스 내부 Docker 설치
- [x] 컨테이너 웹 서비스 실행
- [x] 사용할 컨테이너 이미지 선택
  - [x] 이전 미션 이미지 또는 공개 이미지 사용 가능
- [x] 인스턴스 내부 `curl http://localhost` 정상 응답 확인
- [x] 외부 `http://<퍼블릭 IP>` 접속 또는 `/health` 호출 정상 응답 확인
- [x] Docker 문서에 컨테이너 이미지명과 실행 방식 기록 및 README 링크 연결
- [x] Docker 문서에 포트 매핑 기록 및 README 링크 연결
- [x] `docker ps` 컨테이너 Up 상태 확인 및 스크린샷 저장
- [x] 외부 접속 결과 스크린샷 저장
- [x] Docker 검증 결과 스크린샷 2장 이상 제출

## 제약 사항

- 모든 리소스 AWS 서울 리전 `ap-northeast-2` 생성
- 과제의 micro급 규모 유지, 실제 계정의 무료 혜택 부재에 따른 유료 사용
- 루트 계정 사용 금지
- 별도 IAM 사용자 또는 Role 콘솔 접근
- EC2, VPC, Security Group 실습 필요 권한 제한
- `AdministratorAccess` 권한 사용 금지
- 키페어 1개 생성 및 안전 보관
- 키페어 재발급 불가 전제 관리
- SSH 22번 포트 본인 개인 IP 또는 지정 IP 대역만 허용
- 운영 또는 관리 목적 포트 방치 금지
- `0.0.0.0/0` 대상 전체 포트 허용 규칙 생성 금지
- 생성 리소스 정리 대상 추적
- 실습 종료 후 모든 리소스 종료 또는 삭제
- 정리 대상: EC2, EBS Volume, Elastic IP, Internet Gateway, VPC
- 생성 시 NAT Gateway, ELB/ALB, RDS 삭제 확인
- 모든 리소스 삭제 후 Billing Dashboard 확인 권장

## 결과물

### 기본 구축 및 검증 자료

#### 구축 구성과 과정

- [아키텍처](docs/01_기본_구축/architecture.png)
- [외부 요청과 응답 흐름](docs/01_기본_구축/request-flow.md)
- [기본 구축 흐름](docs/01_기본_구축/basic-build-flow.md)
- [실습 설정 보관본](configs/README.md)

#### 외부 접속 검증

- [HTTP·HTTPS 응답과 스크린샷](docs/02_접속_검증/validation.md)

#### 리소스 정리

- [리소스 정리 체크리스트](docs/06_리소스_정리/cleanup-checklist.md)

#### 트러블 슈팅

- [트러블 슈팅 보고서](docs/05_트러블_슈팅/troubleshooting.md)

### HTTPS 보너스 기록

- [도메인 연결·인증서 적용·자동 갱신·검증 스크린샷](docs/03_HTTPS/https.md)

### Docker 보너스 기록

- [컨테이너 이미지·실행 방식·포트 매핑·검증 스크린샷](docs/04_Docker/docker.md)
