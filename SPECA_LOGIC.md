# Prepilo — Business Logic Specification

## 1. Project Overview

**Prepilo** is an AI-powered study preparation platform that helps students prepare for exams through personalized study plans, AI-generated explanations, quizzes, progress tracking, and peer support.

The main idea of the platform is simple:

A student creates subjects and topics, sets an exam date, receives a study plan, completes tasks, takes quizzes, tracks weak topics, and can ask friends for help when they struggle.

Prepilo combines three core ideas:

1. Personal study planning.
2. AI-powered learning assistance.
3. Help from friends and study peers.

The system is not just a todo-list. It analyzes progress, detects weak topics, recommends actions, and helps the student improve before the exam.

---

## 2. Main Goals

The main goals of Prepilo are:

1. Help students organize exam preparation.
2. Generate personalized study plans based on deadlines and topic difficulty.
3. Use AI to explain topics, generate quizzes, and summarize notes.
4. Track learning progress and detect weak areas.
5. Allow students to ask friends for help.
6. Support collaborative studying through shared quizzes, explanations, and study rooms.
7. Motivate students through streaks, help points, and progress dashboards.

---

## 3. User Roles

### 3.1 Student

A student is the main user of the system.

A student can:

* register and log in;
* create subjects;
* create topics inside subjects;
* set exam dates;
* generate study plans;
* complete study tasks;
* generate AI explanations;
* generate AI quizzes;
* take quizzes;
* track progress;
* add friends;
* send and receive help requests;
* share quizzes with friends;
* join study rooms;
* review learning statistics.

### 3.2 Friend

A friend is another student connected through the friendship system.

A friend can:

* receive help requests;
* send explanations;
* share quizzes;
* see allowed progress information;
* participate in study rooms;
* earn help points.

A friend cannot see private data unless the user allows it through privacy settings.

### 3.3 AI Assistant

The AI Assistant is an internal service, not a real user.

The AI Assistant can:

* generate study plans;
* explain topics;
* generate quizzes;
* analyze weak topics;
* summarize notes;
* create flashcards;
* improve friend explanations;
* recommend which friend can help with a weak topic.

The AI does not directly change database records. The backend validates AI output before saving anything.

---

## 4. Core Modules

Prepilo consists of the following business modules:

1. Authentication and User Profile
2. Subjects
3. Topics
4. Study Plans
5. Study Tasks
6. AI Assistant
7. Quizzes
8. Progress Tracking
9. Friends
10. Help Requests
11. Shared Quizzes
12. Study Rooms
13. Peer Review
14. Notifications
15. Gamification
16. Privacy Settings

---

# 5. Authentication and User Profile

## 5.1 Registration

A user creates an account using:

* username;
* email;
* password.

After registration, the system creates a user profile.

The profile may include:

* username;
* email;
* avatar;
* bio;
* daily study goal;
* privacy settings;
* created date.

## 5.2 Login

The user logs in using email or username and password.

After successful login, the system gives the user an authentication token.

## 5.3 Access Rules

A user can only manage their own:

* subjects;
* topics;
* study plans;
* tasks;
* quizzes;
* quiz results;
* progress data;
* notes.

Friends can only see information allowed by privacy settings.

---

# 6. Subjects

## 6.1 Subject Definition

A subject is a course or discipline the student wants to prepare for.

Examples:

* Operating Systems;
* Web Development;
* Algorithms;
* Databases;
* English.

## 6.2 Subject Data

A subject contains:

* title;
* description;
* exam date;
* color;
* owner user;
* creation date.

## 6.3 Subject Actions

The user can:

* create a subject;
* view subject list;
* view subject details;
* update a subject;
* delete a subject.

## 6.4 Subject Business Rules

One user can have many subjects.

Each subject belongs to only one user.

A subject must have a title.

An exam date is optional at the beginning, but it is required for generating a study plan.

## 6.5 Subject Deletion

When a subject is deleted, the system also deletes or archives related:

* topics;
* study plans;
* study tasks;
* quizzes;
* quiz results;
* progress records.

Deletion must require confirmation because it removes a large amount of data.

---

# 7. Topics

## 7.1 Topic Definition

A topic is a study unit inside a subject.

Example for Operating Systems:

* Processes;
* Threads;
* Scheduling;
* Memory Management;
* File Systems.

## 7.2 Topic Data

A topic contains:

* title;
* description;
* subject;
* difficulty;
* priority;
* estimated hours;
* status;
* creation date.

## 7.3 Topic Difficulty

Difficulty shows how hard the topic is for the user.

Values:

* 1 — very easy;
* 2 — easy;
* 3 — medium;
* 4 — hard;
* 5 — very hard.

## 7.4 Topic Priority

Priority shows how important the topic is for the exam.

Values:

* 1 — low priority;
* 2 — medium priority;
* 3 — high priority.

## 7.5 Topic Statuses

A topic can have one of the following statuses:

* `not_started` — the user has not started the topic;
* `in_progress` — the user is currently studying the topic;
* `done` — the topic is completed;
* `weak` — the user has problems with this topic.

## 7.6 When a Topic Becomes Weak

A topic becomes `weak` if:

* the user scores below 60% on a quiz for this topic;
* the average quiz score for this topic is below 60%;
* the user manually marks the topic as weak;
* AI analysis detects that the user has knowledge gaps;
* the user repeatedly skips tasks related to this topic.

## 7.7 When a Topic Becomes Done

A topic can become `done` if:

* all planned tasks for the topic are completed;
* the latest quiz result is at least 75%;
* the user manually marks it as completed;
* there are no active weak indicators.

---

# 8. Study Plans

## 8.1 Study Plan Definition

A study plan is a schedule that tells the user what to study and when.

It is generated based on:

* subject;
* exam date;
* topics;
* topic difficulty;
* topic priority;
* estimated study time;
* daily available study hours;
* current progress;
* weak topics.

## 8.2 Study Plan Generation

The user clicks “Generate Study Plan”.

The system collects:

* subject data;
* exam date;
* list of topics;
* topic difficulty;
* topic priority;
* estimated hours;
* completed topics;
* weak topics;
* daily study hours.

Then the system generates a daily plan.

The plan can be generated by:

* internal backend algorithm;
* AI Assistant;
* hybrid method: backend prepares data, AI suggests plan, backend validates it.

## 8.3 Study Plan Business Rules

The system must follow these rules:

1. Harder topics receive more study time.
2. High-priority topics are scheduled earlier.
3. Weak topics receive additional review sessions.
4. Completed topics are not scheduled as new learning tasks.
5. Completed topics can appear as review tasks.
6. One or two days before the exam should be used for review and quizzes.
7. The plan cannot schedule more hours per day than the user allows.
8. The plan must not generate tasks after the exam date.
9. If there is not enough time before the exam, the system warns the user.

## 8.4 Study Plan Regeneration

The user can regenerate the plan if:

* the exam date changes;
* new topics are added;
* some topics are marked as weak;
* many tasks are skipped;
* daily available hours change.

When regenerating, the system should preserve completed tasks and only update future tasks.

---

# 9. Study Tasks

## 9.1 Study Task Definition

A study task is a single planned activity inside a study plan.

Example:

Study “Threads” on June 12 for 2 hours.

## 9.2 Study Task Data

A study task contains:

* study plan;
* topic;
* task date;
* planned hours;
* task type;
* status.

## 9.3 Task Types

Task types:

* `learn` — learn a new topic;
* `review` — review an already studied topic;
* `quiz` — take a quiz;
* `notes` — write or read notes;
* `ai_explanation` — read AI explanation;
* `friend_help` — get help from a friend.

## 9.4 Task Statuses

A study task can have one of the following statuses:

* `planned` — task is planned;
* `in_progress` — user started the task;
* `done` — task is completed;
* `skipped` — user skipped the task;
* `overdue` — task was not completed on time.

## 9.5 Task Completion

When the user marks a task as `done`, the system:

* updates topic progress;
* updates subject progress;
* updates daily streak;
* creates an activity record;
* checks whether the topic can become completed.

## 9.6 Skipped Tasks

If a task is skipped, the system can:

* suggest moving the task to another day;
* suggest regenerating the study plan;
* increase the importance of this topic;
* mark the topic as risky if the user skips it multiple times.

---

# 10. AI Assistant

## 10.1 AI Role in the System

AI helps the user study more effectively.

AI is used for:

* study plan generation;
* topic explanation;
* quiz generation;
* weakness analysis;
* note summarization;
* flashcard generation;
* improving friend explanations;
* helper recommendation.

AI must return structured output where possible.

## 10.2 AI Study Plan Generator

The backend sends structured data to AI:

* subject;
* exam date;
* topics;
* difficulty;
* priority;
* estimated hours;
* daily hours;
* weak topics;
* completed topics.

AI returns a suggested plan in JSON format.

The backend validates:

* dates;
* topic IDs;
* planned hours;
* task types;
* total daily hours;
* exam date limits.

Only after validation does the backend save the plan.

## 10.3 AI Topic Explainer

The user selects a topic and explanation mode.

Modes:

* beginner;
* exam-focused;
* examples;
* short summary;
* detailed explanation.

AI generates an explanation.

The user can:

* read the explanation;
* save the explanation;
* convert it into flashcards;
* generate a quiz from it;
* share it with a friend.

## 10.4 AI Quiz Generator

The user selects:

* topic;
* difficulty;
* number of questions.

AI generates questions with:

* question text;
* answer options;
* correct answer;
* explanation;
* difficulty level.

The backend validates the structure before saving the quiz.

## 10.5 AI Weakness Analyzer

After quiz completion, the system analyzes:

* quiz score;
* incorrect answers;
* topic difficulty;
* previous quiz attempts;
* skipped tasks.

AI can generate a recommendation, for example:

“Review ULT vs KLT and take one more quiz on Threads.”

## 10.6 AI Summary from Notes

The user provides lecture notes or text.

AI can generate:

* short summary;
* key terms;
* flashcards;
* possible exam questions;
* simplified explanation.

## 10.7 AI Improve Friend Explanation

A friend can write an explanation manually.

AI can improve it by:

* making it clearer;
* fixing grammar;
* adding structure;
* adding examples;
* making it exam-focused.

Original human explanation must still be stored separately from the AI-improved version.

---

# 11. Quizzes

## 11.1 Quiz Definition

A quiz is a set of questions related to a topic.

A quiz can be:

* AI-generated;
* manually created by a user;
* shared by a friend;
* assigned inside a study room.

## 11.2 Quiz Data

A quiz contains:

* owner user;
* subject;
* topic;
* title;
* difficulty;
* questions;
* creation date.

## 11.3 Question Data

Each question contains:

* question text;
* options;
* correct answer;
* explanation;
* difficulty.

## 11.4 Taking a Quiz

The user answers quiz questions.

After submission, the system:

* checks answers;
* calculates score;
* saves result;
* updates topic progress;
* detects weak areas;
* suggests next action.

## 11.5 Quiz Score Rules

Score interpretation:

* 90–100% — excellent;
* 75–89% — good;
* 60–74% — acceptable;
* below 60% — weak.

## 11.6 If Quiz Score Is Below 60%

The system must:

* mark the topic as weak;
* recommend AI explanation;
* recommend additional review;
* recommend asking a friend for help;
* add the topic to weak topics list.

## 11.7 Quiz Retake

The user can retake a quiz.

The system stores every attempt separately.

Progress should be based on recent attempts and average performance.

---

# 12. Progress Tracking

## 12.1 Topic Progress

Topic progress is based on:

* completed study tasks;
* quiz scores;
* manual topic status;
* weak topic status;
* AI analysis.

## 12.2 Subject Progress

Subject progress is calculated using completed topics.

Basic formula:

completed topics / all topics * 100

Example:

If a subject has 10 topics and 4 are completed, subject progress is 40%.

## 12.3 Weak Topics

The system keeps a separate list of weak topics.

A topic can be weak because of:

* low quiz score;
* repeated mistakes;
* skipped study tasks;
* manual user mark;
* AI analysis.

## 12.4 Dashboard

The dashboard shows:

* today’s tasks;
* upcoming exams;
* subject progress;
* weak topics;
* latest quiz results;
* current streak;
* incoming help requests;
* recommended actions.

## 12.5 Recommended Actions

The system can recommend:

* study today’s task;
* review weak topic;
* generate AI explanation;
* take a quiz;
* ask friend for help;
* regenerate study plan;
* join a study room.

---

# 13. Friends

## 13.1 Friendship Definition

Friendship allows students to help each other.

Friendship is created through a friend request.

## 13.2 Friend Request Statuses

A friend request can have the following statuses:

* `pending` — request sent;
* `accepted` — users are friends;
* `declined` — request declined;
* `blocked` — user is blocked.

## 13.3 Friend Request Rules

A user cannot:

* send a friend request to themselves;
* send duplicate requests to the same user;
* send a request to a blocked user;
* see another user’s private data before friendship is accepted.

## 13.4 After Friendship Is Accepted

Friends can:

* send help requests;
* share quizzes;
* invite each other to study rooms;
* see allowed progress;
* send explanations;
* participate in peer review.

---

# 14. Help Requests

## 14.1 Help Request Definition

A help request is a request from one user to another asking for help with a specific topic.

Example:

“Can you help me understand Threads?”

## 14.2 Help Request Data

A help request contains:

* sender;
* receiver;
* subject;
* topic;
* message;
* status;
* creation date.

## 14.3 Help Request Statuses

A help request can have one of the following statuses:

* `pending` — waiting for response;
* `accepted` — friend accepted the request;
* `declined` — friend declined the request;
* `completed` — help was provided;
* `cancelled` — sender cancelled the request.

## 14.4 Help Request Flow

1. User performs badly on a quiz or marks a topic as weak.
2. System recommends asking a friend for help.
3. User selects a friend and sends a help request.
4. Friend receives notification.
5. Friend accepts or declines.
6. If accepted, friend can send an explanation, notes, or quiz.
7. User reviews the help.
8. User marks the request as completed.
9. Friend receives help points.
10. Topic progress may be updated after user retakes quiz or marks help as useful.

## 14.5 Help Request Rules

A user can send a help request only to an accepted friend.

A user cannot send help requests if the receiver disabled help requests.

A help request must be connected to a topic.

A completed help request cannot be edited.

---

# 15. Friend Explanations

## 15.1 Friend Explanation Definition

A friend explanation is a text answer written by a friend for a help request.

## 15.2 Friend Explanation Data

A friend explanation contains:

* help request;
* author;
* original text;
* AI-improved text;
* creation date.

## 15.3 Friend Explanation Flow

1. Friend accepts help request.
2. Friend writes explanation.
3. Friend optionally improves it with AI.
4. Explanation is sent to the requester.
5. Requester reads and rates it.
6. If helpful, friend receives help points.

## 15.4 Rating

The requester can mark explanation as:

* helpful;
* not helpful.

Optionally, they can rate it from 1 to 5.

---

# 16. Shared Quizzes

## 16.1 Shared Quiz Definition

A shared quiz is a quiz sent from one user to another.

## 16.2 Shared Quiz Flow

1. User creates or selects a quiz.
2. User selects a friend.
3. User sends quiz.
4. Friend receives notification.
5. Friend completes quiz.
6. System saves result.
7. Result visibility depends on privacy settings.

## 16.3 Shared Quiz Rules

A quiz can only be shared with accepted friends.

The receiver can complete the quiz multiple times if retakes are allowed.

The sender can only see the receiver’s result if the receiver allows quiz result sharing.

---

# 17. Study Rooms

## 17.1 Study Room Definition

A study room is a collaborative space for preparing for a subject or exam.

Example:

“Operating Systems Midterm Room”

## 17.2 Study Room Data

A study room contains:

* owner;
* title;
* description;
* subject;
* exam date;
* members;
* room tasks;
* shared quizzes;
* shared notes;
* creation date.

## 17.3 Study Room Roles

Study room roles:

* `owner`;
* `admin`;
* `member`.

## 17.4 Owner Permissions

The owner can:

* edit room information;
* delete the room;
* invite members;
* remove members;
* assign admins;
* create room tasks;
* delete room tasks.

## 17.5 Admin Permissions

An admin can:

* invite members;
* create room tasks;
* assign tasks;
* update task statuses;
* manage shared materials.

## 17.6 Member Permissions

A member can:

* view room content;
* complete assigned tasks;
* add notes;
* take quizzes;
* participate in discussions.

## 17.7 Study Room Rules

Only invited users can join a private study room.

A user can leave a room unless they are the only owner.

Deleting a room removes or archives its tasks and shared materials.

---

# 18. Room Tasks

## 18.1 Room Task Definition

A room task is a collaborative task assigned to a room member.

Example:

“Prepare notes about Scheduling.”

## 18.2 Room Task Data

A room task contains:

* study room;
* title;
* description;
* assigned user;
* due date;
* status.

## 18.3 Room Task Statuses

Room task statuses:

* `todo`;
* `in_progress`;
* `done`.

## 18.4 Room Task Completion

When a member completes a room task, they can attach:

* summary;
* notes;
* quiz;
* AI explanation;
* external link.

Other room members can use these materials.

---

# 19. Peer Review

## 19.1 Peer Review Definition

Peer review allows a user to send their notes or explanation to a friend for feedback.

## 19.2 Peer Review Flow

1. User writes notes.
2. User selects a friend as reviewer.
3. Reviewer receives request.
4. Reviewer reads notes.
5. Reviewer leaves feedback.
6. User improves notes.
7. Peer review is marked as completed.

## 19.3 AI in Peer Review

AI can additionally check:

* missing concepts;
* unclear explanations;
* possible mistakes;
* exam questions based on the note.

AI feedback should be separate from human feedback.

---

# 20. AI Helper Recommendation

## 20.1 Helper Recommendation Definition

The system can recommend a friend who may help with a weak topic.

## 20.2 Recommendation Logic

The system recommends a friend if:

* User A is weak in a topic;
* User B is a friend of User A;
* User B has high quiz results in the same or similar topic;
* User B allows help requests;
* User B is active enough in the system.

Example:

User A score in Threads: 45%.

User B score in Threads: 92%.

System recommends User B as a helper.

## 20.3 Recommendation Output

The system shows:

* recommended friend;
* topic;
* reason;
* button to send help request.

Example:

“Ask Dias for help with Threads. Dias has an average score of 92% in this topic.”

---

# 21. Notifications

## 21.1 Notification Definition

Notifications inform users about important events.

## 21.2 Notification Events

The system creates notifications when:

* friend request is received;
* friend request is accepted;
* help request is received;
* help request is accepted;
* help request is completed;
* friend sends an explanation;
* friend shares a quiz;
* user is invited to a study room;
* exam date is near;
* task is due today;
* task is overdue;
* AI detects a weak topic;
* study plan needs regeneration.

## 21.3 Notification Types

For MVP, the system uses in-app notifications.

Future versions may include:

* email notifications;
* push notifications;
* calendar reminders.

---

# 22. Gamification

## 22.1 Help Points

Users receive help points for helping others.

Possible point rules:

* +10 points for completed help request;
* +5 points for explanation;
* +3 points for shared quiz;
* +15 points for completed peer review;
* +5 points if another user marks help as useful.

## 22.2 Study Streak

A streak increases when the user completes at least one study task per day.

If the user misses a day, the streak resets or pauses depending on future rules.

## 22.3 Badges

The system may give badges:

* First Quiz Completed;
* Helpful Friend;
* 7-Day Streak;
* Exam Ready;
* AI Power User;
* Weak Topic Destroyer.

Badges are optional for MVP.

---

# 23. Privacy Settings

## 23.1 Privacy Options

The user can control what friends can see.

Privacy settings include:

* show progress to friends;
* show weak topics to friends;
* show quiz results to friends;
* allow help requests;
* allow study room invites;
* allow AI helper recommendation.

## 23.2 Privacy Rules

If progress sharing is disabled, friends cannot see subject progress.

If quiz result sharing is disabled, friends cannot see quiz scores.

If help requests are disabled, friends cannot send help requests.

If weak topic sharing is disabled, friends cannot see weak topics.

Privacy settings must be checked before showing any friend-related data.

---

# 24. Main User Scenario

This is the main business scenario of Prepilo:

1. User registers and logs in.
2. User creates a subject: Operating Systems.
3. User sets the exam date.
4. User adds topics: Processes, Threads, Scheduling, Memory.
5. User sets difficulty and priority for each topic.
6. User enters daily available study hours.
7. User generates a study plan.
8. AI suggests a plan.
9. Backend validates and saves the plan.
10. User completes daily study tasks.
11. User takes a quiz on Threads.
12. User gets 45%.
13. System marks Threads as weak.
14. System recommends AI explanation.
15. System also recommends asking a friend for help.
16. User sends a help request to a friend.
17. Friend accepts the request.
18. Friend sends explanation and quiz.
19. User studies the explanation.
20. User retakes quiz and gets 80%.
21. Topic status changes from weak to done.
22. Subject progress increases.
23. Friend receives help points.
24. Dashboard updates.

This scenario is the heart of the project.

---

# 25. MVP Scope

## 25.1 MVP Version 1 — Core Study System

Must include:

* registration and login;
* user profile;
* subjects;
* topics;
* study plans;
* study tasks;
* basic progress tracking.

## 25.2 MVP Version 2 — AI System

Must include:

* AI study plan generation;
* AI topic explanation;
* AI quiz generation;
* AI weakness analysis.

## 25.3 MVP Version 3 — Friends System

Must include:

* friend requests;
* friend list;
* help requests;
* friend explanations;
* shared quizzes;
* basic privacy settings.

## 25.4 MVP Version 4 — Dashboard

Must include:

* today’s tasks;
* upcoming exams;
* subject progress;
* weak topics;
* quiz results;
* incoming help requests;
* recommended actions.

---

# 26. Future Improvements

Features that can be added later:

* study rooms;
* peer review;
* leaderboard;
* badges;
* push notifications;
* email notifications;
* Google Calendar integration;
* file upload for notes;
* AI flashcards;
* mobile app;
* public study groups;
* teacher role.

---

# 27. Business Value

Prepilo solves a common student problem: students often do not know what to study, when to study, and how to fix weak topics.

The platform gives students:

* clear study structure;
* personalized schedule;
* AI explanations;
* automatic quizzes;
* progress tracking;
* social help from friends;
* motivation to continue studying.

For a portfolio project, Prepilo demonstrates:

* real business logic;
* user roles and permissions;
* AI integration;
* social features;
* progress analytics;
* recommendation logic;
* scalable backend architecture.

---

# 28. Short Project Description

Prepilo is an AI-powered peer study platform that helps students prepare for exams through personalized study plans, AI-generated quizzes, topic explanations, progress tracking, weak topic analysis, and help requests between friends.

The system detects weak topics from quiz results and study behavior, then recommends AI explanations, additional practice, or help from friends. Prepilo combines personal planning, artificial intelligence, and peer support into one study preparation platform.
