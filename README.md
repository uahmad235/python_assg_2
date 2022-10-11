# Python assignment 2

Project details:
https://hackmd.io/@gFZmdMTOQxGFHEFqqU8pMQ/S1cZqwefo

## Task 2

### Installation

1. Go to the following directory from the root folder of the project

   ```shell
   cd src/task2
   ```

2. Create microservices:

   ```shell
   docker-compose up
   ```

3. Start interactive terminal session:

   ```shell
   docker run -it --rm --network task2_default task2_app bash
   python main.py
   ```