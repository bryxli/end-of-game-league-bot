## CURRENTLY OUT-OF-DATE
# end-of-game-league-bot  
A Discord bot that allows a user to input specific usernames. The bot will automatically ping a user after their game has ended stating win/loss and KDA. This will allow users who usually play together to easily keep track of each other's in-game statistics via Discord messaging. The bot checks player statistics every minute.    
**IMPORTANT: MUST CHANGE \<RIOT-API-TOKEN> AND \<DISCORD-API-TOKEN> LOCATED IN main.py**  
**Currently only works with specified channel id. Only for NA1 servers.**  
**To start the bot, run $lolsetup to specify text channel to send statistics to.**

Commands:  
$lolsetup <CHANNEL ID> - run bot setup.  
$lolname <SUMMONER NAME> - adds a user to the list.  
$loldel <SUMMONER NAME> - deletes a user from the list.  
$loldelall - clears the user list.  
$lolprint - print all users on the list.  
$lolsave - save names of all users to \data.json.  
$lolimport - imports user list from \data.json.

Bot checks match history of player list every minute. Repeat matches will not be displayed.   
**NOTE: If SUMMONER NAME includes spaces, the name must be surrounded in quotes.**  
**May be detected as a trojan due to the use of PyInstaller to compile.**  
Compiled with command: pyinstaller --onefile --windowed --icon=icon.ico main.py
