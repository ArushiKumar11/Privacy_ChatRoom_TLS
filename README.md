# CryptoChat Messenger

A secure messaging application built with Python, PyQt5, and strong encryption using public key cryptography.

## Overview

Python TLS Chat enables secure communication between users through a client-server architecture. All messages are fully encrypted with public key cryptography, ensuring that your conversations remain private and protected from interception.

## Features

- **Secure Communication**: End-to-end encryption using public key cryptography
- **User-Friendly Interface**: Built with PyQt5 for a responsive GUI experience
- **Direct Messaging**: Connect and chat with individual users
- **Group Chats**: Create and manage group conversations
- **Group Invitations**: Invite friends to join your chat groups

## System Architecture

The application consists of two main components:
- **Client**: Handles the user interface and message encryption/decryption
- **Server**: Manages connections and routes encrypted messages between clients

![image](https://github.com/user-attachments/assets/2dc00035-2a17-425f-a425-bd8172adad44)

### Client Components
- ConnectionScreen: Handles initial server connection
- DashboardScreen: Main navigation interface
- SingleChat: One-to-one messaging interface
- GroupChat: Multi-user chat interface
- CreateGroup: Group creation functionality
- GroupInvite: Invitation management
- Protocol: Communication protocol implementation

### Server Components
- Server: Core server functionality
- Protocol: Server-side protocol implementation

## Installation

### Prerequisites
- Python 3.6 or higher
- PyQt5

### Setup Instructions

1. Install required dependencies:
   ```
   pip install PyQt5
   ```

2. Start the server:
   ```
   cd server
   python server.py
   ```

3. Launch the client application:
   ```
   cd client
   python StartApp.py
   ```

## Usage

1. Connect to the server using the Connection Screen
2. Navigate to the Dashboard to see available options
3. Start a direct chat or create/join group conversations
4. Enjoy secure communication!

## Known Limitations

- The application currently doesn't support multiple users with identical names, which may cause unexpected behavior

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to help improve the application.

## Team Members
1. Arushi Kumar
2. Himanshu Singhal
3. Rishita Agarwal

