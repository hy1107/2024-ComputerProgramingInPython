from flask import Flask, render_template, jsonify, request
from crotch import get_month_revenue_growth  # 確保函數是可以被導入的

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('存股股票程式分析.html')  # 確保HTML檔案名稱正確

@app.route('/analyze', methods=['POST'])
def analyze():
    uniform = request.form.get('uniform', type=int, default=30)
    yield_percent = request.form.get('yield_percent', type=float, default=6.0)
    # 假設 get_best_stock 需要兩個參數: uniform 和 yield_percent
    stock_list, dividends_growth_list = get_month_revenue_growth(uniform, yield_percent)
    return jsonify({'stock_list': stock_list, 'dividends_growth_list': dividends_growth_list})

if __name__ == '__main__':
    app.run(debug=True)