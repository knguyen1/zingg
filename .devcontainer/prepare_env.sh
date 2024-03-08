#!/bin/bash

# the purpose of this script is to prepare the environment for HTTP/S calls
# some users are behind corporate proxies and cert authorities
# use this script to define those features

PROXY_USER=${1:-""}
PROXY_PASSWORD=${2:-""}
PROXY_HOST=${3:-""}
PROXY_PORT=${4:-""}
NO_PROXY_PIPE_DELIMITED=${5:-""}
CA_BUNDLE_URL=${6:-""}
NO_PROXY_COMMA_SEPARATED=${7:-""}

# Build MAVEN_OPTS
mvn_opts=""

http_proxy=""
https_proxy=""
no_proxy=""

touch /etc/profile.d/proxies.sh
chmod +x /etc/profile.d/proxies.sh

# Only set proxies if proxy_user is provided
if [ -n "$PROXY_USER" ]; then
    echo "export http_proxy=http://${PROXY_USER}:${PROXY_PASSWORD}@${PROXY_HOST}:${PROXY_PORT}" >> /etc/profile.d/proxies.sh
    echo "export https_proxy=http://${PROXY_USER}:${PROXY_PASSWORD}@${PROXY_HOST}:${PROXY_PORT}" >> /etc/profile.d/proxies.sh
    echo "export HTTP_PROXY=http://${PROXY_USER}:${PROXY_PASSWORD}@${PROXY_HOST}:${PROXY_PORT}" >> /etc/profile.d/proxies.sh
    echo "export HTTPS_PROXY=http://${PROXY_USER}:${PROXY_PASSWORD}@${PROXY_HOST}:${PROXY_PORT}" >> /etc/profile.d/proxies.sh

    http_proxy="http://${PROXY_USER}:${PROXY_PASSWORD}@${PROXY_HOST}:${PROXY_PORT}"
    https_proxy="http://${PROXY_USER}:${PROXY_PASSWORD}@${PROXY_HOST}:${PROXY_PORT}"

    # Set MAVEN_OPTS proxy settings
    mvn_opts="-Dhttp.proxyUser=${PROXY_USER} -Dhttps.proxyUser=${PROXY_USER} -Dhttp.proxyPassword=${PROXY_PASSWORD} -Dhttps.proxyPassword=${PROXY_PASSWORD} -Dhttp.proxyHost=${PROXY_HOST} -Dhttp.proxyPort=${PROXY_PORT} -Dhttps.proxyHost=${PROXY_HOST} -Dhttps.proxyPort=${PROXY_PORT}"
fi

# Only set no_proxy if no_proxy argument is provided
if [ -n "$NO_PROXY_COMMA_SEPARATED" ]; then
    echo "export no_proxy=${NO_PROXY_COMMA_SEPARATED}" >> /etc/profile.d/proxies.sh
    echo "export NO_PROXY=${NO_PROXY_COMMA_SEPARATED}" >> /etc/profile.d/proxies.sh

    no_proxy=${NO_PROXY_COMMA_SEPARATED}

    # Set MAVEN_OPTS nonProxyHosts
    mvn_opts="${mvn_opts} -Dhttp.nonProxyHosts='${NO_PROXY_PIPE_DELIMITED}'"
fi

# Set MAVEN_OPTS in /etc/profile.d/proxies.sh
if [ -n "${mvn_opts}" ]; then 
    echo "export MAVEN_OPTS=\"\$MAVEN_OPTS ${mvn_opts}\"" >> /etc/profile.d/proxies.sh
fi

# Install necessary packages
http_proxy=${http_proxy} https_proxy=${https_proxy} no_proxy=${no_proxy} yum -y update \
  && http_proxy=${http_proxy} https_proxy=${https_proxy} no_proxy=${no_proxy} yum -y install git openssl wget sudo

# Only import keys if CA_BUNDLE_URL is provided
if [ -n "$CA_BUNDLE_URL" ]; then
    # Download the ca-bundle.crt
    wget -q -O /tmp/ca-bundle.crt ${CA_BUNDLE_URL}

    # Split the file into individual certificate files and import each of them
    csplit -f /tmp/crt- /tmp/ca-bundle.crt '/-----BEGIN CERTIFICATE-----/' '{*}'; \
    for cert_file in /tmp/crt-*; do \
      echo $cert_file; \
      alias=$(openssl x509 -noout -subject -in $cert_file | sed -n 's/.*[[:space:]]*CN[[:space:]]*=[[:space:]]*\([^\/]*\).*/\1/p' | tr -d '[:space:]'); \
      echo $alias; \
      if [ ! -z "$alias" ]; then \
        echo "Importing $alias"; \
        keytool -import -trustcacerts -alias "$alias" -file $cert_file -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -noprompt; \
      fi \
    done
fi
