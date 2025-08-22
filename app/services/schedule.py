from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from sqlmodel import Session, select
from app.models import StandardHours, HourException, Availability
from app.database import engine
import pytz


class ScheduleService:
    TIMEZONE = pytz.timezone('Asia/Bangkok')
    
    @staticmethod
    def get_hours_for_date(target_date: date) -> Dict:
        """Get opening hours for a specific date"""
        with Session(engine) as session:
            # Check for exceptions first
            exception = session.exec(
                select(HourException).where(HourException.exception_date == target_date)
            ).first()
            
            if exception:
                return {
                    'date': target_date,
                    'closed': exception.closed,
                    'time_ranges': exception.time_ranges,
                    'note': exception.note,
                    'is_exception': True
                }
            
            # Get standard hours for this day
            day_of_week = target_date.weekday()
            standard = session.exec(
                select(StandardHours).where(StandardHours.day_of_week == day_of_week)
            ).first()
            
            if standard:
                return {
                    'date': target_date,
                    'closed': len(standard.time_ranges) == 0,
                    'time_ranges': standard.time_ranges,
                    'note': None,
                    'is_exception': False
                }
            
            return {
                'date': target_date,
                'closed': True,
                'time_ranges': [],
                'note': None,
                'is_exception': False
            }
    
    @staticmethod
    def get_week_schedule(start_date: Optional[date] = None) -> List[Dict]:
        """Get schedule for a week starting from given date"""
        if not start_date:
            start_date = datetime.now(ScheduleService.TIMEZONE).date()
        
        # Find Monday of the week
        days_since_monday = start_date.weekday()
        week_start = start_date - timedelta(days=days_since_monday)
        
        schedule = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            schedule.append(ScheduleService.get_hours_for_date(day))
        
        return schedule
    
    @staticmethod
    def get_month_schedule(year: int, month: int) -> List[Dict]:
        """Get schedule for entire month"""
        first_day = date(year, month, 1)
        
        # Calculate last day of month
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        schedule = []
        current = first_day
        while current <= last_day:
            schedule.append(ScheduleService.get_hours_for_date(current))
            current += timedelta(days=1)
        
        return schedule
    
    @staticmethod
    def get_availability_for_date(target_date: date) -> Optional[Availability]:
        """Get availability slots for a specific date"""
        with Session(engine) as session:
            return session.exec(
                select(Availability).where(Availability.availability_date == target_date)
            ).first()
    
    @staticmethod
    def is_open_now() -> bool:
        """Check if currently open"""
        now = datetime.now(ScheduleService.TIMEZONE)
        today_hours = ScheduleService.get_hours_for_date(now.date())
        
        if today_hours['closed']:
            return False
        
        current_time = now.strftime('%H:%M')
        for time_range in today_hours['time_ranges']:
            start, end = time_range.split('-')
            if start <= current_time <= end:
                return True
        
        return False
    
    @staticmethod
    def get_next_open_time() -> Optional[Dict]:
        """Get next opening time"""
        now = datetime.now(ScheduleService.TIMEZONE)
        current_date = now.date()
        
        # Check up to 14 days ahead
        for i in range(14):
            check_date = current_date + timedelta(days=i)
            hours = ScheduleService.get_hours_for_date(check_date)
            
            if not hours['closed'] and hours['time_ranges']:
                # If today, check if any time range is still ahead
                if i == 0:
                    current_time = now.strftime('%H:%M')
                    for time_range in hours['time_ranges']:
                        start, _ = time_range.split('-')
                        if start > current_time:
                            return {
                                'date': check_date,
                                'time': start,
                                'time_range': time_range
                            }
                else:
                    # Future date, return first time range
                    return {
                        'date': check_date,
                        'time': hours['time_ranges'][0].split('-')[0],
                        'time_range': hours['time_ranges'][0]
                    }
        
        return None