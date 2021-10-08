# IAI MOOClet Dashboard
> _Note:_ This document is meant to evolve throughout the planning phase of your project.   That is, it makes sense for you commit regularly to this file while working on the project (especially edits/additions/deletions to the _Highlights_ section). Most importantly, it is a reflection of all the planning you work you've done in the first iteration. 
 > **This document will serve as a master plan between your team, your partner and your TA.**

## Product Details
 
#### Q1: What are you planning to build?

 > Short (1 - 2 min' read)
 * Start with a single sentence, high-level description of the product.
 * Be clear - Describe the problem you are solving in simple terms.
 * Be concrete. For example:
    * What are you planning to build? Is it a website, mobile app,
   browser extension, command-line app, etc.?      
    * When describing the problem/need, give concrete examples of common use cases.
    * Assume your the reader knows nothing about the problem domain and provide the necessary context. 
 * Focus on *what* your product does, and avoid discussing *how* you're going to implement it.      
   For example: This is not the time or the place to talk about which programming language and/or framework you are planning to use.
 * **Feel free (and very much encouraged) to include useful diagrams, mock-ups and/or links**.

----------
 * We are creating a website that allows researchers using the MOOClet engine to easily visualize and download data. 
 * The MOOClet engine, created by the Intelligent Adaptive Interventions (IAI) lab at U of T, allows researchers to conduct a variety of A/B tests with the aim of building self-improving technological systems. Currently, using the MOOClet engine requires accessing it through the command line, which can be challenging for researchers who do not have a background in programming.
 * Our goal is to create a web interface for the MOOClet API where researchers can visualize and download their data without them needing to access them through the command line. Users will be able to create user accounts with an authentication system. Research heads will be able to create, modify, and delete MOOClet objects for their A/B tests through our website, as well as have control over which users can access the data associated with their studies. 
 * Users who are authorized to access data from a study will be able download them in CSV form from our website. They will also be able to interact with the data visually through our website. For example, they will be able to see MOOClet data tables through our GUI and filter them by various fields, as well as see summaries of the data.


#### Q2: Who are your target users?

  > Short (1 - 2 min' read max)
 * Be specific (e.g. a 'a third-year university student studying Computer Science' and not 'a student')
 * **Feel free to use personas. You can create your personas as part of this Markdown file, or add a link to an external site (for example, [Xtensio](https://xtensio.com/user-persona/)).**

----------
 * Our target users are researchers that want to structure and visualize their data using a dashboard-style product. Specifically, the project will allow different roles amongst the researchers. An admin can manage researchers using the product and what access they have; anyone using the product can manipulate the data and visualize it.

#### Q3: Why would your users choose your product? What are they using today to solve their problem/need?

> Short (1 - 2 min' read max)
 * We want you to "connect the dots" for us - Why does your product (as described in your answer to Q1) fits the needs of your users (as described in your answer to Q2)?
 * Explain the benefits of your product explicitly & clearly. For example:
    * Save users time (how much?)
    * Allow users to discover new information (which information? And, why couldn't they discover it before?)
    * Provide users with more accurate and/or informative data (what kind of data? Why is it useful to them?)
    * Does this application exist in another form? If so, how does your differ and provide value to the users?
    * How does this align with your partner's organization's values/mission/mandate?
 
----------   
 * Existing software such as Tableau, the most popular data visualization tool, is unable to satisfy the needs of our target users. It allows its users to visualize the data with suggestions from an AI as well as connect to databases and be deployed. However, our product will be able to hook up to the MOOClet engine and allow for specific features that Tableau and other competitors do not offer. We can automate actions using the MOOClet engine, allowing the user to have control from the dashboard. Not only that, our product will allow administrators to manage access to the platform and data, so that it can meet their specific requirements. 

#### Q4: How will you build it?

> Short (1-2 min' read max)
 * What is the technology stack? Specify any and all languages, frameworks, libraries, PaaS products or tools. 
 * How will you deploy the application?
 * Describe the architecture - what are the high level components or patterns you will use? Diagrams are useful here. 
 * Will you be using third party applications or APIs? If so, what are they?
 * What is your testing strategy?

----------
 * We decided to build the app using Django for our backend, React for our frontend, and PostgreSQL for our database, which we will use to store user access data.
We plan to use Github Actions as our CI/CD tool, and deploy the app on Heroku; however, the lab told us they will get back to us if they have a preferred method of deployment, so our deployment choice may change.
 * As for libraries, we still do not know the specifications of how we will implement the various functions of our app, so we will be doing research as the need for a library arises. However, we do know that we will be interacting with MOOClet, a third party application, which is the lab’s current software used to collect data.
 * We decided that the main high-level components will be: a database storing users info, a login system, a front-end dashboard that allows researchers to select the study they want the data from, and a visualization page for the data and related statistics regarding one study. Components of this section will be filtering and reformatting tools, the possibility of downloading the data or uploading it to Drive, and statistical testing and Data visualization tools. The last component will be a component engine that will sort and visualize the data and create statistics information.
 * For our testing strategy, we will be creating various unit tests for every function of both our frontend and backend, and using Github Actions to test them. We also plan on writing integration tests for our main “linked” components interactions, such as the correct data appearing from the database into the frontend table. Finally, we plan to manually test the UI after our integration test passed.


#### Q5: What are the user stories that make up the MVP?

 * At least 5 user stories concerning the main features of the application - note that this can broken down further
 * You must follow proper user story format (as taught in lecture) ```As a <user of the app>, I want to <do something in the app> in order to <accomplish some goal>```
 * User stories must contain acceptance criteria. Examples of user stories with different formats can be found here: https://www.justinmind.com/blog/user-story-examples/. **It is important that you provide a link to an artifact containing your user stories**.
 * If you have a partner, these must be reviewed and accepted by them

----------
1. As a head of a research study, I want to create new studies and track their data in a website deployed specifically for that purpose so that I can make use of MOOClet objects in my research..
2. As a head of a research study, I want to visualize the data of my research collected by the MOOClet engine, and not any third-party engines.
3. As a head of a research study, I want to authorize members of my research team so that they can view visualizations of the research data and download the data to determine any meaningful trends and results through analysis.
4. As a staff member of the research team, I want to read the research data for a study in a human-readable format on a clear and easy-to-navigate dashboard.
5. As a staff member of the research team, I want to view summaries of my research data on the dashboard so that I can understand the 
6. As a staff member of the research team, I want to download the research data in a human-readable format to my local computer to easily parse it and draw useful information from it.


----
## Intellectual Property Confidentiality Agreement 
> Note this section is **not marked** but must be completed briefly if you have a partner. If you have any questions, please contact David and Adam.
>  
**By default, you own any work that you do as part of your coursework.** However, some partners may want you to keep the project confidential after the course is complete. As part of your first deliverable, you should discuss and agree upon an option with your partner. Examples include:
1. You can share the software and the code freely with anyone with or without a license, regardless of domain, for any use.
2. You can upload the code to GitHub or other similar publicly available domains.
3. You will only share the code under an open-source license with the partner but agree to not distribute it in any way to any other entity or individual. 
4. You will share the code under an open-source license and distribute it as you wish but only the partner can access the system deployed during the course.

**Briefly describe which option you have agreed to. Your partner cannot ask you to sign any legally binding agreements or documents pertaining to non-disclosure, confidentiality, IP ownership, etc.**

----------
* We have agreed with our partner that we can share the software and the code freely with anyone with a MIT license. Their code base for other software/MOOClet is open-source and available on GitHub.
----

## Process Details

#### Q6: What are the roles & responsibilities on the team?

Describe the different roles on the team and the responsibilities associated with each role. 
 * Roles should reflect the structure of your team and be appropriate for your project. Not necessarily one role to one team member.

List each team member and:
 * A description of their role(s) and responsibilities including the components they'll work on and non-software related work
 * 3 technical strengths and weaknesses each (e.g. languages, frameworks, libraries, development methodologies, etc.)

----------
 * **Luca** will be working on the frontend side of the app, as well as on the CI/CD process. He will also collaborate on the writing elements of the project (such as the presentation). Some of his strengths are CSS and HTML knowledge from his internships, quick at learning new languages and processes, and good at handling responsibility and deadlines and at teamwork. Some of his weaknesses are: little knowledge of React and Django (but good knowledge of Javascript), tendency to overwork himself, and no experience in PostGreSQL (but lots of experience in MySQL).

 * **Jordan** will primarily be working on the backend side of the application, specifically . She will also be working on designing the user experience for the data visualization aspect of the software. She has experience writing python scripts and using python to analyze research data. She is also familiar with Django. Her weaknesses include having difficulty prioritizing tasks and unfamiliarity with front-end languages.

 * **Joshua** will be working on the backend using Django, Twilio, and Azure. Joshua will also write unit tests and work on integrating token authentication services between backend and frontend for when a user creates an account/logs in. Some of Joshua's strengths include JavaScript, Python, React, and database integration in projects. Joshua's weaknesses are unfamiliarity with Django, feeling lost in large codebases, lack of CI/CD experience, adhering to clean architecture guidelines, and a tendency to be in a perfectionist mindset.

 * **Khushkaran** will be working on the frontend aspect of the app and the CI/CD process, including tests and deployment. Some of her strengths are HTML, CSS, and JavaScript from projects, good at creating test cases, and quick at learning and applying new content and skills. Some of her weaknesses are not much experience with CI/CD, unfamiliarity with Django and React, and getting too focused on the details. 

 * **Jacob** will be working primarily on the frontend side of the application and to a lesser extent on data storage and retrieval. Some of his strengths are Javascript, CSS, and an understanding of how to design UI/UX. He has designed several personal web application projects and has taken a course on the design of interactive computational media. He also has experience with PostgreSQL, having set up a database for a web application in the past. Some of his weaknesses are inexperience with continuous integration and deployment, failure to always clearly communicate assumptions regarding code architecture, and a tendency to be indecisive.


 * **Piyush** will be working on the backend using Django, Twilio, and Microsoft Azure services. These will interface with the backend with the MOOClet engine. Piyush will also work on the CI/CD of the project to ensure all the tests are run with every change to the repository and deployed. Piyush's strengths are experience with JavaScript, Azure, and API-focused projects. Some weaknesses are minimal experience with Django, trouble learning new frontend frameworks, and connecting CI/CD with the project, which he should be able to get adjusted to very quickly.

 * **Lily** will be working on backend API calls, database and testing. She will also keep track of meeting agendas and be available for communication with the IAI lab. Strengths: managing databases, setting up and maintaining CI/CD workflows, Python. Weaknesses: React, Django and integration testing, but will learn these very soon.


#### Q7: What operational events will you have as a team?

Describe meetings (and other events) you are planning to have. 
 * When and where? Recurring or ad hoc? In-person or online?
 * What's the purpose of each meeting?
 * Other events could be coding sessions, code reviews, quick weekly sync meeting online, etc.
 * You must have at least 2 meetings with your project partner (if you have one) before D1 is due. Describe them here:
   * What did you discuss during the meetings?
   * What were the outcomes of each meeting?
   * You must provide meeting minutes.
   * You must have a regular meeting schedule established by the second meeting.  

----------
 * We are planning to have weekly meetings between team members. We plan on meeting during the tutorial time, and having another ad hoc meeting online using discord if needed, or a short in-person prior to the lecture slot if needed. The purpose of each meeting will generally be on updating other members on progress made, determining how to proceed with a decision, dividing up some task, doing a coding session/review, etc. Some of us will also meet with our partner on Thursdays 3-4, and the meetings will be recorded for future reference. 
 * In the first partner meeting, we discussed the product itself - what the partners needed us to make, who the target user was, what features were needed and a ranking of priority for them, and other details. In this time we also went over ideas for how we would build the product and decided on future meeting times, methods, and how we would stay in touch. In the second partner meeting, we showed the partners our mockup and got feedback on it, and discussed the stack we decided on. 
 * For detailed meeting minutes, please see the Appendix below.

  
#### Q8: What artifacts will you use to self-organize?

List/describe the artifacts you will produce in order to organize your team.       

 * Artifacts can be To-Do lists, Task boards, schedule(s), meeting minutes, etc.
 * We want to understand:
   * How do you keep track of what needs to get done?
   * **How do you prioritize tasks?**
   * How do tasks get assigned to team members?
   * How do you determine the status of work from inception to completion?

----------
 * The main artifact that we will use to self-organize is Jira. We have split the product that we will make into "epics" (or features), and further split each epic into components we need in order to get that epic to work/be complete. The combination of these acts both as a checklist and task board, and it gives us an approximate schedule of when tasks will be started and completed by. This helps us to keep track of what needs to get done. Our partners have informed us the most important features are to them, and we plan on prioritizing tasks based on this. 
 * Team members are split into general subgroups (frontend and backend), and tasks will be split between members by mutual agreement. However, we anticipate the backend tasks being greater in number than the frontend tasks. For this, we plan on frontend members taking a few backend tasks in order for things to get done. Again, this splitting will be done by mutual agreement, factoring in things like which members are familiar with each task/technology. 
 * To determine the status of any task, we will use the Jira board. We have several status indicators, such as in progress, in testing, fixing bugs, and done. These will help us to keep track of the status.


#### Q9: What are the rules regarding how your team works?

Describe your team's working culture.

**Communications:**
 * What is the expected frequency? What methods/channels are appropriate? 
 * If you have a partner project, what is your process (in detail) for communicating with your partner?

----------
 * We are using Discord as our primary digital communication platform. We are expected to catch up on and respond to messages within 24 hours. We will also continuously communicate with each other about our work, providing updates when appropriate.
 * We are using Whatsapp as our platform for communicating with our partner.

 
**Meetings:**
 * How are people held accountable for attending meetings, completing action items? Is there a moderator or process?

----------
 * On Mondays during or after our tutorial, we will meet as a group to check in and discuss our work. We will otherwise schedule meetings when necessary.
 * We are meeting with our partner once a week, on Thursdays. Jacob and Lucy will act as our representatives for these meetings, and will relay any critical information about the meetings to the rest of the group.

**Expectations:**
 * We expect that our group members attend meetings regularly and complete their work in a timely manner. On the other hand, we understand that we have other responsibilities and that unexpected events occur. We expect our group members to communicate with us ahead of time if they are unable to attend meetings or complete work. If this is consistently an issue for a member, we will have a discussion with them about it and try to find a solution to their lack of contribution.

**Conflict Resolution:**
 * List at least three team scenarios/conflicts you discussed in lecture and how you decided you will resolve them. Indecisions? Non-responsive team members? Any other scenarios you can think of?

----------
1. **Indecision:**
 * When the group is unable to make a decision, we will either defer to the decision of the person with the most expertise in the area, or hold a ranked-choice vote, depending on what is most appropriate.

2. **Non-responsive team members:** 
 * If a group member consistently fails to respond to our attempts to communicate with them, we will discuss the issue with them when we can. If we are completely unable to contact them (i.e. they are not attending the tutorial or coming to lectures) , we will bring up the issue with our TA and try to figure out what is going on.

3. **Member is unable to do work:** 
 * If a member is unable to complete their work for any reason, they will communicate with the rest of the team as quickly as possible so that other team members can take on their workload.




----
## Highlights

Specify 3 - 5 key decisions and/or insights that came up during your meetings
and/or collaborative process.

----------
 * Short (5 min' read max)
 * Decisions can be related to the product and/or the team process.
    * Mention which alternatives you were considering.
    * Present the arguments for each alternative.
    * Explain why the option you decided on makes the most sense for your team/product/users.
 * Essentially, we want to understand how (and why) you ended up with your current product and process plan.
 * This section is useful for important information regarding your decision making process that may not necessarily fit in other sections. 


1. The most vital insight that resulted from our partner meetings was the realization that the web application requested by IAI is intended for use specifically by researchers using their open-source technology to conduct research.This was contrary to what the group had assumed based on the proposal document, which led us to believe we were creating some sort of software designed for use by people interacting with MOOClets (I.e. subjects of studies). We now have a renewed understanding and motivation for the project, since the research-centric use case is very interesting to the team.

2. A collection of related key insights are the decisions we made regarding our finalized tech stack: we decided on using Django, React & PostgreSQL as our stack because the partner’s existing code base is in Python and they have lab members with experience to take over and maintain the app at the end of our project/course. Alternatives were Node.js for backend, but the lab has less experience in Node. We chose PostgreSQL for the database because we previously used it for CSC343 assignments. The database for this project will be mainly for user authentication and this data would be suitable for storing in Postgre.

3. We decided to use GitHub Actions for CI/CD because we started learning GitHub Actions in our Assignment 1 and think it’s a productive and valuable tool. Alternative option Azure DevOps would potentially work well with Azure deployment. However, we haven’t fully decided on the deployment platform with our partner yet. Moreover, GitHub Actions would give more visibility for the CSC301 teaching team. Hence, we decided to use GitHub Actions.

4. Another key insight that arose after a team meeting following a lecture was the refinement of our target users into the important groups of head researchers and staff, and the permission structure this division would necessitate. We knew that users would need to be able to create and edit MOOClet objects on the IAI servers as well as retrieve the resulting data, but this insight allowed us to define the former functionality as belonging only to users authorized as head researchers and the latter functionality as belonging to all users, so long as they are a part of the relevant organization. This insight branched into many intuitive assumptions we could 

----------
### Appendix
Meetings with Intelligent Adaptive Interventions Lab for CSC301 Project

List of Meetings:
September 30th, 3-4pm	1
October 7th, 3-4pm	4

September 30th, 3-4pm
Zoom call
Participants: Taneea, Koby, Jiakai, Jacob, Piyush, Joshua, Jordan, Luca, Khushkaran and Lily

The project proposal that our CSC301 team received from Joseph is linked here. More details about the CSC301 Deliverable #1 content can be found here.

Clarification: Text messaging system is complete, we're building a dashboard to aid with data analysis and visualization
Questions from CSC301 Deliverable Requirements:

1.  What are you planning to build?
Web app?
Dashboard
Easy to download and visualize data
MOOClet engine connected to system
Message sequence is sent to user vis MOOClet and user gives a response/rating and that rating gets sent via RESTful API call
Goal = Abstract away the means of getting MOOClet data for researchers
to A/B test personalized messages that help manage symptoms in people dealing with mental health conditions
Example of use cases
Users = Researchers accessing data generated by MOOClet & messaging

How are we accessing / connecting to the existing codebase?
https://github.com/Intelligent-Adaptive-Interventions-Lab/MHA-Data-Collection
In backend, write similar scripts to above and build frontend for researchers to visualize and comprehend data without any understanding of the underlying code


2. Who are your target users?
Do you have a structured idea of the user personas we will be developing for?
Is it possible to get a mockup detailed story or even better, anonymous stories collected from real users?
“18-24 years old Mental Health America users, living in North America and dealing with mental health conditions like anxiety & depression.”

Researchers & PhD students working with the MOOClet data


3. Why would your users choose your product? What are they using today to solve their problem/need?

- Not using data collection repo above in long term because MOOClet data is accessed by id (ex. researchers only know name of data, rather than an associated id)
- Frontend main purpose is to support researchers viewing relevant data in the way they want

4. How will you build it?
Which technologies are set in stone? Stack clarification: specify any and all languages, frameworks, libraries, PaaS products or tools
Integration of Django Dialogue Builder with MOOClet Engine and Twilio text messages
Azure Bot Services - “more robust deployment features, load balancing technologies and monitoring infrastructure” in scope?
Minimal load (~20 concurrent users)
How will you deploy the application?
Heroku, Azure (?), Netlify, (anything accessible in website)
Architecture of the high-level components
Getting and reformatting MOOClet data, ideally, application automatically creates data files in Google Drive (take a look at Google Drive API)
Will you be using third party applications or APIs? 
Testing strategy
GitHub actions (CICD pipeline)

Progress tracking
Jira
2 week sprint intervals (weekly individual/sub-team progress updates during meetings)


5. What are the user stories that make up the MVP?
What is the user flow?
Dashboard (authentication before accessing)
Two groups of users
Staff
View/download data
Admin/Researchers
Create/delete/update (higher level permissions)
Ex. Add new MOOClet for a particular study, add policies
For deleting, user can give MOOClet id as input and MOOClet data corresponding to id is deleted
Interact with MOOClet tables through GUI (filterable, id mapping)
Download raw data files (with reformatting into usable csv)
Integrates with Google Drive
Data summarization (different means, proportions, counts, etc and output them in clean manner)
Download button downloads data and uploads to google drive automatically
Rank the main features (note: these seem not applicable anymore)
Download & reformat
MOOClet automation
Analyzer/summarizer (details of the analysis (statistical tests)) to be performed on the rewards for analyzer, and mean computation, etc for summarizer) 
Input = reformatted csv
TTest = https://www.graphpad.com/quickcalcs/ttest1.cfm
Authentication
Users will interact with different kinds of messages at different intervals as part of different messaging protocols that have been developed. These protocols and the Machine Learning algorithm help choose which user interacts with what kind of protocol and what kind of message content for A/B testing.
Users will be prompted to rate the messages they received. These ratings help the algorithm decide which messages are better, in an HCI-forward manner using crowdsourcing.
Users will be able to type text like ‘Help Me’ and a Help Menu protocol will be launched.
Users will receive periodic text prompts, with a link to a webpage where they can set/change their preferences.
Users are able to set their time zone and start time/end time preferences for receiving messages.
Users will be entered into a risk management protocol should the system receive any concerning messages.
Users will be able to report bugs and technical difficulties in their interaction with the text messaging system.


6. What are the roles & responsibilities on the team?
Suggestions for dividing up roles according to workload for each?
What might be some natural boundary points for individuals/teams to work within?


7. Intellectual Property Confidentiality Agreement
Discuss and agree upon an option with your partner. 
“Students can publish source code (e.g., on GitHub), design, and the software”
MIT license for existing software
Open source, upload anywhere (do not share any data or MOOClet tokens, etc.)
Examples include:
You can share the software and the code freely with anyone with or without a license, regardless of domain, for any use.
You can upload the code to GitHub or other similar publicly available domains.
You will only share the code under an open-source license with the partner but agree to not distribute it in any way to any other entity or individual.
You will share the code under an open-source license and distribute it as you wish but only the partner can access the system deployed during the course.


8. Other questions:
Frequency and time for future meetings / communications	
Lab standard: Record all zoom meetings
Preferred channel: Slack, email, etc.?
Slack or WhatsApp
When is the product planned to be deployed to the users? 
Periodic deployment (deploy to specific set of users, collect data to finetune algorithm)


Other resources mentioned:
t test calculator


October 7th, 3-4pm
Zoom call recording pwd: fe3!@BPp94
Participants: Taneea, Koby, Jiakai, Harsh, Alanna, Jacob, Piyush, Joshua, Jordan, Luca, Khushkaran and Lily

1. To go through our mockup and update as needed
Options refer to inputs to call the MOOClet API
Better if there's an introduction for each project and what the dataset contains
Let researchers choose which dataset they want to export

Data Structure Information:
https://github.com/Intelligent-Adaptive-Interventions-Lab/mooclet-engine 
https://docs.google.com/document/d/1eAuXgSmVpoPxa9R5K02GyP7rgKvPt1InbIz9mg5bS0I/edit#heading=h.uowx5w1vhlfa 

2. To go over a few user stories and personas we’ve written
Undergrad research assistant trying to access data fast
Research head wanting to set up a new study and give access to lab team
Create MOOClet related objects whenever a new study is created
Allow users to download data

3. Created Roadmap (draft) on Jira
Q: Has IAI been using Confluence for documentation?
Most documentation is on Google Docs
to walk through the roadmap and update as needed

4. We decided on the following stack:
Backend = Django
Frontend = React
Database = PostgreSQL
And we’re planning to set up CI/CD workflows and separate environments for Development & Production.
Q: Deployment to Azure using IAI’s resources to streamline with your other software? 
IAI will provide follow-up info later

Note: The meeting minutes were originaly documented in Google Docs and in the format of bullet point.
