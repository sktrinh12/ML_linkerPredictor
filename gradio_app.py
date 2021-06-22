import gradio as gr
import pickle
import numpy as np

def predictor(feat1, feat2, feat3, feat4, feat5, feat6):
    with open('m3.sav', 'rb') as f:
                svm_model = pickle.load(f)

    with open('m1.sav', 'rb') as f:
                linear_regressor = pickle.load(f)

    with open('m2.sav', 'rb') as f:
                xgb1 = pickle.load(f)

    #with open('C:/Users/10273310/Desktop/iCode/Sirigen/BV510-Activation/XGBModel_Act_BV510.sav', 'rb') as f:
               # xgb2 = pickle.load(f)
    
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

feat1 = gr.inputs.Number(default=90,label="Acid Mp (kDa)")
feat2 = gr.inputs.Number(default=196,label="Acid Linker Score (%)")


feat3 = gr.inputs.Slider(minimum=100, maximum=1000, default=500, label="EDC")
feat4 = gr.inputs.Number(default=4,label="Temperature (C)")

feat5 = gr.inputs.Radio(choices=["1 Hour", "Overnight"], type="index",label="Reaction Time")
feat6 = gr.inputs.Radio(choices=["Small","Large"],type="index",label="Reaction Scale")

prediction = gr.outputs.Textbox(type="number", label="Predicted Amine Linker Score (model uncertainty = +/-11%, Amine dye test = +/-3%):")

iface = gr.Interface(predictor, title="BV510 Linker Predictor", article="This app is developed and maintained by Subodh Sonar, Sirigen SE. Please contact subodh.sonar@bd.com for any questions/comments/feedback!", description="Welcome to the BV510 Linker Predictor. This app will assist you in predicting the outcome of your amine activation reaction. \nBefore you begin, ensure that you have complete acid lot information (GPC, acid linker score). The EDC slider allows for a real-time titration once the reaction temperature, scale and time are decided. \nThe prediction model is accurate to upto 11%. Use the screenshot function to save a copy of your work, and attach it to the respective batch record. \nThe table below contains a few example entries which can be RUN to generate predictions. It is recommended for a first-time user to run these mock predictions. Hope you have a pleasant experience! ", server_name="10.7.46.65",server_port=7860, inputs = [feat1, feat2, feat3, feat4, feat5, feat6], 
                     examples=[[ 60,196, 200, 4, 1,0],
                                [ 101,153, 500, 10, 0,1],
                                [ 78,127, 800, 12, 1,1],
                               [150,110, 100, 20, 1,0]], outputs=prediction)
iface.launch(share=False, inbrowser=True, auth=(["sirigenlab","Thisisalongpassword1"]))