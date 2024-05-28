import logging.handlers
import smtplib
import time
from datetime import datetime, timedelta
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import yfinance as yf
from exchangelib import HTMLBody

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)-15s %(levelname)s %(processName)s-%(threadName)s,%(module)s,%(funcName)s,ln %(lineno)d: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

sender = ''
recipients = []
Bcc = []


def get_month_revenue_growth() -> list:
    df_cnyes = pd.DataFrame()
    m = 1
    while True:
        url = f"""https://www.cnyes.com/twstock/financial2.aspx?pi={m}&datetype=ALL&market=T"""
        table = pd.read_html(url)[0]
        if len(table) <= 1:
            break
        time.sleep(0.5)
        df_cnyes = pd.concat([df_cnyes, table], ignore_index=True)
        m += 1

    df_cnyes = df_cnyes[['代碼', '單月營收成長率%']]
    month_growth_list = df_cnyes[df_cnyes['單月營收成長率%'] > 30]['代碼'].astype(str).values.tolist()

    df = pd.read_json('https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL', encoding='utf-8')

    results_list = []
    for code in month_growth_list:
        try:
            trade_volume = df.loc[df['Code'] == code, 'TradeVolume'].astype(int).values.tolist()[0]
            if trade_volume / 1000 > 500:
                results_list.append(code)
        except:
            continue

    return results_list


def get_legal_hold(stock_no: str) -> tuple:
    df = pd.read_html(f'https://histock.tw/stock/chips.aspx?no={stock_no}', encoding='utf-8')
    sites = df[1]['投信']
    foreign = df[1]['外資']

    sites_count = sites.head(5).sum()
    sites_check = int(sites[0] > sites[1:6].sum() and sites[0] > 0)

    foreign_count = foreign.head(5).sum()
    foreign_check = int(foreign[0] > sites[1:6].sum() and foreign[0] > 0)

    return sites_count, sites_check, foreign_count, foreign_check


def send_mail(title: str, content: str):
    message_content = MIMEText(content, 'html', 'utf-8')
    message = MIMEMultipart()
    message['Subject'] = Header(title, 'utf-8')
    message['To'] = ','.join(recipients)
    message.attach(message_content)

    try:
        with smtplib.SMTP('rs1.testritegroup.com') as smtpObj:
            logger.info(f"sender: {sender}")
            logger.info(f"receivers: {recipients}")
            smtpObj.sendmail(sender, recipients + Bcc, message.as_string())
            logger.info("Successfully sent email")
    except (smtplib.SMTPConnectError, smtplib.SMTPAuthenticationError, smtplib.SMTPSenderRefused,
            smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError, smtplib.SMTPException) as e:
        logger.error("Error: unable to send email")
        logger.exception(e)


def main():
    industry_code = {'01': '水泥工業', '02': '食品工業', '03': '塑膠工業', '04': '紡織工業', '05': '電機機械',
                     '06': '電器電纜', '21': '化學工業', '22': '生技醫療', '08': '玻璃陶瓷', '09': '造紙工業',
                     '10': '鋼鐵工業', '11': '橡膠工業', '12': '汽車工業', '24': '半導體業', '25': '電腦及週邊設備業',
                     '26': '光電業', '27': '通訊網路業', '28': '電子零組件', '29': '電子通路業', '30': '資訊服務業',
                     '31': '其他電子業',
                     '32': '文化創意業', '33': '農業科技', '34': '電子商務', '14': '建材營造', '15': '航運',
                     '16': '觀光', '17': '金融', '18': '貿易百貨', '23': '油電燃氣', '19': '綜合', '20': '其他',
                     '80': '管理股票', '91': '台灣存託憑證', '97': '社會企業', '98': '農林漁牧'
                     }
    month_growth_list = get_month_revenue_growth()
    search_time = datetime.now() - timedelta(days=90)
    results_1 = list()
    results_2 = list()
    results_3 = list()
    results_4 = list()
    results_5 = list()
    results_6 = list()
    df_TWSE = pd.read_json('https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL')
    df_TWSE_com = pd.read_json('https://openapi.twse.com.tw/v1/opendata/t187ap03_L')
    df_TWSE_com['公司代號'] = df_TWSE_com['公司代號'].astype(str)

    for stock_no in month_growth_list:
        stock = yf.Ticker(f"{stock_no}.TW")
        stock_data = stock.history(start=search_time)
        close_data = round(stock_data['Close'].iloc[-1], 2)
        high_data = stock_data['High'].apply(lambda x: round(x, 2)).tolist()[:-1]
        volume_data = stock_data['Volume'].tolist()

        if close_data > max(high_data):
            df = df_TWSE[df_TWSE['Code'] == stock_no].iloc[0]
            code, name, close_price, _ = df.values
            n = df_TWSE_com.loc[df_TWSE_com['公司代號'] == stock_no, '產業別'].values[0]
            result = [code, name, industry_code.get(str(n).zfill(2)), close_price]
            results_1.append(result)

            if volume_data[-1] > (sum(volume_data[-6:-1]) / 5) * 1.2:
                results_4.append(result)

            site_count, site_check, foreign_count, foreign_check = get_legal_hold(code)
            if site_count > 0:
                results_2.append(result)
            if foreign_count > 0:
                results_3.append(result)
            if site_check == 1:
                results_5.append(result)
            if foreign_check == 1:
                results_6.append(result)

        time.sleep(1)

    results_dfs = []
    columns = ['股票代碼', '股票名稱', '產業別', '股價']

    results = [results_1, results_2, results_3, results_4, results_5, results_6]

    for result in results:
        df = pd.DataFrame(result, columns=columns).to_html()
        results_dfs.append(df)
    send_mail(title=f"{datetime.now().strftime('%Y-%m-%d')}預測飆股",
              content=HTMLBody(
                  f"""<html><body style="font-family:Microsoft JhengHei">1.單月營收年成長率>30%。
                      <br/>2.突破3個月以上的區間箱型整理。
                      <br/>{results_dfs[0]}
                      <br/>篩選 1：投信5日內買入加總為正值
                      <br/>{results_dfs[1]}
                      <br/>篩選 2：投信當日買進大於前5日加總
                      <br/>{results_dfs[2]}
                      <br/>篩選 3：外資5日內買入加總為正值
                      <br/>{results_dfs[3]}
                      <br/>篩選 4：外資當日買進大於前5日加總
                      <br/>{results_dfs[4]}
                      <br/>篩選 5：當日成交量大於前五個交易日平均20%以上
                      <br/>{results_dfs[5]}
                      </body></html>"""),
              )


if __name__ == "__main__":
    main()
