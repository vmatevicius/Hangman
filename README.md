# Hangman Game App

Hangman Game App is a classic word-guessing game where players try to guess a hidden word by suggesting letters within a limited number of tries. This repository contains a web-based implementation of the Hangman game with user registration, leaderboards, multiple difficulty modes, and user account summaries.

## Getting Started

Follow these instructions to set up and run the Hangman Game App on your local machine.

### Prerequisites

- Python 3.8 or higher
- Docker (optional, for Dockerization)
- Git

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/hangman-game-app.git
cd hangman-game-app
```

## Features

- User registration and login functionality
- Leaderboards displaying the top scores
- Three difficulty modes: easy, medium, and hard
- Score system based on difficulty: easy (10 points), medium (20 points), hard (50 points)
- User account summary with statistics on games played, games won/lost, correct/wrong guesses, and best score


## How to Play

1. Register or log in to your account.
2. Choose a difficulty mode (easy, medium, or hard).
3. Guess letters to reveal the hidden word.
4. Each incorrect guess reduces the remaining tries by 1.
5. Win the game by guessing the entire word within the allotted number of tries.
6. Your score is based on the difficulty level and the number of remaining tries.