from app.db.session import SessionLocal, engine, Base
from app.models.role_db import Role

def init_roles():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    roles = [
        {"name": "admin", "description": "System administrator"},
        {"name": "manager", "description": "Manages tasks and employees"},
        {"name": "employee", "description": "Performs assigned tasks"},
    ]

    for role_data in roles:
        existing = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing:
            db.add(Role(**role_data))

    db.commit()
    db.close()
    print("✅ Roles initialized successfully")

if __name__ == "__main__":
    init_roles()
