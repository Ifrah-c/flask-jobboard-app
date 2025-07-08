from flask import Blueprint, render_template, redirect, url_for, flash, request, abort,current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, JobPost,Application
from app.forms import RegisterForm, LoginForm, JobPostForm,ApplyForm
from app import db, login_manager,mail
import os
from werkzeug.utils import secure_filename
from flask_mail import Message

bp = Blueprint("routes", __name__)

@bp.route('/admin')
@login_required
def admin_dashboard():
    # Optional: check if current_user is admin
    if current_user.role != 'admin':
        return "Unauthorized", 403

    users = User.query.all()
    jobs = JobPost.query.all()
    applications = Application.query.all()

    return render_template('admin_dashboard.html', users=users, jobs=jobs, applications=applications)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route("/")
def home():
    return render_template("index.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("routes.login"))

        hashed_password = generate_password_hash(form.password.data)

        resume_filename = None
        if form.resume.data:
            file = form.resume.data
            resume_filename = secure_filename(file.filename),file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], resume_filename))

        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
            resume=resume_filename
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("routes.login"))
    return render_template("register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("routes.dashboard"))
        flash("Invalid email or password", "danger")
    return render_template("login.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("routes.login"))



@bp.route("/dashboard")
@login_required
def dashboard():
    
    title = request.args.get('title', '').strip()
    location = request.args.get('location', '').strip()

    query = JobPost.query

    if title:
        query = query.filter(JobPost.title.ilike(f"%{title}%"))
    if location:
        query = query.filter(JobPost.location.ilike(f"%{location}%"))

    jobs = query.all()
    return render_template("dashboard.html", jobs=jobs, title=title, location=location,user=current_user)



# @bp.route("/dashboard")
# @login_required
# def dashboard():
#     title = request.args.get("title", "")
#     location = request.args.get("location", "")

#     query = JobPost.query
#     if title:
#         query = query.filter(JobPost.title.ilike(f"%{title}%"))
#     if location:
#         query = query.filter(JobPost.location.ilike(f"%{location}%"))

#     jobs = query.all()

#     return render_template("dashboard.html", jobs=jobs, title=title, location=location, user=current_user)




@bp.route("/post-job", methods=["GET", "POST"])
@login_required
def post_job():
    if current_user.role != "employer":
        abort(403)  # Forbidden access if not employer

    form = JobPostForm()
    if form.validate_on_submit():
        job = JobPost(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            job_type=form.job_type.data,
            description=form.description.data,
            posted_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully!", "success")
        return redirect(url_for("routes.my_jobs"))
    return render_template("post_job.html", form=form)


@bp.route("/my-jobs")
@login_required
def my_jobs():
    if current_user.role != "employer":
        abort(403)
    jobs =JobPost.query.filter_by(posted_by=current_user.id)

    return render_template("my_jobs.html", jobs=jobs)






@bp.route("/apply/<int:job_id>", methods=["GET", "POST"])
@login_required
def apply_job(job_id):
    if current_user.role != 'seeker':
        abort(403)

    job = JobPost.query.get_or_404(job_id)
    employer = job.poster  # ✅ correct relationship

    existing = Application.query.filter_by(job_id=job.id, user_id=current_user.id).first()

    if existing:
        flash("You have already applied for this job.", "info")
        return redirect(url_for("routes.dashboard"))


    form = ApplyForm()
    if form.validate_on_submit():
        # Optional: Save uploaded resume
        if form.resume.data:
            filename = secure_filename(form.resume.data.filename)
            resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(resume_path), exist_ok=True)
            form.resume.data.save(resume_path)
            print("Saved resume at:", resume_path)
            print("Does file exist:", os.path.exists(resume_path))
            current_user.resume = filename
            db.session.commit()

        msg = Message(
            subject=f"New Application for {job.title}",
            sender=current_user.email,
            recipients=[employer.email]
        )
        msg.body = f"""
Hello {employer.name},

{current_user.name} has applied for your job posting: {job.title}

Email: {current_user.email}
Message: {form.message.data}

Resume: {url_for('static', filename='uploads/' + current_user.resume, _external=True) if current_user.resume else 'No resume uploaded'}

Regards,
JobBoard Team
"""
        mail.send(msg)

        application = Application(
            resume_filename = secure_filename(form.resume.data.filename),
            message=form.message.data,
            user_id=current_user.id,
            job_id=job.id
        ) 
        db.session.add(application)
        db.session.commit()
        flash("Your application has been sent to the employer!", "success")
        return redirect(url_for("routes.dashboard"))

    return render_template("apply.html", form=form, job=job)




@bp.route("/job/<int:job_id>/applicants")
@login_required
def view_applicants(job_id):
    if current_user.role != 'employer':
        abort(403)

    job = JobPost.query.get_or_404(job_id)
    if job.posted_by != current_user.id:
        abort(403)

    return render_template("applicants.html", job=job, applicants=job.applications)



@bp.route("/edit-job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    job = JobPost.query.get_or_404(job_id)
    if current_user.role != "employer":
        abort(403)

    form = JobPostForm(obj=job)
    if form.validate_on_submit():
        job.title = form.title.data
        job.company = form.company.data
        job.location = form.location.data
        job.job_type = form.job_type.data
        job.description = form.description.data
        db.session.commit()
        flash("Job updated successfully!", "success")
        return redirect(url_for("routes.my_jobs"))

    return render_template("post_job.html", form=form, edit=True)



@bp.route("/delete-job/<int:job_id>")
@login_required
def delete_job(job_id):
    job = JobPost.query.get_or_404(job_id)
    if current_user.role != "employer" or job.poster != current_user:
        abort(403)

    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully!", "info")
    return redirect(url_for("routes.dashboard"))






