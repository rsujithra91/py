import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
df=pd.read_csv("data.csv")
X=df[['Hours_Studied']]
y=df['Exam_Score']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
model=LinearRegression()
model.fit(X_train,y_train)
st.title("Exam Score Predictor")
st.write("Enter hours studied to predict the exam score")
hours=st.number_input("Hours Studied",min_value=0.0,step=0.1)
if st.button("Predict Score"):
     ps=model.predict([[hours]])[0]
     st.success("Pedicted Score:{ps}")
st.write("sample training data")
st.dataframe(df)
     
