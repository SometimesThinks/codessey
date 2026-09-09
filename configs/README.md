# 실습 설정 보관본

기존 캡처의 명령·파일 내용을 전사한 보관본, 서버에서 직접 내려받은 백업과 구분

| 보관 파일 | EC2 경로 | 근거 |
|---|---|---|
| [default.conf](nginx/default.conf) | `/home/ubuntu/codyssey-nginx/default.conf` | [TLS 설정 캡처](../outputs/11_HTTPS/11_07_Nginx_TLS_설정.png) |
| [index.html](web/index.html) | `/home/ubuntu/codyssey-web/index.html` | [웹 파일 생성 캡처](../outputs/10_Docker/10_06_Docker_웹_실행.png) |
| [health](web/health) | `/home/ubuntu/codyssey-web/health` | [웹 파일 생성 캡처](../outputs/10_Docker/10_06_Docker_웹_실행.png) |
| [reload-nginx.sh](reload-nginx.sh) | `/etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh` | [갱신 훅 캡처](../outputs/12_최종_검증/12_03_갱신_훅_타이머.png) |

- 갱신 훅의 서버 파일 권한: `750`
- 인증서 및 개인 키: 보관 대상 제외, 재배포 시 별도 발급 필요
- [최종 컨테이너 실행 명령](../docs/04_Docker/docker.md)
- [인증서 발급·갱신 기록](../docs/03_HTTPS/https.md)

## IAM 최종 정책

[IAM 개념과 실습 정책 JSON 이해](../docs/01_기본_구축/iam-policy-explained.md) — 정책 항목과 허용 범위 설명

[사용자 제공 최종 JSON](iam-policy.json) — 2026-09-09 대화로 제공된 정책 내용의 보관본. 붙여넣기 과정의 탭 HTML 표기와 별표 이스케이프 정규화

EC2 서비스·서울 리전 제한 및 `ec2:GetSecurityGroupsForVpc` 포함 확인. `Resource: "*"` 사용으로 개별 실습 리소스까지의 제한은 미적용. [최종 연결 목록](../outputs/02_IAM/02_07_IAM_권한_확인.png)에서 본 정책과 `IAMUserChangePassword`의 직접 연결 확인
