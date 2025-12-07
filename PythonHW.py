import json
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional


class EventType(Enum):
    MEETING = "Встреча"
    PHONE_CALL = "Телефонный звонок"
    BIRTHDAY = "День рождения"
    TASK = "Задание"
    REMINDER = "Напоминание"
    OTHER = "Другое"


class Event:
    def __init__(self, title: str, event_type: EventType, date: datetime, 
                 duration_minutes: int, description: str = ""):
        self.title = title
        self.event_type = event_type
        self.date = date
        self.duration_minutes = max(15, duration_minutes)  
        self.description = description
    
    def to_dict(self) -> Dict:
        """Преобразование события в словарь для сохранения в JSON"""
        return {
            "title": self.title,
            "type": self.event_type.value,
            "date": self.date.strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": self.duration_minutes,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Event':
        """Создание события из словаря"""
        event_type = EventType(data["type"])
        date = datetime.strptime(data["date"], "%Y-%m-%d %H:%M")
        return cls(
            title=data["title"],
            event_type=event_type,
            date=date,
            duration_minutes=data["duration_minutes"],
            description=data.get("description", "")
        )
    
    def __str__(self) -> str:
        end_time = self.date + timedelta(minutes=self.duration_minutes)
        return (f"{self.event_type.value}: {self.title}\n"
                f"  Дата: {self.date.strftime('%d.%m.%Y %H:%M')} - "
                f"{end_time.strftime('%H:%M')} ({self.duration_minutes} мин.)\n"
                f"  Описание: {self.description}")


class Organizer:
    def __init__(self, filename: str = "events.json"):
        self.filename = filename
        self.events: List[Event] = []
        self.load_events()
    
    def load_events(self) -> None:
        """Загрузка событий из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = [Event.from_dict(event_data) for event_data in data]
                print(f"Загружено {len(self.events)} событий")
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")
                self.events = []
        else:
            print("Файл с событиями не найден, создан новый список")
    
    def save_events(self) -> None:
        """Сохранение событий в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([event.to_dict() for event in self.events], 
                         f, ensure_ascii=False, indent=2)
            print("События сохранены")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def add_event(self, event: Event) -> None:
        """Добавление нового события"""
        self.events.append(event)
        self.events.sort(key=lambda x: x.date)
        self.save_events()
        print("Событие добавлено!")
    
    def view_events(self, filter_date: Optional[datetime] = None, 
                   filter_type: Optional[EventType] = None) -> None:
        """Просмотр событий с возможностью фильтрации"""
        if not self.events:
            print("Нет запланированных событий")
            return
        
        filtered_events = self.events
        
        if filter_date:
            filtered_events = [
                e for e in filtered_events 
                if e.date.date() == filter_date.date()
            ]
        
        if filter_type:
            filtered_events = [
                e for e in filtered_events 
                if e.event_type == filter_type
            ]
        
        if not filtered_events:
            if filter_date or filter_type:
                print("Событий по заданным критериям не найдено")
            else:
                print("Нет запланированных событий")
            return
        
        print(f"\nНайдено {len(filtered_events)} событий:")
        for i, event in enumerate(filtered_events, 1):
            print(f"\n{i}. {event}")
    
    def edit_event(self, index: int, **kwargs) -> bool:
        """Редактирование события по индексу"""
        if 0 <= index < len(self.events):
            event = self.events[index]
            
            if 'title' in kwargs:
                event.title = kwargs['title']
            if 'event_type' in kwargs:
                event.event_type = kwargs['event_type']
            if 'date' in kwargs:
                event.date = kwargs['date']
            if 'duration_minutes' in kwargs:
                event.duration_minutes = max(15, kwargs['duration_minutes'])
            if 'description' in kwargs:
                event.description = kwargs['description']
            
            self.events.sort(key=lambda x: x.date)
            self.save_events()
            print("Событие отредактировано!")
            return True
        else:
            print("Неверный индекс события")
            return False
    
    def delete_event(self, index: int) -> bool:
        """Удаление события по индексу"""
        if 0 <= index < len(self.events):
            event = self.events.pop(index)
            self.save_events()
            print(f"Событие '{event.title}' удалено!")
            return True
        else:
            print("Неверный индекс события")
            return False
    
    def get_upcoming_events(self, days: int = 7) -> List[Event]:
        """Получение событий на ближайшие дни"""
        now = datetime.now()
        future_date = now + timedelta(days=days)
        
        upcoming = [
            e for e in self.events 
            if now <= e.date <= future_date
        ]
        
        return upcoming


def print_menu():
    """Вывод меню"""
    print("\n" + "="*50)
    print("ОРГАНАЙЗЕР СОБЫТИЙ")
    print("="*50)
    print("1. Просмотреть все события")
    print("2. Просмотреть события на определенную дату")
    print("3. Просмотреть события определенного типа")
    print("4. Добавить новое событие")
    print("5. Редактировать событие")
    print("6. Удалить событие")
    print("7. Просмотреть ближайшие события (на неделю)")
    print("8. Выйти")
    print("="*50)


def get_event_type_from_user() -> EventType:
    """Выбор типа события пользователем"""
    print("\nВыберите тип события:")
    for i, event_type in enumerate(EventType, 1):
        print(f"{i}. {event_type.value}")
    
    while True:
        try:
            choice = int(input("Введите номер типа: "))
            if 1 <= choice <= len(EventType):
                return list(EventType)[choice - 1]
            else:
                print("Неверный номер типа")
        except ValueError:
            print("Пожалуйста, введите число")


def get_date_from_user(prompt: str) -> datetime:
    """Получение даты от пользователя"""
    while True:
        try:
            date_str = input(prompt + " (формат: ДД.ММ.ГГГГ ЧЧ:ММ): ")
            return datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        except ValueError:
            print("Неверный формат даты. Используйте формат ДД.ММ.ГГГГ ЧЧ:ММ")


def get_duration_from_user() -> int:
    """Получение продолжительности от пользователя"""
    while True:
        try:
            duration = int(input("Продолжительность (минут, минимум 15): "))
            if duration >= 15:
                return duration
            else:
                print("Продолжительность должна быть не менее 15 минут")
        except ValueError:
            print("Пожалуйста, введите число")


def main():
    organizer = Organizer()
    
    while True:
        print_menu()
        
        try:
            choice = int(input("\nВыберите действие: "))
            
            if choice == 1:
                organizer.view_events()
            
            elif choice == 2:
                date = get_date_from_user("Введите дату")
                organizer.view_events(filter_date=date)
            
            elif choice == 3:
                event_type = get_event_type_from_user()
                organizer.view_events(filter_type=event_type)
            
            elif choice == 4:
                print("\nДОБАВЛЕНИЕ НОВОГО СОБЫТИЯ")
                title = input("Название события: ").strip()
                if not title:
                    print("Название не может быть пустым")
                    continue
                
                event_type = get_event_type_from_user()
                date = get_date_from_user("Дата и время начала")
                duration = get_duration_from_user()
                description = input("Описание (необязательно): ").strip()
                
                event = Event(title, event_type, date, duration, description)
                organizer.add_event(event)
            
            elif choice == 5:
                if not organizer.events:
                    print("Нет событий для редактирования")
                    continue
                
                organizer.view_events()
                try:
                    index = int(input("\nВведите номер события для редактирования: ")) - 1
                    
                    print("\nЧто вы хотите изменить?")
                    print("1. Название")
                    print("2. Тип")
                    print("3. Дату и время")
                    print("4. Продолжительность")
                    print("5. Описание")
                    print("6. Все поля")
                    
                    edit_choice = int(input("Выберите: "))
                    
                    if edit_choice == 1:
                        new_title = input("Новое название: ").strip()
                        organizer.edit_event(index, title=new_title)
                    elif edit_choice == 2:
                        new_type = get_event_type_from_user()
                        organizer.edit_event(index, event_type=new_type)
                    elif edit_choice == 3:
                        new_date = get_date_from_user("Новая дата и время")
                        organizer.edit_event(index, date=new_date)
                    elif edit_choice == 4:
                        new_duration = get_duration_from_user()
                        organizer.edit_event(index, duration_minutes=new_duration)
                    elif edit_choice == 5:
                        new_description = input("Новое описание: ").strip()
                        organizer.edit_event(index, description=new_description)
                    elif edit_choice == 6:
                        new_title = input("Новое название: ").strip()
                        new_type = get_event_type_from_user()
                        new_date = get_date_from_user("Новая дата и время")
                        new_duration = get_duration_from_user()
                        new_description = input("Новое описание: ").strip()
                        
                        organizer.edit_event(
                            index,
                            title=new_title,
                            event_type=new_type,
                            date=new_date,
                            duration_minutes=new_duration,
                            description=new_description
                        )
                    else:
                        print("Неверный выбор")
                
                except (ValueError, IndexError):
                    print("Неверный номер события")
            
            elif choice == 6:
                if not organizer.events:
                    print("Нет событий для удаления")
                    continue
                
                organizer.view_events()
                try:
                    index = int(input("\nВведите номер события для удаления: ")) - 1
                    organizer.delete_event(index)
                except (ValueError, IndexError):
                    print("Неверный номер события")
            
            elif choice == 7:
                upcoming = organizer.get_upcoming_events(7)
                if upcoming:
                    print(f"\nБлижайшие события на неделю:")
                    for event in upcoming:
                        print(f"\n{event}")
                else:
                    print("На ближайшую неделю событий нет")
            
            elif choice == 8:
                print("Сохранение данных...")
                organizer.save_events()
                print("До свидания!")
                break
            
            else:
                print("Неверный выбор. Попробуйте снова.")
        
        except ValueError:
            print("Пожалуйста, введите число")
        except KeyboardInterrupt:
            print("\n\nСохранение данных...")
            organizer.save_events()
            print("До свидания!")
            break


if __name__ == "__main__":
    main()