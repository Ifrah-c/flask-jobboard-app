from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField,FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo("password")])
    role = SelectField("Register As", choices=[('seeker', 'Job Seeker'), ('employer', 'Employer')])
    resume = FileField("Upload Resume", validators=[
    FileAllowed(['pdf', 'doc', 'docx'], 'Only .pdf, .doc, .docx files allowed!')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# ✅ Make sure this exists and is correctly spelled
class JobPostForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    company = StringField("Company Name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    job_type = SelectField("Job Type", choices=[
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Internship", "Internship"),
        ("Remote", "Remote"),
        ("Contract", "Contract")
    ])
    description = TextAreaField("Job Description", validators=[DataRequired()])
    submit = SubmitField("Post Job")


class ApplyForm(FlaskForm):
    message = TextAreaField("Message to Employer", validators=[DataRequired()])
    resume = FileField("Upload Resume", validators=[
        FileAllowed(["pdf", "doc", "docx","png"], "Only PDF/DOC/DOCX/png files allowed!"),
        DataRequired()
    ])
    submit = SubmitField("Apply")



