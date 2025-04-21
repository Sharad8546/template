from flask import Flask
from flask import render_template,bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf import StringField,PasswordField,selectField,SubmitField
from flask import Flask,render_template,redirect,url_for,flash,session
from wtForms.Validators import DataRequired

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///library.db'

db=SQLAlchemy(app)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    user_name=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)
    DOB=db.Column(db.DateTime,nullable=True)
    role=db.Column(db.String(20),default="student",nullable=False)

    def __repr__(self):
        return f'<User{self.User}>'
class Book(db.Model):
    Bookname=db.Column(db.String(80),nullable=False)
    Book_ID=db.Column(db.Integer,primary_key=True)
    Author=db.Column(db.String(50),nullable=False)
    category=db.Column(db.String(25),nullable=True)
    published_year=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Float,nullable=False)
    review=db.Column(db.String(150),nullable=True)
    ratings=db.Column(db.Integer,nullable=True)

class Service(db.Model):
    s_id=db.Column(db.Integer,primary_key=True)

    user=db.relationship('User',foreign_keys=['user.id'],backref='User')
    
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    Book_id=db.Column(db.Integer,db.ForeignKey('book.Book_ID'),nullable=False)
    Issue_date=db.Column(db.DateTime,nullable=False)
    return_date=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(25),default=False)

class studentRegistrationForm(FlaskForm):
    Username=StringField('Username',validators=[DataRequired()])
    Password=PasswordField('Password',validators=[DataRequired()])
    role=selectField('Role',choices=[('user','user')],validators=[DataRequired])
    submit=SubmitField('Register')

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired])
    Password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

class ServicerequestForm(FlaskForm):
    Username=StringField('username',validators=[DataRequired()])
    Password=PasswordField('Password',validators=[DataRequired()])
    role=selectField('Role',choices=[('user','user')],validators=[DataRequired])
    submit=SubmitField('Login')

class UpdateForm(FlaskForm):
    Username=StringField('username',validators=[DataRequired()])
    Password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

class editbookform(FlaskForm):
    Usernmae=StringField('username',validators=[DataRequired()])
    Password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

@app.route('/')
def home():

    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/register")
def reg():
    return render_template("register.html")

@app.route("/add_book")
def add_book():

    return render_template("add_book.html")

@app.route("/edit_book")
def edit_book():
    return render_template("edit_book.html")

@app.route("/edit_category")
def edit_category():
    return render_template("edit_category.html)

@app.route("/add_category")
def add_category():
    return render_template("add_category.html")

@app.route('/register',methods=['GET','POST'])
def register_user():
    form=studentRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user=User(username=form.username.data, password_hash=hashed_password,role='User',is_approved=False)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'Regsitraion successfull for {form.username.data} as a user awaiting for Admin approval','info')
            return redirect(url_for('login'))
        except:
            flash("Error:User Name already Exists",'danger')
            db.session.rollback()
    return render_template('register.html',form=form)

@app.route('/service',methods=['GET','POST'])
def servicerequest():
    form=ServicerequestForm()
    if form.validate_on_submit():
        def user_approve(user_id):
            if session.get('role')!='user':
                flash('Access denied. User only','danger')
                return redirect(url_for('home'))
user=user.name.query.get_or_404(user.id)


@app.route('/Login',method=['GET','POST'])
def Login_user():
    form=LoginForm()
    if form.validate_on_submit():
        def user_approve(user_id):
            if session.get('role')!='user':
                flash('Access denied.User only','danger')
                return redirect(url_for('home'))
    user=user.query.get_or_404(user.id)
    if user.role=='user' and user.is_approved:
        user.is_approved=True
        db.session.commit()
        flash(f'user has been approed as user','Sucess')
        try:
            db.session.add(servicerequest)
            db.session.commit()
            flash(f'Service request created for {form.user_id.data} waiting for Librarian approval','info')
            return redirect(url_for('login'))
        except:
            flash('Error:Service request not created')
            db.session.rollback()
            return render_template('home.html',form=form)

@app.route('/add_book',methods=['GET','Post'])
form=UpdateForm()
if form.validate_on_submit():
    def updateeBook(Service_id):
        if session.get('role')!='admin':
            flash('Access denied.Admins only','danger')
            return redirect(url_for('home'))
        Service=Service.query.get_or_404(Service_id)
        form=ServicerequestForm(obj=Service)

@app.route('/edit-book',methods=['GET','POST'])
def editbook(bookid):
    if session.get('role')!='admin':
        flash('Acess denied,Admins only','danger')
        return redirect(url_for('home'))
    form=editbookform()
    if form.validate_on_submit:
        db.session.commit()
        flash('book can be updated now')
        try:
            db.session.add(editbook)
            db.session.commit()
            flash('books has been editd Sucessfully','danger')
            return redirect(url_for('home'))
    return render_template('edit_book.html',form=form)


@app.route('/deletebook',methods=['GET','POST'])
def deletebook(bookid):
    if session.get('role')!='Admin':
        flash('Access denied only Admimn can','danager')
        return redirect(url_for('home'))
    Book=book.query.get_or_404(bookid)
    db.session.delete(bookid)
    db.session.commit()
    flash(f'{book.name}has been deleted','danger')
    return render_template('deletebook.html',form=form)

@app.route('/add_category',methods=['GET','POST'])
def addcategory():
    if session.get('role')!='Admin':
        flash('Acess denied only AdimnCan','danger')
        return redirect(url_for('home'))
    
    form=addcategory()
    if form.validate_on_submit:
        db.session.commit()
        flash('category added')
        try:
            db.session.add(add_category)
            db.session.commit()
            flash('category updated','danger')
            return redirect(url_for('add_category'))
    return render_template('add_category.html',form=form)

@app.route('/editcategory',method=['GET','POST'])
def editcategory():
    if session.get('role')!='Admin':
        flash('Acess denied only Admins can','danger')
        return redirect(url_for('home'))
    form=editcategory()
    if form.validate_on_submit():
        db.session.commit()
        flash('category can be edited')
        try:
            db.session.add(editcategory)
            db.session.commit()
            flash('Category edited Suceesfully','danger')
            return redirect(url_for('edit_category.html',form=form))
        

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
