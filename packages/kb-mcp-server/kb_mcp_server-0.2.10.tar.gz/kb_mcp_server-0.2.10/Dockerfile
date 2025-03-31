# Use the existing txtai-cpu image from local cache
FROM neuml/txtai-cpu:latest

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Make sure scripts are executable
RUN chmod +x docker-entrypoint.sh download_models.py

# Create a pip retry configuration to handle network issues
RUN mkdir -p /root/.config/pip && \
    echo "[global]\n\
timeout = 100\n\
retry = 10\n\
default-timeout = 100" > /root/.config/pip/pip.conf

# Install the kb-mcp-server package which includes MCP and all required dependencies
RUN for i in $(seq 1 3); do \
      pip install kb-mcp-server==0.2.6 && break || \
      echo "Attempt $i/3 to install kb-mcp-server failed, retrying in 5 seconds..." && sleep 5; \
    done || echo "WARNING: kb-mcp-server installation failed - offline mode will have limited functionality"

# Install the project in development mode
# The || is to handle possible offline builds
RUN pip install -e . || echo "Installing in development mode failed - continuing anyway"

# Create all necessary directories
RUN mkdir -p /data/embeddings /data/config /data/huggingface

# Set main environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    HF_HOME=/data/huggingface \
    STORAGE_MODE=disk \
    EMBEDDINGS_FILE=/data/embeddings/embeddings.json \
    CONFIG_FILE=/data/config/config.json \
    HOST=0.0.0.0 \
    PORT=8000 \
    TRANSPORT=api

# Set txtai-specific environment variables to leverage txtai's built-in functionality
ENV TXTAI_STORAGE_MODE=persistence \
    TXTAI_INDEX_PATH=/data/embeddings \
    TXTAI_DATASET_ENABLED=true \
    TXTAI_DATASET_NAME=web_questions \
    TXTAI_DATASET_SPLIT=train

# Create volumes for persistent data
VOLUME ["/data/embeddings", "/data/config", "/data/huggingface"]

# Arguments for model downloading
ARG HF_TRANSFORMERS_MODELS=""
ARG HF_SENTENCE_TRANSFORMERS_MODELS="sentence-transformers/nli-mpnet-base-v2"
ARG HF_CACHE_DIR="/data/huggingface"

# Handle Hugging Face cache directory linking
RUN if [ -n "$HF_CACHE_DIR" ] && [ -d "$HF_CACHE_DIR" ]; then \
    mkdir -p /root/.cache/huggingface && \
    ln -s "$HF_CACHE_DIR" /root/.cache/huggingface/hub; \
    fi

# Conditionally download models if specified and if online
# Uses a timeout to avoid hanging in offline environments
RUN timeout 30 python /app/download_models.py \
    --transformers "$HF_TRANSFORMERS_MODELS" \
    --sentence-transformers "$HF_SENTENCE_TRANSFORMERS_MODELS" \
    --huggingface-cache "$HF_CACHE_DIR" || echo "Model download skipped - will attempt at runtime"

# Expose the server port
EXPOSE 8000

# Use the entrypoint script
CMD ["/app/docker-entrypoint.sh"]