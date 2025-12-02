import random

def get_user_choice():
    print("Выберите: 0 - Камень, 1 - Ножницы, 2 - Бумага")
    while True:
        try:
            choice = int(input("Ваш выбор: "))
            if choice in [0, 1, 2]:
                return choice
            else:
                print("Некорректный ввод. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число 0, 1 или 2.")

def get_computer_choice():
    return random.randint(0, 2)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Ничья!"
    elif (user_choice == 0 and computer_choice == 1) or \
         (user_choice == 1 and computer_choice == 2) or \
         (user_choice == 2 and computer_choice == 0):
        return "Вы победили!"
    else:
        return "Компьютер победил!"

def choice_to_string(choice):
    return ["Камень", "Ножницы", "Бумага"][choice]

def main():
    print("Добро пожаловать в игру Камень-Ножницы-Бумага!")
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()

    print(f"Вы выбрали: {choice_to_string(user_choice)}")
    print(f"Компьютер выбрал: {choice_to_string(computer_choice)}")
    result = determine_winner(user_choice, computer_choice)
    print(result)

if __name__ == "__main__":
    main()

