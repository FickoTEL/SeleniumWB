#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    时间：2018-1-23 13:00:41
    作者：Ficko
    版本：
    1.0 可以爬取页面的第二篇微博，并正确print
        1.1 get_content() 添加了initialize；忽略评论可以带图的功能；更新了原创和转发的判断方法
    2.0 可以识别是否有置顶，并自动选择爬取哪一篇
    3.0 ————————————————
    4.0 完善保存至本地文档
    5.0 增加持续监控的能力，察觉变化并保存
        5.1 将 driver 改为无头浏览器（Firefox内核），添加了定时状态打印功能
    6.0 可以部署在服务器上
        6.1 优化 爬取文件和 log文件 的存储
        6.2 记录出错信息，方便维护
        6.3 添加虚拟显示 virtual display，避免在服务器上出错
    7.0 改成了PhantomJS
        7.1 更改了配置文件 DesiredCapabilities 的参数
        7.2 添加了没卵用的请求头
        7.3 更改了请求失败后的执行方式
"""
import random
import os
import traceback
import sys
import io
from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# 开门大吉，预防编码错误「UnicodeEncodeError: 'ascii' codec can't encode characters」
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Variations.
# 引用需要声明全局变量。
# ___ER___ https://weibo.cn/508637358
second_domain = '508637358'
weibo_name = '___ER___'

# 伪装的请求头
user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    时间：2018-1-23 13:00:41
    作者：Ficko
    版本：
    1.0 可以爬取页面的第二篇微博，并正确print
        1.1 get_content() 添加了initialize；忽略评论可以带图的功能；更新了原创和转发的判断方法
    2.0 可以识别是否有置顶，并自动选择爬取哪一篇
    3.0 ————————————————
    4.0 完善保存至本地文档
    5.0 增加持续监控的能力，察觉变化并保存
        5.1 将 driver 改为无头浏览器（Firefox内核），添加了定时状态打印功能
    6.0 可以部署在服务器上
        6.1 优化 爬取文件和 log文件 的存储
        6.2 记录出错信息，方便维护
        6.3 添加虚拟显示 virtual display，避免在服务器上出错
    7.0 改成了PhantomJS
        7.1 更改了配置文件 DesiredCapabilities 的参数
        7.2 添加了没卵用的请求头
        7.3 更改了请求失败后的执行方式
"""
import random
import os
import traceback
from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Variations.
# 引用需要声明全局变量。
# ___ER___ https://weibo.cn/508637358
second_domain = '508637358'
weibo_name = '___ER___'

# 伪装的请求头
user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

def save_to_log(info):
    # 将 info 保存到日志文件中
    is_weibosave()
    m = open('weibosave/weiboPY_running_log_{}.txt'.format(format_weibo_py_running_log_time()), 'a', encoding='utf-8')
    m.write(info)
    m.close()


def is_weibosave():
    # 判断是否存在文件夹 weibosave，没有就创建一个
    if os.path.exists('weibosave'):
        pass
    else:
        os.mkdir('weibosave')


def format_time_now():
    ct = datetime.now()
    time_now = '{}/{}/{}_{}:{}:{}'.format(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)
    return time_now


def format_weibo_save_time():
    ct = datetime.now()
    date_now = '{}_{}_{}'.format(ct.year, ct.month, ct.day)
    return date_now


def format_weibo_py_running_log_time():
    ct = datetime.now()
    hour_now = '{}_{}_{}@{}00'.format(ct.year, ct.month, ct.day, ct.strftime("%H"))
    return hour_now


def get_content():
    global driver
    """
        有2种类型：
        一种是原创，一种是转发
        原创只有一个 div 标签，转发有两个 div 标签
    """

    # 判断原创还是转发
    """
        开始使用的方法是：判断 div 元素的个数，一个是原创，多个是转发；
        但如果原创发了图，会被误认为是转发，然后报错。
        因此转为查找「转发了」字眼来进行判断。
    """
    head_text = driver.find_element_by_id("M_").find_element_by_xpath("div/span[1]").text.strip()[:3]
    if head_text != '转发了':
        content = driver.find_element_by_class_name("ctt").text
        content_time = driver.find_element_by_class_name("ct").text
    else:
        orig_poster = driver.find_element_by_id("M_").find_element_by_xpath("div[1]/span[1]/a").text
        orig_content = driver.find_element_by_id("M_").find_element_by_xpath("div[1]/span[2]").text
        repo = ''.join(driver.find_element_by_id("M_").find_element_by_xpath("div[last()]").text.split('  ')[:-2])
        '''
            这里的repo编写思路：由于微博奇葩的格式，导致直接 find_element 会在后面有两个后缀：「x月x日」和「关注他」；
            由于后缀之间有两个空格，因此用两个空格分割字符，然后将末尾两个抛去；
            list --> str 的方法：'<list元素衔接字符>'.join(list)。这里默认为空。
            ============
            忽略转发的图片，使用 last() 直接选取最后的转发内容，忽略中间的 div 元素
        '''
        content = '@{}：{}\r\n{}：{}'.format(weibo_name, repo, orig_poster, orig_content)
        content_time = driver.find_element_by_id("M_").find_element_by_xpath("div[last()]/span[2]").text

    local_time = format_time_now()

    # 返回三个值：本机抓取时间，发布时间，内容
    return local_time, content_time, content


def is_element_exist_by_xpath(xpath):
    """
        利用 XPath 确定元素是否存在
    """
    is_exist = False
    s = driver.find_elements_by_xpath(xpath)
    if len(s) > 0:
        is_exist = True

    return is_exist


def is_stick():
    s = False
    """
        得到主页后，判断是否存在置顶微博。如果存在，返回 True，否则 False
    """
    if is_element_exist_by_xpath("//span[text()='置顶']"):
        s = True

    return s


def getlatestposturl():
    global driver
    """
        收藏的网址示例：http://weibo.cn/fav/addFav/FEX5UojD7?rl=0&st=b53681
        先用「/」分割，然后取最后一位，再取前9位
    """
    # 根据是否有置顶微博，选择抓取的 list 的位置
    if is_stick():
        n = 1
    else:
        n = 0

    add_fav_url = driver.find_elements_by_xpath("//div[starts-with(@id, 'M_')]")[n].find_element_by_link_text(
        "收藏").get_attribute('href')
    postid = add_fav_url.split('/')[-1][:9]
    full_post_url = 'https://weibo.cn/comment/' + postid
    return full_post_url, postid


def loginsina():
    global driver
    # 对应的是「登陆」
    print('LoginSina，正在登陆中……')
    username = ''
    password = ''

    sleep(3)
    driver.find_element_by_id("loginName").click()
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").click()
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    log = '登陆成功！当前时间：{}。'.format(format_time_now())
    print(log)
    is_weibosave()
    save_to_log(log)
    sleep(3)
    """
        输入文本框如果带有placeholder属性，则使用 .clear() 功能会报错：
        「Element is not currently interactable and may not be manipulated」
        解决方法：直接略过Clear方法。
    """


def welcomesina():
    global driver
    # 对应的是「欢迎登陆」
    print('WelcomeSina，正在登陆中……')
    driver.find_element_by_xpath("/html/body/div/div/a[2]").click()
    sleep(4)

    username = ''
    password = ''

    sleep(3)
    driver.find_element_by_id("loginName").click()
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").click()
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    log = '登陆成功！当前时间：{}。'.format(format_time_now())
    print(log)
    is_weibosave()
    save_to_log(log)
    sleep(3)


def get_target_weibo():
    driver.get('https://weibo.cn/{}'.format(second_domain))

def boot_driver():
    global driver
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(user_agent_list))
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False

    driver = webdriver.PhantomJS()


if __name__ == '__main__':
    global driver
    # 获取微博主页内容。
    boot_driver()
    # 增加出错信息的打印
    try:
        get_target_weibo()
    except Exception:
        exc_info = traceback.format_exc()
        print(exc_info, format_time_now())
        save_to_log('\r\n'.join([exc_info, format_time_now()]))

    # 隐式等待时间
    driver.implicitly_wait(10)

    old_id = '0'        # 初始化
    i = 0
    j = 0
    while True:
        driver.get('https://weibo.cn/{}'.format(second_domain))

        # 获取标题，判断页面状态
        title = driver.title
        if title == '{}的微博'.format(weibo_name):
            pass
        elif title == '登录 - 新浪微博':
            loginsina()
            driver.get('https://weibo.cn/{}'.format(second_domain))
        elif title == '欢迎登录 - 新浪微博':
            welcomesina()
            driver.get('https://weibo.cn/{}'.format(second_domain))
        else:
            print('无法连接！等待 60s 后继续……\r\n')
            sleep(60)
            continue

        # ==========以下是子页面==========
        # 获得最近微博的全文页面
        post_id = getlatestposturl()[1]
        if post_id == old_id:
            j += 1
            if j % 10 == 0:
                # 防止信息泛滥，每 10 条通报一次
                is_weibosave()
                log = '正在监控，已动态监测{}次，已捕捉到{}条动态。当前时间：{}。\r\n'.format(j, i, format_time_now())
                print(log)
                save_to_log(log)

            sleep(10)
            continue
        else:
            driver.get(getlatestposturl()[0])
            # 获取页面内容
            post_info = get_content()
            post_content = '抓取时间：{}\r\n微博时间：{}\r\n{}\r\n\r\n\r\n'.format(post_info[0], post_info[1], post_info[2][1:])

            # 更新 old_id 值
            old_id = post_id

            # 写入文件（合并保存）
            is_weibosave()
            f = open('weibosave/weibo_save_{}.txt'.format(format_weibo_save_time()), 'a', encoding='utf-8')
            f.write(post_content)
            f.close()

            # 输出状态
            i += 1
            capture = '捕捉到{}条动态。抓取时间：{}。\r\n'.format(i, format_time_now())
            print(capture)
            save_to_log(capture)

    driver.quit()

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

def save_to_log(info):
    # 将 info 保存到日志文件中
    is_weibosave()
    m = open('weibosave/weiboPY_running_log_{}.txt'.format(format_weibo_py_running_log_time()), 'a', encoding='utf-8')
    m.write(info)
    m.close()


def is_weibosave():
    # 判断是否存在文件夹 weibosave，没有就创建一个
    if os.path.exists('weibosave'):
        pass
    else:
        os.mkdir('weibosave')


def format_time_now():
    ct = datetime.now()
    time_now = '{}/{}/{}_{}:{}:{}'.format(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)
    return time_now


def format_weibo_save_time():
    ct = datetime.now()
    date_now = '{}_{}_{}'.format(ct.year, ct.month, ct.day)
    return date_now


def format_weibo_py_running_log_time():
    ct = datetime.now()
    hour_now = '{}_{}_{}@{}00'.format(ct.year, ct.month, ct.day, ct.hour)
    return hour_now


def get_content():
    global driver
    """
        有2种类型：
        一种是原创，一种是转发
        原创只有一个 div 标签，转发有两个 div 标签
    """

    # 判断原创还是转发
    """
        开始使用的方法是：判断 div 元素的个数，一个是原创，多个是转发；
        但如果原创发了图，会被误认为是转发，然后报错。
        因此转为查找「转发了」字眼来进行判断。
    """
    head_text = driver.find_element_by_id("M_").find_element_by_xpath("div/span[1]").text.strip()[:3]
    if head_text != '转发了':
        content = driver.find_element_by_class_name("ctt").text
        content_time = driver.find_element_by_class_name("ct").text
    else:
        orig_poster = driver.find_element_by_id("M_").find_element_by_xpath("div[1]/span[1]/a").text
        orig_content = driver.find_element_by_id("M_").find_element_by_xpath("div[1]/span[2]").text
        repo = ''.join(driver.find_element_by_id("M_").find_element_by_xpath("div[last()]").text.split('  ')[:-2])
        '''
            这里的repo编写思路：由于微博奇葩的格式，导致直接 find_element 会在后面有两个后缀：「x月x日」和「关注他」；
            由于后缀之间有两个空格，因此用两个空格分割字符，然后将末尾两个抛去；
            list --> str 的方法：'<list元素衔接字符>'.join(list)。这里默认为空。
            ============
            忽略转发的图片，使用 last() 直接选取最后的转发内容，忽略中间的 div 元素
        '''
        content = '@{}：{}\r\n{}：{}'.format(weibo_name, repo, orig_poster, orig_content)
        content_time = driver.find_element_by_id("M_").find_element_by_xpath("div[last()]/span[2]").text

    local_time = format_time_now()

    # 返回三个值：本机抓取时间，发布时间，内容
    return local_time, content_time, content


def is_element_exist_by_xpath(xpath):
    """
        利用 XPath 确定元素是否存在
    """
    is_exist = False
    s = driver.find_elements_by_xpath(xpath)
    if len(s) > 0:
        is_exist = True

    return is_exist


def is_stick():
    s = False
    """
        得到主页后，判断是否存在置顶微博。如果存在，返回 True，否则 False
    """
    if is_element_exist_by_xpath("//span[text()='置顶']"):
        s = True

    return s


def getlatestposturl():
    global driver
    """
        收藏的网址示例：http://weibo.cn/fav/addFav/FEX5UojD7?rl=0&st=b53681
        先用「/」分割，然后取最后一位，再取前9位
    """
    # 根据是否有置顶微博，选择抓取的 list 的位置
    if is_stick():
        n = 1
    else:
        n = 0

    add_fav_url = driver.find_elements_by_xpath("//div[starts-with(@id, 'M_')]")[n].find_element_by_link_text(
        "收藏").get_attribute('href')
    postid = add_fav_url.split('/')[-1][:9]
    full_post_url = 'https://weibo.cn/comment/' + postid
    return full_post_url, postid


def loginsina():
    global driver
    # 对应的是「登陆」
    print('LoginSina，正在登陆中……')
    username = ''
    password = ''

    sleep(3)
    driver.find_element_by_id("loginName").click()
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").click()
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    log = '登陆成功！当前时间：{}。'.format(format_time_now())
    print(log)
    is_weibosave()
    save_to_log(log)
    sleep(3)
    """
        输入文本框如果带有placeholder属性，则使用 .clear() 功能会报错：
        「Element is not currently interactable and may not be manipulated」
        解决方法：直接略过Clear方法。
    """


def welcomesina():
    global driver
    # 对应的是「欢迎登陆」
    print('WelcomeSina，正在登陆中……')
    driver.find_element_by_xpath("/html/body/div/div/a[2]").click()
    sleep(4)

    username = ''
    password = ''

    sleep(3)
    driver.find_element_by_id("loginName").click()
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").click()
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    log = '登陆成功！当前时间：{}。'.format(format_time_now())
    print(log)
    is_weibosave()
    save_to_log(log)
    sleep(3)


def get_target_weibo():
    driver.get('https://weibo.cn/{}'.format(second_domain))

def boot_driver():
    global driver
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(user_agent_list))
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False

    driver = webdriver.PhantomJS()#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    时间：2018-1-23 13:00:41
    作者：Ficko
    版本：
    1.0 可以爬取页面的第二篇微博，并正确print
        1.1 get_content() 添加了initialize；忽略评论可以带图的功能；更新了原创和转发的判断方法
    2.0 可以识别是否有置顶，并自动选择爬取哪一篇
    3.0 ————————————————
    4.0 完善保存至本地文档
    5.0 增加持续监控的能力，察觉变化并保存
        5.1 将 driver 改为无头浏览器（Firefox内核），添加了定时状态打印功能
    6.0 可以部署在服务器上
        6.1 优化 爬取文件和 log文件 的存储
        6.2 记录出错信息，方便维护
        6.3 添加虚拟显示 virtual display，避免在服务器上出错
    7.0 改成了PhantomJS
        7.1 更改了配置文件 DesiredCapabilities 的参数
        7.2 添加了没卵用的请求头
        7.3 更改了请求失败后的执行方式
"""
import random
import os
import traceback
from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Variations.
# 引用需要声明全局变量。
# ___ER___ https://weibo.cn/508637358
second_domain = '508637358'
weibo_name = '___ER___'

# 伪装的请求头
user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

def save_to_log(info):
    # 将 info 保存到日志文件中
    is_weibosave()
    m = open('weibosave/weiboPY_running_log_{}.txt'.format(format_weibo_py_running_log_time()), 'a', encoding='utf-8')
    m.write(info)
    m.close()


def is_weibosave():
    # 判断是否存在文件夹 weibosave，没有就创建一个
    if os.path.exists('weibosave'):
        pass
    else:
        os.mkdir('weibosave')


def format_time_now():
    ct = datetime.now()
    time_now = '{}/{}/{}_{}:{}:{}'.format(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)
    return time_now


def format_weibo_save_time():
    ct = datetime.now()
    date_now = '{}_{}_{}'.format(ct.year, ct.month, ct.day)
    return date_now


def format_weibo_py_running_log_time():
    ct = datetime.now()
    hour_now = '{}_{}_{}@{}00'.format(ct.year, ct.month, ct.day, ct.strftime("%H"))
    return hour_now


def get_content():
    global driver
    """
        有2种类型：
        一种是原创，一种是转发
        原创只有一个 div 标签，转发有两个 div 标签
    """

    # 判断原创还是转发
    """
        开始使用的方法是：判断 div 元素的个数，一个是原创，多个是转发；
        但如果原创发了图，会被误认为是转发，然后报错。
        因此转为查找「转发了」字眼来进行判断。
    """
    head_text = driver.find_element_by_id("M_").find_element_by_xpath("div/span[1]").text.strip()[:3]
    if head_text != '转发了':
        content = driver.find_element_by_class_name("ctt").text
        content_time = driver.find_element_by_class_name("ct").text
    else:
        orig_poster = driver.find_element_by_id("M_").find_element_by_xpath("div[1]/span[1]/a").text
        orig_content = driver.find_element_by_id("M_").find_element_by_xpath("div[1]/span[2]").text
        repo = ''.join(driver.find_element_by_id("M_").find_element_by_xpath("div[last()]").text.split('  ')[:-2])
        '''
            这里的repo编写思路：由于微博奇葩的格式，导致直接 find_element 会在后面有两个后缀：「x月x日」和「关注他」；
            由于后缀之间有两个空格，因此用两个空格分割字符，然后将末尾两个抛去；
            list --> str 的方法：'<list元素衔接字符>'.join(list)。这里默认为空。
            ============
            忽略转发的图片，使用 last() 直接选取最后的转发内容，忽略中间的 div 元素
        '''
        content = '@{}：{}\r\n{}：{}'.format(weibo_name, repo, orig_poster, orig_content)
        content_time = driver.find_element_by_id("M_").find_element_by_xpath("div[last()]/span[2]").text

    local_time = format_time_now()

    # 返回三个值：本机抓取时间，发布时间，内容
    return local_time, content_time, content


def is_element_exist_by_xpath(xpath):
    """
        利用 XPath 确定元素是否存在
    """
    is_exist = False
    s = driver.find_elements_by_xpath(xpath)
    if len(s) > 0:
        is_exist = True

    return is_exist


def is_stick():
    s = False
    """
        得到主页后，判断是否存在置顶微博。如果存在，返回 True，否则 False
    """
    if is_element_exist_by_xpath("//span[text()='置顶']"):
        s = True

    return s


def getlatestposturl():
    global driver
    """
        收藏的网址示例：http://weibo.cn/fav/addFav/FEX5UojD7?rl=0&st=b53681
        先用「/」分割，然后取最后一位，再取前9位
    """
    # 根据是否有置顶微博，选择抓取的 list 的位置
    if is_stick():
        n = 1
    else:
        n = 0

    add_fav_url = driver.find_elements_by_xpath("//div[starts-with(@id, 'M_')]")[n].find_element_by_link_text(
        "收藏").get_attribute('href')
    postid = add_fav_url.split('/')[-1][:9]
    full_post_url = 'https://weibo.cn/comment/' + postid
    return full_post_url, postid


def loginsina():
    global driver
    # 对应的是「登陆」
    print('LoginSina，正在登陆中……')
    username = ''
    password = ''

    sleep(3)
    driver.find_element_by_id("loginName").click()
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").click()
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    log = '登陆成功！当前时间：{}。'.format(format_time_now())
    print(log)
    is_weibosave()
    save_to_log(log)
    sleep(3)
    """
        输入文本框如果带有placeholder属性，则使用 .clear() 功能会报错：
        「Element is not currently interactable and may not be manipulated」
        解决方法：直接略过Clear方法。
    """


def welcomesina():
    global driver
    # 对应的是「欢迎登陆」
    print('WelcomeSina，正在登陆中……')
    driver.find_element_by_xpath("/html/body/div/div/a[2]").click()
    sleep(4)

    username = ''
    password = ''

    sleep(3)
    driver.find_element_by_id("loginName").click()
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").click()
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    log = '登陆成功！当前时间：{}。'.format(format_time_now())
    print(log)
    is_weibosave()
    save_to_log(log)
    sleep(3)


def get_target_weibo():
    driver.get('https://weibo.cn/{}'.format(second_domain))

def boot_driver():
    global driver
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(user_agent_list))
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False

    driver = webdriver.PhantomJS()


if __name__ == '__main__':
    global driver
    # 获取微博主页内容。
    boot_driver()
    # 增加出错信息的打印
    try:
        get_target_weibo()
    except Exception:
        exc_info = traceback.format_exc()
        print(exc_info, format_time_now())
        save_to_log('\r\n'.join([exc_info, format_time_now()]))

    # 隐式等待时间
    driver.implicitly_wait(10)

    old_id = '0'        # 初始化
    i = 0
    j = 0
    while True:
        driver.get('https://weibo.cn/{}'.format(second_domain))

        # 获取标题，判断页面状态
        title = driver.title
        if title == '{}的微博'.format(weibo_name):
            pass
        elif title == '登录 - 新浪微博':
            loginsina()
            driver.get('https://weibo.cn/{}'.format(second_domain))
        elif title == '欢迎登录 - 新浪微博':
            welcomesina()
            driver.get('https://weibo.cn/{}'.format(second_domain))
        else:
            print('无法连接！等待 60s 后继续……\r\n')
            sleep(60)
            continue

        # ==========以下是子页面==========
        # 获得最近微博的全文页面
        post_id = getlatestposturl()[1]
        if post_id == old_id:
            j += 1
            if j % 10 == 0:
                # 防止信息泛滥，每 10 条通报一次
                is_weibosave()
                log = '正在监控，已动态监测{}次，已捕捉到{}条动态。当前时间：{}。\r\n'.format(j, i, format_time_now())
                print(log)
                save_to_log(log)

            sleep(10)
            continue
        else:
            driver.get(getlatestposturl()[0])
            # 获取页面内容
            post_info = get_content()
            post_content = '抓取时间：{}\r\n微博时间：{}\r\n{}\r\n\r\n\r\n'.format(post_info[0], post_info[1], post_info[2][1:])

            # 更新 old_id 值
            old_id = post_id

            # 写入文件（合并保存）
            is_weibosave()
            f = open('weibosave/weibo_save_{}.txt'.format(format_weibo_save_time()), 'a', encoding='utf-8')
            f.write(post_content)
            f.close()

            # 输出状态
            i += 1
            capture = '捕捉到{}条动态。抓取时间：{}。\r\n'.format(i, format_time_now())
            print(capture)
            save_to_log(capture)

    driver.quit()



if __name__ == '__main__':
    global driver
    # 获取微博主页内容。
    boot_driver()
    # 增加出错信息的打印
    try:
        get_target_weibo()
    except Exception:
        exc_info = traceback.format_exc()
        print(exc_info, format_time_now())
        save_to_log('\r\n'.join([exc_info, format_time_now()]))

    # 隐式等待时间
    driver.implicitly_wait(10)

    old_id = '0'        # 初始化
    i = 0
    j = 0
    while True:
        driver.get('https://weibo.cn/{}'.format(second_domain))

        # 获取标题，判断页面状态
        title = driver.title
        if title == '{}的微博'.format(weibo_name):
            pass
        elif title == '登录 - 新浪微博':
            loginsina()
            driver.get('https://weibo.cn/{}'.format(second_domain))
        elif title == '欢迎登录 - 新浪微博':
            welcomesina()
            driver.get('https://weibo.cn/{}'.format(second_domain))
        else:
            print('无法连接！等待 60s 后继续……\r\n')
            sleep(60)
            continue

        # ==========以下是子页面==========
        # 获得最近微博的全文页面
        post_id = getlatestposturl()[1]
        if post_id == old_id:
            j += 1
            if j % 10 == 0:
                # 防止信息泛滥，每 10 条通报一次
                is_weibosave()
                log = '正在监控，已动态监测{}次，已捕捉到{}条动态。当前时间：{}。\r\n'.format(j, i, format_time_now())
                print(log)
                save_to_log(log)

            sleep(10)
            continue
        else:
            driver.get(getlatestposturl()[0])
            # 获取页面内容
            post_info = get_content()
            post_content = '抓取时间：{}\r\n微博时间：{}\r\n{}\r\n\r\n\r\n'.format(post_info[0], post_info[1], post_info[2][1:])

            # 更新 old_id 值
            old_id = post_id

            # 写入文件（合并保存）
            is_weibosave()
            f = open('weibosave/weibo_save_{}.txt'.format(format_weibo_save_time()), 'a', encoding='utf-8')
            f.write(post_content)
            f.close()

            # 输出状态
            i += 1
            capture = '捕捉到{}条动态。抓取时间：{}。\r\n'.format(i, format_time_now())
            print(capture)
            save_to_log(capture)

    driver.quit()
