# 331-Course-Rating-System
CSCI 331 Course Rating Project

### Authors
Daniel Robinson and Spencer Strutt

## Requirements
 
- Python 3.x
 
## Setup
 
**1. Clone the repository**
```
git clone https://github.com/dwgrob/331-Course-Rating-System
cd your-repo-name
```
 
**2. Create and activate a virtual environment**
 
Windows:
```
python -m venv venv
venv\Scripts\activate
```
 
Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
 
**3. Install dependencies**
```
pip install -r requirements
```
 
**4. Run the app**
```
python3 app.py
```
 
**5. Open your browser and go to:**
```
http://127.0.0.1:5000
```
 
The database will be created automatically on first run with a few default courses already added.
 
## Pages
 
- `/` — Home page, lists all courses and their reviews
- `/createReview` — Form to leave a review for a course
- `/course` — Plain list of all courses and reviews
- `/login` — Placeholder login page (not yet implemented)
 
## Notes
 
- The database file (`courses.db`) is stored in the `instance/` folder and is not tracked by git
- Login/authentication is not yet implemented, it is just a placeholder for now
- The Generate Review button will generate 10 reviews for each course, and the Delete Reviews button will clear all of the reviews that have been made
