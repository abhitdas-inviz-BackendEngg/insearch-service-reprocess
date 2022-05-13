FROM public.ecr.aws/bitnami/python:3.8
WORKDIR /app

#ADD ./configs ./src/resource/configs/
#ADD ./jobs ./src/main/jobs/
#ADD ./tests ./src/main/tests/
#ADD ./config ./src/main/config/
#ADD ./utils ./src/main/utils/

COPY . .
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"
COPY requirement.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install aiobotocore==1.1.1

CMD ["python", "./src/main/main.py"]