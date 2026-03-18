from flask import Flask, render_template

class review:
    
    def createReview(self):
        self.difficulty = input("How difficult was the course on a scale from 1-5:")
        self.workLoad = input("How was the workload on a scale from 1-5:")
        self.enjoyment = input("How much did you enjoy the course on a scale from 1-5:")
        self.comment = input("Any additional comments:")



class course():
    def __init__(self, courseNum: int, program: str, courseYear: int):
        self.courseNum = courseNum
        self.program = program
        self.courseYear = courseYear
        self.reviewList = []
    
    def createReview(self):
        print("For the course", self.courseNum, ":")
        newReview = review()
        newReview.createReview()
        self.reviewList.append(newReview)

    def listReviews(self):
        print("The reviews for the course", self.courseNum, ":")
        for review in self.reviewList:
            print("Difficulty:", review.difficulty)
            print("Enjoyment:", review.enjoyment)
            print("Workload:", review.workLoad)
            print("Comment:", review.comment)




app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/createReview')
def createReview():
    course311 = course(311, 'CSCI', 3)
    course370 = course(370, 'CSCI', 3)
    course260 = course(260, 'CSCI', 2)
    course265 = course(265, 'CSCI', 2)
    
    
    
    return render_template("createReview.html")


@app.route('/course')
def courseRev():
    return render_template("reviewsPage.html")

if __name__ == '__main__':
    app.run()