from flask import Flask,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy

# 创建 Flask 实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interest.db'
db = SQLAlchemy(app)

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Interest %r>' % self.name

#路由和视图函数
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/interests', methods=['GET','POST'])
def interests():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        interest = Interest(name=name, description=description, category=category)
        db.session.add(interest)
        db.session.commit()
        return 'Interest created', 201
    elif request.method == 'GET':
        interests = Interest.query.all()
        return jsonify([interest.__dict__ for interest in interests])

if __name__ == '__main__':
    app.run(debug=True)