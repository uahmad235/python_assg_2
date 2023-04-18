# Python assignment 2

Project details:
https://hackmd.io/@gFZmdMTOQxGFHEFqqU8pMQ/S1cZqwefo

This repo implements an application as **micro-services architecture** for Software Design Course at Innopolis University.

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

### Task2 Directory Structure
```
task2/
├── docker-compose.yml
├── Dockerfile
├── __init__.py
├── main.py
├── requirements.txt
└── src
    ├── __init__.py
    ├── ml_model
    │   ├── api.py
    │   ├── classifier.pkl
    │   ├── Dockerfile
    │   ├── __init__.py
    │   └── requirements.txt
    ├── mongo
    │   ├── __init__.py
    │   └── mongo_client.py
    ├── synchronization
    │   ├── Client_Secret.json
    │   ├── Dockerfile
    │   ├── Google.py
    │   ├── __init__.py
    │   ├── main.py
    │   ├── requirements.txt
    │   └── token_drive_v3.pickle
    └── terminal
        ├── funcs_registry.py
        ├── __init__.py
        ├── terminal.py
        └── user.py
```

### Installation

1. Go to the following directory from the root folder of the project

   ```shell
   cd task2/
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
