import pickle
import win32api,win32con

import sklearn
import sklearn.naive_bayes
import jieba
import pandas as pd

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

texts1=[]
def get_weiboText():

    print(driver.current_url)
    js = 'return document.getElementsByClassName("Feed_body_3R0rO")'
    html = driver.execute_script(js)

    for i in html:
        texts = []
        content = i.find_element(by=By.CLASS_NAME, value="detail_wbtext_4CRf9")
        texts.append(content.text)

        verify = str(i.get_attribute('innerHTML'))

        if verify.find("vblue") != -1:
            texts.pop()
        else:
            texts.append(content.text)

        for m in texts:
            if m not in texts1:
                texts1.append(m)
                rumor_detect(m)

def contents_tokenization(contents):
    contents_S = []
    contents_S.append(jieba.lcut(contents[0]))

    stopwords = get_stopwords()

    contents_clean = []
    line_clean = []

    for word in contents_S[0]:
        if word in stopwords:
            continue
        line_clean.append(word)
    contents_clean.append(line_clean)

    contents_clean=[" ".join (x) for x in contents_clean]
    return contents_clean

def get_stopwords():
    stopwords = pd.read_csv ("stopwords.txt", index_col=False, sep="\t", quoting=3, names=['stopword'],
                             encoding='utf-8')
    return set(stopwords['stopword'].values.tolist())

def rumor_detect(input_text):
    content = vec.transform(contents_tokenization([input_text]))
    if classifier.predict(content) == [0]:
        win32api.MessageBox(0, input_text, "谣言警告", win32con.MB_OK)
        print("rumor:", input_text)

if __name__ == "__main__":

    with open('classifier', 'rb') as f:
        classifier = pickle.load(f)

    with open('vec.pkl', 'rb') as f:
        vec = pickle.load(f)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://weibo.com/login.php")


    while True:

        try:
            if driver.execute_script("return document"):
                driver.switch_to.window(driver.window_handles[-1])
            get_weiboText()

            time.sleep(3)

        except:
            continue