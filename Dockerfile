FROM ubuntu:latest
LABEL authors="zehiu"

ENTRYPOINT ["top", "-b"]