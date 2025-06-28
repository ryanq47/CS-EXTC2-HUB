NEXT:

 - [X] Sort config.json with most important options first
 - [X] ZIP download of controller + client
       idea: post compile, files get zipped (done by python). zip gets named uuid_sometihng, moved to a static folder. These files are shown in a file browser somewhere
 - [ ] Test to make sure controller + client still function as intended
 - [ ] Logging!
 - [ ] Controller runner (runs controllers in backgorund in new thread, data on controllers tab w start/stop)
        - [X] Might need to log controllers in sqlite for restart persistence
        Bug: Can start multiple of same controller.No fail condition on same controller ID?
        - [ ] Add in refresh button working here too, makes life easier
 - [ ] Make it look cool(er)
 - [ ] ICMP x64?
 - [ ] Addtl protocols