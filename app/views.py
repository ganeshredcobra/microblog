from flask import render_template, flash, redirect ,jsonify
from app import app
from .forms import LoginForm
from flask import abort
from flask import make_response
from flask import request



@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Visitor'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)
	 
@app.route("/members/<string:name>/")
def getMember(name):
    return '<h1>Hello {{%s}}</h1>'%name
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,providers=app.config['OPENID_PROVIDERS'])
                           
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

Values = [
	{
		'Count':0,
		'RPM':0,
		'ECT':0
	},
	{
		'Count':1,
		'RPM':1,
		'ECT':1
	}
]

@app.route('/update', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
    
@app.route('/update/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
 
@app.route("/browser")
def brow():
	user_agent = request.headers.get('User-Agent')
	return '<p>Your browser is %s</p>'%user_agent 

@app.route('/newtasks', methods=['POST'])
def create_task():
    if not request.json or not 'RPM' in request.json:
        abort(400)
    ValuesN = {
        #'Count':request.json['Count'],
        'Count': Values[-1]['Count'] + 1,
        'RPM': request.json['RPM'],
        'ECT': request.json['ECT']
    }
    Values.append(ValuesN)
    print Values[0]['Count']
    return jsonify({'Values': Values}), 201
    #return render_template("members.html",VAL=Values)

@app.route("/members")
def members():
    return render_template("members.html",VALS=Values)
    
@app.route('/getvals', methods=['GET'])
def get_vals():
    return jsonify({'VALS': Values})
