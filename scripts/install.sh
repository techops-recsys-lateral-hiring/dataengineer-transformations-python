#!/bin/sh

# batect dependencies
echo "Installing homebrew if it's not installed..."
which brew || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

echo "Installing docker if it's not installed..."
which docker || brew cask install docker

echo "Installing java if it's not installed..."
which java
if [ $? -ne 0 ]; then
  brew tap adoptopenjdk/openjdk
  brew cask install adoptopenjdk11
fi
