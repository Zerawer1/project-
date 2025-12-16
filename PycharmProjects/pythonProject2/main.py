import matplotlib.pyplot as plt


def draw_pie_chart(values, labels):
    total = sum(values
    percentages = [v / total * 100 for v in values]

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=[f"{label} ({p:.1f}%)" for label, p in zip(labels, percentages)],
        autopct=None,
        startangle=90
    )
    plt.title("Круговая диаграмма")
    plt.show()


def main():
    # Исходные данные
    values = [30, 20, 15, 10, 25]
    labels = ["Красный", "Зелёный", "Синий", "Жёлтый", "Оранжевый"]

    while True:
        print("\nТекущий набор значений:")
        for i, (label, value) in enumerate(zip(labels, values), start=1):
            print(f"{i}. {label}: {value}")

        print("\nМеню:")
        print("1 — Построить круговую диаграмму")
        print("2 — Добавить новое значение")
        print("3 — Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            draw_pie_chart(values, labels)
        elif choice == "2":
            name = input("Введите название сектора: ")
            try:
                value = float(input("Введите значение: "))
                labels.append(name)
                values.append(value)
                print("Новое значение добавлено!")
            except ValueError:
                print("Ошибка: нужно ввести число!")
        elif choice == "3":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if name == "__main__":
    main()