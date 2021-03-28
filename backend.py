from flask import Flask, request, render_template
# from api import predict_for_user
import requests
from ast import literal_eval
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('/hook-theme-master/index.html'), 404


@app.route('/predict', methods=['GET'])
def predict():
    if request.method == 'GET':
        id = int(request.args.get('id'))
        data = requests.get('http://localhost:9091/predict?id={}'.format(id)).content.decode()
        print(data)
        return
        return render_template('/hook-theme-master/predict.html', data=data), 404


if __name__ == '__main__':
    app.run()




