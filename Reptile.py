
import re   #正则表达式
from bs4 import BeautifulSoup   #解析网页，获取数据
import urllib.request,urllib.error  #制定URL，获取网页数据
import xlwt #进行excel操作
import sqlite3  #进行SQLite数据库操作

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1. 爬取网页
    datalist = getData(baseurl)
    #2. 解析数据
    savepath = ".\\豆瓣电影Top250.xls"
    #3. 保存数据
    saveData(datalist,savepath)
    #askURL(baseurl)

findLink = re.compile(r'<a href="(.*?)">') #创建正则表达式对象，表示规则(字符串的模式)
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)
findName = re.compile(r'<span class="title">(.*?)</span>')
findScore = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findPerson = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10): #调用获取页面信息的函数
        url = baseurl+str(i*25)
        html = askURL(url) #保存获取到的网页源码
        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"): #查找复合要求的字符串，形成数表
            data = [] #保存一部电影的所有信息
            item = str(item)

            #影片详情的链接
            link = re.findall(findLink,item)[0] #re库用正则表达式查找指定的字符串
            data.append(link)

            #影片的缩略图
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            #影片的名字
            titles = re.findall(findName,item)
            if(len(titles)==2) :
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)
            else :
                data.append(titles[0])
                data.append('')     #其它名留空

            # 影片的评分
            rating = re.findall(findScore,item)[0]
            data.append(rating)

            # 影片的评分人数
            judgeNum = re.findall(findPerson,item)[0]
            data.append(judgeNum)

            # 影片的简介
            inq = re.findall(findInq,item)
            if len(inq)!=0:
                inq = inq[0].replace(".","")
                data.append(inq)
            else:
                data.append(" ")

            # 影片的主演
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd) #去掉<br/>
            bd = re.sub('/'," ",bd)
            data.append(bd)

            datalist.append(data)   #处理好的一部电影放到datalist

    return datalist

#得到一个指定URL网页的内容
def askURL(url):
    head = {
     "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    }

    #用户代理 表示告诉服务器，我们是什么类型的机器，浏览器（我们能接受什么类型的数据）
    request = urllib.request.Request(url,headers=head)
    html =""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

#保存数据到office
def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True) #创建工作表
    col = ("电影链接","图片链接","影片中文名","影片其它名","评分","评分人数","简介","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  #数据
    book.save('豆瓣电影Top250.xls')

if __name__ == '__main__':
    main()