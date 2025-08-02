from flask import Flask
from routes import voice_bp, record_bp

app = Flask(__name__)
app.register_blueprint(voice_bp)
app.register_blueprint(record_bp)

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000)

@app.route('/')
def index():
    return 'Rapid Solutions voice rec api v1.0 <br> contact dev@rapidsolutions.ae if you have any question.'

if __name__ == '__main__':
    context = ('/etc/ssl/certificates/cloudflare.crt', '/etc/ssl/certificates/cloudflare.key') #certificate and key files
    app.run(host='94.130.59.114', port='8443', debug=False, ssl_context=context, threaded=True)
