from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # course number e.g. 311
    program = db.Column(db.String(32), nullable=False)  # e.g. CSCI
    courseYear = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('ReviewModel', backref='course', cascade='all, delete-orphan', lazy=True)

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


class ReviewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course_model.id'), nullable=False)
    difficulty = db.Column(db.Integer)
    workLoad = db.Column(db.Integer)
    enjoyment = db.Column(db.Integer)
    comment = db.Column(db.Text)


def seed_courses():
    db.create_all()
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


def get_courses():
    courses = {}
    for c in CourseModel.query.order_by(CourseModel.program, CourseModel.id).all():
        courses[c.id] = c
    return courses


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

        course = db.session.get(CourseModel, course_num)
        if not course:
            return "Course not found", 400

        rev = ReviewModel(course_id=course.id, difficulty=difficulty, workLoad=workload, enjoyment=enjoyment, comment=comment)
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


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    with app.app_context():
        seed_courses()
    app.run(debug=True)