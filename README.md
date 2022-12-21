# bgStats-dataVisualiser
 
Yet another python project, This takes an exported json file from [bgStats](https://www.bgstatsapp.com/), which graphs and pretties data from the json. 



## Arguments
`-n or --new`: If the data is new and needs to run again, eg games or people have been added

`-v or --verbose`: Enables verbose messages when runing the code, usefull for debugging

`-d or --date`: The date you would like to limit the play data by

`-i or --input`: The directory of the `.json` file you would like to analyse. Defults to todays date in the format "`BGStatsExport/yyy_mm_dd.json`"

## TODO
### Data gathering
- [X] each player obj to also store a list of the UUIDs of each game they're in
- [ ] combine time lim method and load plays method so only running thru the plays list once
- [ ] games obj to track categories & game families
- [ ] have expected win rate as a player category


### Image Gen
- [ ] potion explotion to be bigger in the game info
- [ ] top mechanics pic to be flexible for mechanics/family/category
- [ ] add choice of sort by play count/win count (for cryptid image)
- [ ] top mechanics to come from game plays not from games owned

### Plotting
-[x] exclude my plays from bar graph
-[ ] sort big→ small