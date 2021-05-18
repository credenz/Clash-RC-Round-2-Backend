# CLASH ROUND 2 ONLINE JUDGE:
<p> This platform was developed & deployed successfully for hosting Clash- An event part of the annual techfest Credenz under the PICT IEEE Stident Branch (PISB).</p>
<p>

So, here is a quick guide for setup on your PC and host run this platform locally.

### 1) Clone the project onto your local Machine (from the fullnfinal branch).

### 2) Create a virtual environment and install the required packages.

install python3-env and pip for creating a envirnoment.

	sudo apt-get install python3-venv python3-pip

create a virtual envirnoment:

	python3 -m venv env

activate this virtual envirnoment:

	source env/bin/activate

installing all required packages which are present in requirement.txt:

	pip install -r requirements.txt
#Note:
For installing all the sandboxing packages (i.e required for compilation and running the user's code), run the script seccomp.sh by command:
sh seccomp.sh


### 3) Running the code Setting up timer and starting game

Run this application by command:

	python manage.py runserver

Note: before running the above command, head over to userApp/views.py and set the end variable (line 22) as per the end time you wish to set for the contest to end.


</p>
</details>

## A Glimpse of the User Interface:
#### 1) Login Page -
![Login Page](./screenshots/login.png)

### 2) Instructions Page -
![Instructions Page](./screenshots/instructions.png)

### 3) Coding Page -
![codingpage.png](./screenshots/codingpage.png)

### 4) LeaderBoard -
![leaderboard.png](./screenshots/leaderboard.png)

### 5) Question Page -
![questionhub.png](./screenshots/questionhub.png)

### 6) Results Page -
![resultpage.png](./screenshots/resultpage.png)

### 7) Submissions Page -
![submissions.png](./screenshots/submissions.png)

### 8) Testcase Evaluation Page -
![testcases.png](./screenshots/testcases.png)
