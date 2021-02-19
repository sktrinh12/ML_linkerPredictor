FROM python:3.8
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN mv LinkerPredictor_app.py app.py
CMD ["streamlit", "run", "app.py"]
