import pandas as pd
import ast  # Для коректного перетворення списків


class CocktailDataset:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self):
        """Завантажує датасет та обробляє його."""
        try:
            df = pd.read_csv(self.file_path)

            # Видаляємо зайву колонку, якщо вона є
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])

            # Перетворюємо рядки у списки
            df['ingredients'] = df['ingredients'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
            df['ingredientMeasures'] = df['ingredientMeasures'].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

            return df
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return pd.DataFrame()

    def get_cocktails_by_ingredient(self, ingredient: str, limit: int = 5):
        """Знаходить коктейлі, які містять певний інгредієнт."""
        filtered = self.df[self.df['ingredients'].apply(lambda x: ingredient.lower() in [i.lower() for i in x])]
        return filtered.head(limit).to_dict(orient="records")

    def get_non_alcoholic_with_sugar(self, limit: int = 5):
        """Знаходить безалкогольні коктейлі, які містять цукор."""
        filtered = self.df[
            (self.df['alcoholic'].str.lower() == "non alcoholic") &
            (self.df['ingredients'].apply(lambda x: "sugar" in [i.lower() for i in x]))
            ]
        return filtered.head(limit).to_dict(orient="records")


# Приклад використання:
if __name__ == "__main__":
    dataset = CocktailDataset("../data/final_cocktails.csv")
    print("Cocktails with lemon:")
    print(dataset.get_cocktails_by_ingredient("Lemon"))

    print("\nNon-alcoholic cocktails with sugar:")
    print(dataset.get_non_alcoholic_with_sugar())
