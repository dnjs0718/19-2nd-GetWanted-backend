# 19-2nd-GetWanted-backend

# Project <GetWanted/>

## 🖥 Project Summary
- 2021.04.26 ~ 2021.05.07 까지 2주 간 진행
- 국내 구인구직 온라인 사이트인 원티드를 모티브로한 프로젝트
- Front(이예원, 정새미, 김도희)와 Back(원재연, 이병재, 정재유) 총 6명의 팀원으로 구성


## 👩🏻‍💻 Back-end Work Details

### 원재연(PM)
* 공고 리스트 구현
  - 검색 기능 구현 (회사 검색 가능, 공고명 검색가능, icontains를 활용한 단어검색 가능)
  - 좋아요 기능 구현 (공고에 해당하는 좋아요 수 집계, 데이터베이스 효율성을 높이기 위해 좋아요를 추가하고 삭제할 때 마다 create,delete가 아닌 is_liked column을 추가하여 효율적으로 데이터베이스 관리)
  - 태그를 통한 필터링 구현 (태그에 해당하는 공고 리스트 response)
  
* 공고 상세정보 구현
  - GOOGLE geocoder를 이용한 회사의 위도 및 경도 추출
  - 공고에 해당하는 상세설명, 태그, 이미지, 회사 위치 response
  
* 공고 지원하기
  - 유저에 해당하는 정보와 이력서 목록 불러오기
  - 유저가 해당 공고에 지원했는지 판별
  - 지원을 완료 했다면 유저 지원 목록에 추가
  
* AWS(EC2/RDS),Docker를 활용한 인프라 구축 및 배포

### 이병재
* 이력서 불러오기

* 작성한 이력서 저장하기

* 이력서 PDF 업로드

* 업로드 한 이력서 PDF 다운로드

* 작성 한 이력서 PDF 변환 후 다운로드

* 이력서 목록 불러오기

### 정재유
* 회원가입 및 로그인
  - bcrypt 암호화
  - JWT 액세스 토큰 발행
  - 소셜 로그인 구현(카카오,구글,네이버)
  - 초기화 된 비밀번호 이메일 전송 (비밀번호 찾기)

## 🔧 Skills
- ![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
- ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

## 🔧 Tools
- <img alt="Trello" src="https://img.shields.io/badge/Trello-%23026AA7.svg?&style=for-the-badge&logo=Trello&logoColor=white"/>
- <img alt="Git" src="https://img.shields.io/badge/git-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white"/>
- <img alt="GitHub" src="https://img.shields.io/badge/github-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white"/>
- <img alt="Slack" src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" />
- <img alt="AWS" src="https://img.shields.io/badge/AWS-%23FF9900.svg?&style=for-the-badge&logo=amazon-aws&logoColor=white"/>
- <img alt="Visual Studio Code" src="https://img.shields.io/badge/VisualStudioCode-0078d7.svg?&style=for-the-badge&logo=visual-studio-code&logoColor=white"/>
- <img alt="Vim" src="https://img.shields.io/badge/VIM-%2311AB00.svg?&style=for-the-badge&logo=vim&logoColor=white"/>
- <img alt="PyCharm" src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white"/>
## ✏️ Blogs
- 원재연 : https://velog.io/@dnjs0718
- 정재유 : https://velog.io/@deonii
- 이병재 : https://velog.io/@redlemon

## ✏️ References
- 이 프로젝트는 Wanted를 참고하여 학습용으로 작업 되었습니다.
- 이 프로젝트에서 사용된 모든 무료 이미지는 Unsplash에서 가져왔습니다.
