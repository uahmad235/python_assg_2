# Python assignment 2

Project details:
https://hackmd.io/@gFZmdMTOQxGFHEFqqU8pMQ/S1cZqwefo

## Local Setup

* Clone project using command:
   
   ```
   pip install https://github.com/uahmad235/python_assg_2.git
   ```
  

## Task 1

### Task1 Directory Structure:
```
task1
    ├── data      # contains data files to  save & load object state
    ├── main.py   # driver script
    └── src
        ├── helper
        │   ├── __init__.py
        │   ├── prompt_helper.py
        │   └── utils.py
        ├── __init__.py
        └── lib
            ├── __init__.py
            ├── institution.py
            └── room.py
```

### Installation and Execution

1. Run the following command to navigate to the task-1 directory using:

   ```shell
   cd python_assg_2/ 
   ```

2. Run program using following command:

   ```shell
   python task1/main.py
   ```

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
