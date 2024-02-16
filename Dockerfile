FROM python:3.9


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ /app/src
ENV FLASK_APP=/app/src/critique_film


ENTRYPOINT [ "tail", "-f", "/dev/null" ]