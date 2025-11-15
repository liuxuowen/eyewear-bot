#!/bin/bash

SERVICE=eyewear-bot
LOGFILE=/opt/projects/logs/eyewear-bot.log

function start_service() {
    echo "Starting $SERVICE..."
    sudo systemctl start $SERVICE
    sudo systemctl status $SERVICE --no-pager
}

function restart_service() {
    echo "Restarting $SERVICE..."
    sudo systemctl restart $SERVICE
    sudo systemctl status $SERVICE --no-pager
}

function status_service() {
    sudo systemctl status $SERVICE --no-pager
}

function log_service() {
    tail -n 50 -f $LOGFILE
}

case "$1" in
    start)
        start_service
        ;;
    restart)
        restart_service
        ;;
    status)
        status_service
        ;;
    log)
        log_service
        ;;
    *)
        echo "Usage: $0 {start|restart|status|log}"
        exit 1
        ;;
esac