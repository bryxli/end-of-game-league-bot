# end-of-game-league-bot  
Easy to use Discord bot that allows a user to input specific usernames. The bot will automatically ping a user after their game has ended stating win/loss and KDA. This will allow users who usually play together to easily keep track of each other's in-game statistics via Discord messaging. The bot checks player statistics every minute.    
**Currently only works with specified channel id. Only for NA1 servers.**  
**To start the bot, run $lolsetup to specify text channel to send statistics to.**

Commands:  
$lolhelp - help menu.  
$lolsetup <CHANNEL ID> - run bot setup.  
$lolname <SUMMONER NAME> - adds a user to the list.  
$loldel <SUMMOENR NAME> - deletes a user from the list.  
$lolprint - print all users on the list.  

Bot checks match history of player list every minute. Repeat matches will not be displayed.   
**NOTE: If SUMMONER NAME includes spaces, the name must be surrounded in quotes.**  

Code hosted on www.repl.it and powered by www.uptimerobot.com
