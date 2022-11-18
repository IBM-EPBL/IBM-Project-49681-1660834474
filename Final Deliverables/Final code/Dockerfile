FROM python:3.9
WORKDIR /nutrition
ADD . /nutrition
COPY requirements.txt /nutrition
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install ibm_db
EXPOSE 8080
CMD ["python","nutrition.py"]