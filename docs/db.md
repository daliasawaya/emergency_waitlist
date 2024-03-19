# Database Design

## Patient
* PatientID (Primary Key)
* Name
* Severity
* ArrivalTime
* InQueue (boolean - True if in queue - False if not)
* Treated (boolean - True if treated - False if not)
* TimeInQueue (time spent in the queue for this patient)

## User
* UserID
* Name
* Code (to sign in)

## Admin
* AdminID
* Name


## Queue
* QueueID
* Array of PatientIDs 
* WaitTime (total wait time)
