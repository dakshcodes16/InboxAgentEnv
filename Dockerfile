FROM python:3.10-slim

# Set environment variables for huggingface space
ENV PORT 7860
ENV APP_HOME /app

# Add a standard user for HF spaces
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $APP_HOME
COPY --chown=user . $APP_HOME/

# Install the application components and deps
RUN pip install --no-cache-dir -r requirements.txt

# Start dummy server (to meet port 7860 requirement on space)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
