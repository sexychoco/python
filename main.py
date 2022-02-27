from flask import Flask, render_template, request,redirect,send_file
from so import get_jobs as so_jobs
from ok import get_jobs as ok_jobs 
from wwr import get_jobs as wwr_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      first_jobs = so_jobs(word)
      second_jobs = ok_jobs(word)
      third_jobs = wwr_jobs(word)
      jobs = first_jobs + second_jobs + third_jobs
      db[word] = jobs 
  else:
    return redirect("/")
  return render_template("report.html",searchingBy=word,resultsNumber=len(jobs),jobs=jobs)

@app.route("/export")
def export():
  try:
    word= request.args.get('word')
    if not word:
      raise Exception()
    word=word.lower()
    jobs= db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0", port=8080)
    