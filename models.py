from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base je základní třída, ze které budou dědit všechny naše modely.
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    points = Column(Integer, default=0)
    habits = relationship("Habit", back_populates="owner")
    plans = relationship("Plan", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")
    journal_entries = relationship("JournalEntry", back_populates="owner")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    description = Column(Text, nullable=True)
    title = Column(String, index=True)
    time_category = Column(String, index=True)
    content_category = Column(String, index=True)
    repeat_frequency = Column(String, index=True)
    is_quantifiable = Column(Boolean, default=False)
    is_ban = Column(Boolean, default=False)
    unit = Column(String, nullable=True)

    
    goals = relationship("Goal", secondary="goal_habits", back_populates="habits")
    # Vztah k vlastníkovi (User)
    owner = relationship("User", back_populates="habits")

    # Vztah k záznamům o splnění
    completions = relationship("HabitCompletion", back_populates="habit")


class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, nullable=False)
    status = Column(String) # "completed", "skipped", "missed"
    value = Column(Float, nullable=True) # Pro kvantifikovatelné návyky
    notes = Column(Text, nullable=True)
    
    habit = relationship("Habit", back_populates="completions")

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, nullable=False)
    content = Column(Text, nullable=True)
    mood = Column(String, nullable=True)

    owner = relationship("User", back_populates="journal_entries")

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    period_type = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    owner = relationship("User", back_populates="plans") # PŘIDÁNO: Vztah k uživateli
    goals = relationship("Goal", back_populates="plan")  # PŘIDÁNO: Vztah k cílům

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, index=True)
    motivation_text = Column(Text, nullable=True)

    plan = relationship("Plan", back_populates="goals")
    owner = relationship("User", back_populates="goals")
    habits = relationship("Habit", secondary="goal_habits", back_populates="goals")

    

class GoalHabit(Base):
    __tablename__ = "goal_habits"
    goal_id = Column(Integer, ForeignKey("goals.id"), primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), primary_key=True)


