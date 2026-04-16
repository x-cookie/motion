#!/bin/bash
# Motion Demo Launcher
# Run this script to start the Motion demo with 50 sample tasks

echo "Starting Motion demo..."
docker-compose -f docker-compose.demo.yaml up --build