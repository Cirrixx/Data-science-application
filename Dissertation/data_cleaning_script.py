import pandas as pd
import numpy as np
import glob 

#Bias thresholds:
AFC_BIAS = 14
ONLINE_BIAS = 48 
ONLINE_BIAS_MULTIPLIER = 0.50
BIAS_SD = 1


#-----------------------------------------Custom functions-----------------------------------------#
def online_fixer(df):
    df = df.rename(columns = {"Spreadsheet: randomise_trials":"randomise_trials",
     "Spreadsheet: condition":"condition","Screen":"Screen Name"}) #renames columns to match task builder 1 names (ensures consistency across sheets)
    return df

def AFCfixer(df):
    """Used to fix the spatial condition of the 2-AFC"""
    #determine how many participants will be dropped 
    dropped_ids = df[((df["condition"] == "cueless") & (df["randomiser-wnns"] == "spatial_cue"))]
    ids = dropped_ids["Participant Private ID"].unique()
    with open("problem_data.txt", mode = "a") as text:
        text.write(f"[AFC_FIXER] Data from {len(ids)} participants were dropped due to the programming error. \n")
    #drop all of the erroneous rows 
    return df[~((df["condition"] == "cueless") & (df["randomiser-wnns"] == "spatial_cue"))] #only retains rows not meeting these conditions


def sd_checker(df):
    """Used to calculate standard deviations"""
    df = df.groupby(["id", "block","condition","position"]).mean(numeric_only = True).reset_index()
    deviations = df.groupby("condition")["rt"].std(numeric_only = True).reset_index()
    return deviations

def sd_dropper(df):
    """Drops trials where ppts response time was greater than 2SDs from their mean"""
    #calculate standard deviations
    deviations = sd_checker(df)
    #calculate means
    ppt_means = df.groupby("id").mean().reset_index()
    mean_dict = dict(zip(list(ppt_means["id"]), list(ppt_means["rt"])))
    dev_dict = dict(zip(list(deviations["condition"]), list(deviations["rt"])))
    dropped_rows = 0
    total_rows = 0
    #drop values 2SD greater than ppts means 
    for index, row in df.iterrows():
        if row["rt"] <= (mean_dict[row["id"]]+(dev_dict[row["condition"]] *2)): #checks if participants RT is 2SDs (determined by condition) than their mean
            pass
        else: 
            df.drop(index = index, inplace = True)
            dropped_rows += 1
        total_rows +=1 
    #calculate mean for each subgroup -> moved here to prevent redundant code 
    df = df.groupby(["id", "block","condition","position"]).mean(numeric_only = True).reset_index() #need to reset index to prevent groupby breaking the use of keys
   
    with open("problem_data.txt", "a") as text: 
        text.write(f"[SD DROPPER] Number of dropped rows: {dropped_rows}\tTotal Number of rows: {total_rows}\n")
    return df

def AFC_bias_chekcer(data, dropped_ids):
    
    #get all unique participant ids 
    ids = data.groupby("Participant Private ID").mean().index.tolist()

    count = None #create placeholder value
    for id in ids: 
        ppt_data = data[data["Participant Private ID"] == id] #create smaller dataset containing only participant's id
        count = ppt_data["Response"].value_counts() #count unique responses 
        if count["first"] >= AFC_BIAS or count["second"] >=AFC_BIAS: #determine if made same response more than 80% trials
            dropped_ids.append(id) 
            
        else: 
            pass 
        
    print(f"[2-AFC] Data from {len(dropped_ids)} was dropped for response biases")
    with open("problem_data.txt", mode = "a") as text:
        text.write(f"[2-AFC] Data from {len(dropped_ids)} participants was dropped for response bias\n")
    return data[~ data["Participant Private ID"].isin(dropped_ids)]


def online_bias_checker(data):
    """Counts number of data points that could be considered problematic"""
    data_count = data["Response"].value_counts()
    data = data[["Participant Private ID", "randomise_trials", "Screen Name", "Reaction Time", "condition","Response", "Correct"]]
    data = data.dropna(axis = 0)#drop na values
    data = correct_checker(data) #ensures only trials where participant was correct 
    dropped_ids = []
    
    #get all unique participant ids 
    ids = data.groupby("Participant Private ID").mean().index.tolist()

    #counter variables 
    spatial = 0
    cueless = 0
    #loop through each id 
    for id in ids: 
        ppt_data = data[data["Participant Private ID"] == id] #create smaller dataset containing only participant's id
        count = ppt_data["Response"].value_counts() #count unique responses 
        if count["target"] < (ONLINE_BIAS - (ONLINE_BIAS * ONLINE_BIAS_MULTIPLIER)) or count["target"] > (ONLINE_BIAS + (ONLINE_BIAS * ONLINE_BIAS_MULTIPLIER)): #determine if made same response more than 80% trials
            if id not in dropped_ids:
                #check which condition belonged to. 
                condition = ppt_data["condition"].iloc[0]
                if condition == "spatial_cue":
                    spatial +=1 
                elif condition == "cueless":
                    cueless +=1
                #add to list of ids to drop 
                dropped_ids.append(id) 
        else: 
            pass 
    
    with open("problem_data.txt", mode = "a") as text:
        text.write(f"[ONLINE] Data from {len(dropped_ids)} participants was dropped for response bias. Spatial-cue = {spatial}, Cueless = {cueless}\n")
    return data[~ data["Participant Private ID"].isin(dropped_ids)], dropped_ids #return df with only non-dropped ids + list of dropped ids 

 
# # #alternative version of online_bias_checker
# def online_bias_checker(data):
#     """Checks for participants who were unusually """
    
#     data = data[["Participant Private ID", "randomise_trials", "Screen Name", "Reaction Time", "condition","Correct"]]
#     data = data.dropna(axis = 0)#drop na values
#     dropped_ids = []
    
#     #get all unique participant ids 
#     ids = data.groupby("Participant Private ID").mean().index.tolist()
#     #get mean values for correct 
#     sample_mean = data["Correct"].mean()
#     #get standard deviations 
#     sample_sd = data["Correct"].std()
#     #get mean count values  by participant
#     local_data = data.groupby("Participant Private ID").mean().reset_index()
#     #create counter variables
#     spatial = 0
#     cueless = 0

#     #loop through each participant's data & check if deviates from pre-determined parameters
#     for id in ids: 
#         ppt_data = data[data["Participant Private ID"] == id] #create smaller dataset containing only participant's data
#         ppt_mean = ppt_data["Correct"].mean()
#         if not (sample_mean-(BIAS_SD*sample_sd)) < ppt_mean  < (sample_mean+(BIAS_SD*sample_sd)): 
#             if id not in dropped_ids:
#                 # check which condition belonged to. 
#                 condition = ppt_data["condition"].iloc[0]
#                 if condition == "spatial_cue":
#                     spatial +=1 
#                 elif condition == "cueless":
#                     cueless +=1
#                 #add to list of ids to drop 
#                 dropped_ids.append(id) 
#             pass 
    
    
#     with open("problem_data.txt", mode = "a") as text:
#         text.write(f"[ONLINE] Data from {len(dropped_ids)} participants was dropped for response bias. Spatial-cue = {spatial}, Cueless = {cueless}\n")
#     return data[~ data["Participant Private ID"].isin(dropped_ids)], dropped_ids #return df with only non-dropped ids + list of dropped ids 


def correct_checker(df): 
    """Ensures that only RTs where participants were correct are included """
    # df = df[df["Correct"] == 1] #commented to prevent breaking experiemtn 
    # print(df["Screen Name"].value_counts())
    return df

#create blank text document 
with open(R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\problem_data.txt","w") as text: 
    text.write("") #nothing after as do not write here -> just resets the exisitng document  
#-----------------------------------------Demographic data-----------------------------------------#
# url_1 =R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\demographic_data.csv"
# dem_data = pd.read_csv(url_1)
path = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Raw data\Demographic data"
filenames = glob.glob(path + "\*.csv")
#create a empty pandas dataframe
dem_data = pd.DataFrame()
#add all CSV files in folder to the dataframe 
for file in filenames:
    df = pd.read_csv(file)
    dem_data = dem_data.append(df, ignore_index = True)

#drop all rows that do not refer to age or gender.
age = dem_data[dem_data["Question Key"] == "response-9-year"]
age = age.rename(columns={"Response":"age"})
gender = dem_data[dem_data["Question Key"] == "response-7"]
gender = gender.rename(columns={"Response":"gender"})

#rejoin the datasets based on participant's ID
dem_data = pd.merge(gender,age, on ="Participant Private ID")


#drop unessary columns
dem_data = dem_data.rename(columns={"Participant Private ID":"id"})
dem_data = dem_data[["id","age","gender"]] 

#save data
dem_data.to_csv(R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Clean data\Demographic data\cleaned_demographic_data.csv", index = False)

#-----------------------------------------Online task-----------------------------------------#
# #load the data
# url_1 = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\online practice 1.csv"
# data_1 = pd.read_csv(url_1)
# url_2 = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\online practice 2.csv"
# data_2 = pd.read_csv(url_2)
# url_3 = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\online practice 3.csv"
# data_3 = pd.read_csv(url_3)

# online_data_sets = [data_1, data_2, data_3]
# #merge the datasets
# merged_data =  pd.concat(online_data_sets)

path = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Raw data\Online task data"
filenames = glob.glob(path + "\*.csv")
#create a empty pandas dataframe
merged_data = pd.DataFrame()
#add all CSV files in folder to the dataframe 
for file in filenames:
    df = pd.read_csv(file)
    df = online_fixer(df)
    merged_data = merged_data.append(df, ignore_index = True)


#drop participants showing response bias
merged_data, dropped_ids = online_bias_checker(merged_data)

#drop all but specified columns
online_cleaned_data = merged_data[["Participant Private ID", "randomise_trials", "Screen Name", "Reaction Time", "condition"]]
#drop rows with missing values
online_cleaned_data = online_cleaned_data.dropna(axis = 0)
#rename retained columns 
online_cleaned_data = online_cleaned_data.rename(columns = {"Participant Private ID":"id", "randomise_trials":"block", "Screen Name":"position", "Reaction Time":"rt"})
#create new column with log of reaction times 
online_cleaned_data["rt"] = online_cleaned_data["rt"].astype("float64") #converts it to a float value
online_cleaned_data["log_rt"] = np.log(online_cleaned_data["rt"])


online_cleaned_data = sd_dropper(online_cleaned_data)

#seperate data to retain position data
online_cleaned_data.to_csv(R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Clean data\Online task data\cleaned_online_data_position.csv", index = False)

#calculate OML 
first_position = online_cleaned_data[online_cleaned_data["position"] == "shape_1"] #extract 1st position
first_position = first_position.rename(columns = {"log_rt":"pos1_log_rt"}) #rename column
other_position = online_cleaned_data[online_cleaned_data["position"] != "shape_1"] #extract 2nd & 3rd position 
mean_other = other_position.groupby(["id","block", "condition"]).mean(numeric_only = True).reset_index() #calculates mean of 2nd & 3rd position
isolated_other = mean_other[["id","log_rt", "block", "condition"]] #seperate mean 
isolated_other = isolated_other.rename(columns = {"log_rt":"pos23_log_rt"}) #rename to allow merging
joined = pd.merge(first_position, isolated_other, on= ["id", "block", "condition"], how = "left")
joined["OML"] = joined["pos1_log_rt"] - joined["pos23_log_rt"]


#save OML data
joined.to_csv(R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Clean data\Online task data\cleaned_online_data_OML.csv", index = True)

#-----------------------------------------2-AFC task-----------------------------------------#
# url_1 = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\2-AFC practice 1.csv"
# data_1 = pd.read_csv(url_1)
# url_2 = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\2-AFC practice 2.csv"
# data_2 = pd.read_csv(url_2)
# url_3 = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\2-AFC practice 3.csv"
# data_3 = pd.read_csv(url_3)

# offline_data_sets = [data_1, data_2, data_3]
# #merge the datasets
# merged_data =  pd.concat(offline_data_sets)

path = R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Raw data\Offline task data"
filenames = glob.glob(path + "\*.csv")
#create a empty pandas dataframe
merged_data = pd.DataFrame()
#add all CSV files in folder to the dataframe 
for file in filenames:
    df = pd.read_csv(file)
    #df = AFCfixer(df) #used to remove some erroneous data 
    merged_data = merged_data.append(df, ignore_index = True)


#drop practice trials 
merged_data = merged_data[merged_data["practice"] != "y"]
#drop all rows that are not actually part of the trials -> just gorilla displaying screens 
merged_data = merged_data[merged_data["Screen Name"] == "Screen 8"]
#check for response bias
merged_data = AFC_bias_chekcer(merged_data, dropped_ids)
#remove erroneous data due to programming error 
merged_data = AFCfixer(merged_data)
#drop columns
offline_cleaned_data = merged_data[["Participant Private ID", "condition", "comparison_type", "Correct", "Incorrect"]]
#drop rows with missing values
offline_cleaned_data = offline_cleaned_data.dropna(axis = 0)
#rename retained columns 
offline_cleaned_data= offline_cleaned_data.rename(columns = {"Participant Private ID":"id", "Correct":"correct","Incorrect":"incorrect"})



#seperate the two trial types 
illusionary_cleaned = offline_cleaned_data[offline_cleaned_data["comparison_type"] == "illusionary"]
part_sequence_cleaned = offline_cleaned_data[offline_cleaned_data["comparison_type"] == "part_sequence"]


#calculate total number of correct trials for each particiapnt, by condition 
illusionary_cleaned = illusionary_cleaned.groupby(["id", "condition"]).sum()
part_sequence_cleaned = part_sequence_cleaned.groupby(["id", "condition"]).sum()

#convert to preference ratio 
illusionary_cleaned["correct"] = (illusionary_cleaned["correct"]/6)
part_sequence_cleaned["correct"] = (part_sequence_cleaned["correct"]/12)

#create a full dataset
illusionary_cleaned["comparison_type"] = "illusionary" #adds cosntant value to column for ANOVA
part_sequence_cleaned["comparison_type"] = "part_sequence" #adds cosntant value to column for ANOVA
full_offline = pd.concat((illusionary_cleaned, part_sequence_cleaned), axis = 0)
full_offline.to_csv(R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Clean data\Offline task data\cleaned_2AFC_data_full.csv")

#save data 
illusionary_cleaned.to_csv(R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Clean data\Offline task data\cleaned_2AFC_data_illusionary.csv")
part_sequence_cleaned.to_csv(R"C:\Users\invate\OneDrive\Documents\Nottingham Trent Work\Project lab\Analysis\Clean data\Offline task data\cleaned_2AFC_data_part_sequence.csv")