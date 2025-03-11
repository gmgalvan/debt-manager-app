FROM python:3.9-slim

# Set up build arguments for AWS credentials
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG CDK_DEFAULT_ACCOUNT
ARG CDK_DEFAULT_REGION


# Use build args to set ENV variables inside the container
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
ENV CDK_DEFAULT_ACCOUNT=${CDK_DEFAULT_ACCOUNT}
ENV CDK_DEFAULT_REGION=${CDK_DEFAULT_REGION}



# Install system dependencies: curl, git, gnupg (needed for Node.js installation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git gnupg \
 && rm -rf /var/lib/apt/lists/*

# Install Node.js (using NodeSource script for Node.js LTS, e.g. 18.x)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
 && apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

# Install AWS CDK CLI globally via npm
RUN npm install -g aws-cdk

# Install Jupyter Notebook
RUN pip install --no-cache-dir jupyter

# Set working directory to /app
WORKDIR /app

# Copy and install Python dependencies if requirements.txt exists
COPY requirements.txt ./
RUN if [ -f requirements.txt ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    fi

# Expose Jupyter Notebook port
EXPOSE 8888

# Start Jupyter Notebook (allowing root and binding to all interfaces)
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
