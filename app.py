from flask import Flask, render_template, request, jsonify,redirect,url_for
from flask.views import MethodView
# from typing import Optional
from Mental_Health.constants import APP_HOST, APP_PORT
app = Flask(__name__)

class MentalHealthAssessment(MethodView):
    # def __init__(self):
    #     # Initialize all fields to None
    #     self.age: Optional[str] = None
    #     self.gender: Optional[str] = None
    #     self.family_history: Optional[str] = None
    #     self.benefits: Optional[str] = None
    #     self.care_options: Optional[str] = None
    #     self.anonymity: Optional[str] = None
    #     self.leave: Optional[str] = None
    #     self.work_interfere: Optional[str] = None
        
    def get(self):
        return render_template('mentalhealth.html')

    def post(self):
        from Mental_Health.pipeline.prediction_pipeline import MentalhealthData, MentalHealthClassifier

        # Extract form data
        age = request.form.get('age')
        gender = request.form.get('gender')
        family_history = request.form.get('family_history')
        benefits = request.form.get('benefits')
        care_options = request.form.get('care_options')
        anonymity = request.form.get('anonymity')
        leave = request.form.get('leave')
        work_interfere = request.form.get('work_interfere')
        remote_work = request.form.get('remote_work')
        
        mentalhealth_data = MentalhealthData(
            age=age,
            gender=gender,
            family_history=family_history,
            benefits=benefits,
            care_options=care_options,
            anonymity=anonymity,
            leave=leave,
            work_interfere=work_interfere,
            remote_work = remote_work
        )
        
        mh_data = mentalhealth_data.get_mentalhealth_input_data_frame()
        
        model_predictor = MentalHealthClassifier()
        
        value = model_predictor.predict(dataframe=mh_data)[0]
        
        status = None
        if value == 1:
            status = "No treatment needed"
        else:
            status = "treatment needed"
            
        return render_template("mentalhealth.html",status={"status":status})

        




class TrainMentalHealthModel(MethodView):
    def get(self):
        from Mental_Health.pipeline.training_pipeline import TrainingPipeline

        # Logic for rendering a training page or handling GET requests
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return "Model training finished"

    def post(self):
        # Logic to handle the model training process
        # For instance, initiating model training or uploading training data
        return jsonify({"message": "Model training started"})



# Register the view
app.add_url_rule('/', view_func=MentalHealthAssessment.as_view('mental_health_assessment'))
app.add_url_rule('/train', view_func=TrainMentalHealthModel.as_view('train_mental_health_model'))

if __name__ == '__main__':
    app.run(debug=True,host=APP_HOST,port=APP_PORT)
