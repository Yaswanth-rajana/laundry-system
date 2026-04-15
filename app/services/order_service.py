from datetime import datetime, timedelta
import json
from app.schemas.order import OrderCreate, StatusUpdate
from app.storage.db import get_db

PRICES = {
    'Shirt': 100,
    'Pants': 120,
    'Saree': 150
}

def calculate_total(garments):
    return sum(PRICES[g.type] * g.quantity for g in garments)

def generate_order_id(conn):
    c = conn.cursor()
    c.execute("SELECT seq FROM sequence WHERE name = 'order_id'")
    seq = c.fetchone()['seq']
    c.execute("UPDATE sequence SET seq = seq + 1 WHERE name = 'order_id'")
    return f"ORD-{seq:03d}"

def format_order_row(row):
    return {
        "order_id": row['id'],
        "customer_name": row['customer_name'],
        "phone": row['phone'],
        "garments": json.loads(row['garments_json']),
        "total_amount": row['total'],
        "status": row['status'],
        "status_history": json.loads(row['status_history']),
        "estimated_delivery_date": row['estimated_delivery_date'],
        "last_updated": row['last_updated'],
        "notes": row['notes'],
        "created_at": row['created_at']
    }

def get_order_by_id(order_id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return format_order_row(row)

def create_order_service(order: OrderCreate):
    total_amount = calculate_total(order.garments)
    now = datetime.now().isoformat()
    estimated_delivery = (datetime.now() + timedelta(days=3)).date().isoformat()
    
    conn = get_db()
    order_id = generate_order_id(conn)
    
    garments_json = json.dumps([g.model_dump() for g in order.garments])
    status_history = [{"status": "RECEIVED", "timestamp": now, "changed_by": "system"}]
    status_history_json = json.dumps(status_history)
    
    c = conn.cursor()
    c.execute('''
        INSERT INTO orders (
            id, customer_name, phone, garments_json, total, status, 
            created_at, notes, status_history, estimated_delivery_date, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_id, order.customer_name, order.phone, garments_json, total_amount, "RECEIVED",
        now, order.notes, status_history_json, estimated_delivery, now
    ))
    conn.commit()
    conn.close()
    
    return get_order_by_id(order_id)

def list_orders_service(status: str = None, search: str = None):
    conn = get_db()
    c = conn.cursor()
    
    query = "SELECT * FROM orders WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status.upper())
        
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    
    result = [format_order_row(row) for row in rows]
    
    if search:
        search_lower = search.lower()
        result = [
            o for o in result 
            if search_lower in o['customer_name'].lower() 
            or search_lower in o['phone']
        ]
        
    return {
        "total": len(result),
        "orders": result
    }

def update_status_service(order_id: str, update: StatusUpdate):
    order = get_order_by_id(order_id)
    if not order:
        return None
        
    current_status = order['status']
    new_status = update.status
    
    # We allow any state transition basically
    if current_status != new_status:
        now = datetime.now().isoformat()
        history = order['status_history']
        history.append({
            "status": new_status,
            "timestamp": now,
            "changed_by": "staff"
        })
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE orders 
            SET status = ?, status_history = ?, last_updated = ?
            WHERE id = ?
        ''', (new_status, json.dumps(history), now, order_id))
        conn.commit()
        conn.close()
        
    return get_order_by_id(order_id)

def get_dashboard_service():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    rows = c.fetchall()
    conn.close()
    
    orders = [format_order_row(row) for row in rows]
    total_orders = len(orders)
    
    total_revenue = sum(o['total_amount'] for o in orders if o['status'] == 'DELIVERED')
    
    status_breakdown = {
        "RECEIVED": 0,
        "PROCESSING": 0,
        "READY": 0,
        "DELIVERED": 0
    }
    
    all_amounts = []
    garment_counts = {'Shirt': 0, 'Pants': 0, 'Saree': 0}
    
    for o in orders:
        status_breakdown[o['status']] += 1
        all_amounts.append(o['total_amount'])
        for g in o['garments']:
            garment_counts[g['type']] += g['quantity']
            
    avg_order_value = sum(all_amounts) / len(all_amounts) if all_amounts else 0
    most_common_garment = max(garment_counts, key=garment_counts.get) if any(garment_counts.values()) else "None"
    
    today = datetime.now().date()
    pending_today = sum(1 for o in orders 
                       if o['status'] != 'DELIVERED' 
                       and datetime.fromisoformat(o['created_at']).date() == today)
                       
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "average_order_value": round(avg_order_value, 2),
        "most_common_garment": most_common_garment,
        "status_breakdown": status_breakdown,
        "pending_today": pending_today
    }

def get_order_history_service(order_id: str):
    order = get_order_by_id(order_id)
    if not order:
        return None
    return {
        "order_id": order_id,
        "customer_name": order['customer_name'],
        "status_history": order['status_history']
    }
