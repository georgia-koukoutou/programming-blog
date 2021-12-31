# CS50 Final Project - Programming Blog

The project implements a programming blog where users can create their own posts or view existing ones as well as comment and upvote or downvote.

Technologies used:

- Flask
- Sqlalchemy
- Sqlite3
- Other small libraries or packages

## How the blog works

To create posts you have to register as a user. During registration, you will need to enter these fields:

- Username
- Email
- Password: it is checked to match, must be at least 6 symbols long and is hashed after checks are done
- Password confirmation

If the username and the email you entered does not already exist and the two passwords match, an account is created with the information you entered (the password is hashed before it enters the database). You can then log in with your credentials and start posting, commenting and upvoting or downvoting. At any given moment you can change your account information and you can also upload a profile picture or write a bio.

You can also update the content of your posts or even delete them if you changed your mind.

The project is structured using Flak Blueprints to help with organizing code and separating functionality.

Amongst the most important folders and files are:

### Routes

Each route file defines model specific functions which can be triggered with HTTP requests (CRUD). Some routes require that the user is authenticated. 

### Database

The database stores users, posts, comments, tags and upvotes/downvotes. The tables are linked together using foreign keys.

### Models

The models file specifies all the different entities used by the application (users, posts, comments, tags, votes) and their relationship.

### Templates

The templates include all the HTML code for each page of the blog as well as some custom error pages I have created.

### Static

The static folder includes a CSS file (used in addition to Bootstrap 5's stylesheet) , a Javascript file and the profile pictures of the users. 

### Extras

Extra features present in the blog.

#### Remember me option

Prevents the user from accidentally being logged out when they close their browser. This is done using the Flask-Login extension, which creates a cookie that will be saved on the user’s computer, and then Flask-Login will automatically restore the user ID from that cookie if it is not in the session.

#### Post reading time calculation

The reading time of each post is calculated using Medium's algorithm, with the help of readtime's library. 

#### WYSIWYG HTML Editor

Helps users create more complex posts, by enabling the use of different font styles and sizes, lists, pictures and various other features.

#### Google trends

Presents the most popular google searches related to programming in general. 

#### Most viewed post

Presents the post with the most views, the name of the author and the date posted, with a direct link to visit the post.

#### Most popular tags

Users can click on each tag and read the posts that have been marked with this specific tag. 

## How to launch the application

1. Make sure you have Python version 3 installed
2. Clone the code: https://github.com/georgia-koukoutou/programming-blog.git
3. Open the application directory with `cd programming-blog`
4. Run application with `python3 run.py`
5. Open http://localhost:5000 
6. Enjoy blogging!

## Video presentation

You can find a video presentation of the application on: https://youtu.be/-BRkBzlfQE8 