import sqlite3
from datetime import datetime
from typing import List, Optional

from act.facades.Constant.Constant import ROOT_PATH


class LogModel:
    def __init__(self):
        """初始化数据库连接"""
        self.db_path = ROOT_PATH.joinpath("runtime/act.db")
        self._create_table()

    def _create_table(self):
        """创建log表（如果不存在）"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS logs
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            level TEXT NOT NULL,
                            info TEXT NOT NULL,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                           )
                           ''')
            conn.commit()

    def add_log(self, level: str, info: str, created_at: Optional[datetime] = None) -> int:
        """添加日志记录
        Args:
            level: 日志级别
            info: 日志信息
            created_at: 创建时间，默认为当前时间
        Returns:
            插入记录的ID
        """
        if created_at is None:
            created_at = datetime.now()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO logs (level, info, created_at)
                           VALUES (?, ?, ?)
                           ''', (level, info, created_at.isoformat()))
            conn.commit()
            return cursor.lastrowid

    def get_log_by_id(self, log_id: int) -> Optional[dict]:
        """根据ID获取日志记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id, level, info, created_at
                           FROM logs
                           WHERE id = ?
                           ''', (log_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_logs(self, limit: Optional[int] = None) -> List[dict]:
        """获取所有日志记录
        Args:
            limit: 限制返回的记录数
        Returns:
            日志记录列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = 'SELECT id, level, info, created_at FROM logs ORDER BY created_at DESC'
            if limit is not None:
                query += f' LIMIT {limit}'
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def update_log(self, log_id: int, level: Optional[str] = None, info: Optional[str] = None) -> bool:
        """更新日志记录
        Args:
            log_id: 要更新的日志ID
            level: 新的日志级别（可选）
            info: 新的日志信息（可选）
        Returns:
            是否成功更新
        """
        updates = []
        params = []

        if level is not None:
            updates.append("level = ?")
            params.append(level)
        if info is not None:
            updates.append("info = ?")
            params.append(info)

        if not updates:
            return False

        params.append(log_id)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE logs 
                SET {', '.join(updates)}
                WHERE id = ?
            ''', params)
            conn.commit()
            return cursor.rowcount > 0
    def getLastestLogs(self, offset: int = 0,limit: int = 10):
        """
        获取最新的记录
        :return:
        """
        params = []
        params.append(offset)
        params.append(limit)
        query = '''SELECT * FROM logs WHERE id > ? ORDER BY id DESC LIMIT ? '''
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query,params)
            return [dict(row) for row in cursor.fetchall()]

        return LogsModel.get_all_logs(1)

    def delete_log(self, log_id: int) -> bool:
        """删除日志记录
        Args:
            log_id: 要删除的日志ID
        Returns:
            是否成功删除
        """

LogsModel = LogModel()

if __name__ == '__main__':
    LogsModel.add_log('info', '测试日志')
    print(LogsModel.get_log_by_id(1))
    LogsModel.getLastestLogs(0,10)