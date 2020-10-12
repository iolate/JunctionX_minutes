# Minutes
Project of [JunctionX Seoul 2020](https://app.hackjunction.com/events/junctionx-seoul)

🥉 Placed 3rd in Microsoft Track 🎉 

## About
"Minutes" provides convenient features for reviewing the meetings such as documenting, archiving and searching of online meeting minutes.

### Track
Microsoft : Develop for Collaboration and Remote productivity

### Team Member
* Taeyoon Kim (ddaeddae.kim@gmail.com)
* Jiyoung Lee (ji8196@unist.ac.kr)
* Jiyoon Shin (shinjiyoon1@unist.ac.kr)
* Daeseong Jeon (nero96in@gmail.com)
* Seungho Kim (isho@unist.ac.kr)

## Problem
#### Tedious documenting minutes of the online meetings
Online meeting documenting is essential for its participants, but requires superficial work. Unlike previous methods of viewing entire meeting videos, the automatic scripting of video in "Minute" can solve this problem. It ensures fast and accurate documenting to help focus more on meeting progress.

#### Inefficiency to review online meeting
To document or summarize the contents of the online meetings, the entire video must be viewed from the beginning. "Minutes" allows the meeting to be analyzed through automatically extracted key-phrases, and to identify bookmarks set according to the subjective importance of each user. It also allows users to record subjective opinions about the meeting through marked key-phrases and memo.

## Concept images

<img src="https://github.com/iolate/JunctionX_minutes/blob/main/pictures/concept-1.jpg?raw=true" width="500">
<img src="https://github.com/iolate/JunctionX_minutes/blob/main/app_web/flask_app/static/images/tutorials/2.jpg?raw=true" width="500">
<img src="https://github.com/iolate/JunctionX_minutes/blob/main/app_web/flask_app/static/images/tutorials/3.jpg?raw=true" width="500">
<img src="https://github.com/iolate/JunctionX_minutes/blob/main/app_web/flask_app/static/images/tutorials/4.jpg?raw=true" width="500">
<img src="https://github.com/iolate/JunctionX_minutes/blob/main/app_web/flask_app/static/images/tutorials/5.png?raw=true" width="500">


## Functions and Technologies

### Microsoft Azure 

<img src="https://github.com/iolate/JunctionX_minutes/blob/main/pictures/System_Diagram.png?raw=true" width="500">

##### Auto-scripting online meeting
"Minutes" automatically records the contents of online meeting video entered by the user to reduce the inconvenience of creating minutes. To implement is, we subscribed to **Speech Service of Azure Cognitive Services**. "Minutes" converts meeting videos entered by the user to audio and records the contents of the meeting in minutes with the time they speak.

##### Key-phrases extraction
"Minutes" helps you intuitively understand the content of the meeting by extracting key-phrases from the long recorded minutes. It was implemented by subscribing to **the Text Analytics API of Azure Cognitive Services**. "Minutes" highlights key-phrases extracted in the recorded minutes so users can quickly understand the contents of the meeting without watching the entire long minutes!

### Minutes Website

##### Bookmarks and memo function
"Minutes" provides a bookmark and memo function that users can use when they want to record important contents in the minutes. Saved bookmarks and memo will help users quickly and efficiently understand when they later checked the contents of the meeting.

##### Tagging and search function
"Minutes" provides convenient functions to search and filter accumulated minutes. In addition, users will be able to tag keywords for each minutes and will be able to quickly access the minutes they want to find through the search function.

## Working demo screenshots
<img src="https://github.com/iolate/JunctionX_minutes/blob/main/pictures/demo-1.png?raw=true" width="500">
<img src="https://github.com/iolate/JunctionX_minutes/blob/main/pictures/demo-2.png?raw=true" width="500">

(Bookmark and search functions are not implemented on demo.)
