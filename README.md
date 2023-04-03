# SIGHTS ON BIKES 50 PROJECT
## Video Demo:  <URL HERE>
## Description:
I currently have a bike tour in Mexico City and that tour until now lives exclusively on Airbnb I feel that I can promote it better if a have a webpage for that, so for my final project in **CS50** I decided to make a web page for my tour.
### Implementation:

### Language:

I decide to use *HTML*, *CSS*, *Python*, *flask*, and *Jinja* for this web app.

### Content:

As a *flask* web app, it has:

#### *static* folder where all the *images* and *icons* are located and also includes a file call *styles.css* with all the CSS formatting used in the web app

#### *templates* folder where all the "templates" of the web pages used in the web app are located including *book.html*, *index.html*, *insta.html*, *reviews.html*, and also one called *layout.html* which is the main template for the rest of the pages.

#### *app.py* which is the file that implements how the web app behaves and is written in *Python*

## Explanation:

### static folder includes:

#### all the images
#### all the icons
#### a file called styles.css where are defined all the formats (size, color, alignment, etc.) of the web app

For example defines the background-color: `rgba(208, 126, 255, 0.623)`

### templates folder includes:

#### index.html
Is the *main* page of the web app, it shows a carousel-type gallery made with *CSS* with 50 pictures of the tour, it also has a drop-down menu list and when you choose one of the options it displays on the same web page but below the carousel also displays the information related to that option, the following are the elements available to choose from:

##### What you'll do...

Displays a general description and information of the tour-

##### Where we'll meet...

Displays a Google map inside an "iframe" tag showing the meeting point for the tour.

##### Where you'll be...

Displays an unordered list of the sights that we are going to visit on the tour, and 5 pictures of guests at some of those attractions.

##### Meet your Host...

Displays some information about myself and how I started this tour, and a picture of me on a bike tour.

At the end displays a note about the Length of the tour.

#### layout.html

It is the template for all web pages in the web app and at the beginning of the page it states that is an HTML doc in English after the:

##### head

###### Sets the ASCII "UTF-8" code 
###### Makes the webpage responsive using *CSS*
###### Imports *bootstrap 5.1*
###### Defines the *favicon* to be a bicycle
###### links to the style.css locally for *CSS* format
###### defines the first part of the *title*
###### loads some scripts for JavaScript and for Airbnb specifically

##### body

First, it defines the navigation bar at the top of the pages with the name of the web app and links to all the web pages

###### main using Jinja calls the specific blocks to be displayed for individual web pages, even using an *if statement* for the index.html page according to the *selection* in the drop-down menu.

###### footer displays a contact link through Instagram and displays an Instagram icon


#### book.html

Using the extent layout.html Jinja command uses the same template as all the other web pages and using an embed code from Airbnb gives us the option to book a tour showing the available dates.

#### reviews.html


Also, use the layout.html template to give the same format to the web pages and in this case uses an embed code from Common Ninja to display the last 5 reviews.

#### insta.html 

Also, use the layout.html template to give the same format to the web pages and in this case, uses an *iframe* to display the *Instagram* page of my tour.

### app.py

#### Imports flask and bootstrap5
#### Defines this file (app.py as the app) 
#### Redefines bootstrap as bootstrap5
#### Define how the app suppose to do in case it gets a *get* or a *post* request in each one of the web pages
#### tells the app to do it when is running

### README.md

Is this file and is an explanation of how the web app works using .md

### requirements.txt

Minimal software is required in the server to run this web app.