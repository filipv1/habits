from pydantic import BaseModel
from typing import Optional
from datetime import date

# Základní schéma s atributy, které jsou společné
class HabitBaseModel(BaseModel):
    title: str
    description: Optional[str] = None
    time_category: str
    content_category: str
    is_quantifiable: bool
    is_ban: bool
    repeat_frequency: str
    unit: Optional[str] = None


# Schéma pro vytvoření návyku (co přijmeme od uživatele)
class HabitCreate(HabitBaseModel):
    pass # Dědí vše z HabitBaseModel

# Schéma pro čtení návyku (co pošleme uživateli zpět)
class Habit(HabitBaseModel):
    id: int
    owner_id: int
    

    class Config:
        orm_mode = True # Umožní Pydanticu načíst data z ORM modelu

class UserBaseModel(BaseModel):
    name: str

class UserCreate(UserBaseModel):
    pass

class User(UserBaseModel):
    id: int
    points: int
    class Config:
        orm_mode = True

class HabitCompletionBaseModel(BaseModel):
    date: date
    status: str
    value: Optional[float] = None
    notes: Optional[str] = None

class HabitCompletionCreate(HabitCompletionBaseModel):
    pass

class HabitCompletion(HabitCompletionBaseModel):
    id: int
    habit_id: int
    class Config:
        orm_mode = True

class JournalEntryBaseModel(BaseModel):
    date: date
    content: str
    mood: Optional[str] = None

class JournalEntryCreate(JournalEntryBaseModel):
    pass

class JournalEntry(JournalEntryBaseModel):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class PlanBaseModel(BaseModel):
    title: str
    period_type: str
    description: Optional[str] = None
    start_date: date
    end_date: date

class PlanCreate(PlanBaseModel):
    pass

class Plan(PlanBaseModel):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class GoalBaseModel(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    status: str
    motivation_text: Optional[str] = None

class GoalCreate(GoalBaseModel):
    pass

class Goal(GoalBaseModel):
    id:int
    owner_id: int
    plan_id: Optional[int] = None
    class Config:
        orm_mode = True
