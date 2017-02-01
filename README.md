# probabilistic-user-tracking-2
The approach taken here is to first group together the users by unique ip first as a unique ip indicates a unique user. Also the same user can access the web using a different device or ip so pairwise similarity is also computed to find the similar users based on their browsing pattern.<br>
In order to capture the same user browsing from a different ip, a similarity function is constructed which takes into account the following features from the log files:
* timestamp
* c_user_agent
* x_ec_custom_1

Timestamp is a useful feature to determine if a certain user accessing the web from a different ip is the same or not. We can use the following logic to do so: A user might access a site from his/her office and during his/her commute from office to home the same site can be accessed from a different ip, and again the same site might be accessed from a different ip from the person’s home. So if we put a certain threshold in the timestamp (lets say 10 - 15 mins), and see in that time duration if a user has accessed the same site with the same device but a different ip, there are high chances that it is the same user. <br>
Also the same logic can be applied to users accessing the same site from a different ip and different device but within a certain time frame. There is high probability that the same user is accessing the site from different devices and different places. <br>
We use raw data from the log files without any transformations. The only transformation we do is to extract the root url from the site visited as the user might request different parts of the same site. So we extract only the root url so that when we compare the urls, they are treated as the same. <br>
For example, the following urls are from the same site, but when we do stringwise comparison they are treated as different ones. <br>
* https://www.youngliving.com/en_US/products/essential-oils/blends
* https://www.youngliving.com/vo/ 
* https://www.youngliving.com/en_US
* https://www.youngliving.com/en_US/products/usb-orb-diffuser<br>

So we do a simple transformation just to extract the main root url which would be https://www.youngliving.com, so that we could treat the users who visited this site to be candidates to similar users. <br>

Below is the python code for the similarity function:
```
def similarity_score(a,b):
    score = [0]*3
    if abs(a["timestamp"] - b["timestamp"]) <= 300:
        score[0] = 1
    if a["c_user_agent"] == b["c_user_agent"]:
        score[1] = 1
    try:
        site_a = (re.search("(?P<url>https?://[^\s]+)", a["x_ec_custom_1"]).group("url")).split('/')[2]
    except:
        site_a = None
    try:
        site_b = (re.search("(?P<url>https?://[^\s]+)", b["x_ec_custom_1"]).group("url")).split('/')[2]
    except:
        site_b = None
    if site_a == site_b:
        score[2] = 1
    weights = [1,2,3]
    return sum(np.array(score)*np.array(weights))/6
```
The function receives 2 different records from the users dataframe, first we check the difference in timestamp. If it’s less than or equal to 300s (which is equal to 5 mins), then we store assign the value 1 to the first index in the list score. Then we compare the user_agents, if they are the same then we assign the value 1 to the second index in the list score. Then at last we compare the transformed x_ec_custom_1 of the 2 users, if they are the same then we assign the value 1 to the last index in the list score. <br>
Then we have a weights list which species how important a feature is in determining the similarity of the users. We multiply our score list with the weights list and sum all the elements together. Then we divide the whole sum by the highest possible score to get our normalized similarity score. <br>

The whole algorithm is as follows:<br>
1. Group the data by unique ip addresses first which divides the whole dataset into groups which contain users with same ip addresses 
2. Then we construct a graph where the nodes are all the entries in the dataset, then we add connections between the users with same ip using the groups formed in step 1. Then we get a graph of users where all the similar users are connected within each other.
3. Then we perform pairwise similarity between all possible pairs from the whole dataset, if a pair has a score that surpasses out threshold then we add a connection between those pairs too. Then what we get is all the similar users connected to each other. 
4. Then we can extract all the connected sub-graphs where each sub-graph can be identified as a unique user.
