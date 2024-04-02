from flask import Flask, render_template, request
from models import SentimentAnalyzer
from auth import API_KEY

app = Flask(__name__)
api_key = API_KEY
sentiment_analyzer = SentimentAnalyzer(api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    video_id = request.form['video_id']
    comments_df = sentiment_analyzer.analyze_sentiment(video_id)
    
    positivesvm = 0
    positiverm=0
    negativesvm = 0
    negativerm=0
    neutralsvm = 0
    neutralrm=0
    
    for _, row in comments_df.iterrows():
        if row['SVM Sentiment'] == 'Positive':
            positivesvm += 1
        elif row['SVM Sentiment'] == 'Negative':
            negativesvm += 1
        else:
            neutralsvm += 1
    
    for _, row in comments_df.iterrows():
        if row['Random Forest Sentiment'] == 'Positive':
            positiverm += 1
        elif row['Random Forest Sentiment'] == 'Negative':
            negativerm += 1
        else:
            neutralrm += 1
     
    possvm = round(100 * positivesvm / 15, 2)
    negsvm = round(100 * negativesvm / 15, 2)
    neusvm = round(100 * neutralsvm / 15, 2)
    posrm = round(100 * positiverm / 15, 2)
    negrm = round(100 * negativerm / 15, 2)
    neurm = round(100 * neutralrm / 15, 2)


    svmVerdict = ""
    if(possvm>negsvm):
        svmVerdict="POSITIVE"
    else:
        svmVerdict="NEGATIVE"

    app.logger.info(f"Positive SVM: {positivesvm}, Negative SVM: {negativesvm}, Neutral SVM: {neutralsvm}")
    return render_template('results.html', comments_df=comments_df,possvm=possvm, negsvm=negsvm, neusvm=neusvm, posrm=posrm, negrm=negrm, neurm=neurm,svmVerdict=svmVerdict)

if __name__ == '__main__':
    app.run(debug=True)

