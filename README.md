# Minutes
JunctionX Seoul 2020

### Track
Microsoft : Develop for Collaboration and Remote productivity

### Team Member
* Taeyoon Kim (ddaeddae.kim@gmail.com)
* Jiyoung Lee (ji8196@unist.ac.kr)
* Daeseong Jeon (nero96in@gmail.com)
* Jiyoon Shin(shinjiyoon1@unist.ac.kr)
* Seungho Kim (isho@unist.ac.kr)


## Problem
### Tedious documenting minutes of the online meetings
Online meeting documenting is essential for its participants, but requires superficial work. Unlike previous methods of viewing entire meeting videos, the automatic scripting of video in "Minute" can solve this problem. It ensures fast and accurate documenting to help focus more on meeting progress.

### Inefficiency to review online meeting
To document or summarize the contents of the online meetings, the entire video must be viewed from the beginning. "Minutes" allows the meeting to be analyzed through automatically extracted key-phrases, and to identify bookmarks set according to the subjective importance of each user. It also allows users to record subjective opinions about the meeting through marked key-phrases and memo.

## Real-world impacts
The online collaborating environment has been expanded due to the COVID-19. Especially, online meeting services provide an online field to collaborate without facing each other. "Minutes" identifies the limitations of existing online meeting services. It complements and improves productivity in changing environment from offline to online. Furthermore, it will provide tools to work efficiently in a various collaboration situations through online meetings. It also can be considered as responsible AI in terms of "practices (documentation)".

## Functions and Technologies

### Stack of working demo
"Minutes" is currently produced at the woking demo level. The working demo used **Python's Flask** as a web framework, and database used **SQLite**.

### Microsoft Azure 

##### Auto-scripting online meeting
"Minutes" automatically records the contents of online meeting video entered by the user to reduce the inconvenience of creating minutes. To implement is, we subscribed to **Speech Service of Azure Cognitive Services**. "Minutes" converts meeting videos entered by the user to audio and records the contents of the meeting in minutes with the time they speak.

##### Key-phrases extraction
"Minutes" helps you intuitively understand the content of the meeting by extracting key-phrases from the long recorded minutes. It was implemented by subscribing to **the Text Analytics API of Azure Cognitive Services**. "Minutes" highlights key-phrases extracted in the recorded minutes so users can quickly understand the contents of the meeting without watching the entire long minutes!

##### Bookmarks and memo function
"Minutes" provides a bookmark and memo function that users can use when they want to record important contents in the minutes. Saved bookmarks and memo will help users quickly and efficiently understand when they later checked the contents of the meeting.

##### Tagging and search function
"Minutes" provides convinient functions to search and filter accumulated minutes. In addition, users will be able to tag keywords for each minutes and will be able to quickly access the minutes they want to find through the search function.


