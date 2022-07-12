from operator import methodcaller

from attr import attr
from flask import Flask,redirect,url_for,request,render_template,session #importing the module
from flask_restful import reqparse
from flask_session import Session
from resources.config import Config
from resources.models import db, AuthorModel, PaperModel, ReviewModel, ReviewerModel

# //TODO Pipfile add python version restriction back

app=Flask(__name__) #initiating flask object.
with app.app_context():
    app.config.from_object(Config)
    db.init_app(app)
    db.create_all()
    
Session(app)

@app.route('/')
def index():
    return redirect("/login", code=302)

@app.route("/logout")
def logout():
    session["id"] = None
    return redirect("/")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Flask will return HTTP 400 Bad Request if any request.form[''] entries are null
        parser = reqparse.RequestParser()
        parser.add_argument('email_address', required=True,
                            type=str, help='email_address response is missing')
        parser.add_argument('password', required=True,
                            type=str, help='password response is missing')
        parser.add_argument('account_type', required=True,
                            type=str, help='account_type response is missing')
        request_data = parser.parse_args(strict=True) 
        email = request_data['email_address']
        password = request_data['password']
        login_as = request_data['account_type']
        print(request_data)
        print("choosing an account type");
        if login_as == 'author' or login_as == 'reviewer':
            table_name = login_as

            query = "SELECT * FROM " + table_name + " WHERE email_address = %s AND password = %s"
            result = db.engine.execute(query, (email, password)).fetchone()

            if result is None:
                return render_template('login.html', error_message='User not found in database') # unauthorized, no user in database met criteria

            session['id'] = result[0]
            session['account_type'] = login_as
            session['email_address'] = email
       
            if login_as == 'author':
                return redirect('/author')
            else:   
                return redirect('/reviewer')

        elif login_as == 'admin':
            #hardcode username and ps 
            adminEmail = "admin@a.com"
            adminPs = "admin"

            #check if the user name authenticathe hard coded
            return redirect('/admin')



        else:
            return render_template('login.html', error_message='Invalid account type to login with')
      
        return render_template('login.html') # //FIXME to include any error/success messages
    else:
        if not session.get("id"):
            return render_template('login.html')
        else:
            return redirect("/" + session.get("account_type"))

@app.route('/register', methods = ['POST', 'GET'])
def register(): 
   if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True, type=str,
                            help='first name field is required')
        parser.add_argument('middle_initial', required=True, type=str,
                            help='middle_initial field is required')
        parser.add_argument('last_name', required=True, type=str,
                            help='last_name field is required')
        parser.add_argument('affiliation', required=True, type=str,
                            help='affiliation field is required')
        parser.add_argument('department', required=True, type=str,
                            help='department field is required')
        parser.add_argument('address', required=True,
                            type=str)
        parser.add_argument('city', required=True,
                            type=str, help='city response is missing')
        parser.add_argument('state', required=True,
                            type=str, help='state response is missing')
        parser.add_argument('zip_code', required=True,
                            type=str, help='zip_code response is missing')
        parser.add_argument('phone_number', required=True,
                            type=str, help='phone_number response is missing')
        parser.add_argument('email_address', required=True,
                            type=str, help='email_address response is missing')
        parser.add_argument('password', required=True,
                            type=str, help='password response is missing')
        parser.add_argument('account_type', required=True,
                            type=str, help='account_type response is missing')
        request_data = parser.parse_args(strict=True) 
        # // TODO Try catch for exception handling in render_template return message

        print(request_data)
        first_name = request_data['first_name']
        middle_initial = request_data['middle_initial']
        last_name = request_data['last_name']
        affiliation = request_data['affiliation']
        department = request_data['department']
        address = request_data['address']
        city = request_data['city']
        state = request_data['state']
        zip_code = request_data['zip_code']
        phone_number = request_data['phone_number']
        email = request_data['email_address']
        password = request_data['password']
        account_type = request_data['account_type']

        if account_type != 'reviewer' and account_type != 'author':
            return render_template('register.html', error_message='Invalid account type to register with')
      
        table_name = account_type

        query = "INSERT INTO " + table_name + "(first_name,middle_initial,last_name,affiliation,department,address,city,state,zip_code,phone_number,email_address,password)"
        query += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        db.engine.execute(query, (first_name, middle_initial, last_name, affiliation, department, address, city, state, zip_code, phone_number, email, password))
        print("Created new entry " + email + " in " + table_name)

        return render_template('register.html') # //FIXME to include any error/success messages
   else:
      return render_template('register.html')


@app.route("/author", methods=['POST', 'GET'])
def author():
    if not session.get("id") or session.get("account_type") != 'author':
        return redirect("/login")

    if request.method == 'POST':
        file_name = request.form['file_name']
        title = request.form['title']
        certification = request.form['certification']
        paper_contents = request.form['paper_contents']
        other_description = request.form['other_description']
        topics = tuple(request.form['topics'].split(","))
        query = "INSERT INTO paper (author_id,file_name_original,file_name,title,certification,notes_to_reviewers,other_description"

        for topic in topics:
            query += "," + topic.lower().replace(" ", "_")

        query += ") VALUES (%s,%s,%s,%s,%s,%s,%s"

        for topic in topics:
            query += ",true"

        query += ");"

        db.engine.execute(query, (session.get("id"),file_name,file_name,title,certification,paper_contents,other_description))
    # end if

    papers = db.engine.execute('SELECT title,file_name,certification,other_description FROM paper WHERE author_id = %s', session.get("id")).fetchall()

    return render_template('author.html', papers=papers)

@app.route("/reviewer", methods=['POST', 'GET'])
def reviewer():
    if not session.get("id") or session.get("account_type") != 'reviewer':
        return redirect("/login")

    rating_attributes = db.engine.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'review' AND udt_name = 'float4';").fetchall()

    if request.method == 'POST':
        try:
            print('made it here')
            parser = reqparse.RequestParser()
            parser.add_argument('appropiateness_of_topic', required=True, type=int,
                                    help='appropiateness_of_topic field is required')                         # appropiateness_of_topic: 0,       
            parser.add_argument('timeliness_of_topic', required=True, type=int,
                            help='timeliness_of_topic field is required')                                     # timeliness_of_topic: 0,       
            parser.add_argument('supportive_evidence', required=True, type=int,
                            help='supportive_evidence field is required')                                     # supportiv_eevidence: 0,
            parser.add_argument('technical_quality', required=True, type=int,
                            help='technical_quality field is required')                                       # technical_quality: 0,                      
            parser.add_argument('scope_of_coverage', required=True, type=int,
                            help='scope_of_coverage field is required')                                       # scope_of_coverage: 0,
            parser.add_argument('citation_of_previous_work', required=True, type=int,
                            help='citation_of_previouswork field is required')                                # citation_of_previouswork: 0,
            parser.add_argument('originality', required=True, type=int,
                            help='originality field is required')                                             # originality: 0,
            parser.add_argument('organization_of_paper', required=True, type=int,
                            help='organization_of_paper field is required')                                   # organization_of_paper: 0,
            parser.add_argument('clarity_of_main_message', required=True, type=int,
                            help='clarity_of_mainmessage field is required')                                  # clarity_of_main_message: 0,
            parser.add_argument('mechanics', required=True, type=int,
                            help='mechanics field is required')                                               # mechanics: 0,
            parser.add_argument('suitability_for_presentation', required=True, type=int,
                            help='suitability_for_presentation field is required')                            # suitability_for_presentation: 0,
            parser.add_argument('potential_interestin_topic', required=True, type=int,
                            help='potential_interestin_topic field is required')                              # potential_interestin_topic: 0,
            parser.add_argument('overall_rating', required=True, type=int,
                            help='foverall_rating field is required')                                         # overall_rating: 0,
            parser.add_argument('comfort_level_topic', required=True, type=int,
                            help='comfort_level_topic field is required')                                     # comfort_level_topic: 0,
            parser.add_argument('comfort_level_acceptability', required=True, type=int, 
                            help='comfort_level_acceptability field is required')                             # comfort_level_acceptability: 0,
            parser.add_argument('content_comments', required=True, type=str, 
                            help='content_comments field is required')                                        # content_comments: '',
            parser.add_argument('written_document_comments', required=True, type=str,    
                            help='written_document_comments field is required')                               # written_document_comments: '',
            parser.add_argument('potential_for_oral_presentation_comments', required=True, type=str,    
                            help='potential_for_oral_presentation_comments field is required')                # potential_for_oral_presentation_comments: '',
            parser.add_argument('overall_rating_comments', required=True, type=str,    
                            help='potential_for_oral_presentation_comments field is required')                # overall_rating_comments:'',
            parser.add_argument('paper_id', required=True, type=int,    
                            help='paper_id field is required')
            request_data = parser.parse_args(strict=True) 
            print(request_data)
        except Exception as e:
            print(e)
        # query = "INSERT INTO review (appropiateness_of_topic, timeliness_of_topic, supportiv_eevidence, technical_quality, scope_of_coverage, citation_of_previouswork,"
        # query += "originality, organization_of_paper, clarity_of_main_message, mechanics, suitability_for_presentation, potential_interestin_topic, overall_rating,"
        # query += "comfort_level_topic, content_comments, written_document_comments, potential_for_oral_presentation_comments, overall_rating_comments, author_id"
        query = "INSERT INTO review ("
        for key in request_data:
            query += key + ","
        query = query[:-1]
        query += ") VALUES ("
        for key in request_data:
            query += "%s,"
        query = query[:-1]
        query += ")"
        db.engine.execute(query, (request_data['appropiateness_of_topic'],request_data['timeliness_of_topic'],request_data['supportive_evidence'],request_data['technical_quality'],
        request_data['scope_of_coverage'], request_data['citation_of_previous_work'],request_data['originality'],request_data['organization_of_paper'],request_data['clarity_of_main_message'],
        request_data['mechanics'],request_data['suitability_for_presentation'],request_data['potential_interestin_topic'],request_data['overall_rating'],request_data['comfort_level_topic'],
        request_data['comfort_level_acceptability'],request_data['content_comments'],request_data['written_document_comments'],request_data['potential_for_oral_presentation_comments'],request_data['overall_rating_comments'],request_data['paper_id']))

        # for attr in rating_attributes:
        #     query += "," + attr['column_name']

        # query += ") VALUES (%s,%s,%s,%s"

        # for attr in rating_attributes:
        #     query += ",'" + request.form[attr['column_name']] + "'"

        # query += ");"

        # db.engine.execute(query, (content_comments,potential_for_oral_presentation_comments,overall_rating_comments,session.get("id")))

    #end if

    # Query selects all papers without a review on them
    pending_papers = db.engine.execute('SELECT * FROM paper WHERE (SELECT COUNT(*) FROM review WHERE review.paper_id = paper.paper_id) = 0').fetchall()
    # author_data = db.engine.execute('SELECT first_name, last_name, email_address FROM author WHERE author_id = %s', pending_papers.author_id) # should be a joing but whatever
    return render_template('reviewer.html', rating_attributes=rating_attributes, pending_papers=pending_papers)

@app.route("/administrator")
def administrator():
    if session.get("account_type") != 'administrator':
        return redirect("/login")
    return render_template('admin.html')

@app.route('/profile',methods=['POST', 'GET'])
def profile():

    email = session.get("email_address")
    table_name = session.get("account_type")

    if not session.get("id"):
        return redirect("/login")
    if request.method == 'POST':
        print('made it here')
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', required=True, type=str,
                                help='first name field is required')
            parser.add_argument('middle_initial', required=True, type=str,
                                help='email field is required')
            parser.add_argument('last_name', required=True, type=str,
                                help='email field is required')
            parser.add_argument('affiliation', required=True, type=str,
                                help='password field is required')
            parser.add_argument('department', required=True, type=str,
                                help='phone number field is required')
            parser.add_argument('address', required=True,
                                type=str)
            parser.add_argument('city', required=True,
                                type=str, help='Afiliation response is missing')
            parser.add_argument('state', required=True,
                                type=str, help='Department response is missing')
            parser.add_argument('zip_code', required=True,
                                type=str, help='Address response is missing')
            parser.add_argument('phone_number', required=True,
                                type=str, help='City response is missing')
            request_data = parser.parse_args(strict=True)
            query = "UPDATE " + table_name + " SET first_name = %s,middle_initial = %s,last_name = %s,affiliation = %s,department = %s,address = %s,city = %s,state = %s,zip_code = %s,phone_number = %s "
            query += " WHERE (email_address=%s);"
            db.engine.execute(query,(request_data['first_name'], request_data['middle_initial'], request_data['last_name'], request_data['affiliation'], request_data['department'], request_data['address'], request_data['city'], request_data['state'], request_data['zip_code'], request_data['phone_number'], email))

        except Exception as e:
            print(e)
    query = "SELECT * FROM " + table_name + " WHERE email_address = %s"
    result = db.engine.execute(query, (email)).fetchone()
    return render_template('profile.html', user=result)


@app.route('/papers',methods=['POST', 'GET'])
def paper():
    if not session.get("id"):
        return redirect("/login")
    if session.get('account_type') == 'author':
        # for author get only the papers for the author
        papers="hello"
    if session.get('account_type') == 'reviewer':
        # for reviewerr get all tha papers
        graded_papers = db.engine.execute('SELECT * FROM paper WHERE (SELECT COUNT(*) FROM review WHERE review.paper_id = paper.paper_id) = 1').fetchall()
        # get the columns of the db table to auto generate table with flask 
        paper_attributes = db.engine.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'paper';").fetchall()
        return render_template('papers.html', graded_papers=graded_papers, paper_attributes = paper_attributes)
    if session.get('account_type') == 'admin':
        # do the queries for the required tables
        # fetch reviews 
        # fetch authors 
        # fetch reviewers
        # go to the admin page passing the queries results
        return render_template('adminCPMS.html')

if __name__=='__main__': #calling  main 
    app.debug=True #setting the debugging option for the application instance
    app.run(debug=True) #launching the flask's integrated development webserver
    