# Full Stack API Final Project - Trivia

## Introduction
Udacity trivia is quiz game, project. Based on restful APIs. It has set of categories and each category has some set of question. It has APIs exposed to add question, search, delete and so on. It is a project of level 2, under full stack developer course. It covers below features:
1.	Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2.	Delete questions.
3.	Add questions and require that they include question and answer text.
4.	Search for questions based on a text query string.
5.	Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK_DEBUG=True
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: method not allowed

### Endpoints 
#### GET /categories
- General: Retrive all the categories
    - Returns all categories in key value pair as a dictionary object.  
    - curl call example: `curl http://127.0.0.1:5000/categories`
    - Sample view will be like:
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```
#### GET /questions
- General: Retrive all the questions with categories
    - An endpoint to handle GET requests for questions.
    - Including pagination (every 10 questions).
    - This endpoint returns a list of questions, number of total questions, current category, categories.
    - curl call example: `curl http://127.0.0.1:5000/questions`
    - Sample view will be like:
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": {}, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 28
}
```
#### DELETE /questions/<int:id>
- General: Delete Question on the basis of question id selected from the UI to delete
    - An endpoint to DELETE question using a question ID.  
    - curl call example: `curl -X DELETE http://127.0.0.1:5000/questions/12`
    - Sample view will be like:
```
{
  "deleted": 12,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 27
}

```

#### POST /questions/search
- General: Search Questions if search term is posted
  - A POST endpoint to get questions based on a search term.
  - It returns any questions for whom the search term is a substring of the question.
  - curl call example: `curl -X POST --data "{\"searchTerm\":\"test\"}" --header "Content-Type: application/json" http://127.0.0.1:5000/questions/search`
  - Sample view will be like:
  ```
  {
    "questions": [
      {
        "answer": "test testtest",
        "category": 4,
        "difficulty": 2,
        "id": 26,
        "question": " teste test"
      }
    ],
    "success": true,
    "total_questions": 1
  }
  ```
#### POST /questions
General: Create new Question Set
  - An endpoint to create question with request set "question and answer text, category, and difficulty score" and create a question ID.  
  - curl call example: `curl -X POST --data "{\"question\":\"What is capital of India?\",\"answer\":\"Delhi\", \"category\":\"4\", \"difficulty\":\"3\"}" --header "Content-Type: application/json" http://127.0.0.1:5000/questions`
  - Sample view will be like:    
  ```
  {
    "created": 53,
    "questions": [
      {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      },
      {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      },
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      },
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
      },
      {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
      },
      {
        "answer": "Escher",
        "category": 2,
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      }
    ],
    "success": true,
    "total_questions": 30
  }
  ```

#### GET /categories/<int:category_id>/questions
- General: get questions based on category
    - a GET endpoint to get questions based on category. 
    - curl call example: `curl http://127.0.0.1:5000/categories/4/questions`
    - Sample view will be like:
    ```
    {
      "questions": [
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
          "answer": "Scarab", 
          "category": 4, 
          "difficulty": 4, 
          "id": 23, 
          "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }, 
        {
          "answer": "A resoponse or justification of ask i.e. question", 
          "category": 4, 
          "difficulty": 5, 
          "id": 25, 
          "question": "What is answer?"
        }, 
        {
          "answer": "test testtest", 
          "category": 4, 
          "difficulty": 2, 
          "id": 26, 
          "question": " teste test"
        }, 
        {
          "answer": "Delhi", 
          "category": 4, 
          "difficulty": 3, 
          "id": 53, 
          "question": "What is capital of India?"
        }
      ], 
      "success": true, 
      "total_questions": 5
    }
    ```

#### GET /quizzes
- General: Lets play Quiz, end point to ask questions with selective categories.
    - A POST endpoint to get questions to play the quiz.  
    - endpoint takes category and previous question parameters and return a random question within the given category. 
    - curl call example: `curl -X POST http://127.0.0.1:5000/quizzes --data "{\"quiz_category\":{\"type\": \"History\", \"id\": 4},\"previous_questions\":[2]}" --header "Content-Type: application/json"`
    - Sample view will be like:
    ```
    {
      "question": {
        "answer": "Delhi",
        "category": 4,
        "difficulty": 3,
        "id": 53,
        "question": "What is capital of India?"
      },
      "success": true
    }
    ```