# StellaNow CLI Tool - Contributors

StellaNow CLI is a command-line interface for interacting with the StellaNow services.

## Installation

To install StellaNow CLI, you can use pip:

```
pip install -e .
```

This command installs the CLI in editable mode, which is convenient for development purposes.

## Usage

After installation, you can use the **'stellanow'** command in your terminal to interact with StellaNow services. Here is how to use some of the available commands:

### Configure

You can use the **'configure'** command to set up the necessary credentials and configurations for a specific service. The profile will store a particular set of configurations.

Here is how to use the command:

```
stellanow --profile YOUR_PROFILE_NAME configure SERVICE_NAME
```

If no profile is specified, the configurations will be stored under the `DEFAULT` profile.

#### Options:

- `-p, --profile` specifies the profile for storing configurations (like `DEFAULT`, `testProfile`). If no profile is provided, the `DEFAULT` profile is used.
- `-v, --verbose` enables detailed logging for executed commands, providing more granular information about the operation and process flow.

#### Important: Option Placement for `-p` and `-v`

When using the `-p` (profile), or `-v` (verbose) options, they **must always be placed immediately after the `stellanow` command**.

```bash
stellanow -p testProfile -v code-generator-service events
```

### Configuration Precedence

The StellaNow CLI follows this precedence for determining configuration values:

```
Command Line Options -> Configuration File
```

### Development

StellaNow CLI is built using the Python Click library.

If you want to add a new command, follow these steps:

- Create a new Python file for your command in the **'commands'** directory.
- Define your command as a function, and decorate it with the **'@click.command()'** decorator.
- In **'cli.py'**, import your command function and add it to the main CLI group using **'cli.add_command(your_command_function)'**.

Please note that StellaNow CLI follows the conventions of the Python Click library.

# StellaNow CLI Tool - Users

Welcome to the StellaNow CLI tool. This tool automates the process of generating class code from StellaNow event and model specifications and provides a summary of changes between the generated classes and the specifications fetched from the API. It's recommended to use this tool in conjunction with the StellaNow SDK to ensure that your application's message classes are up-to-date with the latest specifications.

## Installation

To install the StellaNow CLI tool, run the following command:

```
pip install stellanow-cli
```

The tool is hosted on PYPI and can be installed via pip or pipenv.

## Usage

After installation, you can use the **'stellanow'** command in your terminal to interact with StellaNow services. Here is how to use some of the available commands:

### Configure

You can use the 'configure' command to set up the necessary credentials and configurations for a specific service. The profile will store a particular set of configurations.

Here is how to use the command:

```
stellanow --profile YOUR_PROFILE_NAME configure SERVICE_NAME
```

If no profile is specified, the configurations will be stored under the 'DEFAULT' profile. Profile names are case-sensitive.

#### Important: Option Placement for `-p` and `-v`

When using the `-p` (profile), or `-v` (verbose) options, they **must always be placed immediately after the `stellanow` command**.

```bash
stellanow -p testProfile -v code-generator-service events
```

### Configuration Precedence

The StellaNow CLI follows this precedence for determining configuration values:

```
Command Line Options -> Configuration File
```

## Commands

### Code Generator Service Commands

#### COMMAND: `configure code-generator-service`

The **'configure'** command sets up the necessary service credentials and configurations for a specific profile or for the `DEFAULT` profile if none is specified.

##### Command usage:

```
stellanow --profile myProfile configure code-generator-service
```

##### Command options:

- **'--profile'**: The profile name for storing a particular set of configurations. If no profile is specified, the configurations will be stored under the `DEFAULT` profile.
- **'--base_url'**: The host for accessing the StellaNow API. This should be a valid URL string without a trailing slash (`/`)
- **'--username'**: The username credential for accessing the StellaNow API. This should be the same as your StellaNow account username.
- **'--password'**: The password credential for accessing the StellaNow API. This should be the same as your StellaNow account password.
- **'--organization_id'**: The unique identifier (UUID) of the organization in StellaNow. This is used to scope the operations within the given organization's context.

The command validates the provided values to ensure they meet the expected formats: the `base_url` should be proper string in URL format without a trailing slash (`/`)., the `username` should be a valid email address or a string containing only alphanumeric characters, dashes, and underscores; the `password` should be a string with no whitespace and a length of 8-64 characters; and the `organization ID` should be valid UUID.

The command then writes these configurations to a file named `config.ini` in the `.stellanow` directory of your home folder. If this directory or file does not exist, they will be created.

#### COMMAND: `code-generator-service events`

The **'code-generator-service events'** command fetches the latest event specifications from the API and outputs a list of the events into the terminal prompt.

##### Command usage:

```
stellanow code-generator-service events
```

This will print a table of all available events with their metadata (EventID, Event Name, Is Active, Created At, Updated At).

##### Command options:

- **'--project_id'**: The unique identifier (UUID) of the project in StellaNow. This is used to scope the events within the given project's context.

#### COMMAND: `code-generator-service models`

The **'code-generator-service models'** command fetches the latest models specifications from the API and outputs a list of the models into the terminal prompt.

##### Command usage:

```
stellanow code-generator-service models
```

This will print a table of all available models with their metadata (ModelID, Model Name, Created At, Updated At).

##### Command options:

- **'--project_id'**: The unique identifier (UUID) of the project in StellaNow. This is used to scope the models within the given project's context.

#### COMMAND: `code-generator-service generate`

The **'code-generator-service generate'** command fetches the latest event and models specifications from the API and generates corresponding class code in the desired programming language.

##### Command usage:

```
stellanow code-generator-service generate --namespace MyApp --destination . --force --events Event1,Event2 --language csharp
```
This command will generate C# classes for the events 'Event1' and 'Event2', as well as their related model classes. The generated event classes will be placed in the namespace 'MyApp.Events', while the model classes will be in 'MyApp.Models'. Both types of classes will be saved in the current directory. If a file for an event or model already exists, it will be overwritten due to the **'--force'** flag.
##### Command options:

- **'--project_id'**: The unique identifier (UUID) of the project in StellaNow. This is used to scope the operations within the given project's context.
- **'--namespace (-n)'**: The namespace for the generated classes. Defaults to an empty string.
- **'--destination (-d)'**: The directory to save the generated classes. Defaults to the current directory.
- **'--force (-f)'**: A flag indicating whether to overwrite existing files. Defaults to false.
- **'--events (-e)'**: A list of specific events to generate. If this option is not provided, classes for all events will be generated.
- **'--language (-l)'**: The programming language for the generated classes. Can be `csharp`, `python` or `typescript`. Defaults to 'csharp'.

### Data DNA Stream Tester Commands

#### COMMAND: `data-dna-stream-tester simulate-game-match`

The **'data-dna-stream-tester simulate-game-match'** command simulates sending game state data to an MQTT broker, which can be used for testing data ingestion.

##### Command usage:

```
stellanow data-dna-stream-tester simulate-game-match --mqtt_username YOUR_MQTT_USERNAME --mqtt_password YOUR_MQTT_PASSWORD --mqtt_broker YOUR_MQTT_BROKER --input_file /path/to/game_state_data.zip --org_id YOUR_ORG_ID --project_id YOUR_PROJECT_ID --event_type YOUR_EVENT_TYPE --entity_type YOUR_ENTITY_TYPE --entity_id YOUR_ENTITY_ID
```

##### Command options:

- **'--mqtt_username'**: Username to authenticate with the MQTT broker.
- **'--mqtt_password'**: Password to authenticate with the MQTT broker.
- **'--mqtt_broker'**: The URL of the MQTT broker to connect to.
- **'--mqtt_port'**: Port for MQTT broker connection. Default is 8083.
- **'--input_file'**: Path to a zip file containing game state data to send.
- **'--org_id'**: The unique identifier of the organization in StellaNow.
- **'--project_id'** The unique identifier of the project in StellaNow.
- **--event_type**: Event type definition ID for the game state data.
- **--entity_type**: Entity type definition ID for the game state data.
- **--entity_id**: Entity ID for the game state data.
- **--infinite**: If set, the game state data will be sent continuously until the process is interrupted.

## Contact and Licensing

For further assistance and support, please contact us at **help@stella.systems**

The StellaNow CLI is now open-source software, licensed under the terms of the MIT License. This allows for authorized copying, modification, and redistribution of the CLI tool, subject to the terms outlined in the license.

Please note that while the StellaNow CLI is open-source, the StellaNow platform and its associated code remain proprietary software. Unauthorized copying, modification, redistribution, and use of the StellaNow platform is prohibited without a proper license agreement. For inquiries about the licensing of the StellaNow platform, please contact us via the above email.