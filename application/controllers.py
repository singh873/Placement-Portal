from flask import Flask,render_template,redirect,request,flash
from flask import current_app as app
app.secret_key = "secret123"   # ye login page pe message ke liye
from datetime import datetime

from .models import *




# login/register part start---------------------

@app.route("/register",methods=["GET","POST"])
def register():
    
    if request.method=="GET":
        return render_template("register.html")
    else:
        full_name=request.form.get("f_name")
        email_id=request.form.get("email")
        password=request.form.get("pwd")

        this_user=User.query.filter_by(email=email_id).first()

        if this_user:
            flash("Already Register Student. Please login.", "error")
            return redirect("/login")
        else:
            new_user=User(full_name=full_name,email=email_id,password=password)
            db.session.add(new_user)
            db.session.commit()
        return redirect("/login")
    

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email_id = request.form.get("email")
    password = request.form.get("pwd")

    # User table------
    this_user = User.query.filter_by(email=email_id).first()

    if this_user:
        if this_user.status=="blocked":
            flash("Your Account is Blocked", "error")
            return redirect("/login")
        
        elif this_user.password == password:
            if this_user.type == "admin":
                return redirect("/admin_dash")
            else:
                this_user.type == "student"
                return redirect(f"/student_dash/{this_user.id}")
        else:
            flash("Wrong password", "error")
            return redirect("/login")

    # Company table---------
    this_comp = Company.query.filter_by(email=email_id).first()
    if this_comp:
        if this_comp.approval_status=="blocked":
            flash("Your Company Account is Blocked", "error")
            return redirect("/login")
        if this_comp.approval_status=="pending":
            flash("Your Account is Under Verification", "error")
            return redirect("/login")
        
        elif this_comp.password == password:
            return redirect(f"/comp_dash/{this_comp.id}")
        else:
            flash("Wrong password", "error")
            return redirect("/login")

    # If not found anywhere
    flash("Invalid email or password", "error")
    return redirect("/login")

        
# login/register part end ---------------


#company register start-------------------------------

@app.route("/comp_register", methods=["GET","POST"])
def comp_register():
    if request.method=="GET":
        return render_template("comp_register.html")
    else:
        comp_name=request.form.get("c_name")
        email_id=request.form.get("email")
        password=request.form.get("pwd")
        comp_no=request.form.get("num")
        comp_web=request.form.get('web')

        this_comp=Company.query.filter_by(email=email_id).first()
        if this_comp:
            flash("Already Register Company. Please login.", "error")
            return redirect("/login")
        else:
            new_comp=Company(name=comp_name,email=email_id,password=password,company_no=comp_no,website=comp_web)
            db.session.add(new_comp)
            db.session.commit()
        return redirect("/login")
    
#company register end-------------------------------


#admin Dashbord start-----------------

@app.route("/admin_dash",methods=["GET","POST"])
def admin_dash():
    this_user=User.query.filter_by(type="admin").first()
    approve_company = Company.query.filter((Company.approval_status == "approved") | (Company.approval_status == "blocked")).all()
    reg_student=User.query.filter_by(type="student").all()
    req_company=Company.query.filter((Company.approval_status == "pending") | (Company.approval_status == "approved") |(Company.approval_status == "rejected")).all()
    req_jobs=Jobs.query.filter_by(job_status="pending").all()
    ongoing_jobs=Jobs.query.all()
    std_application = Application.query.all()



    return render_template("admin_dash.html",this_user=this_user,approve_company=approve_company,
                           reg_student=reg_student,req_company=req_company,req_jobs=req_jobs,
                           std_application=std_application,ongoing_jobs=ongoing_jobs)


#Company aproove & reject

@app.route("/approve/<int:comp_id>")
def approve_comp(comp_id):
    comp_req=Company.query.filter_by(id=comp_id).first()
    comp_req.approval_status="approved"
    db.session.commit()
    return redirect(f"/admin_dash")

@app.route("/reject/<int:comp_id>")
def reject_comp(comp_id):
    comp_req=Company.query.filter_by(id=comp_id).first()
    comp_req.approval_status="rejected"
    db.session.commit()
    return redirect(f"/admin_dash")


#Company block & unblock

@app.route("/block/<int:comp_id>")
def block_comp(comp_id):
    comp_req=Company.query.filter_by(id=comp_id).first()
    comp_req.approval_status="blocked"
    db.session.commit()
    return redirect(f"/admin_dash")

@app.route("/unblock/<int:comp_id>")
def unblock_comp(comp_id):
    comp_req=Company.query.filter_by(id=comp_id).first()
    comp_req.approval_status="approved"
    db.session.commit()
    return redirect(f"/admin_dash")

#ye student ko block & unblock krega

@app.route("/std_block/<int:std_id>")
def block_std(std_id):
    std_block=User.query.filter_by(id=std_id).first()
    std_block.status="blocked"
    db.session.commit()
    return redirect(f"/admin_dash")

@app.route("/std_unblock/<int:std_id>")
def unblock_std(std_id):
    std_unblock=User.query.filter_by(id=std_id).first()
    std_unblock.status="active"
    db.session.commit()
    return redirect(f"/admin_dash")

#job aproove & reject

@app.route("/job_approve/<int:job_id>")
def job_approve(job_id):
    job_req=Jobs.query.filter_by(id=job_id).first()
    job_req.job_status="approved"
    db.session.commit()
    return redirect(f"/admin_dash")

@app.route("/job_reject/<int:job_id>")
def job_reject(job_id):
    job_req=Jobs.query.filter_by(id=job_id).first()
    job_req.job_status="rejected"
    db.session.commit()
    return redirect(f"/admin_dash")

#ye job show krega(card)

@app.route("/job_details/<int:job_id>",methods=["GET","POST"])
def job_details(job_id):
    view_job=Jobs.query.filter_by(id=job_id).first()
    return render_template("job_details_admin.html",view_job=view_job)


#ye view student application

@app.route("/view_std_app/<int:std_id>/<int:job_id>",methods=["GET","POST"])
def view_std_app(std_id,job_id):
    this_std=User.query.filter_by(id=std_id).first()
    this_job=Jobs.query.filter_by(id=job_id).first()
    return render_template("sdt_appli_admin.html",this_std=this_std,this_job=this_job)


#ye student ko delete krega

@app.route("/delete_std/<int:sdt_id>")
def delete_sdt(sdt_id):
    this_std = User.query.get(sdt_id)

    db.session.delete(this_std)
    db.session.commit()
    return redirect(f"/admin_dash")


#ye company ko delete krega

@app.route("/delete_comp/<int:comp_id>")
def delete_comp(comp_id):
    this_comp = Company.query.get(comp_id)

    db.session.delete(this_comp)
    db.session.commit()
    return redirect(f"/admin_dash")


#ye search krega

@app.route("/admin_search/<int:admin_id>")
def admin_search(admin_id):

    admin=User.query.filter_by(id=admin_id).first()
    key = request.args.get("key")
    search_word = request.args.get("search")

    applied_jobs=None
    jobs=None

    if key == "student":
        results = User.query.filter((User.id == search_word) | (User.full_name == search_word) | (User.email == search_word)).first()
        applied_jobs=Application.query.filter_by(student_id=results.id).all()
    else:
        results = Company.query.filter((Company.id == search_word) | (Company.name == search_word) | (Company.email == search_word)).first()
        jobs=Jobs.query.filter_by(company_id=results.id).all()
    return render_template("admin_search.html", results=results,admin=admin,key=key,applied_jobs=applied_jobs,jobs=jobs)


#admin  end-----------------



# company start-----------------

@app.route("/comp_dash/<int:comp_id>",methods=["GET","POST"])
def comp_dash(comp_id):
    this_comp=Company.query.filter_by(id=comp_id).first()
    comp_job=Jobs.query.filter(Jobs.company_id==comp_id,Jobs.job_status != "complete").all()
    completed_job=Jobs.query.filter(Jobs.company_id==comp_id,Jobs.job_status == "complete").all()
    std_application=Application.query.all()
    return render_template("comp_dash.html",this_comp=this_comp,comp_job=comp_job,
                           completed_job=completed_job,std_application=std_application)



#create job

@app.route("/create_job/<int:comp_id>",methods=["GET","POST"])
def create_job(comp_id):
    if request.method=="GET":
        return render_template("create_job.html",comp_id=comp_id)
    else:
        job_title=request.form.get("job_title")
        job_description=request.form.get("job_desc")
        eligibility=request.form.get("elig")
        salary=request.form.get("sal")
        location=request.form.get("loca")
        deadline_str = request.form.get("deadline")
        job_deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

        new_job=Jobs(company_id=comp_id,job_title=job_title,job_description=job_description,
                     eligibility=eligibility,salary=salary,location=location,job_deadline=job_deadline)
        db.session.add(new_job)
        db.session.commit()

        return redirect(f"/comp_dash/{comp_id}")

#update job

@app.route("/update_job/<int:job_id>/<int:comp_id>",methods=["GET","POST"])
def update_job(job_id,comp_id):
    if request.method=="GET":
        this_job=Jobs.query.filter_by(id=job_id).first()
        return render_template("update_job.html",this_job=this_job,comp_id=comp_id)
    else:
        job_title=request.form.get("job_title")
        job_description=request.form.get("job_desc")
        eligibility=request.form.get("elig")
        salary=request.form.get("sal")
        location=request.form.get("loca")

        update_job=Jobs.query.filter_by(id=job_id).first()

        update_job.job_title=job_title
        update_job.job_description=job_description
        update_job.eligibility=eligibility
        update_job.salary=salary
        update_job.location=location
        update_job.company_id=comp_id

        update_job.job_status="pending"

        db.session.commit()
        return redirect(f"/comp_dash/{comp_id}")
    

#ye company ka 1 job ka sare apllication show krega

@app.route("/comp_appli/<int:job_id>/<int:comp_id>",methods=["GET","POST"])
def comp_appli(job_id,comp_id):
    this_application=Application.query.filter_by(job_id=job_id,status="applied").all()
    this_comp=Company.query.filter_by(id=comp_id).first()
    this_job=Jobs.query.filter_by(id=job_id).first()
    return render_template("comp_application.html",this_application=this_application, this_comp=this_comp,this_job=this_job)

#ye job ko mark as complete karega

@app.route("/mark_comp/<int:job_id>",methods=["GET","POST"])
def mark_comp(job_id):
    this_job=Jobs.query.filter_by(id=job_id).first()
    this_job.job_status="complete"
    db.session.commit()
    return redirect(f"/comp_dash/{this_job.company_id}")


#ye view student application

@app.route("/review_std_appli/<int:std_id>/<int:job_id>",methods=["GET","POST"])
def review_std_appli(std_id,job_id):
    this_std=User.query.filter_by(id=std_id).first()
    this_job=Jobs.query.filter_by(id=job_id).first()
    return render_template("sdt_appli_comp.html",this_std=this_std,this_job=this_job)

#ye view student application

@app.route("/view_all_std_app/<int:std_id>/<int:job_id>",methods=["GET","POST"])
def view_all_std_app(std_id,job_id):
    this_std=User.query.filter_by(id=std_id).first()
    this_job=Jobs.query.filter_by(id=job_id).first()
    return render_template("view_resume.html",this_std=this_std,this_job=this_job)

#ye shortlist krega

@app.route("/update_status/<int:job_id>/<int:std_id>",methods=["GET","POST"])
def update_status(job_id,std_id):
    this_appli=Application.query.filter_by(job_id=job_id,student_id=std_id).first()
    this_job=Jobs.query.filter_by(id=job_id).first()

    status = request.form.get("status")
    this_appli.status= status

    db.session.commit()
    return redirect(f"/comp_appli/{job_id}/{this_job.company_id}")



#company end-----------------


#student start---------------

@app.route("/student_dash/<int:std_id>",methods=["GET","POST"])
def std_dash(std_id):
    this_student=User.query.filter_by(id=std_id).first()
    active_comp=Company.query.filter_by(approval_status="approved").all()
    appiled_jobs=Application.query.filter_by(student_id=std_id).all()
    return render_template("student_dash.html",this_student=this_student,active_comp=active_comp,appiled_jobs=appiled_jobs)

#ye show company all jobs

@app.route("/view_job/<int:comp_id>/<int:std_id>",methods=["GET","POST"])
def view_job(comp_id,std_id):
    this_comp_jobs=Jobs.query.filter_by(company_id=comp_id).all()
    this_comp=Company.query.filter_by(id=comp_id).first()
    return render_template("view_job_std.html",this_comp_jobs=this_comp_jobs,this_comp=this_comp,std_id=std_id)

#ye show paticular 1 ka company 1 ka job

@app.route("/job_details_std/<int:job_id>/<int:std_id>",methods=["GET","POST"])
def job_details_std(job_id,std_id):
    view_job=Jobs.query.filter_by(id=job_id).first()
    # already applied h ya nhi
    allraedy_apply = Application.query.filter_by(student_id=std_id,job_id=job_id).first()
       
    return render_template("job_details_std.html",view_job=view_job,std_id=std_id,allraedy_apply=allraedy_apply)



#ye student profile update kerega

@app.route("/std_prof_update/<int:std_id>",methods=["GET","POST"])
def prof_update(std_id):
    this_std=User.query.filter_by(id=std_id).first()
    if request.method=="GET":
        return render_template("std_profile.html",this_std=this_std)
    else:
        Full_name=request.form.get("f_name")
        Education=request.form.get("edu")
        Cgpa=request.form.get("cgpa")
        Address=request.form.get("addr")
        Linkedin=request.form.get("link")
        Github=request.form.get("git")
        Hobby=request.form.get("hobby")

        update_std=User.query.filter_by(id=std_id).first()

        update_std.full_name=Full_name
        update_std.education=Education
        update_std.cgpa=Cgpa
        update_std.address=Address
        update_std.linkdin=Linkedin
        update_std.github=Github
        update_std.hobby=Hobby

        db.session.commit()

        return redirect(f"/student_dash/{std_id}")


#apply job

@app.route("/apply_job/<int:job_id>/<int:std_id>",methods=["GET","POST"])
def apply_job(job_id,std_id):

    # already applied h ya nhi
    allraedy_apply = Application.query.filter_by(student_id=std_id,job_id=job_id).first()
    this_job=Jobs.query.filter_by(id=job_id).first()
    

    if allraedy_apply:
        flash("You have already applied for this job.")
        return redirect(f"/job_details_std/{this_job.id}/{std_id}")

    # create new application
    new_application = Application(student_id=std_id,job_id=job_id,status="applied")

    db.session.add(new_application)
    db.session.commit()

    flash("Job applied successfully!")
    return redirect(f"/job_details_std/{this_job.id}/{std_id}")


#ye student application history show krega

@app.route("/history/<int:std_id>",methods=["GET","POST"])
def history(std_id):
    appli_hist=Application.query.filter_by(student_id=std_id).all()
    this_std=User.query.filter_by(id=std_id).first()
    return render_template("student_history.html",appli_hist=appli_hist,this_std=this_std)

#student end---------------
#last comit 6 march