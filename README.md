

# Module 1 Group Assignment

CSCI 5117, Spring 2024, [assignment description](https://canvas.umn.edu/courses/413159/pages/project-1)

## App Info:

* Team Name: The Boys
* App Name: Stock Up
* App Link: <https://project-1-the-boys.onrender.com/>

### Students

* Brayden Doyle doyle472@umn.edu
* Maurice Yu yu000464@umn.edu


## Key Features

**Describe the most challenging features you implemented


* One of the things that was interesting to work with was the stock API usage, free plans are kind of rough (understandably) and like 6 different stock API's were used throughout development.
* Considering that we were only 2 people there was not much beyond the base reqs so not much to say here

## Testing Notes

**Is there anything special we need to know in order to effectively test your app? (optional):**
All editing and deleting of posts should be done from the mainpage

* ...


## Screenshots of Site

**[Add a screenshot of each key page (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository)
along with a very brief caption:** (Brevity is a rather large weakness of mine... sorry!)

![](https://media.giphy.com/media/o0vwzuFwCGAFO/giphy.gif)
![Mainpage](/static/images/final_mainpage.PNG)
Mainpage basically has three columns, left one is a stock viewer that allows you to query any stock in the S&P 500 and display the most recent closing data. Center column displays post initially based on upload time (Most recent first) and has a search bar with functionality based on post content. The third column contains a list of stocks within the S&P 500 list, it allows the user to follow or view the stock in the left column. Each ticker is linked to Yahoo finance where the user can find more data.

![Profile](/static/images/final_profile_page.PNG)
The user profile became rather barebones and as such it only displays username, user picture, and all user posts. Profiles can be navigated to by clicking on another users profile picture.

![Sidebar](/static/images/sidebar.PNG)
Not a page but quick explanation of the sidebar navigation. Rather small due to limited options but from top to bottom it goes "Logo" and Home link to "/". + button pulls up the create post popup, non-users who try to submit a post are instead redirected to user sign-in page. Final button contains user profile picture (default for non-users) and links to the user page "/profile" (user sign-in for non-users).

There originally were more pages that focused on each of the columns of mainpage but it seemed rather redundant as the mainpage ties everything together. (hence why Mainpage section is rather long)
## Mock-up 

There are a few tools for mock-ups. Paper prototypes (low-tech, but effective and cheap), Digital picture edition software (gimp / photoshop / etc.), or dedicated tools like moqups.com (I'm calling out moqups here in particular since it seems to strike the best balance between "easy-to-use" and "wants your money" -- the free teir isn't perfect, but it should be sufficient for our needs with a little "creative layout" to get around the page-limit)

In this space please either provide images (around 4) showing your prototypes, OR, a link to an online hosted mock-up tool like moqups.com

**[Add images/photos that show your paper prototype (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository) along with a very brief caption:**

![](https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif)


## External Dependencies

**Document integrations with 3rd Party code or services here.
Please do not document required libraries. or libraries that are mentioned in the product requirements**

* Library or service name: description of use
* ...
Yahoo finance is linked through the stock table
Polygon API is used within the stock viewer
Clearbit logo API is used within the stock viewer
**If there's anything else you would like to disclose about how your project
relied on external code, expertise, or anything else, please disclose that
here:**

...



Mockup photos
![Homepage](/static/images/landingpage.JPG)

This is our stock application homepage. The application itself is leaning towards more of a *stock tips* direction instead of trading so there are social media elements. The homepage shows trending user posts, and two sections of stock data that is yet to be decided (possibly set by the user). The top left has the placeholder name of the site "Stock Up", the user will be prompted to create an account if not logged in or taken to the home page. The home button will redirect the user to the / landing page.  When you click the profile picture popup, the buttons will redirect the user to OAUTH. If a user is logged in and the click the profile picture, they will be redirected to their profile page. If a user is logged in, there will be a button to create a post (like on the left). When a user makes a search, the trending posts section is replaced by the results. Each post has the ability to be liked by logged in users.
![Create Post](/static/images/post.JPG)
Create post view.
![Profile Page](/static/images/sideprofile.JPG)
This is how viewing user profiles will look, the left is a logged in user looking at their own account and the right is otherwise. We do intend to allow the user to set their picture and edit their account information. Content created by a user can be edited/deleted through their profile page while logged in.


![Profile Page](/static/images/figma_edit_profile.JPG)
this is the page if you click the edit gear icon

![Profile Page](/static/images/figma_signup_with_stuff.JPG)
this is if you click the main page without being signed in. clicking signup will redirect to oauth which callback will be the edit profile


