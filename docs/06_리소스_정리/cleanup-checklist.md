# 리소스 정리 체크리스트

## 정리 현황

- 대상: AWS 서울 리전 `ap-northeast-2`의 본 실습 리소스 및 실습 전용 DuckDNS 설정
- 현재 상태: 정리 전, 삭제 결과 미확인
- 정리 시작 시각: 미기록
- 정리 완료 시각: 미기록
- 기록 기준: 실제 콘솔 확인 후 완료 표시 및 확인 시각·증빙 경로 기록
- 미생성 항목: 목록 확인 후 `해당 없음 — 미생성` 기록

## 1. 삭제 전 자료 확보

- [ ] HTTP·HTTPS 및 Docker 검증 캡처의 로컬 보관 확인
- [ ] 아키텍처 이미지와 실습·트러블 슈팅 문서 확인
- [x] 웹 파일, Nginx 설정, 컨테이너 실행 명령 및 갱신 훅의 기록 확인 — [캡처 전사 보관본](../../configs/README.md)
- [x] EC2 인스턴스 ID와 연결된 EBS 볼륨 ID 기록 — 2026-09-09 캡처 확인
- [ ] 실습 리소스 이름·ID 대조 및 다른 프로젝트 리소스와의 구분

EC2 Terminate 이후 재접속·복구 불가 및 삭제 설정된 EBS 데이터 소실에 따른 사전 자료 확보 필요. [AWS EC2 종료 안내](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html)

## 2. 대상 목록

기존 실습 기록 기준 목록이며, 삭제 직전 콘솔에서 대상 재확인 필요

| 대상 | 이름·식별 정보 | 정리 결과 | 확인 시각·증빙 |
|---|---|---|---|
| EC2 | `codyssey-web` / `i-09d0dad7ff6829f76` | 미확인 | — |
| EBS | gp3 8 GiB / `vol-0c4938565c0840fd6` | 미확인 | — |
| Security Group | `codyssey-sg` / `sg-0a04831223ba5fc2d` | 미확인 | — |
| Subnet | `codyssey-pulic-subnet` / `subnet-0c7f8c97172ee3de3` | 미확인 | — |
| Route Table | `codyssey-route-table` / `rtb-056aecce93e02438e` | 미확인 | — |
| Internet Gateway | `codyssey-igw` / `igw-0637dc3e8b222c179` | 미확인 | — |
| VPC | `codyssey-vpc` / `vpc-0ff964261fd866334` | 미확인 | — |
| 키페어 | `codyssey-key` | 미확인 | — |
| DuckDNS | `codyssey.duckdns.org` | 미확인 | — |
| IAM 사용자 | `codyssey-yun` / 실습 전용 여부 확인 후 정리 | 미확인 | — |
| IAM 사용자 지정 정책 | `codyssey-aws-iam` / 다른 연결 대상 확인 후 정리 | 미확인 | — |
| Elastic IP | 기존 기록상 미생성, 자동 할당 퍼블릭 IP 사용 | 목록 확인 전 | — |
| NAT Gateway·ELB/ALB·RDS | 기존 기록상 미생성 | 목록 확인 전 | — |
| EBS 스냅샷·추가 볼륨·사용자 지정 AMI | 생성 여부 확인 필요 | 미확인 | — |

생성·연결 정보 근거: [EC2 보안](../../outputs/06_EC2_EBS/06_05_EC2_보안_확인.png), [EC2 상세](../../outputs/06_EC2_EBS/06_06_EC2_상세_확인.png), [EBS 연결](../../outputs/06_EC2_EBS/06_07_EBS_연결_확인.png). [EBS 종료 시 삭제](../../outputs/06_EC2_EBS/06_08_EBS_종료시_삭제.png) 값 `예` 확인 완료 — 실제 삭제 여부는 정리 후 확인

## 3. 컴퓨트·스토리지 정리

- [ ] 추가 서비스 생성 여부 확인 및 실습용 리소스 존재 시 선행 삭제
- [ ] EC2 `codyssey-web`의 Terminate 실행 및 `Terminated` 상태 확인
- [ ] 연결된 EBS 루트 볼륨의 자동 삭제 여부 확인
- [ ] 남은 실습용 볼륨·스냅샷·사용자 지정 AMI 존재 여부 확인 및 필요 시 정리
- [ ] Elastic IP 목록 확인 및 실습용 할당 존재 시 연결 해제·Release

정리 완료 기준: EC2의 `Stopped` 상태가 아닌 `Terminated` 상태 및 잔여 스토리지 확인

## 4. 네트워크 정리

- [ ] 실습 EC2·서비스에 연결된 네트워크 인터페이스의 정리 확인
- [ ] `codyssey-sg` 삭제 확인
- [ ] `codyssey-pulic-subnet` 삭제 확인
- [ ] `codyssey-route-table` 삭제 확인
- [ ] `codyssey-igw`의 VPC 연결 해제 및 삭제 확인
- [ ] `codyssey-vpc` 삭제 확인

VPC 콘솔의 일괄 삭제 사용 시 삭제 예정 구성 요소 확인 후 위 항목별 결과 기록. 삭제를 막는 서비스 관리 인터페이스 존재 시 해당 원본 서비스의 선행 정리 필요. [AWS VPC 삭제 안내](https://docs.aws.amazon.com/vpc/latest/userguide/delete-vpc.html)

## 5. DNS·키페어·IAM 정리

- [ ] AWS 키페어 `codyssey-key` 삭제 확인
- [ ] 로컬 `codyssey-key.pem`의 다른 사용 여부 확인 및 실습 종료 후 정리
- [ ] DuckDNS의 `codyssey.duckdns.org` 등록 삭제 확인
- [ ] IAM 최종 설정 증빙 확보 및 남은 AWS 확인 작업 완료
- [ ] 다른 관리 주체의 계정 접근 가능 여부 확인
- [ ] 실습 전용 IAM 사용자 `codyssey-yun`의 자격 증명·정책 연결 정리 및 사용자 삭제
- [ ] 다른 연결 대상이 없는 실습 전용 사용자 지정 정책 `codyssey-aws-iam` 삭제

공용 계정·사용자·정책은 삭제 대상에서 제외. `IAMUserChangePassword` 등 AWS 관리형 정책 자체는 삭제 대상에서 제외

## 6. 비용 및 제출 자료 확인

- [ ] 실습 리소스 목록의 삭제·해제·미생성 상태 최종 확인
- [ ] Billing의 비용·사용량 확인 및 확인 시각 기록
- [ ] 이미 발생한 비용과 잔여 리소스 여부의 구분 기록
- [ ] 비용 반영 지연 가능성을 고려한 후속 확인 결과 기록
- [ ] 본 문서 대상 목록의 결과·시각·증빙 기입
- [ ] README의 리소스 정리 체크박스 갱신
- [ ] 실제 정리 완료 후 README에 종료 시각과 기존 서비스 URL 운영 종료 상태 기록

| 확인 항목 | 기록 |
|---|---|
| 비용 확인 시각 | 미기록 |
| 표시된 비용·통화·조회 기간 | 미기록 |
| 잔여 실습 리소스 | 미확인 |
| 후속 비용 확인 결과 | 미기록 |
| 증빙 경로 | 미기록 |

## 증빙 파일명

정리 진행 시 `outputs/13_리소스_정리/`에 아래 형식으로 저장 예정, 실제 캡처 확보 후 링크 추가

- `13_01_EC2_종료.png`
- `13_02_EBS_정리.png`
- `13_03_네트워크_정리.png`
- `13_04_DNS_정리.png`
- `13_05_IAM_정리.png`
- `13_06_비용_확인.png`

[README로 이동](../../README.md)
