import twitter

api = twitter.Api(consumer_key='S0qxTno0fWuYCc175lN0cFDfc', consumer_secret='Hv5IBt1cCeaxWtRyjCilCmLGIUUVDhP3WWDBTfpzuh2xuwP1gk', access_token_key='88917640-oZW6BpeJ7wHMVjPa8o2qquGcN9fxW7985Z4XlxVcO', access_token_secret='Z7sbrHS0WPaTuW6XN4PDsEEViEf67sksh5URKidildgR6')

# print(api.VerifyCredentials())

tweets = api.GetUserTimeline(screen_name='azhryarliansyah', count=10)

for tweet in tweets:
	print(tweet)