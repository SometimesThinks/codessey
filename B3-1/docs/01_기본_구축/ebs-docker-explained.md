# EBS와 Docker 파일 연결 이해

**EBS(Elastic Block Store)는 EC2에 연결해서 쓰는 SSD·하드디스크 역할의 저장 공간**이다. EC2 생성 화면의 EBS 설정은 서버에 사용할 디스크의 종류와 용량을 정하는 단계다.

## 1. EC2·EBS·Docker의 역할

| 구성 요소 | 역할 |
|---|---|
| EC2 | CPU와 메모리를 제공하는 가상 컴퓨터 |
| EBS | 운영체제·프로그램·파일을 저장하는 디스크 |
| Docker | EC2에서 컨테이너를 만들고 실행하는 프로그램 |
| 컨테이너 | Nginx 같은 프로그램이 실행되는 격리된 환경 |

실습의 루트 EBS 설정은 **`gp3`, `8GiB`**다. `gp3`는 범용 SSD 유형이고, `8GiB`는 디스크 용량이다. 루트 볼륨은 Ubuntu 운영체제가 설치된 디스크이며, 이번 구성에서는 Docker 이미지와 웹 파일도 이 저장 공간을 사용한다.

파일은 EBS에 저장되고, 프로그램은 **EC2의 CPU와 메모리를 사용해 실행**된다. EBS 설정 화면의 용량은 메모리(RAM) 용량과 별개다.

## 2. Docker가 EBS의 파일을 사용하는 방법

EBS는 EC2에 디스크로 연결되어 있다. Docker에서는 **EC2에서 보이는 파일·폴더 경로를 컨테이너 안의 경로에 연결**한다. 이를 **바인드 마운트(bind mount)**라고 한다.

```text
EBS에 저장된 EC2의 폴더                 컨테이너에서 보이는 경로
/home/ubuntu/codyssey-web  ──────────→  /usr/share/nginx/html
                         바인드 마운트
```

실습의 Nginx 컨테이너는 이 연결을 통해 웹 파일을 읽는다. 같은 `index.html`이 EC2에서는 `/home/ubuntu/codyssey-web/index.html`, 컨테이너에서는 `/usr/share/nginx/html/index.html`로 보인다. 파일을 복사하는 과정이 아니라 **같은 파일을 컨테이너에서도 사용하는 연결**이다.

## 3. 실제 `docker run` 명령의 `--mount`

[Docker 배포 기록](../04_Docker/docker.md)의 실행 명령에서 웹 폴더를 연결한 옵션은 다음과 같다.

```bash
--mount type=bind,src=/home/ubuntu/codyssey-web,dst=/usr/share/nginx/html,readonly
```

| 설정 | 의미 |
|---|---|
| `--mount` | 파일·폴더 등 저장 공간을 컨테이너에 연결 |
| `type=bind` | EC2의 기존 파일·폴더를 연결하는 방식 |
| `src=/home/ubuntu/codyssey-web` | EC2에 있는 원본 폴더 |
| `dst=/usr/share/nginx/html` | 컨테이너 안에서 사용할 경로 |
| `readonly` | 컨테이너가 이 경로의 파일을 읽기만 하도록 설정 |

**EBS의 ID 대신, EC2에 연결된 디스크의 파일·폴더 경로를 지정하는 것**이다. 최종 실행 명령에서는 아래 세 경로를 모두 읽기 전용으로 연결했다.

| 용도 | EC2의 원본 경로 (`src`) | 컨테이너 경로 (`dst`) |
|---|---|---|
| 웹 파일 | `/home/ubuntu/codyssey-web` | `/usr/share/nginx/html` |
| Nginx 설정 | `/home/ubuntu/codyssey-nginx/default.conf` | `/etc/nginx/conf.d/default.conf` |
| HTTPS 인증서 | `/etc/letsencrypt` | `/etc/letsencrypt` |

## 4. 컨테이너를 삭제하면 파일은 어떻게 되는가

| 저장 위치 | 컨테이너 삭제 시 |
|---|---|
| 컨테이너 자체의 쓰기 공간에만 저장한 파일 | 컨테이너와 함께 삭제 |
| 바인드 마운트로 연결한 EC2의 원본 파일 | EC2 쪽에 유지 |

따라서 실습의 Nginx 컨테이너를 삭제하고 같은 마운트 설정으로 다시 만들면 기존 웹 파일을 다시 사용할 수 있다. 이 보존은 원본 파일과 해당 EBS가 유지되는 것을 전제로 한다.

EC2의 디스크 설정 과정은 [기본 구축 흐름](basic-build-flow.md), 웹 요청 처리 과정은 [외부 요청과 응답 흐름](request-flow.md)을 참고한다.
