#!/bin/bash
# Script to build the Docker image with retry mechanism and network optimizations
set -e

# Default values
TRANSFORMERS_MODELS=""
SENTENCE_TRANSFORMERS_MODELS="sentence-transformers/nli-mpnet-base-v2"
HF_CACHE_DIR="$HOME/.cache/huggingface/hub"
IMAGE_NAME="embedding-mcp-server"
CLEAN_BUILD=true
MAX_RETRIES=3
NETWORK_MODE=""
PULL_POLICY="true"
OFFLINE_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  # Split parameter at equals sign if present
  if [[ $1 == *=* ]]; then
    param=${1%%=*}
    value=${1#*=}
  else
    param=$1
    value=$2
  fi

  case $param in
    --transformers)
      TRANSFORMERS_MODELS="$value"
      if [[ $1 == *=* ]]; then shift 1; else shift 2; fi
      ;;
    --sentence-transformers)
      SENTENCE_TRANSFORMERS_MODELS="$value"
      if [[ $1 == *=* ]]; then shift 1; else shift 2; fi
      ;;
    --cache-dir)
      HF_CACHE_DIR="$value"
      if [[ $1 == *=* ]]; then shift 1; else shift 2; fi
      ;;
    --image-name)
      IMAGE_NAME="$value"
      if [[ $1 == *=* ]]; then shift 1; else shift 2; fi
      ;;
    --no-clean)
      CLEAN_BUILD=false
      shift
      ;;
    --retries)
      MAX_RETRIES="$value"
      if [[ $1 == *=* ]]; then shift 1; else shift 2; fi
      ;;
    --network)
      NETWORK_MODE="--network=$value"
      if [[ $1 == *=* ]]; then shift 1; else shift 2; fi
      ;;
    --pull)
      PULL_POLICY="$value"
      if [[ $1 == *=* ]]; then shift 1; else shift 2; fi
      ;;
    --offline)
      OFFLINE_MODE=true
      PULL_POLICY="false"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Available options:"
      echo "  --transformers MODEL_NAME          Specify Hugging Face transformer models"
      echo "  --sentence-transformers MODEL_NAME Specify Hugging Face sentence-transformer models"
      echo "  --cache-dir PATH                   Path to Hugging Face cache directory"
      echo "  --image-name NAME                  Name for the Docker image"
      echo "  --no-clean                         Don't use --no-cache flag"
      echo "  --retries N                        Number of build retries (default: 3)"
      echo "  --network MODE                     Network mode (default: bridge, try 'host' if build fails)"
      echo "  --pull POLICY                      Image pull policy (default: true, use 'false' for offline builds)"
      echo "  --offline                          Build in offline mode (no network access)"
      exit 1
      ;;
  esac
done

echo "=== Building embedding-mcp-server Docker image ==="
echo "Image name: $IMAGE_NAME"
echo "Max retries: $MAX_RETRIES"
echo "Network mode: ${NETWORK_MODE:-default}"
echo "Pull policy: $PULL_POLICY"
echo "Offline mode: $OFFLINE_MODE"

# Attempt to build with retries
retry_count=0
success=false

while [ $retry_count -lt $MAX_RETRIES ] && [ "$success" = false ]; do
  # Increment retry counter
  retry_count=$((retry_count + 1))
  
  echo "\n=== Build attempt $retry_count of $MAX_RETRIES ==="
  
  # Build command with network optimizations
  if [ "$OFFLINE_MODE" = "true" ]; then
    echo "Building in offline mode - no network access"
    # Use the minimal network settings in offline mode
    BUILD_CMD="docker build --network=none --progress=plain"
  elif [ "$PULL_POLICY" = "true" ]; then
    BUILD_CMD="docker build --pull $NETWORK_MODE --progress=plain"
  else
    BUILD_CMD="docker build $NETWORK_MODE --progress=plain"
  fi
  
  # Add no-cache option if clean build is requested
  if [ "$CLEAN_BUILD" = true ]; then
    BUILD_CMD="$BUILD_CMD --no-cache"
  fi
  
  # Add build arguments
  if [ -n "$TRANSFORMERS_MODELS" ]; then
    BUILD_CMD="$BUILD_CMD --build-arg HF_TRANSFORMERS_MODELS=\"$TRANSFORMERS_MODELS\""
  fi
  
  if [ -n "$SENTENCE_TRANSFORMERS_MODELS" ]; then
    BUILD_CMD="$BUILD_CMD --build-arg HF_SENTENCE_TRANSFORMERS_MODELS=\"$SENTENCE_TRANSFORMERS_MODELS\""
  fi
  
  if [ -n "$HF_CACHE_DIR" ]; then
    BUILD_CMD="$BUILD_CMD --build-arg HF_CACHE_DIR=\"$HF_CACHE_DIR\""
  fi
  
  # Add image name
  BUILD_CMD="$BUILD_CMD -t $IMAGE_NAME ."
  
  # Print the command
  echo "Running: $BUILD_CMD"
  
  # Execute the command
  if eval $BUILD_CMD; then
    success=true
    echo "\n=== Build successful! ==="
  else
    echo "\n=== Build failed (attempt $retry_count of $MAX_RETRIES) ==="
    if [ $retry_count -lt $MAX_RETRIES ]; then
      echo "Waiting 10 seconds before retrying..."
      sleep 10
    fi
  fi
done

if [ "$success" = true ]; then
  echo "\n=== Docker image $IMAGE_NAME built successfully ==="
  docker images | grep $IMAGE_NAME
  
  echo "\nTo run the container, use:"
  echo "docker run -p 8000:8000 -v /path/to/embeddings:/data/embeddings $IMAGE_NAME"
else
  echo "\n=== Failed to build Docker image after $MAX_RETRIES attempts ==="
  echo "Try the following troubleshooting steps:"
  echo "1. Check your network connection"
  echo "2. Run the build with --network=host: ./build-docker.sh --network=host"
  echo "3. Try using a different base image in the Dockerfile"
  echo "4. Try building in offline mode if you have the image locally: ./build-docker.sh --offline"
  exit 1
fi
