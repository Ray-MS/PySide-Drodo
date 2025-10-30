# Drodo

## Command
```
pyside6-rcc resources.qrc -o resources_rc.py
python main.py
```

## File Structure
```
Drodo/
├─- config/
│   ├── __init__.py
│   ├── mapping.py
│   ├── url_manager.py
│   └── urls.yaml
├─- models/
│   ├── __init__.py
│   └── data_model.py
├─- network/
│   ├── __init__.py
│   └── fetcher.py
├─- ui/
│   ├── __init__.py
│   ├── drodo/
│   ├── sidebar/
│   └── main_window.py
├─- resources/
├─- resources.qrc
├─- resources_rc.py
├─- .env
├─- app.py
└── main.py
```
