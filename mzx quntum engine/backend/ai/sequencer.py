# backend/ai/sequencer.py
import time

class Sequencer:
    def __init__(self):
        self.last_trade_time = 0
        self.cooldown = 25
        self.bias_lock = None
        self.bias_lock_strength = 0

    def allow_trade(self, bias):
        now = time.time()

        # Cooldown check
        if now - self.last_trade_time < self.cooldown:
            return False, "Cooldown active"

        # Bias lock — prevents switching direction too fast
        if self.bias_lock and self.bias_lock != bias:
            if self.bias_lock_strength > 0.7:
                return False, "Bias lock engaged"

        return True, "OK"

    def register_trade(self, bias, confidence):
        self.last_trade_time = time.time()

        # Bias lock becomes stronger with confidence
        self.bias_lock = bias
        self.bias_lock_strength = min(1.0, confidence)
