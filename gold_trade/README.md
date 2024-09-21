# Gold Trade API

## Overview
This is a Django RESTful API for trading gold, allowing users to register, log in, check gold prices, and make trades.

## Features
- User registration and authentication
- Fetching real-time gold prices
- Trade transactions
- Dockerized setup with Redis

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Running the Application
1. Clone this repository.
2. Navigate to the project directory.
3. Run the following command to start the application:
    ```bash
    docker-compose up --build
    ```

### API Endpoints
- **POST /trade/register/** - Register a new user.
- **POST /trade/login/** - Log in a user.
- **GET /trade/gold-price/** - Fetch the current gold price.

## Assumptions and Decisions
- The application uses Redis for caching gold prices.
- User authentication is handled using Django's built-in features.

## Bonus Points
- A React frontend is planned for interacting with this API.
- WebSockets will be implemented for real-time gold price updates.
