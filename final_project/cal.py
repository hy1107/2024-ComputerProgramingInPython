# 引入 twstock 套件
import logging.handlers
import random
import smtplib
import sys
import time
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from statistics import mean

import pandas as pd
import requests
import twstock
from bs4 import BeautifulSoup
from exchangelib import HTMLBody
from pandas import json_normalize
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)-15s %(levelname)s %(processName)s-%(threadName)s,%(module)s,%(funcName)s,ln %(lineno)d: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

engine = create_engine('sqlite:///./stock.db')
Session = sessionmaker(bind=engine)
session = Session()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

sender = ''
recipients = []
bcc = []


# bcc = []
def get_stock_no() -> list:
    stock_codes = []
    for code, info in twstock.codes.items():
        if info.type == '股票':
            stock_codes.append(code)
    return sorted(stock_codes)


def get_best_stock(uniform, yield_percent):
    industry_code = {'01': '水泥工業', '02': '食品工業', '03': '塑膠工業', '04': '紡織工業', '05': '電機機械',
                     '06': '電器電纜', '21': '化學工業', '22': '生技醫療', '08': '玻璃陶瓷', '09': '造紙工業',
                     '10': '鋼鐵工業', '11': '橡膠工業', '12': '汽車工業', '24': '半導體業', '25': '電腦及週邊設備業',
                     '26': '光電業', '27': '通訊網路業', '28': '電子零組件', '29': '電子通路業', '30': '資訊服務業',
                     '31': '其他電子業',
                     '32': '文化創意業', '33': '農業科技', '34': '電子商務', '14': '建材營造', '15': '航運',
                     '16': '觀光', '17': '金融', '18': '貿易百貨', '23': '油電燃氣', '19': '綜合', '20': '其他',
                     '80': '管理股票', '91': '台灣存託憑證', '97': '社會企業', '98': '農林漁牧'
                     }
    end_year = datetime.now().year
    time_range = ", ".join(f'''"{str(i)}"''' for i in range(2008, end_year))
    with session.begin():
        dividend_df = pd.read_sql(f'select stock_no, {time_range} from dividend03', con=session.bind).fillna(
            0).to_numpy()
    with requests.get('https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL') as r:
        df_TWSE = json_normalize(r.json())
    with requests.get('https://openapi.twse.com.tw/v1/opendata/t187ap03_L') as r:
        df_TWSE_com = json_normalize(r.json())
    df_TWSE_com.公司代號 = df_TWSE_com.公司代號.astype(str)
    best_stock_list = []
    dividend_growth_list = []
    for item in dividend_df:
        item_m = item[-5:]
        item_s = item[1:]
        if 0.0 not in item_m:
            try:
                if (float(max(item_m)) - float(min(item_m))) / (
                        float(max(item_m)) + float(min(item_m))) < (
                        uniform / 100):
                    stock_price = float(df_TWSE[df_TWSE['Code'] == f"""{item[0]}"""].ClosingPrice.values[0])
                    average_dividend = mean(map(float, item[-6: -1]))
                    Yield = average_dividend / stock_price
                    if Yield > (yield_percent / 100):
                        n1 = df_TWSE[df_TWSE['Code'] == f"""{item[0]}"""].Name.values[0]
                        n2 = df_TWSE_com[df_TWSE_com['公司代號'] == f"""{item[0]}"""].產業別.values[0]
                        n3 = round(Yield * 100, 2)
                        best_stock_list.append([
                            item[0], n1, industry_code[str(n2).zfill(2)], f"{n3}%", stock_price,
                            round(average_dividend / 0.07, 2),
                            round(average_dividend / 0.04, 2)])
                        if mean(item_s[-3:]) > mean(item_s[-6:]) > mean(item_s[-9:]):
                            dividend_growth_list.append([
                                item[0], n1, industry_code[str(n2).zfill(2)], f"{n3}%", stock_price,
                                round(average_dividend / 0.07, 2),
                                round(average_dividend / 0.04, 2)])
            except:
                pass
    return best_stock_list, dividend_growth_list


def Debt_Service_Coverage_Ratio(stock_no: str) -> bool:  # 利息保障倍數
    try:
        time.sleep(0.5)
        # 引入 requests, BeautifulSoup 和 pandas 套件
        # 設定要查詢的網址
        url = f'https://histock.tw/stock/{stock_no}/%E5%88%A9%E6%81%AF%E4%BF%9D%E9%9A%9C%E5%80%8D%E6%95%B8'
        # 使用 requests 套件發送請求，並將回應內容轉換為 UTF-8 編碼，然後儲存為 response
        df = pd.read_html(url)[0]
        avg_dscr = sum(df['利息保障倍數(倍)'][:5]) / 5
        if avg_dscr >= 50:
            return True
        else:
            return False
    except:
        return False


def update_dividends() -> None:
    with session.begin():
        sql = 'CREATE TABLE IF NOT EXISTS dividend03 ("stock_no" TEXT PRIMARY KEY)'
        session.execute(text(sql))
        s = get_stock_no()
        for stock_no in s:
            n = random.randrange(0, 2)
            time.sleep(n)
            print(stock_no)
            d = list()
            try:
                df = pd.read_json(
                    f'https://marketinfo.api.cnyes.com/mi/api/v1/financialIndicator/divided/TWS:{stock_no}:STOCK?year=10&to=1366560000')
            except Exception as e:
                continue
            for data in df['data'].to_numpy():
                d.append([data['year'], data['cashDividend']])
            for j in d:
                if int(j[0]) >= 2008:
                    try:
                        sql = f'ALTER TABLE dividend03 ADD "{str(j[0])}" REAL'
                        session.execute(text(sql))
                    except Exception as e:
                        pass
                    sql = f'insert or ignore into dividend03 ("stock_no") values ("{stock_no}")'
                    session.execute(text(sql))
                    sql = f'Update dividend03 set "{str(j[0])}"="{round(j[1], 2)}" where stock_no="{stock_no}"'
                    session.execute(text(sql))

            time.sleep(0.5)


def Contract_liabilities(stock_no: str) -> bool:  # 合約負債
    try:
        time.sleep(0.5)
        cl_list = list()
        url = f'https://fubon-ebrokerdj.fbs.com.tw/z/zc/zcp/zcpa/zcpa_{stock_no}.djhtm'
        # 設定一個自定義的標頭，模仿一個真正的瀏覽器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        # 使用 with 語法管理 requests 物件，確保資源在使用後正確釋放
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()  # Raise an exception for non-200 status codes
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            st = soup.find_all('div', 'table-row')
            for idx, row in enumerate(st):
                if '合約負債－流動' in row.text:
                    cl_list = st[idx].text.strip().split('\n')
                    break
            cl_list = [float(x.replace(',', '')) for x in cl_list[1:]]
            if cl_list[0] > cl_list[1] > cl_list[2]:
                return True
            else:
                return False
    except requests.exceptions.RequestException as e:
        # Handle network errors gracefully
        raise Exception(f"Error fetching contract liabilities: {e}")


def Reinvestment_Rate(stock_no: str) -> bool:
    try:
        time.sleep(0.5)
        url = f"https://histock.tw/stock/{stock_no}/%E7%9B%88%E9%A4%98%E5%86%8D%E6%8A%95%E8%B3%87%E6%AF%94%E7%8E%87"
        df = pd.read_html(url)[0]
        rpm = df['盈餘再投資比'].iloc[:4].apply(lambda x: float(x[:-1])).mean()
        return 0 < float(rpm) < 80
    except:
        return False


def get_revenue_growth(stock_no: str) -> bool:
    try:
        url = f"""https://concords.moneydj.com/z/zc/zce/zce_{stock_no}.djhtm"""
        # Use with statement to manage the request and response
        with requests.get(url) as response:
            response.raise_for_status()  # Raise an exception for non-200 status codes
            html = response.text
            revenue_df = pd.read_html(html, index_col=False)[2]
            revenue_df = revenue_df.drop(index=[0, 1]).reset_index()
            revenue_df.columns = revenue_df.iloc[0]
            list_EPS = revenue_df['EPS(元)'].drop(index=0).astype(float).values.tolist()
            if mean(list_EPS[:3]) > mean(list_EPS[:6]) > mean(list_EPS[:9]):
                return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching revenue data: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False
    finally:
        # Ensure logging is configured if not already done
        if not logger.handlers:
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.INFO)


def send_mail(title, content):
    message_content = MIMEText(content, 'html', 'utf-8')
    message = MIMEMultipart()
    message['Subject'] = Header(title, 'utf-8')
    message['To'] = ','.join(recipients)
    message.attach(message_content)
    try:
        smtpObj = smtplib.SMTP('rs1.testritegroup.com')
        logger.info(f"""sender : {sender}""")
        logger.info(f"""receivers : {recipients}""")
        # raise
        smtpObj.sendmail(sender, recipients + bcc, message.as_string())
        smtpObj.close()
        logger.info("Successfully sent email")
    except smtplib.SMTPException:
        logger.info("Error: unable to send email")
        logger.info("Unexpected error:", sys.exc_info()[0])
    return


def main():
    # Get the list of stocks with high dividend yield and low volatility
    stock_list, dividends_growth_list = get_best_stock(30, 6)

    # Initialize result lists
    result_1 = []
    result_2 = []

    # Iterate over the stock list
    for stock in stock_list:
        stock_no = stock[0]
        try:
            # Check for additional criteria and add to the result list if met
            if Debt_Service_Coverage_Ratio(stock_no) and Contract_liabilities(stock_no):
                result_1.append(stock)
            if Reinvestment_Rate(stock_no) and get_revenue_growth(stock_no):
                result_2.append(stock)
        except Exception as e:
            logger.error(stock_no, e)
            continue

    # Generate HTML tables for each dataframe
    stock_df = pd.DataFrame(stock_list,
                            columns=['股票代碼', '股票名稱', '產業別', '殖利率', '股價', '便宜價', '昂貴價']).to_html()
    stock_df_2 = pd.DataFrame(dividends_growth_list,
                              columns=['股票代碼', '股票名稱', '產業別', '殖利率', '股價', '便宜價',
                                       '昂貴價']).to_html()
    result_df_1 = pd.DataFrame(result_1, columns=['股票代碼', '股票名稱', '產業別', '殖利率', '股價', '便宜價',
                                                  '昂貴價']).to_html()
    result_df_2 = pd.DataFrame(result_2, columns=['股票代碼', '股票名稱', '產業別', '殖利率', '股價', '便宜價',
                                                  '昂貴價']).to_html()

    # Generate email content
    content = HTMLBody(
        f"""<html><body style="font-family:Microsoft JhengHei">
        篩選條件：每年發放股利；股利波動度 < 30%；殖利率 > 6%
        <br/><b>便宜價：殖利率 >= 7%；昂貴價：殖利率 <= 4% (股利以五年平均計算)</b>
        <br/>{stock_df}
        <br/><b>篩選結果中股利成長個股（3年平均 > 6年平均 > 9年平均）</b>
        <br/>{stock_df_2}
        <br/><b>追加篩選條件 1（利息保障倍數 > 50、合約負債連三季成長）：</b>
        <br/>{result_df_1}
        <br/><b>追加篩選條件 2（0 < 盈再率 < 80、EPS成長[前3季平均 > 前6季平均 > 前9季平均]）：</b>
        <br/>{result_df_2}
        </body></html>"""
    )

    # Send email with the results
    print(content)
    return content


if __name__ == "__main__":
    main()
