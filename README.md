# Web Application for P2P Chat, File Transfer and Live Gaming on a Local Network

## Project Overview

A simple web Application for connecting people in a Local Network

## Key Features

1. **Automatic Device Discovery**: The scanning feature automatically detects devices on the network using the service.
2. **P2P File Transfer and Chatting**: Any two users can directly chat or share files without any server.
3. **Live Notification**: Instant Notification about any received file or message.
4. **Real Time Gaming**: Any two users can play a duo game like Chess, with live updates of hovering and piece position.

## Chatting and File Sharing

- Uses HTTP protocol for both.
Text transfer uses HTTP GET request on the target IP Address, which includes sender information and a message in the parameters.
- File sharing feature uses in-build feature of HTTP using POST request on target IP Address.
- Automatic Device Discovery uses current local IP Address of the device and subnet mask to generate the range of IPs in the network and send signal on all those IPs.
- The live notification continously make request on the its local server in asynchronous manner to get information about any received data.

## Real Time Gaming

- All the functions are performed asynchronously.
- The application stores the current state of the user, and if there is a change in the current state then the application sends the updated state using HTTP GET.


---

## For more information
Documentation >> "Detailed Report.docx"  or  [Click Here](https://github.com/prajjwalsony/Campus-Network-WebApp/tree/main/Documentation)

---

## Download

You can download the project from the following link:
[Download](https://github.com/prajjwalsony/Campus-Network-WebApp/archive/refs/heads/main.zip)
