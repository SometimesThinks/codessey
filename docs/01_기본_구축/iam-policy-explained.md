# 실습용 IAM 정책 JSON 해설

설명 대상은 실습 초기 EC2·VPC 권한 정책이다. 최종 적용 내용은 [IAM 정책 보관본](../../configs/iam-policy.json) 참조. 이 문서는 정책의 뜻을 설명하며, 정책을 변경하지 않는다.

## 1. 이 JSON이 하는 일

이 정책의 뜻을 문장으로 풀면 다음과 같다.

> 이 정책이 연결된 IAM 사용자가 서울 리전의 EC2 서비스에 요청할 때, Action 목록에 적힌 조회·생성·수정·연결·삭제 작업을 허용한다. 대상 리소스는 특정 ID로 한정하지 않는다.

JSON은 정보를 정해진 형식으로 적는 방법이다. 이 JSON을 IAM에 저장하면 **권한 정책**이 된다. 서버를 만드는 실행 스크립트가 아니므로, 정책을 생성하거나 사용자에게 연결하는 것만으로 EC2가 만들어지지는 않는다.

이번 작업에서는 정책을 `b3-1-lab` 사용자에게 연결한다. 사용자 이름은 JSON 안에 적혀 있지 않으며, IAM 콘솔에서 정책을 누구에게 연결하는지로 적용 대상을 정한다. 이처럼 사용자·그룹·Role에 연결하는 정책에는 `Principal` 항목을 넣지 않는다. [AWS IAM 정책 요소 안내](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html).

## 2. 괄호와 기호 읽는 법

| 표기 | 뜻 | 정책에서 보이는 예 |
|---|---|---|
| `{ }` | 이름과 값을 묶는 객체 | 정책 전체, Statement 안의 규칙, Condition |
| `[ ]` | 여러 값을 담는 목록 | Statement 목록, Action 목록 |
| `"이름": 값` | 항목 이름과 그 값을 연결 | `"Effect": "Allow"` |
| `"문자열"` | 문자로 된 값 | `"ap-northeast-2"` |
| `,` | 옆 항목과 구분 | Action 이름 사이의 쉼표 |
| `*` | IAM이 해석하는 와일드카드. 위치에 따라 작업이나 리소스의 범위를 넓힘 | `Describe*`, `"Resource": "*"` |

콜론도 위치에 따라 다르게 읽는다. `"Effect": "Allow"`의 콜론은 JSON의 이름과 값을 연결하지만, `"ec2:CreateVpc"` 안의 콜론은 문자열의 일부이며 AWS 서비스와 작업 이름을 구분한다.

들여쓰기는 사람이 읽기 좋게 하는 형식이다. AWS에 붙여 넣는 JSON에는 설명용 주석이나 마지막 항목 뒤의 쉼표를 추가하지 않는다. `*`의 작업 패턴 의미는 [AWS Action 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_action.html)을 참고한다.

## 3. JSON의 큰 항목 설명

### `"Version": "2012-10-17"`

AWS가 이 문서를 어떤 **IAM 정책 문법 버전**으로 해석할지 정한다. 정책 작성일, 실습 날짜, AWS 계정 생성일이 아니다. 따라서 오늘 날짜로 바꾸지 않고 그대로 사용한다. [AWS Version 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_version.html).

### `"Statement": [ ... ]`

실제 권한 규칙이 들어 있는 목록이다. 규칙 하나는 `{ ... }`로 묶으며, 서로 다른 규칙을 여러 개 넣을 수 있다. 현재 정책에는 규칙이 하나 있으므로, 그 안의 모든 Action에 동일한 Resource와 Condition이 적용된다. [AWS Statement 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_statement.html).

### `"Sid": "Ec2VpcLabInSeoul"`

**Statement ID**, 즉 이 규칙을 구분하기 위한 이름이다. `Ec2VpcLabInSeoul`은 사람이 알아보기 위해 붙인 “서울에서 하는 EC2/VPC 실습”이라는 이름이다.

이 이름 자체는 권한을 제한하지 않는다. 이름에 `Seoul`이 들어 있어도 실제 Condition에 서울 조건이 없으면 지역 제한이 생기지 않는다. 또한 IAM 콘솔에서 정한 정책 이름 `B3-1-EC2-VPC-Lab`과 규칙 이름인 Sid는 서로 다르다. [AWS Sid 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_sid.html).

### `"Effect": "Allow"`

이 규칙의 Action·Resource·Condition이 요청과 맞으면 **허용**한다는 뜻이다. 반대 값은 `Deny`, 즉 명시적 거부다.

`Allow`는 “지금 실행하라”는 뜻이 아니다. 사용자가 나중에 요청할 때 그 요청을 허용할 근거가 된다. [AWS Effect 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_effect.html).

### `"Action": [ ... ]`

사용자에게 허용할 AWS 작업 목록이다. 이 정책에는 `ec2:Describe*`를 포함해 **36개 항목**이 있다. `Describe*`는 여러 조회 작업을 포괄하는 패턴이므로 실제 API 작업 수가 36개라는 뜻은 아니다.

`ec2:CreateVpc`를 나누어 읽으면 `ec2`는 서비스 접두어, `CreateVpc`는 VPC 생성 작업이다. VPC·Subnet·Internet Gateway·Security Group 작업도 EC2 API에 포함되므로 `ec2:`로 시작한다. 목록 순서는 실행 순서가 아니다. [AWS Action 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_action.html), [EC2 API 작업 목록](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Operations.html).

### `"Resource": "*"`

해당 작업의 대상 리소스를 특정 ID로 한정하지 않는다는 뜻이다. 특정 인스턴스만 허용하려면, 그 작업이 리소스 단위 제한을 지원하는지 확인하고 ARN 같은 리소스 식별자를 사용해야 한다.

예를 들어 인스턴스 ARN은 `arn:aws:ec2:ap-northeast-2:<계정 ID>:instance/<인스턴스 ID>`와 같은 형식이다. 현재는 이런 특정 ARN 대신 `*`를 사용한다.

`*`가 있다고 모든 AWS 서비스의 모든 작업이 허용되는 것은 아니다. **Action에 나열된 작업과 Condition도 함께 만족해야 한다.** 다른 사람의 AWS 계정에 있는 모든 리소스를 조작할 수 있다는 뜻도 아니다. [AWS Resource 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html).

현재 정책은 같은 계정의 서울 리전에 있는 기존 EC2/VPC 리소스도 작업 대상에 포함할 수 있다. `B3-1` 이름이나 태그를 붙이는 것만으로 해당 프로젝트에 한정되지 않는다. EC2의 Describe 조회 작업은 리소스 단위 권한 제한을 지원하지 않으므로, 나중에 범위를 좁힐 때는 조회 규칙과 수정·삭제 규칙을 분리해야 한다. [AWS EC2 콘솔 권한 안내](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-policies-ec2-console.html).

### `"Condition": { "StringEquals": { "aws:RequestedRegion": "ap-northeast-2" } }`

추가로 만족해야 하는 조건이다.

| 항목 | 뜻 |
|---|---|
| `Condition` | 이 규칙이 적용될 조건 |
| `StringEquals` | 문자열이 지정한 값과 정확히 같은지 비교 |
| `aws:RequestedRegion` | 요청이 호출하는 AWS 서비스 엔드포인트의 리전 |
| `ap-northeast-2` | 서울 리전 코드 |

이를 풀면 “요청 리전이 서울인 경우에만 이 규칙으로 허용한다”가 된다. 사용자가 실제로 서울에 있어야 한다는 뜻이 아니며, 접속자의 IP를 제한하는 조건도 아니다. IAM 콘솔 자체를 서울에 설치하는 설정도 아니다.

이 키는 요청 엔드포인트를 기준으로 판단한다. 모든 서비스의 처리 결과나 데이터가 무조건 그 리전에만 머무르도록 보장하는 조건은 아니다. [AWS Condition 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html), [AWS RequestedRegion 설명](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-requestedregion).

## 4. Action에 적힌 작업 36개 해석

표의 각 항목은 해당 작업을 **할 수 있는 권한**을 뜻한다. 정책을 저장했다고 이 작업들이 차례대로 실행되는 것은 아니다.

### 조회

| Action | 뜻 |
|---|---|
| `ec2:Describe*` | EC2 서비스에서 이름이 Describe로 시작하는 조회 작업을 허용한다. 인스턴스·VPC·Subnet·볼륨·보안 그룹 등의 목록과 설정을 보는 데 사용한다. |

`Describe*`는 조회 작업 패턴이며 생성·삭제 작업까지 포함하는 `ec2:*`와 범위가 다르다. [AWS EC2 조회 권한 예시](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-policies-ec2-console.html).

### VPC와 Subnet

| Action | 뜻 |
|---|---|
| `ec2:CreateVpc` | 격리된 가상 네트워크인 VPC를 생성한다. |
| `ec2:ModifyVpcAttribute` | VPC의 DNS 해석 같은 속성을 변경한다. |
| `ec2:DeleteVpc` | VPC를 삭제한다. |
| `ec2:CreateSubnet` | VPC 안에 주소 범위를 나눈 Subnet을 생성한다. |
| `ec2:ModifySubnetAttribute` | Subnet의 퍼블릭 IPv4 자동 할당 같은 속성을 변경한다. |
| `ec2:DeleteSubnet` | Subnet을 삭제한다. |

속성 변경은 해당 리소스의 모든 설정을 한 번에 바꾸는 포괄 명령이 아니라 API가 지원하는 속성에 적용된다. [VPC 속성 변경 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcAttribute.html), [Subnet 속성 변경 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifySubnetAttribute.html).

### Internet Gateway

| Action | 뜻 |
|---|---|
| `ec2:CreateInternetGateway` | VPC와 인터넷 사이의 통신에 사용하는 Internet Gateway를 생성한다. |
| `ec2:AttachInternetGateway` | Internet Gateway를 VPC에 연결한다. |
| `ec2:DetachInternetGateway` | Internet Gateway와 VPC의 연결을 해제한다. |
| `ec2:DeleteInternetGateway` | Internet Gateway를 삭제한다. |

`Create`는 만들기, `Attach`는 연결하기, `Detach`는 연결 해제, `Delete`는 삭제다. 생성만 해서는 VPC 연결이나 Subnet 라우팅까지 완성되지 않는다. [AWS Internet Gateway 구성 안내](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-igw.html).

### Route Table과 Route

| Action | 뜻 |
|---|---|
| `ec2:CreateRouteTable` | 트래픽의 목적지별 전달 경로를 담는 Route Table을 생성한다. |
| `ec2:AssociateRouteTable` | 이번 실습에서는 Route Table을 Public Subnet에 연결한다. |
| `ec2:DisassociateRouteTable` | Route Table과 Subnet의 명시적 연결을 해제한다. |
| `ec2:CreateRoute` | Route Table에 경로 한 줄을 추가한다. 예: `0.0.0.0/0 → Internet Gateway`. |
| `ec2:ReplaceRoute` | 기존 경로의 전달 대상을 변경한다. |
| `ec2:DeleteRoute` | Route Table에서 경로 한 줄을 삭제한다. |
| `ec2:DeleteRouteTable` | Route Table 자체를 삭제한다. |

Route Table은 경로 목록을 담는 표이고, Route는 그 안의 경로 한 줄이다. 연결을 해제한 Subnet에는 VPC의 기본 Route Table이 적용될 수 있으므로 연결 해제와 네트워크 차단은 같은 뜻이 아니다. [Route Table 연결 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateRouteTable.html), [연결 해제 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateRouteTable.html).

### Security Group

| Action | 뜻 |
|---|---|
| `ec2:CreateSecurityGroup` | 네트워크 접근 규칙을 담는 Security Group을 생성한다. |
| `ec2:AuthorizeSecurityGroupIngress` | 인바운드, 즉 들어오는 통신의 허용 규칙을 추가한다. |
| `ec2:AuthorizeSecurityGroupEgress` | 아웃바운드, 즉 나가는 통신의 허용 규칙을 추가한다. |
| `ec2:RevokeSecurityGroupIngress` | 기존 인바운드 허용 규칙을 제거한다. |
| `ec2:RevokeSecurityGroupEgress` | 기존 아웃바운드 허용 규칙을 제거한다. |
| `ec2:ModifySecurityGroupRules` | 기존 보안 그룹 규칙을 수정한다. |
| `ec2:DeleteSecurityGroup` | Security Group 자체를 삭제한다. |

`Authorize`는 허용 규칙 추가, `Revoke`는 기존 허용 규칙 제거다. 예를 들어 80번 HTTP를 열 때는 인바운드 규칙에 포트와 소스 IP 범위를 지정한다. 현재 IAM JSON에는 그 포트나 IP 값을 제한하는 조건이 없다. [보안 그룹 인바운드 규칙 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AuthorizeSecurityGroupIngress.html).

### SSH 키페어

| Action | 뜻 |
|---|---|
| `ec2:CreateKeyPair` | EC2 SSH 접속에 사용할 공개 키와 개인 키의 쌍을 생성한다. |
| `ec2:DeleteKeyPair` | AWS에 등록된 키페어 정보를 삭제한다. |

`DeleteKeyPair`는 내 컴퓨터의 `.pem` 파일을 지우지 않는다. 이미 실행 중인 인스턴스 안에 등록된 공개 키도 자동으로 제거하지 않으므로, 이 작업만으로 기존 SSH 접속이 즉시 차단되는 것은 아니다. [키페어 삭제 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteKeyPair.html).

### EC2 인스턴스

| Action | 뜻 |
|---|---|
| `ec2:RunInstances` | 새 EC2 인스턴스를 생성하고 실행한다. |
| `ec2:StartInstances` | 중지 상태인 기존 인스턴스를 시작한다. |
| `ec2:StopInstances` | 인스턴스를 중지한다. 나중에 다시 시작할 수 있다. |
| `ec2:RebootInstances` | 실행 중인 인스턴스를 재부팅한다. |
| `ec2:TerminateInstances` | 인스턴스를 종료하여 제거한다. 같은 인스턴스를 다시 시작할 수 없다. |
| `ec2:ModifyInstanceAttribute` | 인스턴스 유형, 종료 방지, 연결된 보안 그룹 등 API가 지원하는 인스턴스 속성을 변경한다. |

`RunInstances`의 Run은 새 서버를 만드는 작업이고, `StartInstances`는 이미 있는 서버를 다시 켜는 작업이다. [인스턴스 생성 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RunInstances.html).

`Stop`은 인스턴스를 남겨 두며, EBS 볼륨도 유지된다. `Terminate` 시 EBS 삭제 여부는 볼륨의 종료 시 삭제 설정에 따라 달라지므로 별도로 확인한다. [중지 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StopInstances.html), [종료 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_TerminateInstances.html).

`ModifyInstanceAttribute`에는 상태 등 실행 조건이 있는 속성이 있다. IAM에서 허용해도 실행 중인 인스턴스의 유형을 바로 바꾸는 등 모든 요청이 성공하는 것은 아니다. [인스턴스 속성 변경 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyInstanceAttribute.html).

### EBS와 태그

| Action | 뜻 |
|---|---|
| `ec2:DeleteVolume` | 서버의 디스크 역할을 하는 EBS 볼륨을 삭제한다. |
| `ec2:CreateTags` | 리소스에 `Name`, `Project=B3-1` 같은 태그를 추가하거나 같은 키의 값을 갱신한다. |
| `ec2:DeleteTags` | 리소스에서 태그를 제거한다. 리소스 자체를 삭제하는 작업은 아니다. |

EBS 볼륨 삭제는 인스턴스에서 분리되어 삭제 가능한 상태여야 한다. 태그는 리소스를 식별하고 정리할 때 쓰는 이름표이며, 태그에 따라 권한을 제한하려면 정책에 관련 조건을 별도로 작성해야 한다. [EBS 삭제 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVolume.html), [태그 생성 API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTags.html).

## 5. 실제 요청을 넣어서 읽어 보기

아래 표는 **현재 JSON 한 개가 해당 요청에 Allow를 제공하는지**를 설명한다. 다른 정책이나 계정 제한이 없다는 가정이며, IAM 허용과 API 작업의 실제 성공은 구분한다.

| 요청 | 이 정책의 판단 | 이유 |
|---|---|---|
| 서울에서 VPC 만들기 | 허용 근거가 있음 | `CreateVpc`가 있고 리전 조건도 맞음 |
| 도쿄에서 VPC 만들기 | 이 정책으로는 허용하지 않음 | 요청 리전이 `ap-northeast-2`가 아님 |
| 서울에서 EC2 인스턴스 종료하기 | 허용 근거가 있음 | `TerminateInstances`가 포함됨 |
| 서울에서 기존의 다른 프로젝트 인스턴스 종료하기 | 허용 근거가 있음 | 특정 인스턴스나 프로젝트 태그로 Resource를 제한하지 않음 |
| IAM 사용자 추가 생성하기 | 이 정책으로는 허용하지 않음 | `iam:CreateUser`가 없음 |
| S3 버킷 만들기 | 이 정책으로는 허용하지 않음 | `s3:CreateBucket`이 없음 |
| 서울에서 EC2 여러 대 만들기 | 이 정책에 수량 제한은 없음 | `RunInstances`는 있지만 1대 제한 조건이 없음 |

권한이 있어도 VPC에 남은 리소스가 있어 삭제가 실패하거나, 계정 할당량 때문에 인스턴스 생성이 실패할 수 있다. 성공 여부는 권한 외에도 요청값과 현재 리소스 상태에 따라 결정된다.

## 6. `Allow`만 있고 `Deny`가 없다는 뜻

이 정책은 조건에 맞는 요청을 허용하는 규칙이다. 여기에 없는 작업은 **이 정책이 허용하지 않는 것**이며, 계정 전체에 그 작업을 명시적으로 금지하는 규칙은 아니다.

예를 들어 다른 정책에서 도쿄 EC2 생성 권한을 추가로 허용하면 현재 JSON의 서울 조건만으로 그것을 막을 수 없다. 같은 사용자에게 `AdministratorAccess`를 추가하면 이 작은 정책이 상한선 역할을 하지도 않는다.

반대로 다른 적용 정책에 명시적 `Deny`가 있으면 이 정책의 `Allow`보다 우선한다. 권한 경계나 조직 정책도 최종 권한을 더 제한할 수 있다. [AWS 정책 평가 방식](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).

## 7. 과제 지침과 JSON이 실제 강제하는 범위

| 과제에서 지킬 내용 | 현재 JSON에서 자동으로 강제하는가? |
|---|---|
| 서울 리전 사용 | 이 Allow 규칙에는 서울 요청 조건이 있음. 다른 정책의 허용까지 막는 것은 아님 |
| `t3.micro` 1대만 사용 | 아니오. 인스턴스 유형과 수량 제한 조건이 없음 |
| EBS 8~10GiB 사용 | 아니오. 볼륨 크기 제한 조건이 없음 |
| `B3-1` 실습 리소스만 수정·삭제 | 아니오. Resource가 `*`이고 프로젝트 태그 조건이 없음 |
| SSH 22번은 내 IP에서만 허용 | 아니오. 실제 Security Group에서 설정해야 함 |
| 전체 포트를 인터넷에 개방하지 않기 | 아니오. 현재 JSON은 보안 그룹 규칙의 포트 범위를 제한하지 않음 |
| MFA로 로그인 | 이 JSON에는 MFA 조건이 없음. 앞서 IAM 사용자에 MFA를 등록하는 절차로 구성함 |
| 실습 종료 후 리소스 삭제 | 삭제 권한은 제공하지만 자동 삭제를 실행하지 않음 |
| 무료 티어급 규모와 비용 관리 | 이 JSON에는 요금·예산 제한이나 자동 종료 설정이 없음 |

따라서 현재 정책은 **EC2 실습에 필요한 작업과 요청 리전을 중심으로 줄인 시작 정책**이다. 특정 프로젝트 리소스와 실행 조건까지 모두 제한한 최종 최소 권한 정책이라고 보기는 어렵다. 위 표는 현재 JSON에 있는 필드와 없는 조건을 대조한 해석이다.

## 8. IAM 권한과 서버 접속 권한 구분

| 계층 | 이번 실습에서 하는 일 |
|---|---|
| IAM 정책 | `b3-1-lab`이 AWS에서 EC2·VPC를 생성하거나 보안 그룹을 수정할 수 있는지 결정 |
| Security Group | 외부에서 EC2의 22·80·443번 포트로 들어오는 통신을 허용할지 결정 |
| EC2 내부 Linux 계정과 SSH 키 | SSH로 들어온 사용자가 `ubuntu`로 인증하고 서버 안에서 작업하도록 구성 |

예를 들어 `AuthorizeSecurityGroupIngress`는 IAM 사용자에게 **80번 포트를 여는 설정 작업을 할 권한**을 준다. 실제로 80번을 여는 규칙을 추가해야 외부 HTTP 통신이 허용되고, EC2 안의 웹 서버도 실행 중이어야 응답한다.

`sudo apt install nginx`, `docker run`, `curl http://localhost`는 이 IAM JSON에 적는 Action이 아니다. SSH로 EC2에 접속한 후 서버 안에서 실행하는 명령이다.

## 9. 읽은 뒤 확인할 것

- `Version`은 오늘 날짜로 바꾸지 않는다.
- `Sid`와 콘솔의 정책 이름을 구분한다.
- `Action`은 실행 순서가 아니라 허용 작업 목록이다.
- `Resource: "*"`와 `Describe*`에서 별표가 각각 무엇을 넓히는지 구분한다.
- 이 정책을 만들어도 IAM 사용자에 연결하기 전에는 그 사용자의 권한으로 적용되지 않는다.
- JSON 문법 검사가 성공해도 실제 계정에서 모든 작업이 성공한다는 뜻은 아니다. 실습 중 필요한 작업의 권한과 결과를 확인한다.

원본 정책의 36개 Action 항목과 설명 목록을 대조했다. 설명 및 공식 문서 확인일: 2026-09-08.
