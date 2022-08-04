import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import seaborn as sns


class Set_up_data:
    def __init__(self, Teams_per_year, FIFA_df, FIFA_df_name ,PL_df):
        
        # Names of teams each year
        self.Teams_per_year = Teams_per_year
        
        # FIFA dataframe
        self.FIFA_df = FIFA_df
        
        # Store degli anni
        self.FIFA_df_name = FIFA_df_name
        
        # PL dataframe
        self.PL_df = PL_df
    
    def team_18(self):
        for name, team_list in self.Teams_per_year.items():
            name = name[0:-4] #we remove the ".csv"
            team_list = list(team_list)

            if name == self.FIFA_df_name:
                #We Keep only the rows in the team_list file 
                self.FIFA_df = self.FIFA_df[self.FIFA_df["club"].isin(team_list)]

                #We drop the columns that we don't need
                self.FIFA_df = self.FIFA_df.drop(["player_url","long_name", "dob","nationality","wage_eur","player_positions","international_reputation","work_rate","body_type","real_face","release_clause_eur","team_jersey_number","loaned_from","joined","contract_valid_until","nation_position","nation_jersey_number","ls","st", "rs", "lw", "lf", "cf", "rf" ,"rw","lam", "cam", "ram", "lm", "lcm", "cm","rcm","rm","lwb","ldm", "cdm","rdm","rwb","lb","lcb","cb","rcb","rb"],axis = 1)

                # we drop rows with Team position = RES, so the Reserve players 
                self.FIFA_df = self.FIFA_df[self.FIFA_df.team_position != "RES"]

                # we sort teh dataframe by club value (alphabetic order) and overall points
                self.FIFA_df = self.FIFA_df.sort_values(by=['club','overall'], ascending =[True,False])


            # In order to applay out algorithm we have to keep teh 18 strongest players of each team
            counter = 0
            for index, team in zip((list(self.FIFA_df["sofifa_id"])),(list(self.FIFA_df["club"]))):

                # We keep only the first 18 players
                if counter < 18: 
                    counter += 1
                    keep_team = team
                else:
                    next_team = team 
                    if keep_team == next_team:
                        # we drop rows that we don't need (from the 19th strongest player till last non reserve player of the team )                       

                        self.FIFA_df = self.FIFA_df[self.FIFA_df.sofifa_id != index] 
                    else:
                        counter = 1
        return self.FIFA_df

    def overall_df(self):
        self.FIFA_df = Set_up_data.team_18(self)
        #we do the mean for each club of the player 
        ov_df = self.FIFA_df.groupby("club")["overall"].mean()
        ov_df = ov_df.reset_index()

        # We set index the club
        ov_df = ov_df.set_index("club")

        # We fill the dataframe with zero values
        for i in range(1,19):
            ov_df[i] = np.array(0)

        # We convert all the values in float
        ov_df = pd.DataFrame(ov_df.astype(np.float64))

        return ov_df
    
     
    def overall_team_algorithm (self):
    
        
        ov_df = Set_up_data.overall_df(self)
        
        index = 1

        # We set by index the first team
        check_team = ov_df.index[0]
        for player_club, player_overall in zip (self.FIFA_df["club"], self.FIFA_df["overall"]):

            # We select the specific cell
            club_overall = ov_df.at[player_club, "overall"]

            if check_team == player_club :

                #If the overall is higher than the mean and the player is in the 11 strongest players
                if player_overall > club_overall and index < 12:
                    difference = player_overall - club_overall
                    ov_df.at[player_club, index] = difference

                #If the overall is higher than the mean and the player is NOT in the 11 strongest players    
                if player_overall > club_overall and index >= 12:
                    difference = (player_overall - club_overall)/2
                    ov_df.at[player_club, index] = difference

                #If the overall is lower
                if player_overall < club_overall:
                    ov_df.at[player_club, index] = 0          
                index += 1

            else:
                # Reset the index
                index = 1

                #This in order to add to the dataframe the first player of each team
                if player_overall > club_overall:
                    difference = (player_overall - club_overall)
                    ov_df.at[player_club, index] = difference


                if player_overall < club_overall:
                    ov_df.at[player_club, index] = 0    

                check_team = player_club
                index += 1
        ov_df["marginal"] = ov_df.iloc[:,1:19].sum(axis = 1).reset_index().set_index("club")
        ov_df["final team score"] = ((ov_df["overall"])+(ov_df["marginal"])/18)

        return ov_df
    
    def add_to_PL (self):
    
        ov_df = Set_up_data.overall_team_algorithm(self)
        
    
    # Now we add the overall that we have just calculated in the Premier League dataframe    
        for name, team_list in self.Teams_per_year.items():
            home_team_overall = []
            away_team_overall = []
            name = name[0:-4]

            for home_team, away_team in zip(self.PL_df["home_team_name"],self.PL_df["away_team_name"]):
                for club , overall in zip(ov_df.index, ov_df["final team score"]):
                    if club == home_team:
                        home_team_overall.append(overall)
                    if club == away_team:
                        away_team_overall.append(overall)


        self.PL_df["home_team_overall"] = home_team_overall
        self.PL_df["away_team_overall"] = away_team_overall
        
        # We convert the date format
        
        self.PL_df['date_GMT'] = self.PL_df['date_GMT'].apply(lambda x: dt.datetime.strptime(x,'%b %d %Y - %H:%M%p').strftime('%d-%m-%Y'))

        # we create a column to specify which team won -- H is Home, D is Draw and A is Away
        self.PL_df.loc[self.PL_df['home_team_goal_count'] == self.PL_df['away_team_goal_count'], 'Result'] = "D"
        self.PL_df.loc[self.PL_df['home_team_goal_count'] >  self.PL_df['away_team_goal_count'], 'Result'] = "H"
        self.PL_df.loc[self.PL_df['home_team_goal_count'] <  self.PL_df['away_team_goal_count'], 'Result'] = "A"

        return self.PL_df


# Add a column to the dataframe with the matchweek
def match_week(df):
    counter = 1
    MatchWeek = []
    for i in range(380):
        MatchWeek.append(counter)
        if ((i + 1)% 10) == 0:
            counter += 1
    df['MW'] = MatchWeek
    return df    
    

# Read the csv file
def open_csv(file_name,dataset_position):
    
    file_directory = dataset_position + file_name #we set the file directory
    data_read = pd.read_csv(file_directory)
    data = pd.DataFrame(data_read)
    
    # Storing the year in a string
    data.name = file_name[5:-4]
    
    return data

# Storing which team play each year
def PL_team(element, dataset_position):
    data = open_csv(element,dataset_position)
    
    # Remove the duplicates
    team = set(list(data["home_team_name"]))
    return team


# Check the prediction
def check_the_pred(df, Reality, Pred):
    Check = []
    
    for res, pred in zip(df[Reality], df[Pred]):
        if res == pred:
            Check.append(True)
        else:
            Check.append(False)
    return Check
  
# Plot
def plot_confusion_matrix(cf, classes):
    fig, ax = plt.subplots(figsize = (4,4))
    sns.heatmap(cf, annot = True, fmt='g',
                linewidths = .9, square = True, 
                cmap = 'Blues_r', cbar = False,
                xticklabels = classes,
                yticklabels = classes)

    ax.set_ylabel('True Label', fontsize = 10)
    ax.set_xlabel('Predicted Label', fontsize = 10)

def plot_error_graph(stats,  n, x_label):
    
    fig, ax = plt.subplots(figsize = (4,4))

    ax.plot(n, stats[0,:], 'o:', label = 'Error')
    ax.plot(n, stats[1,:], 'o:', label ='Bias$^2$')
    ax.plot(n, stats[2,:], 'o:', label ='Variance')
    ax.set_xlabel(x_label)
    ax.grid()
    ax.legend()
    
def plot_accuracy(L1, L2, lab1, lab2, n, x_label):
    
    fig, ax = plt.subplots(figsize = (4,4))

    ax.plot(n, L1, 'o:', label = 'Accuracy Train')
    ax.plot(n, L2, 'o:', label = 'Accuracy Valid')
    ax.set_xlabel(x_label)
    ax.grid()
    ax.legend()

# columns to scale
scale_col = ['Hteam_G_got_M', 'Ateam_G_got_M', 'Hteam_G_opp_M', 'Ateam_G_opp_M',
 'Hteam_CC_got_M', 'Ateam_CC_got_M', 'Hteam_CC_opp_M',  'Ateam_CC_opp_M',
 'Hteam_F_got_M', 'Ateam_F_got_M', 'Hteam_F_opp_M', 'Ateam_F_opp_M',
 'Hteam_YC_got_M','Ateam_YC_got_M', 'Hteam_YC_opp_M', 'Ateam_YC_opp_M',
 'Hteam_RC_got_M', 'Ateam_RC_got_M', 'Hteam_RC_opp_M', 'Ateam_RC_opp_M',
 'Hteam_SH_got_M', 'Ateam_SH_got_M', 'Hteam_SH_opp_M', 'Ateam_SH_opp_M',
 'Hteam_SoT_got_M', 'Ateam_SoT_got_M', 'Hteam_SoT_opp_M', 'Ateam_SoT_opp_M',
 'Diff_HT_G_M', 'Diff_AT_G_M',
 'Diff_HT_CC_M', 'Diff_AT_CC_M',
 'Diff_HT_F_M', 'Diff_AT_F_M',
 'Diff_HT_RC_M', 'Diff_AT_RC_M',
 'Diff_HT_SH_M', 'Diff_AT_SH_M',
 'Diff_HT_SoT_M', 'Diff_AT_SoT_M',
 'Diff_HT_YC_M', 'Diff_AT_YC_M',
 'Diff_ov', 
 'apparentTemperatureHigh', 'apparentTemperatureLow', 'apparentTemperatureMax', 'apparentTemperatureMin',
 'cloudCover', 'dewPoint', 'humidity', 'moonPhase', 'pressure', 'precipIntensity',  'precipIntensityMax',
 'precipProbability',  'temperatureHigh','temperatureLow','temperatureMax','temperatureMin',
 'uvIndex', 'visibility',  'windBearing', 'windGust', 'windSpeed']