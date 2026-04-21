"""Simple web GUI for Hog game (no external dependencies)."""

import json
import os
import secrets
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import dice
import hog

HOST = "0.0.0.0"
PORT = int(os.environ.get("HOG_GUI_PORT", "31415"))

GAME_STORE = {}

INDEX_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Hog GUI</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:760px;margin:24px auto;padding:0 12px;}
    .card{border:1px solid #ddd;border-radius:8px;padding:14px;margin:12px 0;}
    .row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
    input,select,button{padding:8px;font-size:14px}
    .score{font-size:20px;font-weight:700}
    .log{white-space:pre-wrap;background:#fafafa;border:1px solid #eee;border-radius:6px;padding:10px;min-height:90px}
  </style>
</head>
<body>
  <h1>Hog 游戏 GUI</h1>
  <div class="card">
    <div class="row">
      <label>目标分数 <input id="goal" type="number" min="20" max="500" value="100"></label>
      <label>规则
        <select id="rule">
          <option value="sus">Sus Fuss</option>
          <option value="simple">Simple</option>
        </select>
      </label>
      <label>电脑策略
        <select id="bot">
          <option value="boar_strategy">boar_strategy</option>
          <option value="sus_strategy">sus_strategy</option>
          <option value="final_strategy">final_strategy</option>
          <option value="always_roll_5">always_roll_5</option>
        </select>
      </label>
      <button id="newGame">新游戏</button>
    </div>
  </div>

  <div class="card">
    <div class="score" id="score">你: 0 | 电脑: 0</div>
    <div class="row" style="margin-top:10px">
      <label>你本回合掷骰数量(0-10) <input id="rolls" type="number" min="0" max="10" value="6"></label>
      <button id="playTurn">进行回合</button>
    </div>
    <p id="status">请先点击“新游戏”。</p>
    <div class="log" id="log"></div>
  </div>

  <script>
    let gameId = null;
    const scoreEl = document.getElementById("score");
    const statusEl = document.getElementById("status");
    const logEl = document.getElementById("log");

    function setState(s) {
      scoreEl.textContent = `你: ${s.score0} | 电脑: ${s.score1}`;
      if (s.over) {
        const who = s.winner === 0 ? "你赢了 🎉" : "电脑赢了 🤖";
        statusEl.textContent = `游戏结束：${who}`;
      } else {
        statusEl.textContent = "轮到你了";
      }
    }

    async function postJSON(url, payload) {
      const r = await fetch(url, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)});
      if (!r.ok) {
        const text = await r.text();
        throw new Error(text || "request failed");
      }
      return r.json();
    }

    document.getElementById("newGame").onclick = async () => {
      try {
        const data = await postJSON("/api/new_game", {
          goal: Number(document.getElementById("goal").value || 100),
          use_sus: document.getElementById("rule").value === "sus",
          bot_strategy: document.getElementById("bot").value
        });
        gameId = data.game_id;
        logEl.textContent = "新游戏已开始。";
        setState(data.state);
      } catch (e) {
        statusEl.textContent = "创建游戏失败: " + e.message;
      }
    };

    document.getElementById("playTurn").onclick = async () => {
      if (!gameId) {
        statusEl.textContent = "请先创建新游戏。";
        return;
      }
      try {
        const data = await postJSON("/api/player_turn", {
          game_id: gameId,
          num_rolls: Number(document.getElementById("rolls").value || 0)
        });
        setState(data.state);
        const lines = [];
        lines.push(`你选择掷 ${data.player.num_rolls} 个骰子，得分 +${data.player.gained}，总分 ${data.player.score}`);
        if (data.bot) {
          lines.push(`电脑选择掷 ${data.bot.num_rolls} 个骰子，得分 +${data.bot.gained}，总分 ${data.bot.score}`);
        }
        logEl.textContent = lines.join("\\n");
      } catch (e) {
        statusEl.textContent = "回合执行失败: " + e.message;
      }
    };
  </script>
</body>
</html>
"""


def _json_response(handler, payload, status=HTTPStatus.OK):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _text_response(handler, text, status=HTTPStatus.OK):
    body = text.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/plain; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _state_view(state):
    return {
        "score0": state["score0"],
        "score1": state["score1"],
        "goal": state["goal"],
        "use_sus": state["use_sus"],
        "bot_strategy": state["bot_strategy"],
        "over": state["over"],
        "winner": state["winner"],
    }


def _strategy_map():
    return {
        "boar_strategy": hog.boar_strategy,
        "sus_strategy": hog.sus_strategy,
        "final_strategy": hog.final_strategy,
        "always_roll_5": hog.always_roll_5,
    }


class HogGuiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            body = INDEX_HTML.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/health":
            _json_response(self, {"ok": True})
            return
        _text_response(self, "Not Found", HTTPStatus.NOT_FOUND)

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0"))
        try:
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            data = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            _text_response(self, "Invalid JSON body", HTTPStatus.BAD_REQUEST)
            return

        if path == "/api/new_game":
            self._new_game(data)
            return
        if path == "/api/player_turn":
            self._player_turn(data)
            return

        _text_response(self, "Not Found", HTTPStatus.NOT_FOUND)

    def _new_game(self, data):
        goal = int(data.get("goal", 100))
        if goal < 20 or goal > 500:
            _text_response(self, "goal must be in [20, 500]", HTTPStatus.BAD_REQUEST)
            return
        use_sus = bool(data.get("use_sus", True))
        bot_strategy = data.get("bot_strategy", "boar_strategy")
        if bot_strategy not in _strategy_map():
            _text_response(self, "unsupported bot_strategy", HTTPStatus.BAD_REQUEST)
            return

        game_id = secrets.token_hex(16)
        GAME_STORE[game_id] = {
            "score0": 0,
            "score1": 0,
            "goal": goal,
            "use_sus": use_sus,
            "bot_strategy": bot_strategy,
            "over": False,
            "winner": None,
        }
        _json_response(self, {"game_id": game_id, "state": _state_view(GAME_STORE[game_id])})

    def _player_turn(self, data):
        game_id = data.get("game_id")
        if not game_id or game_id not in GAME_STORE:
            _text_response(self, "invalid game_id", HTTPStatus.BAD_REQUEST)
            return
        state = GAME_STORE[game_id]
        if state["over"]:
            _json_response(self, {"state": _state_view(state), "player": None, "bot": None})
            return

        num_rolls = data.get("num_rolls")
        if not isinstance(num_rolls, int) or num_rolls < 0 or num_rolls > 10:
            _text_response(self, "num_rolls must be an integer in [0, 10]", HTTPStatus.BAD_REQUEST)
            return

        update = hog.sus_update if state["use_sus"] else hog.simple_update

        old0 = state["score0"]
        state["score0"] = update(num_rolls, state["score0"], state["score1"], dice.six_sided)
        player_event = {
            "num_rolls": num_rolls,
            "gained": state["score0"] - old0,
            "score": state["score0"],
        }
        if state["score0"] >= state["goal"]:
            state["over"] = True
            state["winner"] = 0
            _json_response(self, {"state": _state_view(state), "player": player_event, "bot": None})
            return

        bot_func = _strategy_map()[state["bot_strategy"]]
        bot_rolls = bot_func(state["score1"], state["score0"])
        old1 = state["score1"]
        state["score1"] = update(bot_rolls, state["score1"], state["score0"], dice.six_sided)
        bot_event = {
            "num_rolls": bot_rolls,
            "gained": state["score1"] - old1,
            "score": state["score1"],
        }
        if state["score1"] >= state["goal"]:
            state["over"] = True
            state["winner"] = 1

        _json_response(self, {"state": _state_view(state), "player": player_event, "bot": bot_event})

    def log_message(self, format_str, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), HogGuiHandler)
    print(f"Hog GUI running at http://127.0.0.1:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
