import streamlit as st
import pandas as pd
import pickle
import numpy as np

def predictor(feat1, feat2, feat3, feat4, feat5, feat6):
    with open('m3.sav', 'rb') as f:
                svm_model = pickle.load(f)

    with open('m1.sav', 'rb') as f:
                linear_regressor = pickle.load(f)

    with open('m2.sav', 'rb') as f:
                xgb1 = pickle.load(f)

    X = np.array([feat1, feat2, feat3, feat4, feat5, feat6]).reshape(1,-1)
    X2 = np.array([feat1, feat2-7.33, feat3, feat4, feat5, feat6]).reshape(1,-1)
    X3 = np.array([feat1, feat2+7.33, feat3, feat4, feat5, feat6]).reshape(1,-1)
    svm_pred = svm_model.predict(X)[0]
    svm_pred2 = svm_model.predict(X2)[0]
    svm_pred3 = svm_model.predict(X3)[0]
    xgb1_pred = xgb1.predict(X)[0]
    xgb1_pred2 = xgb1.predict(X2)[0]
    xgb1_pred3 = xgb1.predict(X3)[0]
    #xgb2_pred = xgb2.predict(X)[0]
    linear_regressor_pred = linear_regressor.predict(X)[0]
    linear_regressor_pred2 = linear_regressor.predict(X2)[0]
    linear_regressor_pred3 = linear_regressor.predict(X3)[0]
    print("Run successful with input:", X,X2,X3)
    p = float(np.mean([svm_pred,svm_pred2,svm_pred3, xgb1_pred,xgb1_pred2,xgb1_pred3, linear_regressor_pred,linear_regressor_pred2,linear_regressor_pred3]))

    return "{:.2f}".format(p)

st.title('BV510 Linker Predictor')

feat1 = st.number_input(label='Acid Mp (kDa):', value = 100)
feat2 = st.number_input(label='Acid Linker Score (%):', value = 150)
feat4 = st.number_input(label='Temperature (C):', value = 4)
feat3 = st.slider(label = 'EDC:', min_value=100, max_value=1000, value=500, step=50)
time = st.radio('Time of reaction:',('1 Hour', 'Overnight'))
if time == '1 Hour':
    feat5 = 0
else:
    feat5 = 1
scale = st.radio('Scale of reaction:',('Small Scale', 'Large Scale'))
if scale == 'Small Scale':
    feat6 = 0
else:
    feat6 = 1
submit = st.button(label='SUBMIT')
if submit:
    st.subheader('Predicted Linker Score (%):')
    st.write(predictor(feat1, feat2, feat3, feat4, feat5, feat6))
