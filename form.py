from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, SubmitField,FloatField,DecimalField
from wtforms.validators import InputRequired, EqualTo, Email, Length


class UserRegisterForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Email(),Length(max=100)])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])


class LoginForm(FlaskForm):
	email = StringField("Email",validators=[Email(),Length(max=100)])
	password = PasswordField("Password",validators=[InputRequired()])


class AddTransactionForm(FlaskForm):
	amount = StringField("Amount",validators=[InputRequired()])
	name = StringField("Description",validators=[InputRequired()])
	description = TextAreaField("Full Description (optional)")
	status = SelectField("Status",choices= [("Income","Income"),("Expense","Expense")])
	date = DateField("Date",format="%m/%d/%Y")

	
class EditTransactionForm(FlaskForm):	
	amount = StringField("Amount",validators=[InputRequired()])
	name = StringField("Description",validators=[InputRequired()])	
	date = DateField("Date",format="%m/%d/%Y")





class AddProjectsForm(FlaskForm):
	name = StringField("Project Name",validators=[InputRequired(),Length(max=100)])
	customer = StringField("Customer Name",validators=[InputRequired(),Length(max=100)])
	due_date = DateField("Date",format="%m/%d/%Y")
	description = TextAreaField("Projects Description") 	
	revenue = StringField("Estimate Revenue",validators=[InputRequired()])


class AddExpenseForm(FlaskForm):
	amount = StringField("Amount",validators=[InputRequired()])
	name = StringField("Description",validators=[InputRequired()])	
	date = DateField("Date",format="%m/%d/%Y")




