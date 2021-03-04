from flask import Flask, render_template, request, redirect
from scrapping import get_jobs
from save import save_file

app = Flask("Scrapper-saramin")

db = {}

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/search")
def search():
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "search.html", 
    searchBy = word, 
    resultNum = len(jobs), 
    jobs = jobs
  )

@app.route("/save")
def save():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_file(jobs, word)
    return save_file(f"job-{word}.csv", attachment_filename=f"job-{word}.csv", as_attachment = True)
  except:
    return redirect("/")

app.run(host="0.0.0.0")