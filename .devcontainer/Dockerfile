FROM maven:3.9.6-amazoncorretto-11

# Declare ARGs
ARG PROXY_USER
ARG PROXY_PASSWORD
ARG PROXY_HOST
ARG PROXY_PORT
ARG NO_PROXY_PIPE_DELIMITED
ARG NO_PROXY_COMMA_SEPARATED
ARG CA_BUNDLE_URL

COPY ./prepare_env.sh /prepare_env.sh
RUN chmod +x /prepare_env.sh
RUN /prepare_env.sh $PROXY_USER $PROXY_PASSWORD $PROXY_HOST $PROXY_PORT $NO_PROXY_PIPE_DELIMITED $CA_BUNDLE_URL $NO_PROXY_COMMA_SEPARATED

# Setup a non-root user that matches the host
ARG USERNAME=vscode
ARG USER_UID=1001
ARG USER_GID=$USER_UID

# Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

# Change PS1
RUN echo 'export PS1="\[\033[0;32m\]\u@\h\[\033[0m\]:\[\033[0;34m\]\w\[\033[0m\] \\$ "' >> ~/.bashrc

# Add git aliases
RUN echo "alias gba='git branch -a'" >> ~/.bashrc && \
    echo "alias gbr='git branch -r'" >> ~/.bashrc && \
    echo "alias gbl='git branch -l'" >> ~/.bashrc && \
    echo "alias gcm='git commit -m'" >> ~/.bashrc && \
    echo "alias gco='git checkout'" >> ~/.bashrc && \
    echo "alias gcob='git checkout -b'" >> ~/.bashrc && \
    echo "alias gs='git status -sb'" >> ~/.bashrc && \
    echo "alias gf='git fetch'" >> ~/.bashrc && \
    echo "alias gpom='git pull origin master'" >> ~/.bashrc && \
    echo "alias gpo='git pull origin'" >> ~/.bashrc && \
    echo "alias gc='git clone'" >> ~/.bashrc && \
    echo "alias rebase='gf & git pull --rebase'" >> ~/.bashrc && \
    echo "alias gaa='git add .'" >> ~/.bashrc && \
    echo "alias publish-branch='git push -u origin HEAD'" >> ~/.bashrc && \
    echo "alias jav=\"mvn formatter:format && mvn com.github.ekryd.sortpom:sortpom-maven-plugin:sort -Dsort.keepBlankLines\"" >> ~/.bashrc && \
    echo "alias gp='git pull origin \$(git rev-parse --abbrev-ref HEAD)'" >> ~/.bashrc && \
    echo "alias push='git push origin \$(git rev-parse --abbrev-ref HEAD)'" >> ~/.bashrc && \
    echo "alias gfp='gf && gp'" >> ~/.bashrc
