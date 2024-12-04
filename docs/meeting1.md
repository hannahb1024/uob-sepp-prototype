# Meeting 1 Minutes
- Decision was made to use an agile methodology.
  The team recognises that due to limited time and project aspirations, most of the time would be spent getting the first iteration working.
  Once the first iteration is finished - iterative changes will be made to more closely align with the EDR.
- Decision was made to use github for version control and project management.
- Decision was made to break down work into work units, which would each be assigned to one/multiple team members.
  - Work units will be monitored on a Github projects Kanban board.
- Basic UI Mockups were made in the meeting
  [Initial UI Mockup](./EDR_example_UI-meeting1.webp)
- Special consideration was made for where people's functions and work interacts with each other and how these would interface.
- Decisions were made on the database:
  - Since most data processing is done client-side with CSRS, the server-side consists of essentially just the database.
  - CSRS uses containerisation on the server side, so we will make a docker container which we can eventually deploy to production 
  - In the mean-time, team members will download their own copy of the container
- Graph implementation will be through the standard QT graphs package.
  - There will be a slider to adjust a markers scores to be more in line with the average.
