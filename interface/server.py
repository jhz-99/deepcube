import json
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
from colordetect import IR
app=Flask(__name__)
from tools import getResults
import ast


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('mofang.html')

@app.route('/initState', methods=['POST'])
def initState():
    if request.method=='POST':
        #rev=request.get_json()['city']
        #result=selcity(rev)
        os.chdir("C:\\Users\\guoyy\\Desktop\\deepcube\\deepcube\\interface")
        with open('initState.json', 'r') as f:
            result = json.load(f)
        return jsonify(result)

@app.route('/solve', methods=['POST'])
def solve():
    if request.method == 'POST':
        rev = request.form
        print(rev)
        print("computing...")
        data = rev.to_dict()
        state = []
        data['state'] = ast.literal_eval(data['state'])
        print(data['state'])
        for i in data['state']:
            state.append(int(i))
        result = getResults(state)
        print("complete!")
        return jsonify(result)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

# 添加路由
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static\images',secure_filename(f.filename))
        f.save(upload_path)
        file_dir = "static\images"
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.jpg':
                    t = os.path.join(root,file)
                    L.append(t)
        return render_template('mofang.html',datas = L)
    # 重新返回上传界面
    return render_template('mofang.html',datas ="上传失败")

@app.route('/imagerecognition', methods=['GET'])
def imagerecognition():
    DIR = "static/images"
    nums = len(os.listdir(DIR))
    color_order = ''
    i=0
    if (nums == 6):
        num_str = IR()
        for item in num_str:
            if (item == 'D'):
                color_order  = color_order + '0 '
            elif (item == 'U'):
                color_order  = color_order + '1 '
            elif (item == 'B'):
                color_order  = color_order + '2 '
            elif (item == 'F'):
                color_order  = color_order + '3 '
            elif (item == 'L'):
                color_order  = color_order + '4 '
            elif (item == 'R'):
                color_order  = color_order + '5 '
            i=i+1
    return(color_order)

if __name__=='__main__':
    app.run(debug=True)