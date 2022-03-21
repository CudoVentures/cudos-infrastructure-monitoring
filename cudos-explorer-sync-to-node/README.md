## CUDOS SYNC CHECKER

The main purpose of the script is to monitor the sync levels between the root node and explorers and to 
alert via dedicated Slack channel for anomalies such as any of the explorers is too far behind the node height or if 
the node itself is stuck because of a chain halt or network problems. It works by making scheduled REST API calls for the current height 
of the participating modules and applies logic to the results.

At this point it is meant to monitor the said points, but it can be further developed to include health checks for 
more modules depending on up do date information from the node for their correct work. 

### SETTINGS

For a correct set-up, all variables in settings.py have to be set. 

* Global settings
   - SCHEDULE_TIME
     > Sets the global cron job intervals / in MINUTES
   - MAX_SYNC_TOLERANCE
     > The maximum acceptable delay in height for a module to be behind the node.
   - MIN_AVERAGE
     > The difference in height under which we consider the node stuck during a self-check.
   - SELF_CHECK_INTERVAL
     > Every SELF_CHECK_INTERVAL time, the script will perform a self-health check of the node.
   - REMINDER
     > If there is unresolved problem during an active SILENT_MODE a reminder message will kick in every REMINDER minutes
   - SILENT_MODE
     > This is automatically activated when an error is detected in order to avoid spamming with repeated errors. 
     It will remain active, until the error/s are dealt with and the system is back on track as expected.

### SELF CHECK
a simple and configurable algorithm is introduced to monitor the node itself and alert about network halts at early stage.
#### SELF CHECK FORMULA
 - The value of
    > abs((last SELF_CHECK_INTERVAL node heights* / SELF_CHECK_INTERVAL) - last node height)
   
   ***obtained at SCHEDULE_TIME minutes intervals**
 
If the result is <= MIN_AVERAGE we may consider the current state of the node as unhealthy and an alert will be triggered 
 via Slack for further investigation.
