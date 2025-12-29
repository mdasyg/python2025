import socket
import threading

import sys
sys.path.append("../database/")
import database_lib as db  # <-- Εισαγωγή της βιβλιοθήκης μας

HOST = '0.0.0.0'
PORT = 50007
DB_FILE = "server_scores.db"

# --- 1. Αρχικοποίηση Βάσης (τρέχει μία φορά στην αρχή) ---
def init_db():
    print("--- Initializing Database ---")
    # Χρησιμοποιούμε τη βιβλιοθήκη μας με verbose=1 για να δούμε ότι συνδέθηκε
    conn = db.create_connection(DB_FILE, verbose=1)
    
    # Query δημιουργίας πίνακα
    sql_create = """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            clicks INTEGER,
            seconds REAL,
            click_rate REAL
        );
    """
    # Εκτέλεση μέσω της βιβλιοθήκης
    db.execute_query(conn, sql_create, verbose=1)
    conn.close() # Κλείνουμε τη σύνδεση αφού τελειώσαμε το setup


# --- 2. Η συνάρτηση που τρέχει ΠΑΡΑΛΛΗΛΑ για κάθε φοιτητή ---
def handle_client(conn_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        # Λήψη δεδομένων
        data = conn_socket.recv(1024).decode('utf-8')
        if not data:
            return

        # Επεξεργασία (Parsing)
        parts = data.split(',')
        username = parts[0]
        clicks = int(parts[1])
        seconds = float(parts[2])

        # Υπολογισμός Click Rate
        click_rate = round(clicks / seconds, 2) if seconds > 0 else 0
        
        print(f"[{addr}] User: {username} | Rate: {click_rate}")

        """
        επειδή χρησιμοποιούμε Threads, έχουμε το πλεονέκτημα ότι μπορούμε να έχουμε κοινές μεταβλητές (όπως τη λίστα active_users). Όμως, με τις Βάσεις Δεδομένων πρέπει να είμαστε προσεκτικοί: Η σύνδεση είναι σαν το στυλό. Παρόλο που καθόμαστε στο ίδιο τραπέζι (κοινή μνήμη), δεν μπορούμε να γράφουμε με το ίδιο στυλό ταυτόχρονα. Ο καθένας πρέπει να πάρει το δικό του στυλό (connection) για να γράψει στο τετράδιο (database file).
        """

        # --- DB INTERACTION ME TH ΒΙΒΛΙΟΘΗΚΗ ---
        # ΠΡΟΣΟΧΗ: Ανοίγουμε ΝΕΑ σύνδεση για κάθε thread (Thread-safety)
        # Βάζουμε verbose=0 για να μην γεμίσει η κονσόλα του server
        thread_db_conn = db.create_connection(DB_FILE, verbose=0)

        # Α. Εγγραφή (INSERT)
        # Χρησιμοποιούμε f-string (σημείωση: σε production θα θέλαμε parameterized queries για ασφάλεια)
        sql_insert = f"""
            INSERT INTO scores (username, clicks, seconds, click_rate) 
            VALUES ('{username}', {clicks}, {seconds}, {click_rate});
        """
        db.execute_query(thread_db_conn, sql_insert, verbose=0)

        # Β. Ανάγνωση Leaderboard (SELECT)
        sql_select = "SELECT username, click_rate FROM scores ORDER BY click_rate DESC LIMIT 5"
        
        # Η βιβλιοθήκη επιστρέφει (column_names, result). Κρατάμε μόνο το result.
        _, leaders = db.execute_read_query(thread_db_conn, sql_select, verbose=0)
        
        thread_db_conn.close() # Κλείνουμε τη σύνδεση της βάσης για αυτό το thread
        # ----------------------------------------

        # Δημιουργία απάντησης για τον Client
        response = "--- TOP 5 FASTEST CLICKERS ---\n"
        for i, row in enumerate(leaders, 1):
            # row[0] είναι το username, row[1] είναι το click_rate
            response += f"{i}. {row[0]}: {row[1]} c/s\n"
        
        response += f"\nYour Rate: {click_rate} c/s"

        conn_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        conn_socket.close() # Κλείνουμε τη σύνδεση δικτύου


# --- 3. Κυρίως Server Loop ---
def start_server():
    init_db() # Φτιάχνουμε τον πίνακα
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        # Δημιουργία νέου νήματος για κάθε σύνδεση
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # Προαιρετικό: Τυπώνουμε πόσοι είναι συνδεδεμένοι ταυτόχρονα (ενεργά threads - 1 το main)
        print(f"[ACTIVE THREADS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()