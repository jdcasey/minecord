# Use Fedora Minimal for a smaller base image.
FROM fedora-minimal:latest

LABEL maintainer="Gemini Code Assist"
LABEL description="Container for the Minecord Discord Bot"

# Install Python and other required packages.
RUN microdnf install -y python3 python3-pip && \
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

WORKDIR /minecord
RUN pip3 install --no-cache-dir .

# Switch to the non-root user
USER minecord

# Set the default command to run the bot.
# The bot is configured to look for `minecord.yaml` in the current directory ($PWD),
# which is /app. Users should mount their config and data files.
#
# Example usage with Podman:
# podman build -t minecord-bot -f Containerfile .
#
# podman run -d --name minecord \
#   -v ./minecord.yaml:/app/minecord.yaml:ro,z \
#   -v ./admins.yaml:/app/admins.yaml:z \
#   localhost/minecord-bot:latest
ENTRYPOINT ["/bin/bash"]
#CMD ["python", "-m", "minecord.bot"]