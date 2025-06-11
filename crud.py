from sqlalchemy.orm import Session
import models
import schemas

def get_habit(db: Session, habit_id: int):
    """Vrátí jeden konkrétní návyk podle jeho ID."""
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()

def get_habits_by_user(db: Session, user_id: int):
    
    return db.query(models.Habit).filter(models.Habit.owner_id == user_id).all()

def create_user_habit(db: Session, habit: schemas.HabitCreate, user_id: int):
    """Vytvoří nový návyk pro konkrétního uživatele."""
    # Vytvoříme SQLAlchemy model z Pydantic schématu.
    # **habit.dict() rozbalí Pydantic data na klíč-hodnota argumenty
    db_habit = models.Habit(**habit.dict(), owner_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit) # Obnoví objekt, aby obsahoval data z DB (např. nové ID)
    return db_habit

def get_user(db: Session, user_id: int):
    """Vrátí jednoho uživatele podle ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Vrátí seznam všech uživatelů."""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Vytvoří nového uživatele."""
    # TODO: Zde bude v budoucnu hashování hesla!
    db_user = models.User(name=user.name) # Pro zjednodušený model
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_goal(db: Session, goal_id: int):
    """Vrátí jeden konkrétní goal podle jeho ID."""
    return db.query(models.Goal).filter(models.Goal.id == goal_id).first()

def get_goals_by_user(db: Session, user_id: int):
    
    return db.query(models.Goal).filter(models.Goal.owner_id == user_id).all()

def create_user_goal(db: Session, goal: schemas.GoalCreate, user_id: int):
    """Vytvoří nový Goal pro konkrétního uživatele."""
    # Vytvoříme SQLAlchemy model z Pydantic schématu.
    # **habit.dict() rozbalí Pydantic data na klíč-hodnota argumenty
    db_goal = models.Goal(**goal.dict(), owner_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal) # Obnoví objekt, aby obsahoval data z DB (např. nové ID)
    return db_goal