#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import random
import os
import traceback
from time import sleep
from datetime import datetime
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from html.parser import HTMLParser
from urllib.parse import unquote




# Variations.

# 引用需要声明全局变量。
# ___ER___ https://weibo.com/508637358
second_domain = '508637358'
weibo_name = '___ER___'
target_URL_Homepage = "https://weibo.com/{}?loc=nickname&is_all=1".format(second_domain)

# 绝对路径，默认为空。如果在执行时出现了路径问题，可以修改此处的值。
# 【---------- 上传时注意修改这里的路径！----------】
# 这里在最后加斜杠的意义是：如果abs_path是空，那么路径的最开始就不应该有斜杠，所以就将斜杠转移到变量中
# abs_path = os.path.abspath('') + '/'
# abs_path = "/root/PycharmProjects/weiboCOM/"
abs_path = ""



class Myparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = ''    # 初始化内容

    def handle_starttag(self, tag, attrs):
        # 在def中又嵌套了一个def，用来判定是否存在某个属性，如果存在则输出属性值
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:  # 如果符合date-title，就return他的值：湄公河行动
                    return each[1]
            return None

        def is_attr_exist(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:  # 如果符合date-title，就返回True
                    return True
            return False

        for i in ['a', 'img']:      # 获取<a><img>标签里的 alt 属性值
            if tag == i and is_attr_exist(attrs, 'alt'):
                filte_result = _attr(attrs, 'alt')
                self.content += filte_result

    def handle_data(self, data):
        self.content += data


def drive_with_phantomjs():
    global driver
    service_args = [
        '--load-images=no',    # 禁止加载图片
    ]

    # 由于PhantomJS会被当成爬虫而被屏蔽，因此有必要对UA进行伪装
    # 将 DesiredCapabilities 转换为一个字典，方便添加键值对
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 添加一个浏览器标识的键值对
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19 "
    )

    driver = webdriver.PhantomJS(service_args=service_args, desired_capabilities=dcap)


def drive_with_chrome():
    '''
    drive_with_chrome 指的用Chrome进行代码的调试；
    '''
    global driver
    chrome_options = webdriver.ChromeOptions()

    # 【可选】给 chrome 添加启动参数（仅在Linux系统root账号中使用，因为 Chrome 在root下需要添加「--no-sandbox」才能正常启动）
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')  # 有无头的区别在这一行

    # 禁止加载图片，网页打开更快更省流量
    prefs = {
        'profile.default_content_setting_values' : {
            'images' : 2
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)

    # 定义 driver 作为 global 参数
    driver = webdriver.Chrome(chrome_options=chrome_options)

def format_time_now():
    time_now = datetime.now().strftime("%Y.%m.%d_%H:%M:%S")
    return time_now

def format_date_now():
    date_now = datetime.now().strftime("%Y_%m_%d")
    return date_now

def is_weibo_folder_exist():
    # 判断是否存在主文件夹，没有就创建
    if not os.path.exists('{}weibosave'.format(abs_path)):
        os.mkdir('{}weibosave'.format(abs_path))

def save_to_log(info):
    info_break = format_time_now() + ' ' + info + '\r\n'
    is_weibo_folder_exist()
    m = open('{}weibosave/running_log.txt'.format(abs_path), 'a', encoding='utf-8')
    m.write(info_break)
    m.close()
    print(info_break)  # 向屏幕输入信息

def save_to_log_without_timestamp(info):
    info_break = info + '\r\n'
    is_weibo_folder_exist()
    m = open('{}weibosave/running_log.txt'.format(abs_path), 'a', encoding='utf-8')
    m.write(info_break)
    m.close()
    print(info_break)  # 向屏幕输入信息

def save_weibo_to_file(post_content):
    is_weibo_folder_exist()
    f = open('weibosave/weibo_save_{}.txt'.format(format_date_now()), 'a', encoding='utf-8')
    f.write(post_content)
    f.close()

def save_issues_log_to_file(post_content):
    is_weibo_folder_exist()
    f = open('weibosave/Issue_Report_Page_Source_{}.txt'.format(format_time_now(), 'a', encoding='utf-8'))
    f.write(post_content)
    f.close()


def is_element_exist_by_xpath(driver_name, xpath):
    """
        利用 XPath 确定元素是否存在
    """
    is_exist = False
    s = driver_name.find_elements_by_xpath(xpath)
    if len(s) > 0:
        is_exist = True

    return is_exist



def is_stick_on_top():
    topPin_Xpath = "//div[@class='WB_detail']/div[@class='WB_text W_f14']/a[@ignore='ignore']"

    return is_element_exist_by_xpath(driver, topPin_Xpath)


def check_isConect():
    '''
        检查网络是否通畅，否则报错退出
    '''
    link_time = 0
    while link_time < 6:
        try:
            driver.set_page_load_timeout(30)
            driver.get(target_URL_Homepage)
            save_to_log_without_timestamp('-' * 40)
            save_to_log('浏览器打开成功！')
            break
        except Exception:
            save_to_log(traceback.format_exc())
            link_time += 1
            save_to_log('第{}次连接出错，正在尝试重新连接……'.format(link_time))
    else:
        save_to_log('无法连接，程序退出！')
        save_to_log('-' * 40)
        driver.quit()

def check_is_inUserHomePage():
    title = driver.title

    is_inUserHomePage = False
    if "的微博" in title:
        is_inUserHomePage = True

    return is_inUserHomePage

def check_is_inOrder():
    currentURL = driver.current_url

    is_inOrder = True
    if "is_hot" in currentURL:
        is_inOrder = False

    return is_inOrder

def refresh_userWebsite_checkTitle():
    refresh_time = 0
    while refresh_time < 6:
        driver.refresh()
        refresh_time += 1
        save_to_log('检测页面未在微博用户主页，正在第{}次刷新'.format(refresh_time))
        driver.get(target_URL_Homepage)
        sleep(10)

        if check_is_inUserHomePage():
            save_to_log('进入成功！')
            break
        else:
            continue
    else:
        save_to_log('刷新失败，程序退出！')
        save_to_log_without_timestamp('-' * 40)
        driver.quit()

def refresh_userWebsite_checkOrder():
    refresh_time = 0
    while refresh_time < 6:
        driver.refresh()
        refresh_time += 1
        save_to_log('检测页面未按照顺序排列，正在第{}次刷新'.format(refresh_time))
        sleep(10)

        if check_is_inOrder():
            save_to_log('进入成功！')
            break
        else:
            continue
    else:
        save_to_log('刷新失败，程序退出！')
        save_to_log_without_timestamp('-' * 40)
        driver.quit()


def get_origin_weibo():
    # 原创页面中无图微博  也可能有 WB_media_wrap，需要判定
    # 原创微博又分为内部没有超链接 和 有超链接 两种情况；但可以读取标签中的 alt值 来简化抓取

    # 获取HTML代码
    try:
        content_words_RAW = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_text W_f14']").get_attribute("innerHTML").strip()
    except Exception:
        # 保存当前页面源代码，以供排查错误
        error_page_source = driver.page_source
        save_issues_log_to_file(error_page_source)
        # 自定义异常
        raise Exception("获取原创页面源代码错误！具体请查看日志。")

    # 使用HTMLParser解析代码
    myparser = Myparser()
    myparser.feed(content_words_RAW)
    myparser.close()
    content_words = myparser.content

    content_time = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_from S_txt2']/a").text

    # 识别是否存在图片，如果有，则抓取图片链接
    if is_element_exist_by_xpath(driver, "//div[@class='WB_detail']/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul[@node-type='fl_pic_list']"):
        # 如果是多个图片（list）
        image_url_RAW = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul").get_attribute('action-data')
        # 截取到图片链接，然后转义URL编码
        image_url_unquote = unquote(image_url_RAW.split('&')[2].split('=')[1], 'utf-8')
        image_url = image_url_unquote.replace('//', '\r\n').replace('mw690', 'large')
    elif is_element_exist_by_xpath(driver, "//div[@class='WB_detail']/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul/li[@node-type='fl_h5_video']"):
        # 如果是视频
        image_url = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul/li[@node-type='fl_h5_video']/div[@node-type='fl_h5_video_pre']/img").get_attribute('src')
    elif is_element_exist_by_xpath(driver, "//div[@class='WB_detail']/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul[starts-with(@action-data, 'isPrivate')]"):
        # 如果不是多个图片，而是单个图片（not list）
        image_url_RAW = driver.find_element_by_xpath(
            "//div[@class='WB_detail']/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul").get_attribute(
            'action-data')
        # 截取到图片链接，然后转义URL编码
        image_url_unquote = unquote(image_url_RAW.split('&')[2].split('=')[1], 'utf-8')
        image_url = image_url_unquote.replace('//', '\r\n').replace('mw690', 'large')
    else:
        # 其他情况，例如  专属会员图片
        image_url = ''

    # 将抓取的图片链接与上面得到的文字内容合并
    content_words += image_url

    return content_time, content_words

def get_repost_weibo():
    # 转发的页面也可能没有 WB_media_wrap，需要判定

    # ----- 获取转发的内容的代码 -----
    repost_content_RAW = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_text W_f14']").get_attribute("innerHTML").strip()
    # 使用HTMLParser解析代码，得到转发的内容
    myparser = Myparser()
    myparser.feed(repost_content_RAW)
    myparser.close()
    repost_content = myparser.content


    # ----- 获取被转发的微博的ID -----
    first_post_ID = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_info']/a").text

    # 获取被转发的微博的内容，分为有图片和没图片
    # 获取被转发的微博的文字内容
    first_post_content_RAW = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_text']").get_attribute("innerHTML").strip()
    # 使用HTMLParser解析代码，得到被转发人的内容
    myparser = Myparser()
    myparser.feed(first_post_content_RAW)
    myparser.close()
    first_post_content = myparser.content

    # 判断并获取被转发人的图片链接

    if is_element_exist_by_xpath(driver, "//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul[@node-type='fl_pic_list']"):
        # 如果是图片list
        image_url_RAW = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul").get_attribute('action-data')
        # 截取到图片链接，然后转义URL编码
        image_url_unquote = unquote(image_url_RAW.split('&')[2].split('=')[1], 'utf-8')
        image_url = image_url_unquote.replace('//', '\r\n').replace('mw690', 'large')
    elif is_element_exist_by_xpath(driver, "//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul/li[@node-type='fl_h5_video']"):
        # 如果是视频
        image_url = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul/li[@node-type='fl_h5_video']/div[@node-type='fl_h5_video_pre']/img").get_attribute('src')
    elif is_element_exist_by_xpath(driver, "//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul[starts-with(@action-data, 'isPrivate')]"):
        # 如果是单个图片
        image_url_RAW = driver.find_element_by_xpath(
            "//div[@class='WB_detail']/div[@class='WB_feed_expand']/div[starts-with(@class, 'WB_expand')]/div[@class='WB_media_wrap clearfix']/div[@class='media_box']/ul").get_attribute(
            'action-data')
        # 截取到图片链接，然后转义URL编码
        image_url_unquote = unquote(image_url_RAW.split('&')[2].split('=')[1], 'utf-8')
        image_url = image_url_unquote.replace('//', '\r\n').replace('mw690', 'large')
    else:
        # 其他情况，例如  专属会员图片
        image_url = ''

    # 将抓取的图片链接与上面得到的文字内容合并
    first_post_content += image_url

    content_words = '@{}：{}\r\n{}：{}'.format(weibo_name, repost_content, first_post_ID, first_post_content)

    content_time = driver.find_element_by_xpath("//div[@class='WB_detail']/div[@class='WB_from S_txt2']/a").text

    return content_time, content_words


def is_weibo_repost():
    judgement = is_element_exist_by_xpath(driver, "//div[@class='WB_detail']/div[@class='WB_feed_expand']")
    return judgement


def get_content(latest_post_link):
    # 分为  原创  和  转发。原创有图  很容易被判定为转发，因为内容都在“class="WB_text W_f14"”中；
    # 原创：原创无图，原创有图，原创无链接，原创有链接；
    # 转发：转发原微博无图，原微博有图，评论无图，评论有图；评论无链接，评论有链接（alt处理方式）

    # 如果有超链接，则提取 alt属性内容（先判断是否存在alt属性，没有则忽略）

    driver.get(latest_post_link)
    # 判断是原创还是转发
    if is_weibo_repost():
        # 这里是对转发微博的采集
        # content_time = get_repost_weibo()[0]
        # content = get_repost_weibo()[1]
        # 如果按照上面的方法来写，也没有问题，但是要执行两次 get_repost_weibo()，浪费资源
        (content_time, content) = get_repost_weibo()
    else:
        # 这里是对原创微博的采集
        # content_time = get_origin_weibo()[0]
        # content = get_origin_weibo()[1]
        (content_time, content) = get_origin_weibo()


    local_time = format_time_now()
    # 返回三个值：本机抓取时间，发布时间，内容
    return local_time, content_time, content


if __name__ == '__main__':
    # 选择调试浏览器
    drive_with_chrome()
    # drive_with_phantomjs()

    # 隐式等待5秒，可以自己调节
    driver.implicitly_wait(5)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    driver.set_page_load_timeout(10)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(10)

    check_isConect()
    sleep(10)

    '''
        ---------- 以下是 while 大循环 ----------
    '''
    # 注意！参数的初始化必须在大循环之前，否则每次循环都会执行一次初始化！
    old_post_link = '0'  # 初始化
    i = 0
    j = 0

    while True:
        # 为循环重置首页
        driver.get(target_URL_Homepage)
        # 检查浏览器标题，查看是否在用户页面
        if check_is_inUserHomePage():
            pass
        else:
            refresh_userWebsite_checkTitle()

        # 通过检查网址是否被篡改，来检查是否为顺序排列的微博
        # 如果被篡改成热门排序，在网址中会存在“?is_hot=1”字样
        if check_is_inOrder():
            pass
        else:
            refresh_userWebsite_checkOrder()

        # 检查是否是置顶
        if is_stick_on_top():
            n = 3
        else:
            n = 2
        # 获取最近微博的链接
        sleep(5)
        latest_post_link_Xpath = "//div[starts-with(@id, 'Pl_Official_MyProfileFeed')]/div/div[{}]/div[starts-with(@class, 'WB_feed_detail')]/div[@class='WB_detail']/div[@class='WB_from S_txt2']/a[1]".format(n)
        latest_post_link = driver.find_element_by_xpath(latest_post_link_Xpath).get_attribute('href').split('?')[0]

        '''
            ----- 获取最新微博子页面的内容 -----
        '''
        # 检查是否是新的微博
        if latest_post_link == old_post_link:
            j += 1
            if j % 10 == 0:
                # 防止信息泛滥，每 10 条通报一次
                log = '正在监控，已动态监测{}次，已捕捉到{}条动态。\r\n'.format(j, i)
                save_to_log(log)

            # 这里是延时设置，由于上面有5秒的sleep，因此总体延时是下面的数值+5秒
            sleep(5)
            continue
        else:
            # 获取页面内容，如果获取失败则报错退出
            attempt_time = 0
            while attempt_time<6:
                try:
                    post_info = get_content(latest_post_link)  # 这里调用了获取微博信息的函数，这里改变了页面
                    break   # 如果成功就跳出
                except Exception:
                    save_to_log(traceback.format_exc())
                    attempt_time += 1
                    save_to_log('第{}次抓取子页面出错！正在刷新……'.format(attempt_time))
                    sleep(10)
                    continue
            else:
                save_to_log('子页面无法获取，程序退出！')
                save_to_log('-' * 40)
                driver.quit()


            post_content = '{}\r\n抓取时间：{}\r\n微博时间：{}\r\n{}\r\n\r\n\r\n'.format(latest_post_link, post_info[0], post_info[1], post_info[2])

            # 更新 old_post_link 值
            old_post_link = latest_post_link

            # 写入文件（合并保存）
            save_weibo_to_file(post_content)

            # 输出状态
            i += 1
            capture = '捕捉到{}条动态。\r\n'.format(i, format_time_now())
            save_to_log(capture)

    driver.quit
