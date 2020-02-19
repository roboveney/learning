#!/bin/bash

echo update GitHub repositories
cd ~/learning
git pull origin
echo update Gogs repositories
cd ~/code/CodeBase
git pull origin
cd ../FractureID
git pull origin
cd
echo all repositories are up to date
