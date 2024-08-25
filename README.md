# Skincare Journal

A Skincare Journal is a straightforward app designed to help users manage their skincare routines. 

As a skincare enthusiast, I've noticed that it can be challenging to keep track of all the products in my routine, especially when some are used only a few times a week, while others are designated for specific times like morning or evening.

Initially, I had the idea of creating an app that would leverage APIs to do more than just help users track their skincare routines. My goal was to design a platform that could also offer personalized product recommendations and direct users to purchase the products they need. 
The inspiration for this project came from my passion for skincare, and I saw this as an opportunity to build something that could genuinely enhance the skincare experience for others. I wanted to combine technology with my interest in skincare to create a tool that would be both practical and enjoyable for users. 

However, I encountered challenges in finding APIs that would be suitable for my app, and that is how I decided to develop a Skincare Journal instead, leaving the door open for my initial idea. 

![Responsiveness]()

## Rationale and Purpose

### Why a Skincare Routine Tracker?
Maintaining a consistent and effective skincare routine can be challenging, especially for those new to skincare or looking to optimize their regimen. I recognized a gap in accessible tools that could guide users through this process.

### The Problem:
1. Product Confusion: With a plethora of skincare products available, it can be overwhelming to remember what products to use.

2. Timing and Order: The effectiveness of skincare products can depend significantly on the order of application and the time of day they are used.

3. Product Incompatibility: Certain skincare ingredients should not be mixed due to potential adverse reactions or reduced efficacy.

### The Solution:

The Skincare Routine Tracker is a simple app designed to assist users in managing their skincare routines. By allowing users to log their skincare products, the app helps them keep track of the products used.

**Target audience:**

Individuals, particularly women, who are passionate about maintaining and optimizing their skincare routines. This includes anyone interested in tracking their daily skincare habits, monitoring product usage, and improving their overall skin health through consistent and informed practices. 

**Real-World Application:**


## UX Design Process

### Wireframes and Mock-ups 
In the initial stages of development, wireframes were created using Figma to visualize the app’s layout and user flow. These wireframes served as a blueprint for the design, ensuring that the user interface was both intuitive and aesthetically pleasing.
However, I found myself changing the wireframes heavily during the development process, as I did not have a defined idea of what I wanted to achieve in terms of database.

### Design Decisions and Reasoning

The design of the Skincare Journal was guided by the principles of simplicity and user-friendliness. Each element, from the navigation to the logging forms, was designed to be straightforward and easy to use. The goal was to create an app that users could quickly integrate into their daily skincare routine without unnecessary complexity.

## Features

**Product Logging:** Users can create a profile, log in and input and store information about their skincare products.
**Personalized Routine Generation:** Based on the logged products, the app creates a customized routine tailored to the user's specific needs and preferences.
**Guidance on Product Use:** The app provides recommendations on the optimal timing and order of application for each product.


## Technologies Used

- HTML
- CSS
- Python
- Mongo
- Figma for Wireframes
- Git and Github for version control
- Visual Studio Code
- Chrome developer tools
- Pexels for images

## Installation

To install the game locally, follow these steps:

1. Clone the repository using the following command:

git clone https://

2. Open the project folder and open home.html in your preferred browser.

## Deployment

The website was successfully deployed to GitHub. Steps to deploy it:

1. Go to the **Settings** tab in the GitHub repository.

2. Scroll down to **GitHub Pages** and click on **"Check it out here!"**

3. Make sure to choose **"main"** under **"Source"**.

4. The page will automatically refresh, showing a detailed ribbon display confirming the deployment.

The live site can be found at the following link: https:/

## Bugs

1. Users Unable to Log Back In After Logging Out

A significant issue encountered during development is that users are unable to log back into the application after they have logged out. Once a user logs out, attempting to log in again with the same credentials results in a failure, requiring the user to create a new account to regain access.
The problem stems from how the session is managed and how user authentication is handled. When a user logs out, the session is cleared, which is expected behavior. However, upon logging back in, the system does not correctly retrieve or validate the user's credentials from the database. 

This bug significantly impacts the user experience, as it effectively locks users out of their accounts once they log out. Resolving this issue is critical to ensure that users can seamlessly log in and out of the application as needed.

2. Skin Type Only Temporarily Saved in the Database
Another major issue discovered during development is that a user's selected skin type is only temporarily saved in the database. After restarting the server, the skin type appears to be deleted or lost, and the user needs to update their skin type again.

This bug also significantly affects the user experience by causing frustration and confusion. Users may believe their preferences are saved, only to find them missing later. Fixing this issue is crucial to ensuring that users can reliably set and maintain their skin type preferences across sessions.

## UX Scope Testing


1. User Interface (UI) Testing:


2. User Experience (UX) Testing:



## Manual Testing

Principles:

Human Insight: Manual testing leverages human intuition and experience to identify issues that automated tests might overlook.

Flexibility: Manual testers can adapt to changes and explore the game in creative ways, beyond predefined test cases.

User Experience: Manual testing is essential for evaluating the game's user interface and overall user experience.

Exploratory Testing: Manual testers can actively explore the game to uncover unexpected behavior and bugs.


**Device Compatibility Test:**

## Automated Testing

**Principles:**


- WS3 HTML Testing Validator

[W3C Validator](https://validator.w3.org/)
![HTML testing result](/assets/images/)

- CSS 

[CSS Validator](https://validator.w3.org/)
![CSS testing result](/assets/images/)

- 


[CSS testing result](https://www.jslint.com/)
![JavaScript testing result](/assets/images/)

- Google Lighthouse

![Google Lighthouse desktop performance](/assets/images/)
![Google Lighthouse mobile performance](/assets/images/)

## User Stories