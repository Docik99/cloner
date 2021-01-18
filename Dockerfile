FROM python:3

COPY . .

RUN pip install requests

ENTRYPOINT [ "python", "./gitlab_user_sync.py" ]

CMD  []
