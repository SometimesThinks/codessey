# HTTPS 인증서·TLS·SSL·Certbot 이해

## 1. HTTPS·TLS·SSL의 관계

**HTTPS는 HTTP 통신에 TLS를 적용해 데이터를 보호하는 방식**이다.

| 용어 | 의미 |
|---|---|
| TLS (Transport Layer Security) | 상대를 인증하고 통신 내용을 암호화하며 변조를 탐지하는 통신 규약 |
| SSL (Secure Sockets Layer) | TLS의 이전 규약. 보안 문제로 사용이 중단되고 TLS로 대체됨 |
| HTTPS | TLS로 보호하는 HTTP 통신. 기본 포트는 `443` |

흔히 말하는 **SSL 인증서는 오늘날 TLS에서도 사용하는 인증서를 가리킨다.** 실습의 Nginx 설정도 `listen 443 ssl`이라고 쓰지만, 실제 허용한 규약은 `TLSv1.2`와 `TLSv1.3`이다.

## 2. HTTPS 인증서란 무엇이며 왜 필요한가

**인증서는 도메인과 공개 키의 연결을 인증 기관(CA)이 서명해 증명한 전자 문서**다. 도메인·공개 키·발급 기관·유효 기간 등이 들어가며, 대응하는 개인 키는 서버에 별도로 보관한다.

암호화만으로는 통신 상대가 내가 접속하려던 서버인지 알 수 없다. 인증서는 브라우저가 **해당 도메인의 서버인지 확인하는 근거**가 된다.

브라우저는 TLS 연결을 맺는 동안 인증서의 도메인·유효 기간·신뢰할 수 있는 발급 경로를 확인하고, 서버가 대응하는 개인 키를 가지고 있는지도 검증한다. 이후 HTTP 요청과 응답은 TLS가 암호화하고 변조 여부를 검사한다.

실습에서는 `codyssey.duckdns.org`에 대한 인증서를 Nginx에 적용했다. 443번 포트를 여는 것에 더해, 인증서·개인 키와 TLS 설정이 있어야 HTTPS 연결을 처리할 수 있다.

## 3. Certbot이란 무엇인가

**Certbot은 인증서 발급 요청과 갱신을 자동화하는 무료 오픈 소스 도구**다. 실습에서는 EC2에 설치해 Let's Encrypt에서 인증서를 발급받았다.

| 구성 요소 | 실습에서의 역할 |
|---|---|
| Let's Encrypt | 도메인 제어 권한을 확인하고 인증서를 발급하는 인증 기관 |
| Certbot | 인증 기관에 발급을 요청하고, 인증서를 EC2에 저장·갱신하는 도구 |
| Nginx | 인증서와 개인 키를 사용해 브라우저의 HTTPS 연결을 처리하는 웹 서버 |

실습의 **webroot 방식**에서는 Certbot이 `/home/ubuntu/codyssey-web/.well-known/acme-challenge/`에 임시 검증 파일을 만든다. Let's Encrypt가 해당 도메인의 HTTP 80번 포트로 파일을 확인해 도메인 제어 권한을 검증한다.

사용한 `certbot certonly --webroot` 명령은 인증서를 발급받는 단계이며, Nginx의 TLS 설정은 직접 작성했다.

## 4. 실습에서 인증서를 사용하는 방법

Certbot이 저장한 `/etc/letsencrypt`를 Docker 컨테이너에 연결하고, Nginx가 아래 파일을 읽도록 설정했다. 두 파일은 `/etc/letsencrypt/live/codyssey.duckdns.org/` 아래에 있다.

| 파일 | 역할 |
|---|---|
| `fullchain.pem` | 서버 인증서와 중간 인증서. 브라우저가 인증서의 신뢰 경로를 확인할 때 사용 |
| `privkey.pem` | 서버가 인증서에 대응하는 키의 소유자임을 증명할 때 사용하는 개인 키. 브라우저에 보내지 않음 |

인증서에는 유효 기간이 있으므로 갱신이 필요하다. 실습에서는 `certbot.timer`로 갱신을 주기적으로 시도하고, 갱신 성공 후 훅에서 Nginx 설정 검사와 `reload`를 실행해 새 인증서를 적용하도록 구성했다.

발급 명령과 검증 증빙은 [HTTPS 적용 기록](https.md), 실제 파일 경로와 TLS 설정은 [Nginx 설정](../../configs/nginx/default.conf)을 참고한다.
