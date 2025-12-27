# INIArkitect 2.0

**INIArkitect** is a premium management tool for ARK: Survival Evolved configuration files. It provides a sleek, modern interface to effortlessly swap between different INI presets while ensuring your data is safe with automatic backups.

![INIArkitect Mockup](https://raw.githubusercontent.com/username/repo/main/assets/mockup.png) *(Placeholder for your mockup)*

## ✨ New Features

- 🌑 **Modern Dark UI**: Powered by `customtkinter` for a premium, high-tech look.
- 💾 **Auto-Backups**: Automatically creates timestamped backups of your current INIs before applying new ones.
- ⚡ **Dynamic Presets**: Automatically detects folders in your source directory and generates action buttons.
- 📂 **Quick Navigation**: One-click access to your source and destination folders.
- 🔄 **Live Refresh**: Update your preset list without restarting the app.
- 🛡️ **Robust Config**: Reliable handling of source and destination paths via `config.ini`.

## ⚙️ Configuration

Settings are now managed directly inside the app, or via `config.json` in the application root:

```json
{
    "destination_dir": "C:\\Path\\To\\ARK\\Engine\\Config",
    "source_dir": "C:\\Path\\To\\Your\\INI\\Presets"
}
```

- `destination_dir`: Where the active `Game.ini` and `GameUserSettings.ini` reside.
- `source_dir`: A folder containing subfolders (presets), each with its own `.ini` files.

## 🚀 Getting Started

1. **Configure**: Set your paths in `config.ini`.
2. **Organize**: Place your INI presets in folders within your source directory (e.g., `inis/PVP`, `inis/PVE`, `inis/Boosted`).
3. **Run**: Launch `INIArkitect` and click a preset to apply it.

## 🛠️ Requirements

- **Windows 10/11**
- **ARK: Survival Evolved**
- Python 3.10+ (if running from source)

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.