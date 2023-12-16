import tkinter as tk
from tkinter import messagebox
import random

# 블랙잭 게임 로직 클래스
class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_chips = 100
        self.current_bet = 0

    @staticmethod
    def create_deck():
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        deck = [{'suit': suit, 'value': value} for suit in suits for value in values]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        if len(self.deck) > 0:
            card = self.deck.pop()
            hand.append(card)

    def calculate_hand_value(self, hand):
        value = 0
        ace_count = 0
        for card in hand:
            if card['value'] in ['Jack', 'Queen', 'King']:
                value += 10
            elif card['value'] == 'Ace':
                value += 11
                ace_count += 1
            else:
                value += int(card['value'])

        while value > 21 and ace_count > 0:
            value -= 10
            ace_count -= 1

        return value

    def start_round(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)

# 블랙잭 게임 GUI 클래스
class BlackjackGUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("Blackjack Game")
        self.window.geometry("800x400")
        self.window.configure(bg='navy')
        self.create_widgets()
        self.show_start_button()

    def create_widgets(self):
        retro_font = ("Courier", 12, "bold")
        self.status_label = tk.Label(
            self.window, text="Welcome to Blackjack!", font=retro_font, bg='navy', fg='lime'
        )
        self.status_label.pack(pady=10)

        self.button_frame = tk.Frame(self.window, bg='navy')
        self.button_frame.pack(pady=20)

        # 배팅 금액 묻는 레이블 추가
        self.bet_label = tk.Label(
            self.button_frame, text="Enter your bet amount:", font=retro_font, bg='navy', fg='white'
        )
        self.bet_label.pack()

        self.bet_entry = tk.Entry(self.button_frame, font=("Courier", 12), width=10)
        self.bet_entry.pack(pady=10)

        self.hit_button = tk.Button(
            self.button_frame, text="Hit", command=self.hit, fg='white', bg='green', font=retro_font, height=2, width=10
        )
        self.stay_button = tk.Button(
            self.button_frame, text="Stay", command=self.stay, fg='white', bg='red', font=retro_font, height=2, width=10
        )
        self.start_button = tk.Button(
            self.button_frame, text="Game Start", command=self.start_game, fg='white', bg='blue', font=retro_font, height=2, width=20
        )

        self.chips_label = tk.Label(
            self.window, text=f"Your chips: {self.game.player_chips}", font=retro_font, bg='navy', fg='white'
        )
        self.chips_label.pack(pady=5)

    def show_start_button(self):
        self.hit_button.pack_forget()
        self.stay_button.pack_forget()
        self.start_button.pack(pady=10)
        self.bet_label.pack()   # 배팅 금액 레이블 표시
        self.bet_entry.pack()   # 배팅 입력창 표시

    def show_hit_stay_buttons(self):
        self.start_button.pack_forget()
        self.bet_label.pack_forget()  # 배팅 금액 레이블 숨기기
        self.bet_entry.pack_forget()  # 배팅 입력창 숨기기
        self.hit_button.pack(side=tk.LEFT, padx=10)
        self.stay_button.pack(side=tk.RIGHT, padx=10)

    def update_status(self, text):
        self.status_label.config(text=text)

    def start_game(self):
        bet_amount = self.get_bet_amount()
        if bet_amount is None:
            return  # 유효하지 않은 배팅 금액 입력 시 게임 시작 중지
        self.game.current_bet = bet_amount
        self.game.start_round()
        self.show_hit_stay_buttons()
        self.update_game_status()

    def get_bet_amount(self):
        try:
            bet_amount = int(self.bet_entry.get())
            if bet_amount > 0 and bet_amount <= self.game.player_chips:
                return bet_amount
            else:
                messagebox.showinfo("Invalid Bet", "Bet amount must be within your chip count.")
                return None
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter a valid number.")
            return None

    def hit(self):
        self.game.deal_card(self.game.player_hand)
        self.update_game_status()
        player_value = self.game.calculate_hand_value(self.game.player_hand)
        if player_value > 21:
            messagebox.showinfo("Bust", "You bust! Dealer wins.")
            self.game.player_chips -= self.game.current_bet
            self.game_over()

    def stay(self):
        while self.game.calculate_hand_value(self.game.dealer_hand) < 17:
            self.game.deal_card(self.game.dealer_hand)

        self.update_game_status(final=True)
        self.evaluate_winner()

    def update_game_status(self, final=False):
        player_hand = ", ".join([f"{card['value']} of {card['suit']}" for card in self.game.player_hand])
        player_value = self.game.calculate_hand_value(self.game.player_hand)
        dealer_hand = ", ".join([f"{card['value']} of {card['suit']}" for card in self.game.dealer_hand[:1]])
        if final:
            dealer_hand = ", ".join([f"{card['value']} of {card['suit']}" for card in self.game.dealer_hand])
        dealer_value = self.game.calculate_hand_value(self.game.dealer_hand)

        self.update_status(f"Your hand: {player_hand} (Total: {player_value})\nDealer's hand: {dealer_hand} (Total: {dealer_value if final else '...'})")
        self.chips_label.config(text=f"Your chips: {self.game.player_chips}")

    def evaluate_winner(self):
        player_value = self.game.calculate_hand_value(self.game.player_hand)
        dealer_value = self.game.calculate_hand_value(self.game.dealer_hand)
        is_blackjack = player_value == 21 and len(self.game.player_hand) == 2

        if dealer_value > 21 or player_value > dealer_value:
            winnings = self.game.current_bet * 3 if is_blackjack else self.game.current_bet * 2
            messagebox.showinfo("Winner", f"You win! You won {winnings} chips.")
            self.game.player_chips += winnings
        elif dealer_value == player_value:
            messagebox.showinfo("Tie", "It's a tie! You get your bet back.")
        else:
            messagebox.showinfo("Loser", f"You lost your bet of {self.game.current_bet} chips.")
            self.game.player_chips -= self.game.current_bet

        self.chips_label.config(text=f"Your chips: {self.game.player_chips}")
        self.game_over()

    def game_over(self):
        if self.game.player_chips <= 0:
            messagebox.showinfo("Game Over", "You have no more chips.")
            self.window.destroy()
        else:
            self.show_start_button()
            self.update_status("Click 'Game Start' for a new round.")

    def run(self):
        self.window.mainloop()

# 게임 인스턴스 생성 및 GUI 실행
game = BlackjackGame()
gui = BlackjackGUI(game)
gui.run()
