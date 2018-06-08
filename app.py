# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
from config import database, secret
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import LoginManager , UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_mail import Mail,Message 
from functools import wraps
from form import AccountRegisterForm,AddUserForm,EditUserForm,UserRegisterForm,LoginForm,AddTransactionForm,EditTransactionForm,AddProjectsForm,AddExpenseForm,EditProjectsForm,ChangeCurrencyForm
import sys




app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SECRET_KEY"] = secret 
db = SQLAlchemy(app)
app.debug = True 



class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100))
	email = db.Column(db.String(200))
	password = db.Column(db.String(500))
	token = db.Column(db.String(500))
	role = db.Column(db.String(100))
	status = db.Column(db.String(100))	
	trial_date = db.Column(db.DateTime())
	start_date = db.Column(db.DateTime())	
	admin = db.Column(db.Integer())
	accountowner = db.relationship("Account",backref="accountowner",lazy="dynamic")

	def is_active(self):
		return True

	def get_id(self):
		return self.id

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False


class Account(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	amount = db.Column(db.BigInteger())
	currency = db.Column(db.String(200))
	accountowner_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
	transactionowner = db.relationship("Transaction",backref="transactionowner",lazy="dynamic")
	projectsowner = db.relationship("Projects",backref="projectsowner",lazy="dynamic")


class Projects(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	customer = db.Column(db.String(200))
	description = db.Column(db.UnicodeText())
	due_date = db.Column(db.DateTime())
	status = db.Column(db.String(100))
	revenue = db.Column(db.BigInteger())		
	cashowner = db.relationship("Transaction",backref="cashowner",lazy="dynamic") 
	projectsowner_id = db.Column(db.Integer(), db.ForeignKey("account.id"))




class Transaction(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(300))
	amount = db.Column(db.BigInteger())	
	status = db.Column(db.String(200))
	date = db.Column(db.DateTime())	
	owner = db.Column(db.Integer())
	cashowner_id = db.Column(db.Integer(), db.ForeignKey("projects.id"))
	transactionowner_id = db.Column(db.Integer(), db.ForeignKey("account.id"))



#################################################### Decorator ##############################################################################

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "UserLogin"

#user loader
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))

#fungsi mail
app.config.from_pyfile("config.py") 
mail = Mail(app)
s = URLSafeTimedSerializer("secret")

#unicode
reload(sys)
sys.setdefaultencoding('utf-8')

#mengatur role 
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return redirect(url_for("UserDashboard"))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

   


############################################ Auth route ############################################################
@app.route("/register",methods=["GET","POST"])
def UserRegister():
	form = UserRegisterForm()
	if form.validate_on_submit():
		hass = generate_password_hash(form.password.data,method="sha256")		
		today = datetime.today()
		start = today + timedelta(days=12)
		token = s.dumps(form.email.data)
		user = User(username=form.username.data,email=form.email.data,password=hass,token=token,trial_date=today,start_date=start,role="user",status="trial")
		check_user = User.query.filter_by(email=form.email.data).all()
		if len(check_user) > 0 :
			flash("Email already exist","danger")
		else :		

			db.session.add(user)			
			db.session.commit()

			user = User.query.filter_by(email=form.email.data).first()
			#menambah saldo di account					
			account = Account(amount=0,accountowner_id=user.id,currency="$")

			db.session.add(account)
			db.session.commit()


			login_user(user)
			flash("Registration Complete","success")
			return redirect(url_for("UserDashboard",token=user.token))

	return render_template("auth/register.html",form=form)		



@app.route("/login",methods=["GET","POST"])
def Login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password,form.password.data):
				login_user(user)

				flash("login success","success")
				return redirect(url_for("UserDashboard",token=user.token))

		flash("Invalid login","danger")

	return  render_template("auth/login.html",form=form)			



@app.route("/logout",methods=["GET","POST"])
@login_required
def Logout():
	logout_user()
	return redirect(url_for("UserRegister"))






########################################################## Dashboard & Setting #################################
@app.route("/dashboard",methods=["GET","POST"])
@login_required
def UserDashboard():
	return render_template("dashboard/dashboard.html")


@app.route("/dashboard/setting",methods=["GET","POST"])
@login_required
@requires_roles("user","Admin")
def Setting():	
	return render_template("setting/setting.html")


@app.route("/dashboard/change/currency",methods=["GET","POST"])
@login_required
@requires_roles("user","Admin")
def ChangeCurrency():
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	form = ChangeCurrencyForm()
	form.currency.data = account.currency
	if form.validate_on_submit():
		account.currency = request.form["currency"]
		db.session.commit()
		return redirect(url_for("Setting"))
	return render_template("setting/currency.html",form=form,account=account)	




























###################################################### User & Activity ############################################ 
#all user 
@app.route("/dashboard/all/user",methods=["GET","POST"])
@login_required
@requires_roles("Admin","user")
def AllUser():
	users = User.query.filter_by(admin=current_user.id).all()
	form = AddUserForm()
	if form.validate_on_submit():
		email = form.email.data			
		user = User.query.filter_by(email=email).first()
		if user :
			flash("Email already registered","danger")
		else :	
			new = User(email=email,username=form.username.data,role=form.role.data,admin=current_user.id) 
			
			token = s.dumps(email, salt="email-confirm")						 				

			msg = Message("Account Invite", sender="founderhacker@gmail.com", recipients=[email])

			link = url_for("AccountInvite",token=token, _external=True)

			username = current_user.username
			msg.body = "your are invited to founderhacker.com by {} register in this link {}".format(username,link)
			mail.send(msg)

			db.session.add(new)
			db.session.commit()
		
			flash("Email with registration link was sent","success")
			return redirect(url_for("AllUser"))

	return render_template("dashboard/all_user.html",users=users,form=form)

#user registered
@app.route("/account/invite/<token>",methods=["GET","POST"])
def AccountInvite(token):	
	try :
		email = s.loads(token, salt="email-confirm", max_age=3000)	
	except :
		return "link expired"		
	form = AccountRegisterForm()			
	user = User.query.filter_by(email=email).first()
	form.email.data = user.email
	form.username.data = user.username
	if form.validate_on_submit():			
		hass = generate_password_hash(form.password.data,method="sha256")		 				
		user.password = hass
		user.username = request.form["username"] 
						
		db.session.commit()

		flash("Registration Complete","success")
		return redirect(url_for("Login"))
	

	return render_template("auth/invite.html",form=form)	


@app.route("/dashboard/edit/user/<id>",methods=["GET","POST"])
@login_required
@requires_roles("Admin","user")
def EditUser(id):
	users = User.query.filter_by(admin=current_user.id).all()
	user = User.query.filter_by(id=id).first()
	form = EditUserForm()
	form.role.data = user.role
	form.username.data = user.username
	form.email.data = user.email
	if form.validate_on_submit():
		user.role = request.form["role"]
		db.session.commit()

		flash("User edited successfully","success")
		return redirect(url_for("AllUser"))

	return render_template("dashboard/edit_user.html",users=users,form=form,user=user)

@app.route("/dashboard/delete/user/<id>",methods=["GET","POST"])
@requires_roles("Admin","user")
@login_required
def DeleteUser(id):
	user = User.query.filter_by(id=id).first()
	db.session.delete(user)
	db.session.commit()

	flash("User successfully deleted","success")
	return redirect(url_for("AllUser"))





###################################################### Transaction ###########################################
@app.route("/dashboard/transaction",methods=["GET","POST"])
@login_required
def UserTransaction():	
	form = AddTransactionForm()
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	transaction = Transaction.query.filter_by(transactionowner_id=account.id).order_by(Transaction.date.desc()).all()	
	income = Transaction.query.filter_by(status="Income",transactionowner_id=account.id).all()
	expense = Transaction.query.filter_by(status="Expense",transactionowner_id=account.id).all()
	if form.validate_on_submit():		
		amount = (form.amount.data)
		jumlah = int(amount.replace(',',''))
		status = form.status.data	
		trans = Transaction(amount=jumlah,name=form.name.data,description=form.description.data,date=form.date.data,status=status,owner=current_user.id,transactionowner_id=account.id)		

		db.session.add(trans)
		db.session.commit()

		flash("Transaction successfully added","success")
		return redirect(url_for("UserTransaction"))		
	return render_template("dashboard/transaction.html",account=account,income=income,expense=expense,form=form,transaction=transaction)




@app.route("/dashboard/transaction/<id>",methods=["GET","POST"])
@login_required
def EditTransaction(id):	
	form = AddTransactionForm()
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	transaction = Transaction.query.filter_by(transactionowner_id=account.id).order_by(Transaction.date.desc()).all()
	trans = Transaction.query.filter_by(id=id).first()
	
	income = Transaction.query.filter_by(status="Income",transactionowner_id=account.id).all()
	expense = Transaction.query.filter_by(status="Expense",transactionowner_id=account.id).all()
	form.name.data = trans.name
	form.amount.data = trans.amount
	form.date.data = trans.date 
	form.status.data = trans.status		
	if form.validate_on_submit():
		date = datetime.strptime(request.form["date"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		amount = request.form["amount"]	
		jumlah = int(amount.replace(',',''))
		status = request.form["status"] 	
		

		trans.amount = jumlah
		trans.name = request.form["name"]
		trans.date = date 
		trans.status = status

		db.session.commit()		

		flash("Transaction successfully edited","success")
		return redirect(url_for("UserTransaction"))	

	return render_template("dashboard/edit.html",income=income,expense=expense,form=form,transaction=transaction,trans=trans,account=account)

@app.route("/dashboard/delete/transaction/<id>",methods=["GET","POST"])
@login_required
def DeleteTransaction(id):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	trans = Transaction.query.filter_by(id=id).first()			
				
	db.session.delete(trans)
	db.session.commit()

	flash("Transaction delete successfully","success")
	return redirect(url_for("UserTransaction"))






######################################################### Projects ################################################
@app.route("/dashboard/projects",methods=["GET","POST"])
@login_required
def AllProjects():
	account = Account.query.filter_by(accountowner_id=current_user.id).first()	
	projects = Projects.query.filter_by(projectsowner_id=account.id).all()
	total_ex = Transaction.query.filter(Transaction.transactionowner_id==account.id,Transaction.status=="Expense",Transaction.cashowner_id != "NULL").all() 
	total_in = Transaction.query.filter(Transaction.transactionowner_id==account.id,Transaction.status=="Income",Transaction.cashowner_id != "NULL").all() 
	form = AddProjectsForm()
	if form.validate_on_submit():
		amount = (form.revenue.data)
		revenue = int(amount.replace(',',''))		 
		projects = Projects(name=form.name.data,customer=form.customer.data,description=form.description.data,revenue=revenue,due_date=form.due_date.data,status="On Progress",projectsowner_id=account.id)
		db.session.add(projects)
		db.session.commit()

		return redirect(url_for("ProjectsId",id=projects.id))

	return render_template("projects/all.html",form=form,projects=projects,total_ex=total_ex,total_in=total_in,account=account)



@app.route("/dashboard/edit/projects/<id>",methods=["GET","POST"])
@login_required
def EditProjects(id):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	form = AddProjectsForm()
	project = Projects.query.filter_by(id=id).first()
	transaction = Transaction.query.filter_by(cashowner_id=project.id).all()
	total_ex = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Expense").all() 
	total_in = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Income").all() 
	form.name.data = project.name
	form.customer.data = project.customer
	form.description.data = project.description
	form.revenue.data = project.revenue
	form.due_date.data = project.due_date	
	if form.validate_on_submit():
		date = datetime.strptime(request.form["due_date"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		amount = request.form["revenue"]	
		jumlah = int(amount.replace(',',''))
		project.name = request.form["name"]
		project.customer = request.form["customer"]
		project.description = request.form["description"]
		project.revenue = jumlah
		project.due_date = date	

		db.session.commit()
		return redirect(url_for("ProjectsId",id=id))
	return render_template("projects/edit_project.html",account=account,project=project,form=form,transaction=transaction,total_ex=total_ex,total_in=total_in)	


@app.route("/dashboard/delete/project/<id>",methods=["GET","POST"])
@login_required
def DeleteProjects(token,id):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	project = Projects.query.filter_by(id=id).first()	
	total_ex = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Expense").all() 
	total_in = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Income").all() 
	
	delete_ex = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Expense").delete()
	delete_in = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Income").delete()
	
	db.session.delete(project)
	db.session.commit()	

	return redirect(url_for("AllProjects"))



@app.route("/dashboard/projects/<id>",methods=["GET","POST"])
@login_required
def ProjectsId(id):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	project = Projects.query.filter_by(id=id).first()
	transaction = Transaction.query.filter_by(cashowner_id=project.id).all()
	total_ex = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Expense").all() 
	total_in = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Income").all() 
	form = AddTransactionForm()
	if form.validate_on_submit():
		amount = (form.amount.data) 
		jumlah = int(amount.replace(',',''))
		status = form.status.data	
		trans = Transaction(amount=jumlah,name=form.name.data,date=form.date.data,status=status,cashowner_id=project.id,owner=current_user.id,transactionowner_id=account.id)
		
		db.session.add(trans)
		db.session.commit()

		return redirect(url_for("ProjectsId",id=id))	
			

	return render_template("projects/project.html",project=project,transaction=transaction,form=form,total_ex=total_ex,total_in=total_in,account=account)




@app.route("/dashboard/projects/edit/<id>/<transid>",methods=["GET","POST"])
@login_required
def EditProjectTransaction(id,transid):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	project = Projects.query.filter_by(id=id).first()
	trans = Transaction.query.filter_by(id=transid).first()
	transaction = Transaction.query.filter_by(cashowner_id=project.id).all()
	total_ex = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Expense").all() 
	total_in = Transaction.query.filter_by(cashowner_id=project.id).filter_by(status="Income").all() 
	form = AddTransactionForm()
	form.name.data = trans.name
	form.amount.data = trans.amount
	form.date.data = trans.date 
	form.status.data = trans.status
	if form.validate_on_submit():
		date = datetime.strptime(request.form["date"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		amount = request.form["amount"]	
		jumlah = int(amount.replace(',',''))	
		status = request.form["status"] 			

		trans.status = status		
		trans.amount = jumlah
		trans.name = request.form["name"]
		trans.date = date


		db.session.commit()

		return redirect(url_for("ProjectsId",id=id))
	return render_template("projects/edit_trans.html",account=account,project=project,transaction=transaction,form=form,trans=trans,total_ex=total_ex,total_in=total_in)	

 



@app.route("/dashboard/projects/delete/<id>/<transid>",methods=["GET","POST"])
@login_required
def DeleteProjectTransaction(id,transid):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	project = Projects.query.filter_by(id=id).first()
	trans = Transaction.query.filter_by(id=transid).first()
	
	db.session.delete(trans)
	db.session.commit()
	return redirect(url_for("ProjectsId",id=id))



























if __name__ == "__main__":
	app.run()







































