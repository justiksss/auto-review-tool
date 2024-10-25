For run project make sure that you have docker
and fill env file by .env.example

`docker compose up`




Tasks
  - Write exceptions handlers
  - Add some tests
  - Setup loguru (sentry-sdk mb?)


Part 2 What if

- Set max length for description 
- Allow only code files (remove package.json, poetry.lock) for analyze only source code
- Setup gunicorn for faster requests handling
- Use AI for analyze on docker container, remove http delay (LamaAI or something)
- Use asyncio for concurrently requests (GitHub)
