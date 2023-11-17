# Use the official Rasa image as the base image
FROM rasa/rasa:latest-full

# Set the working directory to the Rasa project directory
WORKDIR /app

# Copy the Rasa project files into the container
COPY . /app

# Install any additional dependencies if needed
RUN pip install -r requirements.txt

# Expose the port on which Rasa will run
EXPOSE 5005

# Start both Rasa server and actions server
ENTRYPOINT ["rasa"]
CMD ["run", "-m", "models", "--enable-api", "--cors", "*", "&&", "run", "actions"]

