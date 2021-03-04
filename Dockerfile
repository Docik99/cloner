FROM python:3

COPY . .

RUN pip install requests && pip install PrettyTable

ENTRYPOINT [ "python", "./gitlab_user_sync.py" ]

CMD  []
