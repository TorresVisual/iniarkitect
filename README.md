# INIArkitect

INIArkitect is a tool designed to manage and modify INI configuration files for ARK: Survival Evolved. It provides a streamlined way to handle configuration changes and maintain consistency across your ARK server or client installations.

## Features

- Simple configuration management through `config.ini`
- Source and destination directory configuration
- Easy modification of ARK configuration files

## Configuration

The tool uses a `config.ini` file to manage its settings:

```ini
[Settings]
destination_dir = D:\SteamLibrary\steamapps\common\ARK\Engine\Config
source_dir = D:\Coding\INIArkitect\inis
```

- `destination_dir`: The path to your ARK Engine Config directory
- `source_dir`: The path where your INI files are stored

## Usage

1. Configure your `config.ini` file with the appropriate paths
2. Place your INI files in the source directory
3. Run the application to apply the configurations

## Requirements

- Windows operating system
- ARK: Survival Evolved installation
- Access to the ARK Engine Config directory

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 