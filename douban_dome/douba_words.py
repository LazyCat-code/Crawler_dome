import requests
from bs4 import BeautifulSoup
import json
import re
import jieba
from wordcloud import WordCloud

def Get_douban_json(start_num,limit_num,type_name,shortcomments_max):
    short_comments_data = []
    short_names_data = []
    score_data = []
    Movie_data = []
    regions_data = []
    release_date = []
    counts_data = []
    url_data = []

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
    }
    types = {
        "剧情":11,"喜剧":24,"动作":5,"爱情":13,"科幻":17,"动画":25,
        "悬疑":10,"惊悚":19,"恐怖":20,"纪录片":1,"短片":23,"情色":6,
        "音乐":14,"歌舞":7,"家庭":28,"儿童":8,"传记":2,"历史":4,
        "战争":22,"犯罪":3,"西部":27,"奇幻":16,"冒险":15,"灾难":12,
        "武侠":29,"古装":30,"运动":18,"黑色电影":31
    }
    url = f'https://movie.douban.com/j/chart/top_list?type={types[type_name]}&interval_id=100%3A90&action=&start={start_num}&limit={limit_num}'

    # 类型排行榜json数据
    response_data = requests.get(url, headers=headers).json()
    # 写入json数据
    # with open("./douban.json", "w",encoding='utf-8') as fp:
    #     json.dump(response_data, fp,indent=4,ensure_ascii=False)

    # 获取评论数据
    for i in range(len(response_data)):
        self_url = response_data[i]["url"] + f'comments?limit={shortcomments_max}&status=P&sort=new_score'
        self_movie_data = requests.get(self_url, headers=headers).text
        soup = BeautifulSoup(self_movie_data,'html.parser')
        # 短评,评论
        short_comments = soup.find_all('span',class_='short')

        for j in short_comments:
            short_comments_data.append(j.text)

    # josn 里的数据        
    for j in range(limit_num):
        name = response_data[j]["title"]
        score = response_data[j]["score"]
        Movie_type = response_data[j]["types"]
        regions = response_data[j]["regions"]
        release = response_data[j]["release_date"]
        counts = response_data[j]["vote_count"]
        name_url = response_data[j]["url"]

        short_names_data.append(name)
        score_data.append(score)
        Movie_data.append(Movie_type)
        regions_data.append(regions)
        release_date.append(release)
        counts_data.append(str(counts))
        url_data.append(name_url)

    with open("./douban_data.txt", "w",encoding='utf-8') as fp:
        for f in range(limit_num):
            fp.write("电影名: " + short_names_data[f] + " 评分: " + score_data[f] + " 类型: " + (",".join(Movie_data[f])) + 
                     " 地区: " + (",".join(regions_data[f])) + " 日期: " + release_date[f] + " 评论人数: " + counts_data[f] + 
                     "\n" + "链接: "+ url_data[f] + "\n")
        fp.close()

    with open("./short_comments_data.txt", "w",encoding='utf-8') as fp:
        for s in short_comments_data:
            fp.write(s+'\n') 
        fp.close()

def Analyze_data_words():
    #打开文件
    fp = open('./short_comments_data.txt','r',encoding='utf-8').read()
    #去除不需要的字符，只保留中文 re.S 字符串作为一个整体,如果不使用re.S参数，则只在每一行内进行匹配
    new_data = re.findall('[\u4e00-\u9fa5]+', fp, re.S) #至少匹配一个汉字
    new_data = " ".join(new_data)
    # jieba分词
    cut_text = " ".join(jieba.cut(new_data))
    #设置字体
    font = "C:/Windows/Fonts/simfang.ttf"
    #排除不显示的词
    die_words ={
        "我","的","他","回复","你","了","啊","也","是","都","电影","这","在"
    }
    # background_color 图片背景颜色  max_words 显示的最大单词数量    
    wordcloud = WordCloud(font_path=font,background_color="white",width=1000,height=900,max_words=300,stopwords=die_words).generate(cut_text)
    #输出图片
    wordcloud.to_file("short_comments_data.png")



if __name__=="__main__":
    # 初始配置
    start_num = 0  # 从第几部电影开始
    limit_num = 10 # 第几部电影结束
    type_name = "动作" # 电影类型
    comments_max = 50 # 每部电影获取的评论
    Get_douban_json(start_num,limit_num,type_name,comments_max)
    Analyze_data_words()