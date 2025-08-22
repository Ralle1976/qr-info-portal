from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from datetime import datetime, date
from app.services import StatusService, ScheduleService, I18nService
from app.models import Announcement
from app.database import engine
from sqlmodel import Session, select
import yaml

public_bp = Blueprint('public', __name__)

@public_bp.route('/healthz')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'qr-info-portal'
    }), 200

@public_bp.route('/')
def home():
    """Home page with today's status and hours"""
    # Get current status
    status = StatusService.get_current_status()
    
    # Get today's hours
    today = datetime.now(ScheduleService.TIMEZONE).date()
    today_hours = ScheduleService.get_hours_for_date(today)
    
    # Get current language
    lang = I18nService.get_current_language()
    
    # Get announcements for current language
    with Session(engine) as session:
        announcements = session.exec(
            select(Announcement).where(
                Announcement.lang == lang,
                Announcement.active == True
            ).order_by(Announcement.created_at.desc())
        ).all()
    
    # Check if currently open
    is_open = ScheduleService.is_open_now()
    next_open = ScheduleService.get_next_open_time() if not is_open else None
    
    # Load config for contact info
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return render_template('home.html',
        status=status,
        today_hours=today_hours,
        announcements=announcements,
        is_open=is_open,
        next_open=next_open,
        config=config,
        today=today
    )

@public_bp.route('/week')
def week_view():
    """Week view of opening hours"""
    # Get week parameter
    week_offset = request.args.get('offset', 0, type=int)
    start_date = datetime.now(ScheduleService.TIMEZONE).date()
    
    # Apply offset (weeks)
    from datetime import timedelta
    if week_offset != 0:
        start_date += timedelta(weeks=week_offset)
    
    # Get week schedule
    week_schedule = ScheduleService.get_week_schedule(start_date)
    
    # Get status
    status = StatusService.get_current_status()
    
    return render_template('week.html',
        week_schedule=week_schedule,
        week_offset=week_offset,
        status=status,
        today=datetime.now(ScheduleService.TIMEZONE).date()
    )

@public_bp.route('/month')
def month_view():
    """Month view of opening hours"""
    # Get month/year parameters
    now = datetime.now(ScheduleService.TIMEZONE)
    year = request.args.get('year', now.year, type=int)
    month = request.args.get('month', now.month, type=int)
    
    # Get month schedule
    month_schedule = ScheduleService.get_month_schedule(year, month)
    
    # Get status
    status = StatusService.get_current_status()
    
    # Calculate prev/next month
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    return render_template('month.html',
        month_schedule=month_schedule,
        year=year,
        month=month,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        status=status,
        today=datetime.now(ScheduleService.TIMEZONE).date()
    )

@public_bp.route('/set-language/<language>')
def set_language(language):
    """Set user language preference"""
    I18nService.set_language(language)
    # Redirect to referrer or home
    return redirect(request.referrer or url_for('public.home'))