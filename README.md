# AnomalyDetection
A simple unsupervisied machine learning algorithm that detects anomalies in testing data based on prior training data. 
It uses different clustering methods to create an original knowledge base in order to detect anomalies

Generator.py generates random data. User input is prompted during running the program. Run with "python Generator.py"
main.py is the main program. It also prompts user input during the program. Run with "python main.py"

Examples of the clustering that I have so far:

![alt tag](https://github.com/eswardhinak/AnomalyDetection/blob/master/pics/figure_1.png)
This is just with 2 dimensions specifying each point in order to make it easier to visualize. The clustering can take as many dimensions as specified. Each dimension (x and y) can range from 0 to 10,000. It is with randomly generated 500 points with 20 clusters. The red points are the centers of the clusters. All the points of the same color surrounding a red point are in that cluster. I am using matplotlib to graph it. 

![alt tag](https://github.com/eswardhinak/AnomalyDetection/blob/master/pics/figure_2.png)
This is also 2 dimensions. Same as the previous image, each dimension ranges from 0 to 10,000. It is with randomly generated 750 points with 20 clusters. The red points are the centers. 

![alt tag](https://github.com/eswardhinak/AnomalyDetection/blob/master/pics/figure_3.png)
This is 3 dimensions. It is sort of hard to see what is going on. Although some different colors look to be right next to each other, one of the colors is actually deeper into picture. This is with randomly generated 750 points with 20 clusters. The red points are centers of the clusters. 

Issues:
This is pretty slow. It takes about a minute for it to cluster 750 points. I am looking into seeing if I can do it faster by threading it or with a more efficient clustering algorithm. 

Things To Do: 
I will be figuring out how to normalize points so that I can use data.gov data to see the algorithms performance. I will need to normalize because different dimensions values can range but their effect on the anomaly should be the same.






