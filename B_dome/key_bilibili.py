import requests
import re
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud

def get_bilbil(url):
    # 数据
    plays = [] # 播放量
    Bvids = [] # 视频Bvid
    sort_Bvids = [] # 排序过后的视频Bvid
    sort_likes = [] # 排序过后的视频点赞量
    sort_Coins = [] # 排序过后的视频投币量
    sort_collection = [] # 排序过后的视频收藏量
    data_Bvids = {}
    data_likes = {}
    data_Coins = {}
    data_collection = {}

    bvid_url = 'https://www.bilibili.com/video/'

    # UA伪装
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
        
    } 

    print('请求到bilbil....')
    #请求到bilbil
    bilbil_text = requests.get(url=url,headers=header).text
    Video_Num = re.findall('bvid:".*?"',bilbil_text) # 用正则匹配获取Bvid
    for i in Video_Num:
        Bvids.append(i[6:-1])

    print('正在获取数据....')
    for B in range(len(Bvids)):
        bvid_text = requests.get(url=(bvid_url + Bvids[B]),headers=header).text
        Play_num = re.findall('title="总播放数.*?"',bvid_text)[0] # 用正则匹配获取播放量
        Likes_num = re.findall('"info-text">.*?<',bvid_text)[0] # 用正则匹配获取点赞量
        Coins_num = re.findall('"info-text">.*?<',bvid_text)[1] # 用正则匹配获取投币量
        collection_num = re.findall('"info-text">.*?<',bvid_text)[2] # 用正则匹配获取收藏量
        
        # 数据处理 
        lst_Play = Play_num[11:-1]
        islike = Likes_num[12:-1]
        isCoins = Coins_num[12:-1]
        iscollection =collection_num[12:-1]
        
        # 单位划分
        if(islike[-1] == '万'):
           islike = str(float(islike[:-1]) * 10000)
        if(isCoins[-1] == '万'):
            isCoins = str(float(isCoins[:-1]) * 10000)
        if(isCoins[-2:] == '投币'):
            isCoins = '0'
        if(iscollection[-1] == '万'):
            iscollection = str(float(iscollection[:-1]) * 10000)
        
        # 数据存储
        plays.append(int(lst_Play))
        data_Bvids[int(lst_Play)] = Bvids[B] # 把播放量做为key存入字典
        data_likes[int(lst_Play)] = islike # 把播放量做为key存入字典
        data_Coins[int(lst_Play)] = isCoins # 把播放量做为key存入字典
        data_collection[int(lst_Play)] = iscollection # 把播放量做为key存入字典

    print('正在对数据进行排序....')
    # 对字典key和plays排序排序
    plays.sort(reverse = True)
    for T_0 in sorted(data_Bvids,reverse = True):
        sort_Bvids.append(data_Bvids[T_0])
    for T_1 in sorted(data_likes,reverse = True):
        sort_likes.append(data_likes[T_1])
    for T_2 in sorted(data_Coins,reverse = True):
        sort_Coins.append(data_Coins[T_2])
    for T_3 in sorted(data_collection,reverse = True):
        sort_collection.append(data_collection[T_3])


    with open('./data_bilibili.txt','w',encoding='utf-8') as fp:
        for num in range(len(sort_Bvids)):   # 储存
            fp.write(bvid_url + sort_Bvids[num] + " " + str(plays[num]) + " " + sort_likes[num] + " " + sort_Coins[num] + " " + sort_collection[num] + "\n")
            
        fp.close()
    print('写入文件成功....')

    Analyze_data(sort_Bvids) #柱状图
    Get_comments(sort_Bvids,header) # 词云

def Get_comments(sort_Bvids,headers):
    num = 10
    page = 1
    data_comments = []
    # 获取番剧评论
    print('获取番剧评论....')
    for i in range(num):
        #评论url
        url_comments = f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={page}&type=1&oid={sort_Bvids[i]}&mode=3'
        comments_text = requests.get(url=url_comments,headers=headers).text
        # 正则定位
        comments = re.findall('"message":".*?"',comments_text) #获取所有评论
        #评论数据处理
        for s in range(1,len(comments)):
            data_comments.append(comments[s])

    #数据存储
    with open('./data_comment.txt','w',encoding='utf-8') as fp:   # 储存
        [fp.write(str(itme)+'\n') for itme in data_comments] #换行
        fp.close()
    print('写入文件成功....')

    Analyze_data_words() #词云可视化

def Analyze_data(sort_name):
    #'生成信息'
    num = 10
    sort_Play = [] #排序的播放量
    sort_like = [] #排序的点赞量
    sort_Coins = [] #排序的投币量
    
    # 打开文件
    fp = open('./data_bilibili.txt','r',encoding='UTF-8').readlines()
    for i in fp:
        i = i.strip("\n")  # 去除掉换行符
        i = i.split(" ")  # 用空格分隔
        sort_Play.append(int(i[1])) # 播放量
        sort_like.append(float(i[2])) # 点赞量
        sort_Coins.append(float(i[3])) # 投币量
          
    print('正在生成数据....')
    # 数据分析
    plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
    plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
    plt.figure(figsize=(15,7)) #界面大小
    plt.tick_params(labelsize=8) #字体大小

    # 显示
    for i in range(num):
        x_data = ["第{}名\nBvid:{}".format(i+1,sort_name[i])]
        p1 = plt.bar(x_data,round(sort_Play[i]/10000,2),label=sort_name[i],color='lightpink')
        plt.bar(x_data,round(sort_like[i]/1000,2),color='lightsteelblue')
        plt.bar(x_data,round(sort_Coins[i]/1000,2),color='thistle')
        plt.bar_label(p1, label_type='edge')
    plt.legend(('播放量(万)','点赞数(千)','投币数(千)'))
    plt.title("排名播放量分析")
    plt.xlabel("排名")
    plt.show()

def Analyze_data_words():
    #打开文件
    fp = open('./data_comment.txt','r',encoding='UTF-8').read()
    #去除不需要的字符，只保留中文 re.S 字符串作为一个整体,如果不使用re.S参数，则只在每一行内进行匹配
    new_data = re.findall('[\u4e00-\u9fa5]+', fp, re.S) #至少匹配一个汉字
    new_data = " ".join(new_data)
    # jieba分词
    cut_text = " ".join(jieba.cut(new_data))
    #设置字体
    font = "C:/Windows/Fonts/simfang.ttf"
    #排除不显示的词
    die_words ={
        "我","的","他","回复","你","了","啊","也","是","都"
    }
    # background_color 图片背景颜色  max_words 显示的最大单词数量    
    wordcloud = WordCloud(font_path=font,background_color="white",width=1000,height=900,max_words=300,stopwords=die_words).generate(cut_text)
    #输出图片
    wordcloud.to_file("comment_bilbil.png")

