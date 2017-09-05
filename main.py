from flask import Flask, request, redirect, render_template, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO']=True
db= SQLAlchemy(app)
app.secret_key = 'y8696kkjf740jfv7B' #attach session cookie to particular application

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title= db.Column(db.String(120))
    body=db.Column(db.Text)    

    def __init__(self, title, body, owner):
        # self.completed= False
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120))
    # email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogpost=db.relationship('Blog', backref='owner')   ######

    def __init__(self, nameg, passwordw):
        self.name= nameg
        self.password= passwordw

@app.before_request
def require_login():
    allowed_routes=['login','allBlogs', 'actualPage','signup'] #inside are the same of the functions of the handler route
    if request.endpoint not in allowed_routes and 'name' not in session:
        return redirect('/login')

@app.route("/", methods=["GET"]) #is it both both or either?
def actualPage():
    x = User.query.all()
    return render_template('index.html', x= x)

@app.route("/newpost", methods=["POST","GET"])
def aNewPost():
    if request.method=='POST':
        mytitle= request.form['new_title']
        mypost= request.form['new_post']
        owner=User.query.filter_by(name=session['name']).first()

        if mytitle =="":
            flash("Must enter a title for blog", 'title')
        if mypost=="":
            flash("Must have content",'blogbody')
        if mytitle =="" or mypost=="":
            return redirect("/newpost")
        else:
            new_blog=Blog(mytitle, mypost,owner)
            db.session.add(new_blog)
  
            db.session.commit()
            the_id=str(new_blog.id)
            return redirect('/blog?id='+ the_id)

    return render_template("/newpost.html") # for a get method, displays form

   
@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method =='POST':
        author_name= request.form['username']
        password= request.form['password']
        verify= request.form['verify']

        name_require=""
        short_name=""
        short_password=""
        bad_password=""
        password_require=""

        error=False

        # TODO - validate user's data
        existing_user = User.query.filter_by(name=author_name).first()

        if existing_user:
            flash("User already exist.","exist")
            return redirect("/login")

        if author_name=="":
            flash("Must enter a name to register.","name_require")
            error = True
        if len(author_name)<3:
            flash("Invalid username ","short_name")
            error = True
        if len(password)<3:
            flash("Invalid password ","short_password")
            error = True
        if password!=verify:
            flash("Password does not match.","bad_password")
            error = True
        if password=="":
            flash("Must enter a password.","password_require")
            error = True
        if verify=="":
            flash("Must enter a password.","password_require")
            error = True

        if error:
            return render_template("/signup.html",name_require=name_require, short_name=short_name,
                                         short_password=short_password,bad_password=bad_password,
                                         password_require=password_require )
        
        
        if not existing_user or not error:
            new_user = User(author_name, password)
            db.session.add(new_user) # refers to session in data base
            db.session.commit() # refers to session in data base
            session['name']=author_name # keep session in browser cookie
            return redirect('/newpost')

    return render_template('/signup.html') # to view page initially and it is a get method

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        user_name=request.form['the_name']
        user_password=request.form['the_password']

        user=User.query.filter_by(name=user_name).first()
    #       the_id=Blog.query.filter_by(id)

        if user and user.password==user_password:
            session['name']=user_name
            # flash("Logged in")
            # print(session)

            return redirect('/newpost')
        if not user:
            flash("User does not exist","user_error")
            return render_template("/signup.html")
        elif user.password!=user_password:
            flash("User password is incorrect","password_er")

            return redirect('/login',the_name=user_error, the_password=password_er)  
    else: # it is a Get method
       return  render_template("login.html")


# @app.route("/blog", methods=["POST","GET"])


#     return render_template('blog.html', )


@app.route('/logout', methods=['GET'])
def logout():
    del session['name']
    return redirect('/blog')


@app.route('/blog', methods=['POST','GET'])
def allBlogs():
   # writer=User.query.filter_by(name=name).first()
    blog_id = request.args.get('id')
    user_id = request.args.get('user')
    if request.method == 'GET':
        if blog_id:
            blog_id = request.args.get('id')
            post = Blog.query.get(blog_id)
            primary_author=post.owner.name

            # print(post.owner.name)
            # print(post.owner.id)
            # print(post.owner.password)
            # print('##########')
            # print('##########')
            # print('##########')

            return render_template('singleUser.html',  single_blog =  post,the_author=primary_author)  
        # elif user:
        #     author=Blog.query.filter_by(owner_id=)
        if user_id:
            user = User.query.get(int(user_id))
            posts = user.blogpost
            return render_template('blog.html', total_blogs=  posts, the_author=user)
        # return render_template(‘blog.html’, blogs=blogs, title=user.username, blogger=user)
        else:
            total_blogs=Blog.query.all()   
            return render_template('blog.html',  total_blogs =  total_blogs)


if __name__=="__main__":
    app.run()