from flask import Flask, jsonify,render_template
import subprocess
# from crotch import fetch_data  # 导入上面定义的函数
import crotch
import cal
app = Flask(__name__)

# @app.route('/run_script')
# def run_script():
#     result = subprocess.run(['python', 'crotch.py'], capture_output=True, text=True)
#     return jsonify(output=result.stdout)

@app.route('/run_script')
def run_script():
    data = crotch.main()  # 调用函数获取数据
    return jsonify(data)  # 将数据以 JSON 格式返回

@app.route('/')
def index():
    return render_template('預測飆股.html')

@app.route('/2')
def index2():
    return render_template('存股.html')
@app.route('/3')
def index3():
    return render_template('final_project_index.html')

@app.route('/run_script2')
def run_script2():
    data = cal.main()  # 调用函数获取数据
    return data  #


if __name__ == '__main__':
    app.run(debug=True)
