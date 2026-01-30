from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def job_sequencing(jobs):
    # Sort jobs by profit descending
    jobs_sorted = sorted(jobs, key=lambda x: x['profit'], reverse=True)
    
    n = len(jobs)
    slot = [False] * n
    scheduled_jobs = []

    for job in jobs_sorted:
        # Find a free slot before job's deadline
        for j in range(min(n, job['deadline']) - 1, -1, -1):
            if not slot[j]:
                slot[j] = True
                scheduled_jobs.append(job)
                break

    # Selection array for all jobs in original order
    selection = [1 if job in scheduled_jobs else 0 for job in jobs]

    total_profit = sum(job['profit'] for job in scheduled_jobs)
    return scheduled_jobs, total_profit, selection

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jobs = []
        job_ids = request.form.getlist('job_id')
        deadlines = request.form.getlist('deadline')
        profits = request.form.getlist('profit')

        # Build jobs first
        for jid, dl, pf in zip(job_ids, deadlines, profits):
            if jid and dl and pf:
                jobs.append({
                    'id': jid,
                    'deadline': dl,
                    'profit': pf
                })

        # 🔴 Duplicate Job ID check
        if len(job_ids) != len(set(job_ids)):
            return render_template(
                'index.html',
                jobs_entered=jobs,
                error="Job ID must be unique. Duplicate Job IDs found."
            )

        # Convert to int after validation
        for job in jobs:
            job['deadline'] = int(job['deadline'])
            job['profit'] = int(job['profit'])

        scheduled_jobs, total_profit, selection = job_sequencing(jobs)

        return render_template(
            'index.html',
            jobs_entered=jobs,
            scheduled_jobs=scheduled_jobs,
            selection=selection,
            total_profit=total_profit
        )

    return render_template('index.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
