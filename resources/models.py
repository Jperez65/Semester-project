from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

                      
class AuthorModel(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(50))
    affiliation = db.Column(db.String(50))
    department = db.Column(db.String(50))
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    phone_number = db.Column(db.String(50))
    email_address = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(5))
     # Paper = db.relationship('Paper', lazy='dynamic')
    def execute_sql(sql_string):
        try:
            data = db.engine.execute(sql_string)
            return data
        except Exception as e:
            print(e)
            return None

    @classmethod
    def create(cls, dict_author):
        query = "INSERT INTO author ("
        for key in dict_author:
            query += key + ","
        query = query[:-1]
        query += ") VALUES ("
        for key in dict_author:
            query += "'" + dict_author[key] + "',"
        query = query[:-1]
        query += ")"
        data = cls.execute_sql(query)
        return data
    
    @classmethod
    def login(cls, dict_login_data):
        try:
            query = f"SELECT password, author_id from author where email_address = '{dict_login_data['email']}'"
            print('query is: '+ query)
            data = cls.execute_sql(query)
            result = data.fetchone()
            if result:
                pass_match = result[0] == dict_login_data['password']
                if pass_match:
                    print('this is true')
                return result[1]
            return None
        except Exception as e:
            print(e)
            return None

class PaperModel(db.Model):
    __tablename__= 'paper'
    paper_id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    active = db.Column(db.Boolean)
    file_name_original = db.Column(db.String(100))
    file_name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    certification = db.Column(db.String(3))
    notes_to_reviewers = db.Column(db.String)
    analysis_of_algorithms = db.Column(db.Boolean)
    applications = db.Column(db.Boolean)
    architecture = db.Column(db.Boolean)
    artificial_intelligence = db.Column(db.Boolean)
    computer_engineering = db.Column(db.Boolean)
    curriculum = db.Column(db.Boolean)
    data_structures = db.Column(db.Boolean)
    databases = db.Column(db.Boolean)
    distance_learning = db.Column(db.Boolean)
    distributed_systems = db.Column(db.Boolean)
    ethical_societal_issues = db.Column(db.Boolean)
    first_year_computing = db.Column(db.Boolean)
    gender_issues = db.Column(db.Boolean)
    grant_writing = db.Column(db.Boolean)
    graphics_image_processing = db.Column(db.Boolean)
    first_year_computing = db.Column(db.Boolean)
    human_computer_interaction = db.Column(db.Boolean)
    laboratory_environments = db.Column(db.Boolean)
    literacy = db.Column(db.Boolean)
    mathematics_in_computing = db.Column(db.Boolean)
    multimedia = db.Column(db.Boolean)
    networking_data_communications = db.Column(db.Boolean)
    nonmajor_courses = db.Column(db.Boolean)
    object_oriented_issues = db.Column(db.Boolean)
    operating_systems = db.Column(db.Boolean)
    parallel_processing = db.Column(db.Boolean)
    pedagogy = db.Column(db.Boolean)
    programming_languages = db.Column(db.Boolean)
    research = db.Column(db.Boolean)
    security = db.Column(db.Boolean)
    software_engineering = db.Column(db.Boolean)
    systems_analysis_and_design = db.Column(db.Boolean)
    using_technology_in_the_classroom = db.Column(db.Boolean)
    web_and_internet_programming = db.Column(db.Boolean)
    other = db.Column(db.Boolean)
    other_description = db.Column(db.String(50))
    # Author = db.relationship('Author', lazy='dynamic')

class ReviewerModel(db.Model):
    __tablename__= 'reviewer'
    reviewer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(50))
    affiliation = db.Column(db.String(50))
    department = db.Column(db.String(50))
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    phone_number = db.Column(db.String(50))
    email_address = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(5))
    analysis_of_algorithms = db.Column(db.Boolean)
    applications = db.Column(db.Boolean)
    architecture = db.Column(db.Boolean)
    artificial_intelligence = db.Column(db.Boolean)
    computer_engineering = db.Column(db.Boolean)
    curriculum = db.Column(db.Boolean)
    data_structures = db.Column(db.Boolean)
    databases = db.Column(db.Boolean)
    distance_learning = db.Column(db.Boolean)
    distributed_systems = db.Column(db.Boolean)
    ethical_societal_issues = db.Column(db.Boolean)
    first_year_computing = db.Column(db.Boolean)
    gender_issues = db.Column(db.Boolean)
    grant_writing = db.Column(db.Boolean)
    graphics_image_processing = db.Column(db.Boolean)
    first_year_computing = db.Column(db.Boolean)
    human_computer_interaction = db.Column(db.Boolean)
    laboratory_environments = db.Column(db.Boolean)
    literacy = db.Column(db.Boolean)
    mathematics_in_computing = db.Column(db.Boolean)
    multimedia = db.Column(db.Boolean)
    networking_data_communications = db.Column(db.Boolean)
    non_major_courses = db.Column(db.Boolean)
    object_oriented_issues = db.Column(db.Boolean)
    operating_systems = db.Column(db.Boolean)
    parallel_processing = db.Column(db.Boolean)
    pedagogy = db.Column(db.Boolean)
    programming_languages = db.Column(db.Boolean)
    research = db.Column(db.Boolean)
    security = db.Column(db.Boolean)
    software_engineering = db.Column(db.Boolean)
    systems_analysis_and_design = db.Column(db.Boolean)
    using_technology_in_the_Classroom = db.Column(db.Boolean)
    web_and_internet_programming = db.Column(db.Boolean)
    other = db.Column(db.Boolean)
    other_description = db.Column(db.String(50))
    reviews_acknowledged = db.Column(db.Boolean)
    review = db.relationship('ReviewModel', backref='review', lazy='dynamic') # This will generate objects from the database dynamically
    active = db.Column(db.Boolean)

    def execute_sql(sql_string):
        try:
            data = db.engine.execute(sql_string)
            return data
        except Exception as e:
            print(e)
            return None

    @classmethod
    def login(cls, dict_login_data):
        try:
            query = f"SELECT password, reviewer_id from reviewer where email_address = '{dict_login_data['email']}'"
            print('query is: '+ query)
            data = cls.execute_sql(query)
            result = data.fetchone()
            if result:
                pass_match = result[0] == dict_login_data['password']
                if pass_match:
                    print('this is true')
                return result[1]
            return None
        except Exception as e:
            print(e)
            return None

    @classmethod
    def create(cls, dict_reviewer):
        topics = dict_reviewer.pop("topics")
        print(topics)
        topic_list = [topic.replace(" ", "_").lower() for topic in topics]
        query = "INSERT INTO reviewer ("
        for key in dict_reviewer:
            query += key + ","
        for topic in topic_list:
            query += topic + ","
        query = query[:-1]
        query += ") VALUES ("
        for key in dict_reviewer:
            query += "'" + dict_reviewer[key] + "',"
        for topic in topic_list:
            query += "'" + '1' + "',"
        query = query[:-1]
        query += ")"
        data = cls.execute_sql(query)
        print(query)
        return data

class ReviewModel(db.Model):
    __tablename__= 'review'
    review_id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    paper_id =   db.Column(db.Integer, db.ForeignKey('paper.paper_id'))
    reviewer_id = db.column(db.Integer, db.ForeignKey('reviewer.reviewer_id'))
    appropiateness_of_topic = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    timeliness_of_topic = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    supportive_evidence = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    technical_quality = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    scope_of_coverage = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    citation_of_previous_work = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    originality = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    content_comments = db.Column(db.String)
    organization_of_paper = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    clarity_of_main_message = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    mechanics = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    written_document_comments = db.Column(db.String)
    suitability_for_presentation = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    potential_interestin_topic = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    potential_for_oral_presentation_comments = db.Column(db.String)
    overall_rating = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    overall_rating_comments = db.Column(db.String)
    comfort_level_topic = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    comfort_level_acceptability = db.Column(db.Float(precision=3, decimal_return_scale=2), default=0.0)
    complete = db.Column(db.Boolean)

class DefaultsModel(db.Model):
    __tablename__= 'Defaults'
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    Enabled_Reviewers = db.Column(db.Boolean)
    Enabled_Authors = db.Column(db.Boolean)
