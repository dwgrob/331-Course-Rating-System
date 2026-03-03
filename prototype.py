# Creating a sample python class to store different courses and reviews

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





if __name__ == "__main__":
    course1 = course(260, "CSCI", 2)
    course2 = course(261, "CSCI", 2)
    course3 = course(223, "MATH", 2)

    course1.createReview()
    course1.listReviews()
    course1.createReview()
    course2.createReview()
    course3.createReview()
    course1.listReviews()
    course2.listReviews()
    course3.listReviews()
