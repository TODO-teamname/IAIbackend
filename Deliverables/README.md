//TODO: Team Name

### Description

Our application allows researchers using the MOOClet engine to conduct A/B testing to easily access and read the data, download it in CSV format, and automatically upload it to Google Drive, all while managing multiple studies.

Currently, using the MOOClet engine requires accessing it through the command line, which can be challenging for researchers who do not have a background in programming, so our web interface will help many researchers save time by having a more accessible platform to handle MOOClets.

### Key Features

A user needs to login through the login interface. Right now, the user needs to insert the username "Test" and password "123". At that point, they will have access to the Dashboard, where they will be able to view all of their MOOClets, as well as the other users that belong to their organization. At the bottom of this page, they can also create a new MOOClet with custom Policies, Variables, and Versions. There is support for Choose Policy Group, TS Configurable, and limited support Thompson Sampling Contextual policy parameters, which researchers can choose from and customize to suit their needs.

From the dashboard, a user can click on a MOOClet card to navigate to the data view page for that MOOClet. This page displays the information associated with that MOOClet, such as its name, id, and policy. From this page, a user will be able to easily download a CSV file containing the raw and/or re-formatted MOOClet data, but this feature is still in development.

The backend API of the app is demonstrated more fully in [this document](https://docs.google.com/document/d/1BqGckkTbuxG7kCC_4mgWsWmuofnbaz0UCU61uWVA6TA/edit?usp=sharing ).

The interface is demonstrated here: https://youtu.be/vuvlERZOYuc.

### Instructions

To test the website, a user will need to access the following URL: iai-app.herokuapp.com.They will see the login page, where they will need to insert ‘Test’ as Username and ‘123’ as password. These are hard-coded values, since we have not yet implemented a user authentication system.

The user can test closing their tab or their browser, and they will notice that they will not need to re-do a redundant login, since they will still be logged in.

Then, the user will be redirected to the Dashboard, where they can test out various features. They can add a new MOOClet on this page, and by clicking on an existing MOOClet card, they can go to the data view to see information about it.

### Development requirements

If someone wants to deploy the frontend locally, all they need to do is install npm and run in the frontend folder npm install and npm start. Npm should automatically install all the required components to run the website.

For the backend, the deployment machine should have python 3.9 and the pipenv python package installed. Then, “pipenv install” should be run in the root directory of the project to install all the required python libraries listed in the Pipfile. To launch the backend server, run “python manage.py runserver”. Then, the frontend will be able to call the internal API to communicate with the backend, and the backend will be able to call the external partner-provided API to create or retrieve resources from the IAI lab’s server.

### Deployment and Github Workflow

We have a main branch and a development branch. 

When an individual programmer wants to merge their code, they make a pull request into the development branch. They are responsible for ensuring that there are no merge conflicts; however, if they need help with handling merge conflicts, other group members will help out. One approval is required for merging into the development branch. We only require one approval at the moment to speed up the development process, but will require more approvals in the future. The programmer requests an approval from a group member who’s been working on similar areas of the code and should be familiar with it. The approver reads over the code and does basic tests before approving it. The person who made the pull request then merges the pull request.

After any major changes, we merge the development branch into the master branch. This requires 2 approvals. We set up Heroku for continuous deployment so that every time a change is made to the development branch, a build is deployed to the Heroku application address. Both automatic and manual, branch-specific deployments can occur since Heroku is connected to the GitHub repository.

### Licenses
We will use the MIT license for our application because the partner organization IAI is already using the MIT license for their open-source Mooclet Engine. By using the MIT license, our application can be more widely-used and permitting any business users to not have to disclose their proprietary code. Moreover, the MIT license doesn’t restrict any codebase development we’re undertaking.


