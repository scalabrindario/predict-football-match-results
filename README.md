# Can you do better than bookmakers?
The objective of this project was to respond to the question: “Can you do better than bookmakers?”. The task was to try to predict the outcome of an event, see with what level of accuracy we were able to carry out this task, then compare it with that of the bookmakers. We are going to illustrate how we tackled the issue and the process that lead us to formulate our prediction model as well as our betting strategy in the end.

We chose to focus on predicting the outcome of football matches, a predicament that had the right amount of complexity thanks to the many factors that could have an influence on it, aided by the abundance of data available, but still retained enough familiarity for us to break it up into smaller steps and decide on the right course of action.

Among all the different tournaments and leagues, we decided upon the Premier League. The dedication of its fans is often paired with a passion for betting on match results, which in turn leads to much scrutiny from bookmakers and the like, which keep detailed records of every aspect regarding the competition in order to produce the best betting odds possible, maximizing their profits.
To start, we sought after all the necessary data about what could influence the ending result of a match and what could give us useful insights about the opponents, to help us predict the winner.

The first and most obvious set of data we looked for was a detailed record of all the information regarding the matches, and we found them from season 2014-15 to 2018-19. This dataset also included the odds for each outcome of the matches, given from an unspecified bookmaker.
This feature stemmed our curiosity and lead us to ask ourselves what the accuracy of a bookmaker is, in order to set a clear goal regarding what level of accuracy should we strive for and try to beat. We calculated the accuracy of the results predicted by the bookmaker in this dataset by comparing the lowest odd of each match to the actual results, calculating how many were right, and found out that they had an accuracy of 55%. This number was not as high as we expected from an agency whose entire business is based on predicting outcomes, but maybe understandable, given the complexity of the task. However, among the seasons contained in this dataset, is the one in which the Leicester won the tournament, against evey possible prediction, so that might have factored in skewing the accuracy compared to periods that didn’t present such anomalies.

In order to verify the truthfulness of the odds currently at our disposal, we looked for additional information about what is the average accuracy of a bookmaker and found out they all fluctuate around that same value. This meant that the exceptional winnings of Leicester didn’t actually change anything, but it was very indicative of just how hard it is to predict these outcomes.

## Data Gathering and Feature Engineering
Now that we understood who we were facing against, we still needed to get data that could help us assess the performance of each team, their strength and their historical match behaviour. In order to do that, we retrieved a dataset listing all the players’ performances in great detail, evaluated by teams of experts of the game FIFA, originally meant to bring the game as close to real life as possible, but also very useful in our case in order to calculate a value that mirrors the overall strength of a team, based on its components.

We calculated this value, called the “Overall” rating by summing each player’s rating, adding a so-called Correction Factor to it, and dividing everything by the number of players. Before proceeding, we must define all the different factors of this formula, starting from the most straight forward, the number of players. We know that each team is made up of 18 players: the starting 11 players with 7 additional substitutes. The Correction Factor is an index that we compute by summing how much does each player’s score differ from the average team score, but halving the value we get for substitute players, so that they will have less of an impact on the Overall equation. After obtaining the CF, we sum it to all the individual scores of the players and divide everything by the number of them.

From this point forward, we calculated many other variables pertaining to the statistics of each match: number of goals, yellow cards, red cards, total shots, shots on target, corners and fouls. All of these stats are calculated for both home and away team, and they are the cumulative number of actions performed by them or conceded to their opponents. These features are then divided by the match week.

These values are an average “thus far”, meaning that they only consider what happened in previous matches, since it would be impossible to know the statistics of a specific match before it starts. For this reason, we didn’t take into consideration any match from the first match week.

However, we also wanted to have a way to evaluate the performance of each of the opponents, based on the results of the previous matches. In order to do that, we took the results of the 5 previous matches and put them into dummies indicating if the results were a win, a loss or a draw, for both teams. This meant that if we wanted to have a full dataset, with all the features being calculated properly and without empty values, we had to take away the first 5 match weeks.

As a final source of data, we looked for a dataset of stadium coordinates, which we used in conjunction with a weather API in order to evaluate the weather at the time of each match. This data was hard to extract, and the numerous calls to the API took a while to complete, but once it was done it helped us infer if there were weather conditions that could affect the players’ performances.

<p align="center"><img src="https://drive.google.com/uc?id=14n3rnTata8lZn_VFMsZpi6Vfrt9facFi" width="600"/></p>

As we can see from the bar chart, the best performing models are: Random forest, Logistic Regression and XGboost.

## Recursive Features Selection
We decided to take the random forest as the core model for the further developments of this project. We started from plotting the importance of all the features.

<p align="center"><img src="https://drive.google.com/uc?id=1Vo28D70yhh0AkNBPzyGkFkclWMgLWSEl" width="600"/></p>


All of this was made with the intent of individuating noisy features that could have a negative impact on the accuracy of our model. The algorithm was able to find the most optimal combination of features to boost the performances of the random forest. This process, followed by bagging, is able to give a higher level of accuracy overall.

<p align="center"><img src="https://drive.google.com/uc?id=1csIgXJQcX2gdeRQbAZqj79UDtKHnL-I-" width="600"/></p>


## Neural network
We wanted to challenge ourselves by trying to use a deep learning method, a neural network. This could help us raise our accuracy more than machine learning techniques. However, due to the limited quantity of data we didn’t make use of the full extent of its capabilities. In fact, the accuracy of this model is more or less on the same level of the above-mentioned prediction methods.

Below you can observe the summary of the sequential model that we applied to our neural network.

<p align="center"><img src="https://drive.google.com/uc?id=1uPvgaxTFRpzi50mj4cGCRPX-WkGCae4m" width="600"/></p>


## Clustering
With the intent of checking if we could improve the accuracy of our models, we wanted to gain some insights about their outputs. These plots reflect the work done so far in the prediction section. In fact, thanks to the elbow method, we observed the presence of three clusters: home win, away win and draw.

We used the two most influential features: the “overall difference” and the “average difference between the corners done and conceded by the away team”.

<p align="center"><img src="https://drive.google.com/uc?id=1yyoaxbI5G97UYKOfDj7K_stgqilRFAX8" width="600"/></p>

Given the values of the two axes, we can insert a point in the graph and see to which cluster the match belongs. This way, we can state the outcome of the match, though with a percentage of uncertainty.

After this, we wanted to distinguish which predictions were wrong and which were not. We did so by plotting the matches with different colors, green for the right ones, red for the ones for which our prediction was incorrect.

<p align="center"><img src="https://drive.google.com/uc?id=1D_SCqAJwA_sxpOABy7rdyAAOpqYZJw0I" width="600"/></p>

We observed that there is a high percentage of wrong predictions in the middle area of the plot, while on the sides there is a low presence of them. The opposite happened with the right predictions, having a higher prevalence on the sides of the plot. This is because a draw is more difficult to predict as a result than a home or an away team win. Additionally, the model used (in this case the random forest) performs better with a high difference between the overall ratings. This is supported by the math computations shown in the related notebook.

## Betting Strategy
As a conclusion for this project, we elaborated a betting strategy.

Of the five years of recorded and processed data at our disposal, we take the 4 least recent ones as training for our algorithm, while we keep the last one for testing. We train the random forest and we try to predict the result of the most recent year, adding to the dataset all the probabilities for the three different outcomes that our model calculated, Home win, Away win and Draw. Then, we apply the following strategy to avoid betting on matches with too little of a difference between the odds. We will try to bet on the best matches for us, but what do we mean by “best”?

In order to define what are the most desirable matches for us to bet on, we must think about what our goal is. What we want is to get the highest return on the money we invest on bets, while also retaining a high level of certainty. This means that we have to strike the right balance between betting on matches with an almost obvious outcome, thus with a slim return, and betting on matches that have a high return, but in turn are very risky. To do that we invented the Caution Betting Index (CBI).

First, we separate the 330 matches into the 10 per week scheduled by the calendar. For each match week, we take the 5 biggest probabilities among all the different odds for the three possible outcomes. Then we calculate the CBI, which is the absolute value of the difference between the half of the highest probability and the absolute value of the difference between the two smaller probabilities. The bigger the difference between the probabilities of the outcome, the bigger the index will be. This index allows us to rank the 5 most likely outcomes from the safest to the riskiest.
Once we rank them, we take the bottom 3, the ones with the smallest CBI, in order to bet on the outcomes with the highest return while still being pretty likely to be correct.

Finally, when all the three predictions prove to be correct, we multiply their odds and multiply it by the amount of money we bet on them. If we bet € 1 per week, we will have a total expense of € 33. On the other hand, the winning would be € 70, so the net profit would be € 37.

<p align="center"><img src="https://drive.google.com/uc?id=12rSSjugYXgJGJxhYqBOxA55MeBgZgpAf" width="600"/></p>

## Collaborators
- [Dario Scalabrin](https://www.linkedin.com/in/scalabrindario/)
- [Andrea Parisi](https://www.linkedin.com/in/andrea-parisi-17950b197)
- [Luca Ballistri](https://www.linkedin.com/in/lucaballistri/)
- [Enrico Grandi](https://www.linkedin.com/in/enrico-grandi/)
- [Rebecca Galassi](https://www.linkedin.com/in/rebecca-galassi-a1b65918b/)
