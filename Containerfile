# Use Fedora Minimal for a smaller base image.
FROM fedora-minimal:latest

LABEL maintainer="John Casey <casey.john.d@gmail.com>"
LABEL description="Container for the Minecord Discord Bot"

# Install Python and other required packages.
RUN microdnf install -y python3 python3-pip which && \
    microdnf clean all

# Set environment variables to improve logging and performance
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Create a non-root user to run the application for better security
RUN groupadd --system --gid 1001 minecord && \
    adduser --system --uid 1001 --gid 1001 minecord

# Copy the application source code into the container.
# The source code is expected to be in a `minecord` directory in the build context.
COPY --chown=minecord:minecord minecord/ /minecord/minecord/
COPY --chown=minecord:minecord pyproject.toml /minecord/pyproject.toml

# Switch to the non-root user
USER minecord

WORKDIR /minecord
RUN python -m venv ./venv && \
    source ./venv/bin/activate && \
    pip install --upgrade pip && \
    pip install .

#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/minecord/venv/bin/minecord"]
