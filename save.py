import csv

def save_file(jobs, word):
  file = open(f"job-{word}.csv", mode="w", encoding="utf-8")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Condition", "Link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return