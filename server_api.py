from flask import Flask, request, render_template
from api import predict_for_user

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('/hook-theme-master/index.html'), 404


@app.route('/predict', methods=['GET'])
def predict():
    if request.method == 'GET':
        id = int(request.args.get('id'))
        data = predict_for_user(id, iloc=False, n=5)
        data['submit'] = data['submit'].to_dict()
        return data


if __name__ == '__main__':
    app.run('localhost', 9091)




