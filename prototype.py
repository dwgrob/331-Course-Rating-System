# Creating a sample python class to store different courses and reviews
   


class review():

    def __init__(self, courseNum, courseYear, difficulty, workLoad, enjoyment):
        self.courseNum = courseNum
        self.courseYear = courseYear
        self.difficulty = difficulty
        self.workLoad = workLoad
        self.enjoyment = enjoyment

    def view(self):
        print("Course: ", self.courseNum)
        print("Year: ", self.courseYear)
        print("Difficulty: ", "*" * self.difficulty)
        print("WorkLoad: ", "*" * self.workLoad)
        print("Enjoyment: ", "*" * self.enjoyment)

    def addComment(self):
        self.comment = input("Enter your comment about the class: ")

    def viewComment(self):
        print(self.comment)



r1 = review(265, 2, 2, 4, 5)
r1.view()
r1.addComment()
r1.viewComment()





