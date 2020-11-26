from bs4 import BeautifulSoup
import urllib.parse, urllib.request, urllib.response, urllib.error
import re
import xlwt

findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findGame = re.compile(r'此日无比赛数据')
findTeam = re.compile(r'[\u4e00-\u9fa5]{1,3}')
findHostPoint = re.compile(r'(\d+\.?\d*)-')
findHomePoint = re.compile(r'-(\d+\.?\d*)')
findTeamLink = re.compile(r'href=".(.*?)"')
row = 1
col = 0
workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)


def nba_crawler():
    url_1 = "http://www.stat-nba.com/teamList.php"
    html_1 = askURL(url_1)
    bs_1 = BeautifulSoup(html_1,"html.parser")
    t_list_1 = bs_1.find_all(class_= "team",target = "_blank")
    url_l = "http://www.stat-nba.com"
    for i in range(30):
        url_r = re.findall(findTeamLink,str(t_list_1[i]))[0]
        team_link = url_l+str(url_r)
        html_2 = askURL(team_link)
        bs_2 = BeautifulSoup(html_2, "html.parser")


def askURL(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    return html


def def_table():
    col = ("Game Data", "Home Team", "Host Team", "Home_point", "Host_point")
    for i in range(len(col)):
        worksheet.write(0, i, col[i])


nba_crawler()
def_table()
workbook.save('nab-game.xls')
