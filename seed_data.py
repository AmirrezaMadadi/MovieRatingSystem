from app.db.database import SessionLocal
from app.models.models import Genre, Director

def seed():
    db = SessionLocal()
    if not db.query(Genre).first():
        db.add_all([Genre(name="Action"), Genre(name="Sci-Fi"), Genre(name="Drama")])
    if not db.query(Director).first():
        db.add(Director(name="Christopher Nolan"))
    
    db.commit()
    db.close()
    print("داده‌های اولیه با موفقیت اضافه شد!")

if __name__ == "__main__":
    seed()