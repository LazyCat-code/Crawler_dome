import key_bilibili
# 柱状图加词云
if __name__ == '__main__':
    # 初始数据配置
    page = 1 #页码
    userSeach = '原神' #搜索的关键字
    url = f'https://search.bilibili.com/video?keyword={userSeach}&page={page}' #请求的url
    key_bilibili.get_bilbil(url) #调用函数