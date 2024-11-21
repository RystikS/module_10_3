import threading
import time
import random


class Bank:
    def __init__(self, balance: int):
        self.balance = balance
        self.lock = threading.Lock()
        self.delay = 0.001

    def deposit(self):
        for i in range(100):
            random_num = random.randint(50, 500)
            with self.lock:
                self.balance += random_num
                print(f'Пополнение:{random_num}. Баланс: {self.balance}', f'Порядок итерации {i}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()


            time.sleep(self.delay)

    def take(self):
        for i in range(100):
            random_num = random.randint(50, 500)
            with self.lock:
                print(f'Запрос на {random_num}', f'Порядок итерации {i}')
                if random_num > self.balance:
                    print(f'Запрос отклонен, недостаточно средств')
                    self.lock.acquire()
                else:
                    self.balance -= random_num
                    print(f'Снятие: {random_num}. Баланс: {self.balance}', f'Порядок итерации {i}')

            time.sleep(self.delay)


bk = Bank(balance=0)

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
