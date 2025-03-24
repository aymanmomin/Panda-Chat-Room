#  Panda-Chat Room
## About
A Python-based client-server chat application themed around pandas. Features real-time messaging, ASCII art sharing, and fun commands. Built with `socket` and `threading`


## Features  
### Core Features  
- **Multi-Client Support**: Handle unlimited users via threading.  
- **Panda-Themed Messaging**:  
  - Auto-adds random panda emojis (`🐼`, `🎍`) to messages. 
- **View all users**
- **Fun Facts**

### Extra Credit  
- **ASCII Art Gallery**:  
  - 10+ custom panda ASCII images triggered by `@bonus`.  
  - Error handling for invalid key (e.g., `@bonus pizza` → private error message).

## Installation  
**No additional software required!**  
1. Ensure **Python 3.x** is installed.  
2. Download these files:  
   - [`server.py`](#server-code)  
   - [`client.py`](#client-code)  

## Setup  
1. **Server Setup**:  
   - Run `server.py` first:  
     ```bash  
     python server.py  
     ```  
   - Default IP/Port: `127.0.0.1:5555` (modify in code if needed).  

2. **Client Setup**:  
   - Run `client.py` in separate terminals:  
     ```bash  
     python client.py  
     ```  
   - Enter a **unique panda name** when prompted. 

# Usage  
### Commands  
| Action          | Input Example          | Result                                  |  
|-----------------|------------------------|-----------------------------------------|  
| Send message    | `Hello!`               | Broadcasts: `🐼 Sarah: Hello!`          |  
| Get panda fact  | `@bamboo`              | Sender sees: `📚 Panda Fact: [...]`     |  
| List users      | `@grove`               | Sender sees: `🌿 Connected Pandas: [...]` |  
| Share ASCII art | `@bonus hey`           | All see: `Sarah:\n[ASCII art]`          |  
| Exit chat       | `@leaves`              | Broadcasts: `🍂 Sarah left the grove...` |  


## Outputs
1. **User Joins**: 🐼 Sarah joined the grove!
2. **ASCII Art Broadcast**:  "Test it your self 😜"
3. **Invalid Command (Private Error)**:  🐼 No ASCII found for this mood! Try: hey, shy, sleeping, dab, shocked, swag, thanks,

## Referred Links  
1. Python `socket` module: [Official Documentation](https://docs.python.org/3/library/socket.html)  
2. ASCII Art Inspiration/Used from: [ASCII Archive](https://www.asciiart.eu/) and [Emoji Combos](https://emojicombos.com/panda)
