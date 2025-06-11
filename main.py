# main.py

# ---------------------------------------------------------------------------
# 1. Importy - Načteme všechny potřebné nástroje
# ---------------------------------------------------------------------------
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importujeme naše vlastní moduly, které jsme vytvořili
import crud
import models
import schemas
from database import SessionLocal, engine

# ---------------------------------------------------------------------------
# 2. Nastavení databáze a aplikace
# ---------------------------------------------------------------------------

# Tento příkaz řekne SQLAlchemy, aby vytvořilo všechny tabulky definované
# v models.py, pokud v databázi ještě neexistují.
# Pro seriózní aplikace se později používá nástroj Alembic, ale pro začátek je toto ideální.
models.Base.metadata.create_all(bind=engine)

# Vytvoříme instanci naší FastAPI aplikace
app = FastAPI()


# ---------------------------------------------------------------------------
# 3. Databázová závislost (Dependency)
# ---------------------------------------------------------------------------

def get_db():
    """
    Tato funkce se spustí pro každý příchozí API požadavek.
    Otevře nové spojení (session) s databází, poskytne ho endpointu
    a po dokončení requestu ho VŽDY bezpečně uzavře.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Základní endpoint pro ověření, že aplikace běží."""
    return {"message": "Vítejte v API pro vaši Habit Tracker aplikaci!"}


# --- Endpoints pro Uživatele (Users) ---

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Vytvoří nového uživatele.
    TODO: V reálné aplikaci zde bude chybět registrace s emailem a hashování hesla!
    """
    # Pro jednoduchost zatím neověřujeme, zda uživatel existuje.
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Vrátí seznam všech uživatelů se stránkováním."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Vrátí jednoho konkrétního uživatele podle jeho ID."""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# --- Endpoints pro Návyky (Habits) ---

@app.post("/users/{user_id}/habits/", response_model=schemas.Habit)
def create_habit_for_user(
    user_id: int, habit: schemas.HabitCreate, db: Session = Depends(get_db)
):
    """Vytvoří nový návyk pro konkrétního uživatele."""
    # Ověříme, zda uživatel existuje, než mu přiřadíme návyk
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Propojení s CRUD vrstvou
    return crud.create_user_habit(db=db, habit=habit, user_id=user_id)


@app.get("/users/{user_id}/habits/", response_model=List[schemas.Habit])
def read_habits_for_user(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Vrátí seznam návyků pro konkrétního uživatele."""
    # Ověříme, zda uživatel existuje
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    habits = crud.get_habits_by_user(db, user_id=user_id)
    return habits

@app.post("/users/{user_id}/goals/", response_model=schemas.Goal)
def create_goal_for_user(
    user_id: int, goal: schemas.GoalCreate, db: Session = Depends(get_db)
):
    """Vytvoří nový goal pro konkrétního uživatele."""
    # Ověříme, zda uživatel existuje, než mu přiřadíme návyk
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Propojení s CRUD vrstvou
    return crud.create_user_goal(db=db, goal=goal, user_id=user_id)

@app.get("/users/{user_id}/goals/", response_model=List[schemas.Goal])
def read_goals_for_user(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Vrátí seznam golů pro konkrétního uživatele."""
    # Ověříme, zda uživatel existuje
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    goals = crud.get_goals_by_user(db, user_id=user_id)
    return goals