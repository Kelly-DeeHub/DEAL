# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 18:55:13 2025

@author: MRS. DORIS PC
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.options.future.infer_string = True

st.title("Sales Performance Through Probabilistic Analysis")
st.write("select a name to get started")

#Phase 1

#list of names: Sales Reps
names= ["select a name", "Amir", "Karl", "Doris", "Queen", "Prince","James","Tega","Ola"]

#Dropdown
selected_name = st.selectbox("choose a name",names)

#only run the rest of the code below if valid name is chosen
if selected_name != "select a name":
    st.write(f"you selected:{selected_name}")
    uploaded_file = st.file_uploader("Choose a file")


#-----PHASE 2 ----------
#DATA INGESTION AND CLEANING
#Detect file type by extension
    if uploaded_file is not None:
      try:
       file_name = uploaded_file.name.lower()
       if file_name.endswith("csv"):
          df = pd.read_csv(uploaded_file)
       elif file_name.endswith(("xlsx","xls")):
         df=pd.read_excel(uploaded_file)
       else:
         st.error("unsupported file type please upload a csv or Excel file")
         st.stop()
#Remove Duplicate
         df.drop_duplicates(inplace=True)
#Rename column if exists
         if "Unnamed: 0" in df.columns:
             df.rename(columns={"Unnamed: 0": "sales_pitch_id"}, inplace=True)
#Validation Check
         req_columns = {"status", "client", "product", "amount"}
         missing_cols = req_columns - set(df.columns)

         if len(missing_cols)>0:
           st.error(f"The uploaded file is missing required columns {missing_cols}")
           st.stop()

         df["amount"] = df["amount"].abs()

         st.success(f"{file_name} has been cleaned and validated.")
      except Exception as e:
         st.error(f"An error occured while cleaning the file {e}.")
    
    
    #-----------phase3 core metrics---------
      # Success and failure probabilities
      p_success = (df['status'] == "Won").mean().round(4) * 100
      p_failure = (df['status'] == "lost").mean().round(4) * 100


    # Win-rate per client type
      new_client_win =(df.groupby("client").get_group("New")["status"] == "Won").mean().round(3)* 100
      current_client_win =(df.groupby("client").get_group("Current")["status"] == "Won").mean().round(3)* 100


     # Spread (standard deviation of amount)
      amount_std = round(df['amount'].std(), 3)


     # Status storage (1 = win, 0 = loss)
      status_bin = (df["status"] == "Won").astype(int).to_list()
     # Function to compute longest streaks
      def longest_streak(collection, value):
          max_run = 0       # longest streak
          current = 0       # current streak

    # Loop through the collection
          for c in collection:
            if c == value:
               current += 1
               max_run = max(max_run, current)
            else:
               current = 0
          return max_run

     # Longest win & loss streaks
      longest_win_streak = longest_streak(status_bin, 1)
      longest_loss_streak = longest_streak(status_bin, 0)


      # Conditional probabilities
      after_win = []
      after_loss = []

      for index in range(len(status_bin) - 1):
          if status_bin[index] == 1:
           after_win.append(status_bin[index + 1])
          else:
           after_loss.append(status_bin[index + 1])

     # Compute conditional probabilities
      p_win_after_win = np.mean(after_win).round(4) * 100
      p_win_after_loss = np.mean(after_loss).round(4) * 100
      
                       #product win rate
      product_win_rate = df.groupby("product")["status"].apply(lambda s:(s =="Won").mean()).round(3)*100
      top_5_product_winrate = product_win_rate .nlargest(5)


        # Streamlit spacing
      st.write("")
      st.write("")

       # -------- Phase 4: Summary --------
      st.subheader(f"{selected_name}'s performance:")
      data ={"Metrics": ["Success Rate","Failure Rate","New Client Win Rate","Current Client Win Rate","Longest Win Streak",
                       "Longest Loss Streak","Probability of a win after a win","probability of a win after a loss","spread"],
             "Values":[p_success, p_failure, new_client_win, current_client_win,longest_win_streak,longest_loss_streak,
                      p_win_after_win,p_win_after_loss,amount_std]}
      data_df = pd.DataFrame(data)
      st.dataframe(data_df,use_container_width= True)
      
      
      st.write("")
      st.write("")
      
      
      #                          PHASE FIVE Visualization
      st.subheader("Performace Visuals")
      fig, ax = plt.subplots()
      ax.hist(df['amount'],color='firebrick',edgecolor='white')
      ax.set_title(f"Distribution of{selected_name}'s Sales Amount",color='white')
      
      ax.tick_params(axis="x", colors="white")
      ax.tick_params(axis="y", colors="white")
      
                   
      fig.patch.set_alpha(0.0)
      ax.patch.set_alpha(0.0)
      st.pyplot(fig)
      
      st.write("")
      
      fig, ax = plt.subplots()
      bars = ax.bar(top_5_product_winrate.index, top_5_product_winrate.values, color='blue',edgecolor='white')
      ax.bar_label(bars,labels = top_5_product_winrate.values, color='white')
      ax.set_title("Top 5 product by win rate %",color='white')
      ax.set_yticks([])
      
      
      ax.tick_params(axis="x", colors="white")
      ax.tick_params(axis="y", colors="white")
      
                   
      fig.patch.set_alpha(0.0)
      ax.patch.set_alpha(0.0)
      st.pyplot(fig)
      
      
else:
    st.warning("please select a valid name to continue")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    