from flask import Flask, request, redirect, render_template, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:befitandactive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db= SQLAlchemy(app)
app.secret_key = 'y8696kkjf740jfv7B'

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(120))
    # owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title= db.Column(db.String(120))
    body=db.Column(db.Text)

    def __init__(self, title, body):
        # self.completed= False
        self.title = title
        self.body = body

# class User(db.Model):
#     id =db.Column(db.Integer,primary_key=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(120))
#     blogpost=db.relationship('Blog', backref='owner')

    # def __init__(self, email, password):
    #     self.email= email
    #     self.password= password

# @app.before_request
# def require_login():
#     allowed_routes=['login','register']
#     if request.endpoint not in allowed_routes and 'email' not in session:
#         return redirect('/blog')

@app.route("/", methods=["POST","GET"])
def actualPage():
    return redirect("/blog")

@app.route("/newpost", methods=["POST","GET"])
def aNewPost():
    if request.method=='POST':
        mytitle= request.form['new_title']
        mypost= request.form['new_post']

        if mytitle =="":
            flash("Must enter a title for blog", 'title')
        if mypost=="":
            flash("Must have content",'blogbody')
        if mytitle =="" or mypost=="":
            return redirect("/newpost")
        else:
            new_blog=Blog(mytitle, mypost)
            db.session.add(new_blog)
  
            db.session.commit()
            the_id=str(new_blog.id)
            return redirect('/blog?id='+the_id)

    return render_template("/newpost.html") # for a get method
#         user=User.query.filter_by(email=email).first()
# #       the_id=Blog.query.filter_by(id)
#         if user and user.password==password:
#             session['email']=email
#             flash("Logged in")
#             print(session)

#             return redirect('/blog')
#         else:
#             flash("User password incorrect, or user does not exist","error")
   


# @app.route("/blog", methods=["POST","GET"])
# def individualBlog():
#     if request.method =='POST':
#         the_title=Blog.query.filter_by(title)
#         the_body=Blog.query.filter_by(body)
#         total_blogs=Blog.query.filter_by(email=email)

#     return render_template('blog.html', )
# @app.route("/register", methods=["POST","GET"])
# def register():
#     if request.method =='POST':
#         email= request.form['email']
#         password= request.form['password']
#         verify= request.form['verify']

#         # TODO - validate user's data

#         existing_user=User.query.filter_by(email=email).first()
#         if not existing_user:
#             new_user = User(email, password)
#             db.session.add(new_user)
#             db.session.commit()
#             session['email']=email
#             return redirect('/blog')
#         else:
#             # TODO -user better response message
#             return "<h1>Duplicate user</h1>"

#     return render_template("/register.html")

# @app.route('/logout')
# def logout():
#     del session['email']
#     return redirect('/blog')


@app.route('/blog', methods=['POST','GET'])
def allBlogs():
    
    if request.method == 'GET':
        if request.args:
            id = request.args.get('id')
            blogpost=Blog.query.filter_by(id = id).first()
            return render_template('individualblog.html',  single_blog =  blogpost)

        else:
            total_blogs=Blog.query.all()   
            return render_template('blog.html',  total_blogs =  total_blogs)
#    owner=User.query.filter_by(email=session['email']).first()

    # if request.method=='POST':
    #     task_name = request.form["task"]
    #     new_task=Task(task_name, owner)

    #     db.session.add(new_task)
    #     db.session.commit()

    # blogpost=Blog.query.filter_by(completed=False, owner=owner).all()
    # completed_entry=Blog.query.filter_by(completed=True, owner=owner).all()

if __name__=="__main__":
    app.run()