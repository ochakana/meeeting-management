import os
from datetime import datetime

from flask import Flask, Response, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from modules.MongoDBClient import MongoDBClient

app = Flask(__name__)

CORS(app)

DATABASE_NAME = "meeting_manager"
COLLECTION_NAME = "agenda"


@app.errorhandler(500)
def internal_error(error):
    print(error)
    return "Internal Server Error", 500


@app.errorhandler(400)
def bad_request(error):
    print(error)
    return jsonify({"error": "Bad Request", "details": str(error)}), 400


@app.route("/api/save", methods=["POST"])
def save_data():
    try:
        # フォームデータの取得するぜ
        data = request.form
        form_data = data.to_dict()

        # 現在の日付と時刻を取得
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        form_data["date"] = current_datetime

        # ファイルの取得と保存
        uploaded_file = request.files.get("file")

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join("/app/uploaded_files", filename))
            form_data["file"] = filename  # ファイル名を辞書に追加

        # MongoDBにデータを保存（MongoDBClientのインスタンスが必要）
        mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")

        mongo_client.insert_data(COLLECTION_NAME, form_data)

        return jsonify({"message": "Done!!"}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/api/get-agendas", methods=["GET"])
def get_agendas():
    try:
        mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")
        agendas = mongo_client.get_data(COLLECTION_NAME)

        # '_id'フィールドを削除
        for agenda in agendas:
            del agenda["_id"]

        return jsonify({"agendas": agendas}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/api/get-agenda/<int:record_id>", methods=["GET"])
def get_agenda(record_id):
    try:
        mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")
        agenda = mongo_client.get_data(COLLECTION_NAME, record_id)

        if agenda:
            del agenda["_id"]
            return jsonify({"agenda": agenda}), 200
        else:
            return jsonify({"error": "Record not found"}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/api/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_from_directory("/app/uploaded_files", filename, as_attachment=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/api/update", methods=["POST"])
def update_data():
    try:
        # フォームデータの取得
        data = request.form
        form_data = data.to_dict()

        # 一意の識別子（例：record_id）を取得
        record_id = form_data.get("record_id")

        # MongoDBに接続
        mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")

        # すべてのフィールドを更新するためのデータを作成
        update_data = {
            "category": form_data.get("category"),
            "proposerName": form_data.get("proposerName"),
            "agendaTitle": form_data.get("agendaTitle"),
            "content": form_data.get("content"),
            "remarksOrQuestions": form_data.get("remarksOrQuestions"),
            # 他のフィールドもここに追加
        }

        # ファイルの取得と保存
        uploaded_file = request.files.get("newFile")

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join("/app/uploaded_files", filename))
            update_data["file"] = filename  # ファイル名を辞書に追加

        # ドキュメントを更新
        mongo_client.update_data(COLLECTION_NAME, record_id, update_data)

        return jsonify({"message": "Updated successfully!"}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/api/delete/<record_id>", methods=["DELETE"])
def delete_data(record_id):
    # MongoDBに接続
    mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")
    mongo_client.delete_data(COLLECTION_NAME, record_id=record_id)
    return jsonify({"message": "Document deleted successfully"}), 200


@app.route("/api/save-category", methods=["POST"])
def save_category():
    mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")
    data = request.json
    mongo_client.insert_data("categories", {"category": data["name"]})
    return jsonify({"message": "Category saved successfully"}), 200


@app.route("/api/delete-category", methods=["DELETE"])
def delete_category():
    data = request.json
    category_names = data.get("selectedNames")  # 配列で受け取る
    mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")
    mongo_client.delete_data("categories", category_names=category_names)

    return jsonify({"message": "Deleted successfully"}), 200


@app.route("/api/get-categories", methods=["GET"])
def get_categories():
    mongo_client = MongoDBClient(f"mongodb://db:27017/{DATABASE_NAME}")
    data = mongo_client.get_data("categories")
    names = [
        item["category"] for item in data if "category" in item
    ]  # 'category'フィールドだけを抽出
    return jsonify(names), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
