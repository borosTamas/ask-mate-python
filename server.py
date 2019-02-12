from flask import Flask, render_template
import data_manager
app = Flask(__name__)

@app.route('/')
def render_index():
    questions = data_manager.collect_qestions()
    return render_template('index.html', questions=questions)


if __name__=="__main__":
    app.run(
        debug=True,
        port=5000
    )
