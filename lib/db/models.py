from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    annual = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(512), nullable=False)
    # Relationships
    reminders = relationship("Reminder", back_populates="user")
    todos = relationship("Todo", back_populates="user")
    smtp_settings = relationship("SmtpShipping", back_populates="user")
    whatsapp_settings = relationship("WhatsappSettings", back_populates="user")
    calendars = relationship("Calendar", back_populates="user")


class Reminder(Base):
    __tablename__ = "reminders"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    reminder_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    reminder_datetime = Column(DateTime, nullable=False)
    priority = Column(String(20), nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reminders")
    logs = relationship("ReminderLog", back_populates="reminder")
    deliveries = relationship("ReminderForDelivery", back_populates="reminder")
    calendar_events = relationship("CalendarEvent", back_populates="related_reminder")


class ReminderLog(Base):
    __tablename__ = "reminder_logs"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id_log_id = Column(Integer, primary_key=True, index=True)
    reminder_id = Column(Integer, ForeignKey("reminders.reminder_id"), nullable=False)
    original_text = Column(Text, nullable=True)
    ai_generated_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    reminder = relationship("Reminder", back_populates="logs")


class DeliveryChannel(Base):
    __tablename__ = "delivery_channels"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    channel_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    deliveries = relationship("ReminderForDelivery", back_populates="channel")


class ReminderForDelivery(Base):
    __tablename__ = "reminder_deliveries"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    delivery_id = Column(Integer, primary_key=True, index=True)
    reminder_id = Column(Integer, ForeignKey("reminders.reminder_id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("delivery_channels.channel_id"), nullable=False)
    delivery_status = Column(String(50), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    
    # Relationships
    reminder = relationship("Reminder", back_populates="deliveries")
    channel = relationship("DeliveryChannel", back_populates="deliveries")


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    todo_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="todos")


class SmtpShipping(Base):
    __tablename__ = "smtp_settings"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    smtp_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    smtp_server = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="smtp_settings")


class WhatsappSettings(Base):
    __tablename__ = "whatsapp_settings"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    wa_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    api_key = Column(String(500), nullable=False)
    phone_number_id = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="whatsapp_settings")


class Calendar(Base):
    __tablename__ = "calendars"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    calendar_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    calendar_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="calendars")
    events = relationship("CalendarEvent", back_populates="calendar")


class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    event_id = Column(Integer, primary_key=True, index=True)
    calendar_id = Column(Integer, ForeignKey("calendars.calendar_id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    related_reminder_id = Column(Integer, ForeignKey("reminders.reminder_id"), nullable=True)
    
    # Relationships
    calendar = relationship("Calendar", back_populates="events")
    related_reminder = relationship("Reminder", back_populates="calendar_events")