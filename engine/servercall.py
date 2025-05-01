import mysql.connector
import threading


ip = "serverip"

# Cache da conexão global
_conexao_global = None
_cursor_global = None
_lock_db = threading.Lock()
_stop_thread = False
_thread = None

def _abrir_conexao():
    global _conexao_global, _cursor_global
    if _conexao_global is None or not _conexao_global.is_connected():
        _conexao_global = mysql.connector.connect(
            host=ip,
            user="adam",
            password="adam",
            database="coordenadas"
        )
        _cursor_global = _conexao_global.cursor()

def _fechar_conexao():
    global _conexao_global, _cursor_global
    if _cursor_global:
        _cursor_global.close()
        _cursor_global = None
    if _conexao_global:
        _conexao_global.close()
        _conexao_global = None

def create_player(x, y, nome):
    with _lock_db:
        _abrir_conexao()
        cursor = _cursor_global
        try:
            cursor.execute("SELECT id FROM pontos WHERE nome = %s", (nome,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("UPDATE pontos SET online = TRUE WHERE nome = %s", (nome,))
                print(f"Jogador '{nome}' já existia. Setado como online.")
            else:
                cursor.execute("INSERT INTO pontos (x, y, nome, online) VALUES (%s, %s, %s, TRUE)", (x, y, nome))
                print(f"Novo jogador '{nome}' inserido e setado como online.")
            _conexao_global.commit()
        except Exception as e:
            print("Erro em create_player:", e)


def multy_move_player(x, y, nome):
    with _lock_db:
        _abrir_conexao()
        cursor = _cursor_global
        try:
            cursor.execute("SELECT id FROM pontos WHERE nome = %s", (nome,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("UPDATE pontos SET x = %s, y = %s WHERE nome = %s", (x, y, nome))
                _conexao_global.commit()
        except Exception as e:
            print("Erro em multy_move_player:", e)

def get_player(nome):
    with _lock_db:
        _abrir_conexao()
        cursor = _cursor_global
        try:
            cursor.execute("SELECT x, y FROM pontos WHERE nome = %s", (nome,))
            player = cursor.fetchone()
            return player if player else (None, None)
        except Exception as e:
            print("Erro em get_player:", e)
            return None, None

def _sync_loop(player_local, jogadores_remotos, nome_local, interval):
    global _stop_thread
    while not _stop_thread:
        try:
            multy_move_player(player_local.x, player_local.y, nome_local)

            for player_obj in jogadores_remotos:
                nome_remoto = getattr(player_obj, "nome", None)
                if nome_remoto:
                    x, y = get_player(nome_remoto)
                    if x is not None and y is not None:
                        player_obj.set_position(x, y)
        except Exception as e:
            print("Erro na sync_loop:", e)
        time.sleep(interval)



def start_sync(player_local, jogadores_remotos, nome_local, interval=0):
    global _thread, _stop_thread
    _stop_thread = False
    _thread = threading.Thread(
        target=_sync_loop,
        args=(player_local, jogadores_remotos, nome_local, interval),
        daemon=True
    )
    _thread.start()

def stop_sync(nome):
    global _stop_thread
    _stop_thread = True

    if nome:
        with _lock_db:
            _abrir_conexao()
            cursor = _cursor_global
            try:
                cursor.execute("UPDATE pontos SET online = FALSE WHERE nome = %s", (nome,))
                _conexao_global.commit()
                print(f"Jogador '{nome}' foi marcado como offline.")
            except Exception as e:
                print("Erro ao setar offline:", e)

def get_online_players():
    with _lock_db:
        _abrir_conexao()
        cursor = _cursor_global
        try:
            cursor.execute("SELECT nome, x, y FROM pontos WHERE online = TRUE")
            jogadores = cursor.fetchall()
            # Retorna como lista de dicionários ou tuplas, você escolhe:
            return [{"nome": nome, "x": x, "y": y} for nome, x, y in jogadores]
        except Exception as e:
            print("Erro em get_online_players:", e)
            return []

