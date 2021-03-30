from twython import Twython
from keys import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

message = "Test tweet from my Pi using Python. Hello?"
twitter.update_status(status=message)
print("Tweeted: " + message)