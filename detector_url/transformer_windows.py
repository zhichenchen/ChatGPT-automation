

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
from tqdm import tqdm
import xlrd
from urllib import parse
#pip install 
from selenium.webdriver.chrome.service import Service
#from selenium import *

driver = ''


def strs(row):
    values = ""
    for i in range(len(row)):
        if i == len(row) - 1:
            values = values + str(row[i])
        else:
            values = values + str(row[i])
    return values


def main():
    i = False
    # excel名称
    file_name = 'n=5.xls'  #"merged.xls"
    # 导出文件名称
    d_name = 'merged_resulted.xls'
    url = 'https://openai-openai-detector.hf.space/'
    option = webdriver.ChromeOptions()
    option.add_argument("--start-maximized")
    option.add_argument('--log-level=3')
    option.add_argument("--test-type")
    option.add_argument("--ignore-certificate-errors")  # 忽略证书错误
    option.add_argument("--disable-popup-blocking")  # 禁用弹出拦截
    option.add_argument("no-default-browser-check")  # 禁止默认浏览器检查
    option.add_argument("about:histograms")
    option.add_argument("about:cache")
    # option.add_argument('--headless')  # 无界面
    option.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    option.add_argument("disable-translate")  # 禁用翻译
    option.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
    # option.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片, 提升速度
    option.add_experimental_option("detach", True)
    global driver
    driver = webdriver.Chrome(service=Service(r'driver/chromedriver'), options=option) # /usr/local/bin/chromedriver
    driver.get(url)
    # 读取excel
    # raw_text = raw_data.values[0:len(raw_data), 1:2]
    real_arr = []
    fake_arr = []
    # 打开文件
    data = xlrd.open_workbook(f"{file_name}")  # 旧版xlrd
    table = data.sheets()[0]  # 表头，第几个sheet表-1
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(1)  # 某一行数据
    # 打印出行数列数
    for ronum in tqdm(range(1, nrows)):
        row = table.cell_value(rowx=ronum, colx=1)  # 只需要修改你要读取的列数-1
        values = strs(row)  # 调用函数，将行数据拼接成字符串
        t_text = values
        # print(t_text)
        try:
            # 定位输入框
            input_box = driver.find_element_by_id('textbox')
            # 输入内容
            input_box.clear()
            print("ready for input")

            # js = f"element = document.getElementById('textbox');element.value = '"+t_text+"';event = document.createEvent('HTMLEvents');event.initEvent('change', true, true);element.dispatchEvent(event);"
            # driver.execute_script(js)
            try:
                input_box.send_keys(t_text)
            except:
                pass
            print("inputing")
        except Exception as e:
            print('fail')
        print(driver.current_url)
        if str(url) not in str(driver.current_url):
            print("last page")
            i = True
            js = 'window.history.go(-1);'
            time.sleep(0.1)
            driver.execute_script(js)
        else:
            time.sleep(0.1)
        while True:
            try:
                real_div = driver.find_element_by_id("real-percentage").text
                break
            except:
                print("waiting for loading")
                time.sleep(1)
        # 判断是否加载完毕
        # 最多5秒
        l_type = False
        for i in range(0, 5):
            load_text = driver.find_element_by_id("message").text
            if "Predicting ..." in str(load_text):
                time.sleep(1)
                l_type = False
            else:
                l_type = True
                break
        if l_type is False:
            real_div = 'no_result'
            fake_div = 'no_result'
        else:
            for i in range(0, 5):
                time.sleep(1)
                real_div = driver.find_element_by_id("real-percentage").text
                fake_div = driver.find_element_by_id("fake-percentage").text
                if '%' in str(real_div):
                    break
        real_arr.append(real_div)
        fake_arr.append(fake_div)
        print(f"fake:{fake_div}")
        print(f"real:{real_div}")
    raw_data = pd.read_excel(f"{file_name}")
    raw_data["real"] = real_arr
    raw_data["fake"] = fake_arr
    raw_data.to_excel(f"{d_name}", index=False)


if __name__ == "__main__":
    main()
