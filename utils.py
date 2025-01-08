import sqlite3

def get_leaderboard_for_category(category_id):
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT u.username, l.score FROM leaderboard l
                      JOIN users u ON l.user_id = u.id
                      WHERE l.category_id = ? ORDER BY l.score DESC''', (category_id,))
    leaderboard = cursor.fetchall()
    conn.close()
    return leaderboard

def get_user_profile(user_id):
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT u.username, c.name, us.score FROM user_scores us
                      JOIN categories c ON us.category_id = c.id
                      JOIN users u ON us.user_id = u.id
                      WHERE us.user_id = ?''', (user_id,))
    profile = cursor.fetchall()
    conn.close()
    return profile
