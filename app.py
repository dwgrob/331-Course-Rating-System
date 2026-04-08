from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_security import SQLAlchemySessionUserDatastore, RoleMixin
from better_profanity import profanity


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "secretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)


#The database model for the course
class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # course number e.g. 311
    program = db.Column(db.String(32), nullable=False)  # e.g. CSCI
    courseYear = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('ReviewModel', backref='course', cascade='all, delete-orphan', lazy=True)

    #funtion to get average rating to us for the display
    def average_ratings(self):
        if not self.reviews:
            return {'difficulty': None, 'workLoad': None, 'enjoyment': None}
        count = len(self.reviews)
        avg_d = sum(r.difficulty for r in self.reviews) / count
        avg_w = sum(r.workLoad for r in self.reviews) / count
        avg_e = sum(r.enjoyment for r in self.reviews) / count
        return {
            'difficulty': round(avg_d, 1),
            'workLoad': round(avg_w, 1),
            'enjoyment': round(avg_e, 1)
        }


#Database model for the reviews
class ReviewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course_model.id'), nullable=False)
    difficulty = db.Column(db.Integer)
    workLoad = db.Column(db.Integer)
    enjoyment = db.Column(db.Integer)
    comment = db.Column(db.Text)
    writer = db.Column(db.String(50), nullable=False)

#table to connect users and their roles
roles_users = db.Table('roles_users', 
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )

#Database model for users
class Users(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
    def is_admin(self):
        return any(role.name == 'Admin' for role in self.roles)

#Database model for Roles
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

user_datastore = SQLAlchemySessionUserDatastore(db.session, Users, Role)

#Preparing the database for when the app starts
with app.app_context():
    db.create_all()

#Creats the default courses once when the app first starts
def seed_courses():
    default_courses = [
        (311, 'CSCI', 3),
        (370, 'CSCI', 3),
        (260, 'CSCI', 2),
        (265, 'CSCI', 2),
        (111, 'MATH', 1),
        (115, 'ENG', 1),
    ]
    for cid, prog, yr in default_courses:
        if not db.session.get(CourseModel, cid):
            db.session.add(CourseModel(id=cid, program=prog, courseYear=yr))
    db.session.commit()

#Creats the roles for when the app first starts
def create_roles():
    if not Role.query.filter_by(name='Admin').first():
        db.session.add(Role(id=1, name='Admin'))
    if not Role.query.filter_by(name='user').first():
        db.session.add(Role(id=2, name='user'))
    db.session.commit()


def get_courses():
    courses = {}
    for c in CourseModel.query.order_by(CourseModel.program, CourseModel.id).all():
        courses[c.id] = c
    return courses

#Script to populate the database with some reviews
def genRandomReviews(numReviews=10):
    courses = CourseModel.query.all()

    comments = [
        "Was a Blast!!",
        "Was so hard!!",
        "I learned so much.",
        "Wait this isn't rate my professor.",
        "I think that this course was super useful for my future career.",
        "This class was useless!!",
        "Was a hard course but I am a better person because of it."
    ]

    for course in courses:
        for _ in range(numReviews):
            review = ReviewModel(
                course_id=course.id,
                difficulty=random.randint(1, 5),
                workLoad=random.randint(1, 5),
                enjoyment=random.randint(1, 5),
                comment=random.choice(comments),
                writer='Admin'
            )
            db.session.add(review)
    db.session.commit()

#Deletes all the reviews
def clearReviews():
    ReviewModel.query.delete()
    db.session.commit()

#Helps verify someone is logged in
@login_manager.user_loader
def loadUser(user_id):
    return Users.query.get(int(user_id)) 

@app.route('/')
def home():
    courses = get_courses()
    return render_template('home.html', courses=courses)


@app.route('/createReview', methods=['GET', 'POST'])
def createReview():
    courses = get_courses()

    if request.method == 'POST':
        course_num = int(request.form['course'])
        difficulty = int(request.form.get('difficulty', 0))
        workload = int(request.form.get('workload', 0))
        enjoyment = int(request.form.get('enjoyment', 0))

        # make sure ratings are valid
        if not (1 <= difficulty <= 5 and 1 <= workload <= 5 and 1 <= enjoyment <= 5):
            return "Ratings must be between 1 and 5", 400

        comment = request.form.get('comment', '')
        if profanity.contains_profanity(comment): ##if swear, delete comment
            comment = ''
       
        # comment = profanity.censor(comment, '****') ##REPLACES PROFANITY 

        course = db.session.get(CourseModel, course_num)
        if not course:
            return "Course not found", 400

        rev = ReviewModel(course_id=course.id, difficulty=difficulty, workLoad=workload, enjoyment=enjoyment, comment=comment, writer=current_user.username)

        db.session.add(rev)
        db.session.commit()

        return redirect(url_for('home'))

    # pre-select a course if one was passed in the URL
    selected = None
    if request.args.get('course'):
        selected = int(request.args.get('course'))

    return render_template('createReview.html', courses=courses, selected_course=selected)


@app.route('/course')
def courseRev():
    courses = get_courses()
    return render_template('reviewsPage.html', courses=courses)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template('login.html')



@app.route('/generateReviews', methods=['GET', 'POST'])
def genReviews():
    genRandomReviews(10)
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if not current_user.is_admin():
        return "Unauthorized", 403
    reviewtoDelete = ReviewModel.query.get(int(id))
    try:
        db.session.delete(reviewtoDelete)
        db.session.commit()
        return redirect('/')
    except:
        return "Couldn't delete review"

@app.route('/clearReviews', methods=['GET', 'POST'])
def delReviews():
    clearReviews()
    return redirect(url_for('home'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if Users.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already taken!")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username=username, password=hashed_password)
        role = Role.query.filter_by(id=int(request.form['options'])).first()
        if role:
            new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == '__main__':
    with app.app_context():
        seed_courses()
        create_roles()
    app.run(debug=True)