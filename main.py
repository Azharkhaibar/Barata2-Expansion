import random
import pygame
import time
import os



class KarakterFiguran:
    def __init__(self, nama, power):
        self.nama = nama
        self.health = 250
        self.power = power

    def attack(self, target):
        damage = random.uniform(0.8, 1.2) * self.power
        print(f"{self.nama} melakukan serangan dengan power {damage}!")
        target.defend(damage)
        if not self.is_alive():
            print(f"{self.nama} sudah mati, tidak bisa menyerang!")
            return

    def defend(self, damage):
        actual_damage = max(0, damage)
        self.health -= actual_damage

        if self.is_alive():
            print(f"{self.nama} menerima serangan dan kehilangan {actual_damage} health!")

        else:
            print("================ 【d】【e】【a】【d】 ========================")
            print(f"{self.nama} telah mati!")

    def is_alive(self):
        return self.health > 0


class Pemain:
    def __init__(self, nama, strategy):
        self.nama = nama
        self.health = 500
        self.power = random.randint(10, 50)
        self.defense = random.randint(5, 20)
        self.skill = random.choice(["Fireball", "Ice Shard", "Thunder Strike", "Slash Sword", "Heal", "Lightning One"])
        self.strategy = strategy

    def attack(self, target):
        critical_chance = random.uniform(0, 1)
        damage = self.power
        healing = self.health
        if self.skill == "Fireball":
            print(f"{self.nama} menggunakan Fireball dengan power {damage * 1.5}!")
            damage *= 1.5
        elif self.skill == "Ice Shard":
            print(f"{self.nama} menggunakan Ice Shard dengan power {damage * 1.2}!")
            damage *= 1.2
        elif self.skill == "Thunder Strike":
            print(f"{self.nama} menggunakan Thunder Strike dengan power {damage * 1.8}!")
            damage *= 1.8
        elif self.skill == "Slash Sword":
            print(f"{self.nama} menggunakan Slash Sword dengan power {damage * 1.4}!")
            damage *= 1.4
        elif self.skill == "Heal":
            print(f"{self.nama} menggunakan healing mode, darah bertambah {self.health * 1.2}!")
            healing *= 1.2
            print("=" * 30)
        elif self.skill == "Lightning One":
            print(f"{self.nama} menggunakan vitalitas mode (Lightning One) dengan power {damage * 3.0}!")
            damage *= 3.0

        if critical_chance > 0.8:
            print(f"{self.nama} melakukan serangan kritis dengan power {damage * 2}!")
            damage *= 2
        else:
            print(f"{self.nama} melakukan serangan dengan power {damage}! Strategi: {self.strategy}")

        target.defend(damage)

    def defend(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        if self.is_alive():
            print(f"{self.nama} menerima serangan dan kehilangan {actual_damage} health!")

        else:
            print("===================== 【d】【e】【a】【d】 ====================== ")
            print(f"{self.nama} telah mati!")

    def is_alive(self):
        return self.health > 0


class Wilayah:
    def __init__(self, nama, health_territory, penguasa):
        self.nama = nama
        self.health_territory = health_territory
        self.penguasa = penguasa

    def dikuasai(self, penguasa_baru):
        print(f"*** {self.nama} dikuasai oleh {penguasa_baru.nama}!")
        self.penguasa = penguasa_baru

    def direbut_kembali(self):
        print(f"*** {self.nama} berhasil direbut kembali!")
        self.health_territory = 100


class GamePerang:
    def __init__(self, player1, player2, player3, player4, figuran1, figuran2, wilayah1, wilayah2, wilayah3, wilayah4):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.figuran1 = figuran1
        self.figuran2 = figuran2
        self.base_health = 5000
        self.wilayah1 = wilayah1
        self.wilayah2 = wilayah2
        self.wilayah3 = wilayah3
        self.wilayah4 = wilayah4

    def attack_wilayah(self, attacker, wilayah):
        damage = attacker.power * random.uniform(0.8, 1.2)
        print(f"{attacker.nama} menyerang ||{wilayah.nama}|| dengan power {damage}!")
        wilayah.health_territory -= damage

        if wilayah.health_territory <= 0:
            wilayah.dikuasai(attacker)

    def attack_base(self, attacker):
        damage = attacker.power * random.uniform(0.8, 1.2)
        print(f"-" * 50)
        print(f"{attacker.nama} menyerang base dengan power {damage}!")
        print(f"-" * 50)
        self.base_health -= damage

    def game_loop(self):
        while any(player.is_alive() for player in [self.player1, self.player2, self.player3, self.player4]):
            if self.player1.is_alive():
                target = random.choice([self.player2, self.player3, self.player4])
                self.player1.attack(target)
                self.attack_wilayah(self.figuran1, self.wilayah1)
                time.sleep(2)

            if self.player2.is_alive():
                target = random.choice([self.player1, self.player3, self.player4])
                self.player2.attack(target)
                self.attack_wilayah(self.figuran2, self.wilayah2)
                time.sleep(2)

            if self.player3.is_alive():
                target = random.choice([self.player1, self.player2, self.player4])
                self.player3.attack(target)
                self.attack_wilayah(self.figuran1, self.wilayah3)
                time.sleep(2)

            if self.player4.is_alive():
                target = random.choice([self.player1, self.player2, self.player3])
                self.player4.attack(target)
                self.attack_wilayah(self.figuran2, self.wilayah4)
                time.sleep(2)


class GameMenu:
    def __init__(self):
        self.game = None

    def play_music(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def start_game(self):
        music_file = "TOKYOPILL"
        music_path = os.path.join(os.path.dirname(__file__), music_file)

        if os.path.exists(music_path):
            self.play_music(music_path)
        else:
            print(f"File musik tidak ditemukan: {music_path}")

        self.game.game_loop()

        winners = [player.nama for player in [self.game.player1, self.game.player2, self.game.player3, self.game.player4] if player.is_alive()]
        print(f"{', '.join(winners)} menang!")

        if self.game.base_health <= 0:
            print("Base hancur! Musuh menang!")
        else:
            print(f"Base bertahan dengan {self.game.base_health} health. Pasukan menang!")

        if self.game.wilayah1.penguasa:
            print(f"{self.game.wilayah1.nama} dikuasai oleh {self.game.wilayah1.penguasa.nama}!")
        else:
            print(f"{self.game.wilayah1.nama} belum dikuasai!")

        if self.game.wilayah2.penguasa:
            print(f"{self.game.wilayah2.nama} dikuasai oleh {self.game.wilayah2.penguasa.nama}!")
        else:
            print(f"{self.game.wilayah2.nama} belum dikuasai!")

        if self.game.wilayah3.penguasa:
            print(f"{self.game.wilayah3.nama} dikuasai oleh {self.game.wilayah3.penguasa.nama}!")
        else:
            print(f"{self.game.wilayah3.nama} belum dikuasai!")

        if self.game.wilayah4.penguasa:
            print(f"{self.game.wilayah4.nama} dikuasai oleh {self.game.wilayah4.penguasa.nama}!")
        else:
            print(f"{self.game.wilayah4.nama} belum dikuasai!")

        self.stop_music()

    def main_menu(self):
        yggdrasil = Wilayah("Yggdrasil", 100, None)
        marwick_castle = Wilayah("Marwick Castle", 100, None)
        ionion = Wilayah("Ionion", 100, None)
        wilayah4 = Wilayah("YurestForest", 100, None)

        p1 = Pemain("|| KENZLEER", "Attack from the front")
        p2 = Pemain("|| AVONI ARMY", "Flank from the left")
        p3 = Pemain("|| RADEONM", "Defensive stance")
        p4 = Pemain("|| EVE'S BANDIT", "Hit and run")
        figuran1 = KarakterFiguran("JINZUU", 30)
        figuran2 = KarakterFiguran("KINGOFELENOR", 25)

        self.game = GamePerang(p1, p2, p3, p4, figuran1, figuran2, yggdrasil, marwick_castle, ionion, wilayah4)

        while True:
            print(" || ================== 乃卂ㄒ卂尺卂2 ====================== ||")
            print("[1] mulai permainan")
            print("[2] Exit")
            choice = input("Pilih Opsi [1/2] : ")

            if choice == "1":
                print("░       ░░░      ░░       ░░░      ░░        ░░      ░░")
                print("▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒▒▒  ▒▒▒▒  ▒▒▒▒  ▒")
                print("▓       ▓▓  ▓▓▓▓  ▓       ▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓")
                print("█  ████  █        █  ███  ██        ████  ████        █")
                print("█       ██  ████  █  ████  █  ████  ████  ████  ████  █")

                print("▂▃▅▇█▓▒░ Barata2 ░▒▓█▇▅▃▂ ▂▃▅▇█▓▒░ Barata2 ░▒▓█▇▅▃▂ ▂▃▅▇█▓▒░ Barata2 ░▒▓█▇▅▃▂")
                self.start_game()
            elif choice == "2":
                print("Anda Keluar dari game, Terima Kasih!")
                break
            else:
                print("Pilihan Salah. ketik 1 atau 2.")


if __name__ == "__main__":
    menu = GameMenu()
    menu.main_menu()
