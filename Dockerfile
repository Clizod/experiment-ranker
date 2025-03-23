FROM python:3.9

# Install any necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

ENV LD_LIBRARY_PATH = "$LD_LIBRARY_PATH:/usr/local/lib/python3.9/site-packages/tensorrt_libs"

# Copy the notebooks to the container
COPY . /app

# Installing a local package in src\clizod_ranker in editable mode to help code re-use
RUN pip install -e .

# Set the default command to run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--notebook-dir=/app"]