# Drodo

## Command
```
pyside6-rcc resources/resources.qrc -o resources_rc.py
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
│   ├── gemtd/
│   ├── steam/
│   ├── data_model.py
│   └── player_manager.py
├─- network/
│   ├── __init__.py
│   └── fetcher.py
├─- ui/
│   ├── __init__.py
│   ├── drodo/
│   │   ├── __init__.py
│   │   ├── gemtd/
│   │   │   ├── __init__.py
│   │   │   └── leaderboard/
│   │   ├── gemtd_herosea/
│   │   │   ├── __init__.py
│   │   │   └── herosea.py
│   │   ├── gemtd_main.py
│   │   ├── gemtd_store.py
│   │   └── gemtd_rank.py
│   ├── sidebar/
|   │   ├── __init__.py
|   │   └── sidebar.py
│   ├── info_view.py
│   └── main_window.py
├─- resources/
├─- resources.qrc
├─- resources_rc.py
├─- .env
├─- app.py
└── main.py
```
