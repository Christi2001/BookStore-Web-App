from flask import render_template, flash, request, redirect
from flask.wrappers import Request
from app import app, db
from app.models import Assessment
from .forms import AssessmentForm, IdTypeForm

@app.route('/', methods=['GET', 'POST'])
def home():
	home={'description1':'Welcome to MyToDo!', 'description2':'Select a tab from the navigation bar for the action you want to perform!'}
	return render_template('home.html', title='Home', home=home)

@app.route('/all_assessments', methods=['GET', 'POST'])
def all_assessments():
    # form1,2 are used to retrieve the id of an assessment and the type of button when a button is pushed
    form1 = IdTypeForm()
    form2 = IdTypeForm()
    assessments = Assessment.query
    # rows is used to check if there are assessments created
    rows = assessments.count()
    if request.method == "POST":
        assessment_to_update = Assessment.query.get(form1.id.data)
        # check which button was pressed and perform the corresponding action
        if form2.type.data == "uncompleted":
            assessment_to_update.status = 1
        elif form2.type.data == "completed":
            assessment_to_update.status = 0
        elif form2.type.data == "delete":
            db.session.delete(assessment_to_update)
        try:
            db.session.commit()
            return redirect('/all_assessments')
        except:
            return redirect('/all_assessments')
    else:
        return render_template('all_assessments.html',
                                title='All Assessments',
                                assessments=assessments,
                                form1=form1,
                                form2=form2,
                                rows=rows)

@app.route('/create_assessment', methods=['GET', 'POST'])
def create_assessment():
    form = AssessmentForm()
    if form.validate_on_submit():
        flash('Succesfully added the assessment!')
    if request.method == "POST":
        new_assessment = Assessment(title=form.title.data,
                                    module_code=form.module_code.data,
                                    deadline=form.deadline.data,
                                    description=form.description.data,
                                    status=0)
        try:
            db.session.add(new_assessment)
            db.session.commit()
            return redirect('/create_assessment')
        except:
            return render_template('create_assessment.html',
                        title='Create Assessment',
                        form=form)
    else:
        return render_template('create_assessment.html',
                        title='Create Assessment',
                        form=form)

@app.route('/completed_assessments', methods=['GET', 'POST'])
def completed_assessments():
    # form1,2 are used to retrieve the id of an assessment and the type of button when a button is pushed
    form1 = IdTypeForm()
    form2 = IdTypeForm()
    assessments = Assessment.query.filter_by(status=1)
    # rows is used to check if there are assessments created
    rows = assessments.count()
    if request.method == "POST":
        assessment_to_update = Assessment.query.get(form1.id.data)
        # check which button was pressed and perform the corresponding action
        if form2.type.data == "uncompleted":
            assessment_to_update.status = 1
        elif form2.type.data == "completed":
            assessment_to_update.status = 0
        elif form2.type.data == "delete":
            db.session.delete(assessment_to_update)
        try:
            db.session.commit()
            return redirect('/completed_assessments')
        except:
            return redirect('/completed_assessments')
    else:
        return render_template('completed_assessments.html',
                                title='Completed Assessments',
                                assessments=assessments,
                                form1=form1,
                                form2=form2,
                                rows=rows)

@app.route('/uncompleted_assessments', methods=['GET', 'POST'])
def uncompleted_assessments():
    # form1,2 are used to retrieve the id of an assessment and the type of button when a button is pushed
    form1 = IdTypeForm()
    form2 = IdTypeForm()
    assessments = Assessment.query.filter_by(status=0)
    # rows is used to check if there are assessments created
    rows = assessments.count()
    if request.method == "POST":
        assessment_to_update = Assessment.query.get(form1.id.data)
        # check which button was pressed and perform the corresponding action
        if form2.type.data == "uncompleted":
            assessment_to_update.status = 1
        elif form2.type.data == "completed":
            assessment_to_update.status = 0
        elif form2.type.data == "delete":
            db.session.delete(assessment_to_update)
        try:
            db.session.commit()
            return redirect('/uncompleted_assessments')
        except:
            return redirect('/uncompleted_assessments')
    else:
        return render_template('uncompleted_assessments.html',
                                title='Uncompleted Assessments',
                                assessments=assessments,
                                form1=form1,
                                form2=form2,
                                rows=rows)