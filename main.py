from youtube_functions import Youtube
import pandas as pd

obj1 = Youtube("Krish Nayak")
response = []
comment=[]
for i in range(1):
    details, comments=obj1.extract_everything_from_video(i)
    # details.update(comments)
    response.append(details)
    comment.append(comments)
pd.DataFrame(response).to_csv("data.csv")
pd.DataFrame(comment).to_csv("comments.csv")
