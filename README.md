data-analyst-api/
├── app/
│   ├── main.py
│   ├── routers/
│   │   └── datasets.py
│   ├── services/
│   │   ├── dataset_service.py   # leitura CSV, metadados
│   │   └── query_service.py     # LLM + execução segura
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   └── core/
│       └── config.py            # env vars (API keys)
├── uploads/                     # CSVs temporários
├── requirements.txt
└── .env