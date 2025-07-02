NEXT:

 - [X] Sort config.json with most important options first
 - [X] ZIP download of controller + client
       idea: post compile, files get zipped (done by python). zip gets named uuid_sometihng, moved to a static folder. These files are shown in a file browser somewhere
 - [ ] Test to make sure controller + client still function as intended
 - [X] Logging!
 - [ ] Controller runner (runs controllers in backgorund in new thread, data on controllers tab w start/stop)
        - [X] Might need to log controllers in sqlite for restart persistence
        - [ ] Bug: Can start multiple of same controller. No fail condition on same controller ID?
        - [X] Add in refresh button working here too, makes life easier
        - [X] BUG: Upon restart, the unique constraint fails, making it so the contorller data is not updated, and has old pid, so "[Errno 3] No such process" is shown.
~~        - [ ] Make it so when you delete a package file, it delete the contorller entry too?. I see pros/cons for the connected, and disconnected versions. I dunno.~~
 - [ ] Make it look cool(er)
 - [ ] ICMP x64?
      - [ ] Stuck on waiting for pipe. 
 - [ ] Addtl protocols



 #### Bugs & Considerations:
  - Need to check if 2 icmp controllers at once would break. May not due to filtering of PID, tag, and seq. 
  - Restarting a controller in current way makes a new UUID, which causes confusion
  