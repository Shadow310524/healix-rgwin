from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any
import datetime

from app.api import deps
from app import models

router = APIRouter()

@router.get("/dashboard-stats")
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Fetch lightweight application-level monitoring metrics for the Admin Dashboard.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # 1. System Status
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False
        
    from app.core.config import settings
    gemini_ok = bool(settings.GEMINI_API_KEY)
    cloudinary_ok = bool(settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY)
    
    # 2. Today's Statistics
    logins_today = db.execute(
        text("SELECT COUNT(*) FROM audit_logs WHERE action = 'Login' AND result = 'Success' AND timestamp >= CURRENT_DATE")
    ).scalar() or 0
    
    ai_requests_today = db.execute(
        text("SELECT COUNT(*) FROM ai_queries WHERE timestamp >= CURRENT_DATE")
    ).scalar() or 0
    
    product_views_total = db.execute(
        text("SELECT COALESCE(SUM(views), 0) FROM products")
    ).scalar() or 0
    
    uploads_today = db.execute(
        text("SELECT COUNT(*) FROM audit_logs WHERE action = 'File Uploaded' AND result = 'Success' AND timestamp >= CURRENT_DATE")
    ).scalar() or 0
    
    failed_requests_today = db.execute(
        text("SELECT COUNT(*) FROM audit_logs WHERE result = 'Failure' AND timestamp >= CURRENT_DATE")
    ).scalar() or 0
    
    # 3. AI Monitoring
    failed_ai_today = db.execute(
        text("SELECT COUNT(*) FROM ai_queries WHERE success = FALSE AND timestamp >= CURRENT_DATE")
    ).scalar() or 0
    
    avg_ai_response_time = db.execute(
        text("SELECT COALESCE(AVG(duration_ms), 0) FROM ai_queries WHERE timestamp >= CURRENT_DATE")
    ).scalar() or 0
    
    # 4. Database Monitoring
    active_connections = db.execute(
        text("SELECT COUNT(*) FROM pg_stat_activity")
    ).scalar() or 0
    
    # 5. Recent Activity (latest 20 events)
    recent_activities = db.execute(
        text("SELECT timestamp, user_email, action, resource, result FROM audit_logs ORDER BY timestamp DESC LIMIT 20")
    ).fetchall()
    
    activity_list = [
        {
            "timestamp": row[0].isoformat() if row[0] else "",
            "user": row[1] or "System",
            "action": row[2],
            "resource": row[3],
            "result": row[4]
        }
        for row in recent_activities
    ]
    
    # 6. Error Dashboard (last 20 errors)
    recent_errors = db.execute(
        text("""
            SELECT timestamp, resource, user_email, action 
            FROM audit_logs 
            WHERE result = 'Failure' 
            ORDER BY timestamp DESC 
            LIMIT 20
        """)
    ).fetchall()
    
    error_list = [
        {
            "timestamp": row[0].isoformat() if row[0] else "",
            "endpoint": row[1],
            "user": row[2] or "System",
            "error_type": row[3]
        }
        for row in recent_errors
    ]
    
    return {
        "system_status": {
            "api": "online",
            "database": "connected" if db_ok else "offline",
            "gemini": "configured" if gemini_ok else "offline",
            "cloudinary": "configured" if cloudinary_ok else "offline",
        },
        "statistics": {
            "logins": logins_today,
            "ai_requests": ai_requests_today,
            "product_views": product_views_total,
            "uploads": uploads_today,
            "failed_requests": failed_requests_today
        },
        "ai_monitoring": {
            "requests_today": ai_requests_today,
            "failed_calls": failed_ai_today,
            "avg_response_ms": round(float(avg_ai_response_time), 1)
        },
        "database_monitoring": {
            "active_connections": active_connections
        },
        "recent_activity": activity_list,
        "error_dashboard": error_list
    }

@router.get("/analytics-stats")
def get_analytics_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve product view rankings and AI question frequency for administrative review.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # 1. Most Viewed Products
    most_viewed_products = db.execute(
        text("SELECT id, name, views FROM products ORDER BY views DESC LIMIT 5")
    ).fetchall()
    
    product_views = [
        {"id": row[0], "name": row[1], "views": row[2]}
        for row in most_viewed_products
    ]
    
    # 2. Most Viewed Categories
    most_viewed_categories = db.execute(
        text("""
            SELECT c.name, COALESCE(SUM(p.views), 0) as total_views 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.is_deleted = FALSE
            GROUP BY c.name 
            ORDER BY total_views DESC 
            LIMIT 5
        """)
    ).fetchall()
    
    category_views = [
        {"name": row[0], "views": int(row[1])}
        for row in most_viewed_categories
    ]
    
    # 3. Most Asked AI Questions
    most_asked_questions = db.execute(
        text("""
            SELECT query, COUNT(*) as count 
            FROM ai_queries 
            GROUP BY query 
            ORDER BY count DESC 
            LIMIT 5
        """)
    ).fetchall()
    
    ai_questions = [
        {"query": row[0], "count": row[1]}
        for row in most_asked_questions
    ]
    
    # 4. Overall Totals
    total_logins = db.execute(
        text("SELECT COUNT(*) FROM audit_logs WHERE action = 'Login' AND result = 'Success'")
    ).scalar() or 0
    
    total_ai_usage = db.execute(
        text("SELECT COUNT(*) FROM ai_queries")
    ).scalar() or 0
    
    total_uploads = db.execute(
        text("SELECT COUNT(*) FROM audit_logs WHERE action = 'File Uploaded' AND result = 'Success'")
    ).scalar() or 0
    
    return {
        "product_views": product_views,
        "category_views": category_views,
        "ai_questions": ai_questions,
        "counts": {
            "logins": total_logins,
            "ai_usage": total_ai_usage,
            "uploads": total_uploads
        }
    }
