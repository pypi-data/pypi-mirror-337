import psycopg2.extras
from datetime import datetime
from typing import Optional, Dict, List, Any
from .client import db_client

# 创建模型记录
def create_model_record(model_data: Dict[str, Any]) -> bool:
    """创建模型记录"""
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor()
        
        # 数据清理
        cleaned_data = db_client.clean_string_values(model_data)
        
        # 构建SQL插入语句
        fields = []
        values = []
        placeholders = []
        
        for key, value in cleaned_data.items():
            fields.append(key)
            values.append(value)
            placeholders.append('%s')
        
        fields_str = ', '.join(fields)
        placeholders_str = ', '.join(placeholders)
        
        sql = f"""
            INSERT INTO agent_engine.model_record_t ({fields_str})
            VALUES ({placeholders_str})
        """
        
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def update_model_record(model_id: int, update_data: Dict[str, Any]) -> bool:
    """更新模型记录"""
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor()
        
        # 数据清理
        cleaned_data = db_client.clean_string_values(update_data)
        
        # 构建SQL更新语句
        set_clause = []
        values = []
        
        for key, value in cleaned_data.items():
            set_clause.append(f"{key} = %s")
            values.append(value)
        
        # 添加更新时间
        set_clause.append("update_time = %s")
        values.append(datetime.now())
        
        # 添加model_id条件
        values.append(model_id)
        
        set_clause_str = ', '.join(set_clause)
        
        sql = f"""
            UPDATE agent_engine.model_record_t
            SET {set_clause_str}
            WHERE model_id = %s
        """
        
        cursor.execute(sql, values)
        affected_rows = cursor.rowcount
        conn.commit()
        return affected_rows > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def delete_model_record(model_id: int) -> bool:
    """删除模型记录（软删除）并更新更新时间戳"""
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor()
        
        sql = """
            UPDATE agent_engine.model_record_t
            SET delete_flag = 'Y', update_time = CURRENT_TIMESTAMP
            WHERE model_id = %s
        """
        
        cursor.execute(sql, (model_id,))
        affected_rows = cursor.rowcount
        conn.commit()
        return affected_rows > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def get_model_records(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    获取模型记录列表

    Args:
        filters: 过滤条件字典，可选参数

    Returns:
        List[Dict[str, Any]]: 模型记录列表
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # 基础查询
        sql = """
            SELECT * FROM agent_engine.model_record_t
            WHERE delete_flag = 'N'
        """
        
        # 添加过滤条件
        values = []
        if filters:
            where_clauses = []
            for key, value in filters.items():
                if value is None:
                    where_clauses.append(f"{key} IS NULL")
                else:
                    where_clauses.append(f"{key} = %s")
                    values.append(value)
            
            if where_clauses:
                sql += " AND " + " AND ".join(where_clauses)
        
        cursor.execute(sql, values)
        records = cursor.fetchall()
        return [dict(record) for record in records]
    except Exception as e:
        raise e
    finally:
        db_client.close_connection(conn)

def get_model_by_name(model_name: str, model_repo: str) -> Optional[Dict[str, Any]]:
    """
    根据模型名称和仓库获取模型记录

    Args:
        model_name: 模型名称
        model_repo: 模型仓库

    Returns:
        Optional[Dict[str, Any]]: 模型记录
    """
    filters = {
        'model_name': model_name,
        'model_repo': model_repo
    }
    
    records = get_model_records(filters)
    return records[0] if records else None
