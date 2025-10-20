FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install flask google-generativeai PyMuPDF
EXPOSE 5000
CMD ["python", "app.py"]
