# Makefile for TravelHax0r MCP Server

.PHONY: debug-up debug-down logs

# Start the debug container (HTTP transport) in detached mode
debug-up:
	docker-compose -f docker-compose.yml.debug up --build -d

# Stop the debug container
debug-down:
	docker-compose -f docker-compose.yml.debug down

# Show logs from the debug container
logs:
	docker-compose -f docker-compose.yml.debug logs -f
