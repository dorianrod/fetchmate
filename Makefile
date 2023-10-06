build:
	docker build -t peanut-ai-sql-requester .
	
start:
	docker run -d peanut-ai-sql-requester