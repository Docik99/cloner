# our base image
FROM python:3

COPY . .

RUN pip install requests

ENTRYPOINT [ "python", "./script.py" ]

# run the application
CMD  []
