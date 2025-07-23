NEXT:

- [ ] Stats for nerds reads controller logs
- [ ] X64 chain busted for some reason

 - [ ] Addtl protocols



 #### Bugs & Considerations:
  - Need to check if 2 icmp controllers at once would break. May not due to filtering of PID, tag, and seq. 
  - Restarting a controller in current way makes a new UUID, which causes confusion
  - [X] Wrong controller gets started in gui, wonder if lambda issue with vars/choosing last

  - Make sure logs end up in correct controller folder?
  - Add in stats for nerds live log feed from that dir