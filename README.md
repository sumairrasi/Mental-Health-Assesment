
# Mental Health Assesment

The "Mental Health Assesment" project leverages machine learning and MLOps techniques to detect, analyze, and address mental health challenges within workplace environments. This system is designed to provide early warnings for potential mental health issues, analyze contributing factors, and suggest personalized interventions to promote a healthier work environment.

This project is also aimed at career optimization, highlighting the integration of modern data science practices with real-world mental health challenges in a professional setting.


## Project Architecture

The project follows an MLOps pipeline with six essential steps:

**Data Ingestion:** The data is collected and ingested from a MongoDB database, serving as the primary source for training.

**Data Validation:** Data validation is performed using the MLOps tool, Evidently, to monitor data drift and ensure the dataset's consistency and reliability.

**Data Transformation:** Data preprocessing steps are applied to clean and prepare the data for model training, including handling missing values, feature scaling, and encoding.

**Model Training:** Machine learning models are trained using various algorithms to detect signs of mental health issues based on the input features.

**Model Evaluation:** Models are evaluated based on performance metrics, with the F1 score as the primary measure to ensure balance between precision and recall.

**Model Pusher:** The best-performing model (based on the highest F1 score) is automatically deployed to an AWS S3 bucket for further use.


## MLOps Pipeline

The project employs an MLOps pipeline for continuous integration and deployment (CI/CD), ensuring the workflow is efficient, scalable, and reliable. The key components of the pipeline are:

* **Data Ingestion:** MongoDB is used to extract data for the assessment model.

* **Evidently:** Used for detecting data drift and validating data quality.
* **AWS S3:** The deployment destination for the final model.
## License

[MIT](https://choosealicense.com/licenses/mit/)



