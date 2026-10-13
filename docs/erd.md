erDiagram
    USERS {
        uuid id PK "UUID, Primary Key"
        string full_name "NOT NULL"
        string email "UNIQUE, NOT NULL"
        string password_hash "NOT NULL"
        datetime created_at "NOT NULL, DEFAULT now()"
    }

    PREDICTIONS {
        uuid id PK "UUID, Primary Key"
        uuid user_id FK "FK to USERS.id, NOT NULL"
        string input_hash "NOT NULL"
        jsonb input_data "NOT NULL"
        jsonb prediction_result "NOT NULL"
        float confidence_score "NOT NULL, CHECK (0.0 <= score <= 1.0)"
        boolean is_fallback_triggered "NOT NULL, DEFAULT false"
        datetime created_at "NOT NULL, DEFAULT now()"
    }

    USERS ||--o{ PREDICTIONS : "owns / makes"