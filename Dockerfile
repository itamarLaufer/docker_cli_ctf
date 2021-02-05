FROM python:3.6-buster
COPY docker_cli_ctf /opt/code
ENTRYPOINT ["python", "/opt/code/main.py"]
EXPOSE 7979