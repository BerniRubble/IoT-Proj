from flask import Flask, render_template,request


#Server base, non ottimizzato in un nulla per vedere se tutto funziona

app=Flask(__name__)

buffer=['']

@app.route('/', methods=['GET'])
def home():
    print(buffer[0])
    return render_template('home.html', buffer=buffer[0])

@app.route('/', methods=['POST'])
def updateBuffer():
    buffer[0]=request.get_data().decode("utf-8")
    return 'OK'

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8080)
