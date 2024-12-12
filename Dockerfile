FROM python:3.9-slim

RUN useradd -m -u 1000 tictactoe

WORKDIR /app

COPY . /app

RUN chown -R tictactoe:tictactoe /app

RUN pip install flask

EXPOSE 5000

USER tictactoe

CMD ["python", "app.py"]
