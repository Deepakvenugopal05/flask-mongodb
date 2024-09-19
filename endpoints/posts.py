from flask import request, Blueprint, jsonify
from database.db import db
from uuid import uuid1
from datetime import datetime

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/count', methods=['GET'])
def count():
    try:
        data = db.posts.count_documents({})
        return jsonify({"count": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/', methods=['GET', 'POST'])
def posts():
    try:
        if request.method == 'POST':
            _id = str(uuid1().hex)
            data = dict(request.json)
            date_now = datetime.now()
            data['date_added'] = date_now.strftime("%d-%m-%Y %H:%M:%S")
            data.update({"_id": _id})

            db.posts.insert_one(data)
            return jsonify({"message": "Collection added", "id": _id}), 201

        data = db.posts.find({})
        return jsonify({"data": list(data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/sort', methods=['GET'])
def sort():
    try:
        sorted_data = list(db.posts.find({}).sort('title'))
        if not sorted_data:
            return jsonify({"message": "No data found"}), 404
        return jsonify({"Sorted_data": sorted_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/get_specific/<id>', methods=['GET'])
def get_specific(id):
    try:
        find_data = db.posts.find_one({"_id": id})
        if not find_data:
            return jsonify({"message": "No data found"}), 404
        return jsonify({"data": find_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    try:
        result = db.posts.delete_one({"_id": id})
        if result.deleted_count == 0:
            return jsonify({"message": "No post found with that ID"}), 404
        return jsonify({"message": "Post deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/limiteddoc/<int:page>/<int:PAGE_DOC>', methods=['GET'])
def pagination(page, PAGE_DOC):
    try:
        cursor = db.posts.find({}).sort("title").skip(PAGE_DOC * (page - 1)).limit(PAGE_DOC)
        doc_count = db.posts.count_documents({})
        total_pages = (doc_count + PAGE_DOC - 1) // PAGE_DOC

        if page > total_pages or page < 1:
            return jsonify({"message": "No data found"}), 404

        data = list(cursor)
        return jsonify({"PaginatedData": data, "total_pages": total_pages, "current_page": page}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/update/<id>', methods=['PATCH'])
def update_user(id):
    try:
        data = {"$set": dict(request.json)}
        result = db.posts.update_one({"_id": id}, data)

        if result.matched_count == 0:
            return jsonify({"message": "No post found with that ID"}), 404

        return jsonify({"message": f"Post {id} updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
