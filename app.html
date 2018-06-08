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
from form import UserRegisterForm,LoginForm,AddTransactionForm,EditTransactionForm,AddProjectsForm,AddExpenseForm
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
	expense = db.Column(db.BigInteger())
	profit = db.Column(db.BigInteger())
	expenseowner = db.relationship("Transaction",backref="expenseowner",lazy="dynamic") 
	projectsowner_id = db.Column(db.Integer(), db.ForeignKey("account.id"))




class Transaction(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(300))
	amount = db.Column(db.BigInteger())	
	status = db.Column(db.String(200))
	date = db.Column(db.DateTime())	
	owner = db.Column(db.Integer())
	expenseowner_id = db.Column(db.Integer(), db.ForeignKey("projects.id"))
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




###################################################### Transaction ###########################################

@app.route("/dashboard/<token>",methods=["GET","POST"])
@login_required
def UserDashboard(token):	
	form = AddTransactionForm()
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	transaction = Transaction.query.filter_by(transactionowner_id=account.id).order_by(Transaction.date.desc()).all()
	balance = account.amount
	income = Transaction.query.filter_by(status="Income",transactionowner_id=account.id).all()
	expense = Transaction.query.filter_by(status="Expense",transactionowner_id=account.id).all()
	if form.validate_on_submit():		
		amount = (form.amount.data)
		jumlah = int(amount.replace(',',''))
		status = form.status.data	
		trans = Transaction(amount=jumlah,name=form.name.data,description=form.description.data,date=form.date.data,status=status,owner=current_user.id,transactionowner_id=account.id)
		if status == "Income" :
			account.amount = account.amount + jumlah
		elif status == "Expense":
			account.amount = account.amount - jumlah
		else :
			return "no access"		

		db.session.add(trans)
		db.session.commit()

		flash("Transaction successfully added","success")
		return redirect(url_for("UserDashboard",token=current_user.token))		
	return render_template("dashboard/transaction.html",balance=balance,income=income,expense=expense,form=form,token=token,transaction=transaction)




@app.route("/dashboard/<token>/<id>",methods=["GET","POST"])
@login_required
def EditTransaction(token,id):	
	form = AddTransactionForm()
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	transaction = Transaction.query.filter_by(transactionowner_id=account.id).order_by(Transaction.date.desc()).all()
	trans = Transaction.query.filter_by(id=id).first()
	balance = account.amount
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
		if trans.expenseowner_id is None:
			if trans.status == "Income" and status == "Income" :
				#Kurangi total saldo dengan jumlah income sebelum di edit 
				account.amount = account.amount - trans.amount + jumlah
			elif trans.status == "Income" and status == "Expense":
				account.amount = account.amount - trans.amount - jumlah
			elif trans.status == "Expense" and status == "Expense":
				account.amount = account.amount + trans.amount - jumlah					
			else :
				#Kurangi total saldo dengan jumlah expense sebelum di edit 	
				account.amount = account.amount + trans.amount + jumlah
			
		else :
			project = Projects.query.filter_by(id=trans.expenseowner_id).first()
			if trans.status == "Income" and status == "Income" :
				#Kurangi total saldo dengan jumlah income sebelum di edit 
				account.amount = account.amount - trans.amount + jumlah
				project.profit = project.profit - trans.amount + jumlah

			elif trans.status == "Income" and status == "Expense":			
				account.amount = account.amount - trans.amount - jumlah
				project.profit = project.profit - trans.amount - jumlah

			elif trans.status == "Expense" and status == "Expense":		
				account.amount = account.amount + trans.amount - jumlah
				project.profit = project.profit + trans.amount - jumlah

			else :
				#Kurangi total saldo dengan jumlah expense sebelum di edit 				
				account.amount = account.amount + trans.amount + jumlah
				project.profit = project.profit + trans.amount + jumlah

		trans.amount = jumlah
		trans.name = request.form["name"]
		trans.date = date 
		trans.status = status

		db.session.commit()		

		flash("Transaction successfully edited","success")
		return redirect(url_for("UserDashboard",token=token))	

	return render_template("dashboard/edit.html",balance=balance,income=income,expense=expense,form=form,token=token,transaction=transaction,trans=trans)

@app.route("/dashboard/<token>/delete/<id>",methods=["GET","POST"])
@login_required
def DeleteTransaction(token,id):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	trans = Transaction.query.filter_by(id=id).first()
	if trans.expenseowner_id is None:
		if trans.status == "Income":
			#kurangi saldo dengan income yg di hapus
			account.amount = account.amount - trans.amount
		else :
			#tambah saldo dengan expense yg di hapus
			account.amount = account.amount + trans.amount
	else :
		project = Projects.query.filter_by(id=trans.expenseowner_id).first()
		if trans.status == "Expense":
			account.amount = account.amount + trans.amount		
			project.profit = project.profit + trans.amount
		else :
			account.amount = account.amount - trans.amount		
			project.profit = project.profit - trans.amount
			

		
		
	db.session.delete(trans)
	db.session.commit()

	flash("Transaction delete successfully","success")
	return redirect(url_for("UserDashboard",token=token))







######################################################### Projects ################################################
@app.route("/dashboard/<token>/projects",methods=["GET","POST"])
@login_required
def AllProjects(token):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()	
	projects = Projects.query.filter_by(projectsowner_id=account.id).all()
	form = AddProjectsForm()
	if form.validate_on_submit():
		amount = (form.revenue.data)
		revenue = int(amount.replace(',',''))		 
		projects = Projects(name=form.name.data,customer=form.customer.data,description=form.description.data,revenue=revenue,due_date=form.due_date.data,expense=0,profit=0,status="On Progress",projectsowner_id=account.id)
		db.session.add(projects)
		db.session.commit()

		return redirect(url_for("ProjectsId",id=projects.id,token=token))

	return render_template("projects/all.html",form=form,projects=projects)


@app.route("/dashboard/<token>/projects/<id>",methods=["GET","POST"])
@login_required
def ProjectsId(id,token):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	project = Projects.query.filter_by(id=id).first()
	expenses = Transaction.query.filter_by(expenseowner_id=project.id).all()
	total_ex = Transaction.query.filter_by(expenseowner_id=project.id).filter_by(status="Expense").all() 
	total_in = Transaction.query.filter_by(expenseowner_id=project.id).filter_by(status="Income").all() 
	form = AddTransactionForm()
	if form.validate_on_submit():
		amount = (form.amount.data) 
		jumlah = int(amount.replace(',',''))
		status = form.status.data	
		trans = Transaction(amount=jumlah,name=form.name.data,date=form.date.data,status=status,expenseowner_id=project.id,owner=current_user.id,transactionowner_id=account.id)
		if status == "Income" :
			account.amount = account.amount + jumlah
			project.profit = project.profit + jumlah
		elif status == "Expense":
			account.amount = account.amount - jumlah
			project.profit = project.profit - jumlah
		else :
			return "no access"		

		db.session.add(trans)
		db.session.commit()

		return redirect(url_for("ProjectsId",id=id,token=token))	
			

	return render_template("projects/project.html",project=project,expenses=expenses,form=form,total_ex=total_ex,total_in=total_in)




@app.route("/dashboard/<token>/projects/edit/<id>/<expenseid>",methods=["GET","POST"])
@login_required
def EditProjects(id,token,expenseid):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	project = Projects.query.filter_by(id=id).first()
	expense = Transaction.query.filter_by(id=expenseid).first()
	expenses = Transaction.query.filter_by(expenseowner_id=project.id).all()
	total_ex = Transaction.query.filter_by(expenseowner_id=project.id).filter_by(status="Expense").all() 
	total_in = Transaction.query.filter_by(expenseowner_id=project.id).filter_by(status="Income").all() 
	form = AddTransactionForm()
	form.name.data = expense.name
	form.amount.data = expense.amount
	form.date.data = expense.date 
	form.status.data = expense.status
	if form.validate_on_submit():
		date = datetime.strptime(request.form["date"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		amount = request.form["amount"]	
		jumlah = int(amount.replace(',',''))	
		status = request.form["status"] 
		
		if expense.status == "Income" and status == "Income" :
			#Kurangi total saldo dengan jumlah income sebelum di edit 
			account.amount = account.amount - expense.amount + jumlah
			project.profit = project.profit - expense.amount + jumlah

		elif expense.status == "Income" and status == "Expense":			
			account.amount = account.amount - expense.amount - jumlah
			project.profit = project.profit - expense.amount - jumlah

		elif expense.status == "Expense" and status == "Expense":		
			account.amount = account.amount + expense.amount - jumlah
			project.profit = project.profit + expense.amount - jumlah

		else :
			#Kurangi total saldo dengan jumlah expense sebelum di edit 				
			account.amount = account.amount + expense.amount + jumlah
			project.profit = project.profit + expense.amount + jumlah


		expense.status = status		
		expense.amount = jumlah
		expense.name = request.form["name"]
		expense.date = date


		db.session.commit()

		return redirect(url_for("ProjectsId",id=id,token=token))
	return render_template("projects/edit_expense.html",project=project,expenses=expenses,form=form,expense=expense,total_ex=total_ex,total_in=total_in)	

 



@app.route("/dashboard/<token>/projects/delete/<id>/<expenseid>",methods=["GET","POST"])
@login_required
def DeleteExpense(id,expenseid,token):
	account = Account.query.filter_by(accountowner_id=current_user.id).first()
	project = Projects.query.filter_by(id=id).first()
	expense = Transaction.query.filter_by(id=expenseid).first()
	if expense.status == "Expense":
		account.amount = account.amount + expense.amount		
		project.profit = project.profit + expense.amount
	else :
		account.amount = account.amount - expense.amount		
		project.profit = project.profit - expense.amount
		

	db.session.delete(expense)
	db.session.commit()
	return redirect(url_for("ProjectsId",id=id,token=token))






























if __name__ == "__main__":
	app.run()







































