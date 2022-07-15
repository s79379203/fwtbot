cd D:/fwtbot

git init

heroku git:remote -a bot20220715

git add .

git commit -am "update custorders"

git push heroku main
