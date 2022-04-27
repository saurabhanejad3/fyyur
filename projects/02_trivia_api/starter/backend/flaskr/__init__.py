import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    print(page)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    def get_all_categories():
        categories = Category.query.order_by(Category.id).all()
        all_categories = {}     
        for category in categories:
            all_categories[category.id]=category.type
        
        if len(categories) == 0:
            abort(404)
        
        return all_categories

    # Retrive all the categories 
    @app.route("/categories", methods=["GET"])
    @cross_origin()
    def retrieve_categories():
        return jsonify({
            "categories":get_all_categories()
        })

    # Retrive all the questions with categories
    @app.route("/questions")
    @cross_origin()
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,            
                "questions": current_questions,
                "categories": get_all_categories(),
                "current_category":{},
                "total_questions": len(selection),
            }
        )
    
    # Delete Question on the basis of question id selected from the UI to delete
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    @cross_origin()
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)

    # Search Questions if search term is posted also facilitate to create a new question set 
    @app.route("/questions", methods=["POST"])
    @cross_origin()
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_dificulty = body.get("difficulty",None)
        search = body.get("searchTerm", None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                    }
                )

            else:
                question = Question(question=new_question, 
                            answer=new_answer, 
                            category=new_category,
                            difficulty=new_dificulty)

                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                    }
                )

        except:
            abort(422)

    # get questions based on category
    @app.route("/categories/<int:category_id>/questions")
    def retrieve_question_by_category(category_id):
        category = Category.query.get(category_id)
        if (category is None):
            abort(404)

        try:
            selection = Question.query.filter_by(category=str(category_id)).all()
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,            
                "questions": current_questions,
                "total_questions": len(selection)
            })

        except:
            abort(400)

    '''
    @Done: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    # Lets play Quiz, end point to ask questions with selective categories.
    @app.route("/quizzes", methods=["POST"])
    @cross_origin()
    def play_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        category_id = quiz_category["id"]
        try:
            if (category_id == 0):
                questions = Question.query.all()                
            else:
                category = Category.query.get(category_id)
                if (category is None):
                    abort(404)
                questions = Question.query.filter_by(category=str(category.id)).all()

            next_question = random.choice(questions)
            while next_question.format().get("id") in previous_questions:                
                next_question = random.choice(questions)               
            
            return jsonify({
                "success": True,            
                "question": next_question.format(),
            })

        except:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
            "success": False, 
            "error": 404, 
            "message": "resource not found"
            }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
            }), 
            400
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({
            "success": False, 
            "error": 405, 
            "message": "method not allowed"
            }),
            405,
        )

    
    return app

    