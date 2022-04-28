import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_paginate import Pagination
import random
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


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
        try:
            categories = Category.query.order_by(Category.id).all()
            all_categories = {}
            for category in categories:
                all_categories[category.id] = category.type

            if len(categories) == 0:
                abort(404)

            return all_categories
        except Exception as ex:
            print(ex)
            abort(422)

    # Retrive all the categories
    @app.route("/categories", methods=["GET"])
    @cross_origin()
    def retrieve_categories():
        try:
            return jsonify({
                "categories": get_all_categories()
            })
        except Exception as ex:
            print(ex)
            abort(422)

    def paginate_questions(request, questions):
        try:
            page = request.args.get("page", 1, type=int)
            return [q.format() for q in questions.paginate(page, QUESTIONS_PER_PAGE).items]
        except Exception as ex:
            print(ex)
            abort(422)

    # Retrive all the questions with categories

    @app.route("/questions")
    @cross_origin()
    def retrieve_questions():
        try:
            questions = Question.query.order_by(Question.id)
            current_questions = paginate_questions(request, questions)

            if len(questions.all()) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "categories": get_all_categories(),
                    "current_category": {},
                    "total_questions": len(questions.all()),
                }
            )
        except Exception as ex:
            print(ex)
            abort(422)

    # Delete Question on the basis of question id selected from the UI to delete
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id)
            current_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(questions.all()),
                }
            )
        except Exception as ex:
            print(ex)
            abort(422)

# Search Questions if search term is posted else abort
    @app.route("/questions/search", methods=["POST"])
    @cross_origin()
    def search_question():
        body = request.get_json()
        search = body.get("searchTerm", None)

        try:
            if search:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, questions)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(questions.all()),
                    }
                )

            else:
                abort(422)
        except Exception as ex:
            print(ex)
            abort(422)

    # create a new question set if question and answer are non blank fields

    @app.route("/questions", methods=["POST"])
    @cross_origin()
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_dificulty = body.get("difficulty", None)

        if (len(new_question) == 0 or len(new_answer) == 0):
            abort(422)
        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_dificulty)

            question.insert()

            questions = Question.query.order_by(Question.id)
            current_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(questions.all()),
                }
            )
        except Exception as ex:
            print(ex)
            abort(422)

    # get questions based on category
    @app.route("/categories/<int:category_id>/questions")
    def retrieve_question_by_category(category_id):
        category = Category.query.get(category_id)
        if (category is None):
            abort(404)

        try:
            questions = Question.query.filter_by(category=str(category_id))
            current_questions = paginate_questions(request, questions)
            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions.all())
            })

        except Exception as ex:
            print(ex)
            abort(400)

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
                questions = Question.query.filter_by(
                    category=str(category.id)).all()

            next_question = random.choice(questions)
            while next_question.format().get("id") in previous_questions:
                next_question = random.choice(questions)

            return jsonify({
                "success": True,
                "question": next_question.format(),
            })

        except Exception as ex:
            print(ex)
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
