##EARTHQUAKES##

###WHAT MORE CAN WE DO###
 
- As of now, I retrieve all the values from the DB and its not an Async call. First step would be to make it async and 
give users the newest data if its 30 days

- DB used right now is relational. If we think our uses cases are not going to expand, we might consider using a Time
Series DB or even Key Value Store Directly for Places and Lat Long

- In terms of completion, we need TESTS. The code is modular enough to write them, but did not get enough time to do that. 

- 