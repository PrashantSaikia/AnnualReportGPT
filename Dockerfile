FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install dependencies
RUN git clone https://github.com/facebookresearch/detectron2.git
RUN python -m pip install -e detectron2
RUN apt-get update && apt-get install libgl1 -y
RUN pip install -U nltk
RUN [ "python3", "-c", "import nltk; nltk.download('punkt')" ]

# Give user access to write (for the locally saved vectorstore parquet files)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY --chown=user . $HOME/app

# Run the application:
CMD ["python", "-u", "app.py"]
