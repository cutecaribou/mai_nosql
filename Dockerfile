FROM python:3.11.8-slim-bullseye

RUN useradd -m otter

USER otter

COPY --chown=otter:otter requirements.txt /home/otter/
RUN pip install -r /home/otter/requirements.txt

COPY otterchat_app /home/otter/otterchat_app
WORKDIR /home/otter/otterchat_app
ENV PYTHONPATH=$PYTHONPATH:/home/otter/otterchat_app

EXPOSE 8000
ENTRYPOINT ["python", "/home/otter/otterchat_app/main.py"]
