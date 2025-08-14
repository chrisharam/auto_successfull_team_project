# auto_successfull_team_project
SW CAMP PROJECT

1. 새로운 브랜치 만들기

// git checkout -b 브랜치이름

2. 새로운 브랜치에서 작업 후 github에 올리기

// git add .
// git commit -m "message"

3. 새 브랜치를 main에 합치기

// git merge 브랜치이름

만약 충돌나면, git hub이 원인 알려줌 --> 해결 후 
git add . 
git commit -m "message"

4. 깃헙 사이트에 반영하기

git push origin main
혹은
***git push -u origin 새로만든 브랜치 이름***




+현재 브랜치 확인 
git branch
* 표시가 있는 곳이 현재 브랜치

+브랜치 옮기기
git checkout 브랜치이름


+++++ 로컬에서 팀원들 브랜치 보는 법 +++++
먼저 git fetch origin → git branch -r로 확인 → 필요하면 checkout -b로 로컬 브랜치 생성