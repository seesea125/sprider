from bs4 import BeautifulSoup
import urllib.parse, urllib.request, urllib.response, urllib.error
import re
import xlwt


findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)
findGame = re.compile(r'此日无比赛数据')
findTeam = re.compile(r'[\u4e00-\u9fa5]{1,3}')
findHostPoint = re.compile(r'(\d+\.?\d*)-')
findHomePoint = re.compile(r'-(\d+\.?\d*)')
row = 1
col = 0
workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

def nba_crawler():
    url_l = "http://www.stat-nba.com/gameList_simple-2019-"
    url_r = ".html"

    for i in range(1,13):
        url_m = str(i)
        url = url_l+url_m+url_r
        html = askURL(url)
        bs = BeautifulSoup(html, "html.parser")
        t_list = bs.find_all(class_="cheight")
        for item in t_list:
            if item.get_text().isspace() or item.get_text() == 0:
                t_list.remove(item)
            elif len(findGame.findall(item.get_text())) != 0:
                t_list.remove(item)
            else:
                global row, col
                game_list = item.get_text().split('\n')
                for i in range(2,len(game_list)-1):
                    worksheet.write(row, col, game_list[1])
                    col = col+1
                    host_team = re.findall(findTeam,game_list[i])[0]
                    home_team = re.findall(findTeam,game_list[i])[1]
                    HostPoint = re.findall(findHostPoint, game_list[i])[0]
                    HomePoint = re.findall(findHomePoint, game_list[i])[0]
                    if host_team == "人" :
                        host_team = "76人"
                    if home_team == "人" :
                        home_team = "76人"
                    worksheet.write(row, col, home_team)
                    col = col+1
                    worksheet.write(row, col, host_team)
                    col = col+1
                    worksheet.write(row, col, (int)(HomePoint))
                    col = col + 1
                    worksheet.write(row, col, (int)(HostPoint))
                    row = row + 1
                    col = 0
def askURL(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    return html

def def_table():
    col = ("Game Data", "Home Team", "Host Team", "Home_point","Host_point")
    for i in range(len(col)):
        worksheet.write(0,i,col[i])


nba_crawler()
def_table()
workbook.save('nab-game.xls')

