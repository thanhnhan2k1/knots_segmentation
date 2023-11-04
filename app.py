import json
import base64
from flask import Flask
from flask import render_template, url_for, redirect, request, send_from_directory, jsonify
import cv2
import predict_knots as predict
from image_segmetation import Output
from werkzeug.utils import secure_filename
import os
import firebase_storage_service as storage
import json

app = Flask(__name__, template_folder='templates', static_folder="images")
app.config["UPLOAD_FOLDER"] = "G:/DA/knots_prediction/uploads"
app.add_url_rule(
    "/upload_image", endpoint="predict_image", build_only=True
)
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], "image.jpg"))
        # image_b64 = base64.b64encode(image.read()).decode('utf8')
        # cv2.imwrite("images/image.jpg", cv2.imread(image))
        # return redirect(url_for('download_file', name = filename))
        return render_template(url_for('upload_image'))
    # file = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', title = 'Home')

@app.route('/uploads', methods = ["GET", "POST"])
def predict_knot():
    image = request.args.get('image')
    result = predict.predict_image_remote(image)
    result_url = storage.upload_image_to_firebase("images/result.jpg")
    if result != None:
        number_of_single, number_of_double, average_area_single, average_area_double = predict.get_average_area(result)
        output = Output(number_of_single, number_of_double, average_area_single, average_area_double)
        return jsonify(output.toJson(result_url))
    else: 
        return jsonify("No result")

@app.route("/upload_image", methods=["POST"])
def upload_image():
    result = predict.predict_image_local("uploads/image.jpg")
    # image_b64 = request.form.get("/image/image.jpg")
    number_of_single, number_of_double, average_area_single, average_area_double = predict.get_average_area(result)
    return render_template("upload_image.html", image_link = "/uploads/image.jpg", result_link = "/images/result.jpg"
    , number_single = number_of_single, number_double = number_of_double,
    area_single = average_area_single, area_double = average_area_double)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    # index()