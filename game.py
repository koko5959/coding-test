import random
import sys

class Game:

    #状態
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"

    def __init__(self):
        words = ["apple", "banana", "cherry", "diamond", "electrician", "fungi", "guide", "humble", "island", "jacket", "kindness"]

        self.word = random.choice(words)
        self.guessed_letters = set()
        self.counter = 5
        self.state = self.PLAYING
    
    def get_display_word(self):
        """現在の表示用単語を返す"""
        return ''.join(c if c.lower() in self.guessed_letters else '_' for c in self.word)
    
    def process_guess(self, guess):
        """入力された文字を処理して状態を更新する"""
        if len(guess) != 1 or not guess.encode("utf-8").isalpha(): #encodeが必要、
            return "半角のアルファベットを1文字入力してください"
        guess = guess.lower()
        

        # すでに予測済みの文字
        if guess in self.guessed_letters:
            return "その文字はすでに入力されました"
        
        self.guessed_letters.add(guess)
        if guess not in self.word.lower():
            self.counter -= 1
        
        if '_' not in self.get_display_word():
            self.state = self.WON
        elif self.counter <= 0:
            self.state = self.LOST
        
        return None

    def get_status(self):
        """現在のゲーム状態に応じたメッセージを返す"""
        if self.state == self.WON:
            return f"おめでとうございます！単語「{self.word}」を当てました！"
        elif self.state == self.LOST:
            return f"ゲームオーバー。正解は「{self.word}」でした。"
        else:
            return None

def test():
    # ナイーブなユニットテスト
    game = Game()

    print("game.get_display_word()のテスト")
    game.guessed_letters = {"a", "b", "c"}
    game.word = "abc"
    print(game.get_display_word() == "abc")
    game.word = "abcd"
    print(game.get_display_word() == "abc_")
    game.word = "kkkk"
    print(game.get_display_word() == "____")

    print("game.process_guess(strint)のテスト")
    game.guessed_letters = set("a")
    print(game.process_guess("") == "半角のアルファベットを1文字入力してください")
    print(game.process_guess("あ") == "半角のアルファベットを1文字入力してください")
    print(game.process_guess("@") == "半角のアルファベットを1文字入力してください")
    print(game.process_guess("ab") == "半角のアルファベットを1文字入力してください")
    print(game.process_guess("１") == "半角のアルファベットを1文字入力してください")
    print(game.process_guess("a") == "その文字はすでに入力されました")
    game.word = "abc"
    game.guessed_letters = set()
    game.process_guess("a")
    print((game.counter, game.get_display_word()) == (5, "a__"))
    game.process_guess("d")
    print((game.counter, game.get_display_word()) == (4, "a__"))
    game.process_guess("b")
    print((game.counter, game.get_display_word()) == (4, "ab_"))
    game.process_guess("c")
    print((game.counter, game.get_display_word(), game.state) == (4, "abc", Game.WON))
    lost_game = Game()
    lost_game.word = "kkkk"
    lost_game.counter = 1
    lost_game.process_guess("a")
    print((lost_game.counter, lost_game.get_display_word(), lost_game.state) == (0, "____", Game.LOST))

    #get_status(self)のunit-testは省略


def main():
    game = Game()
    while game.state == Game.PLAYING:
        print(game.get_display_word())
        print(game.counter)

        user_input = input()

        error = game.process_guess(user_input)
        if error:
            print(error)
    
    print(game.get_display_word())
    print(game.get_status())

if __name__ == "__main__":
    main()
    sys.exit(0)