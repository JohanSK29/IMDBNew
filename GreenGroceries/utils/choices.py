import os
import pandas as pd

#from GreenGroceries import app

DATASET_PATH = os.path.join('C:/Users/johan/OneDrive - University of Copenhagen/2. år/DIS/Project/GreenGroceries/GreenGroceries/dataset/revised_movies_database_brain_rot_score.csv')


def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]


df = pd.read_csv(DATASET_PATH, sep=',')

ProduceCategoryChoices = ModelChoices(df.Genre.unique())
ProduceItemChoices = ModelChoices(df.Moviename.unique())
ProduceVarietyChoices = ModelChoices(df.MainActor.unique())
ProduceUnitChoices = ModelChoices(df.Summary.unique())

UserTypeChoices = ModelChoices(['Farmer', 'Customer'])

if __name__ == '__main__':
    print(df.item.unique())
    print(ProduceItemChoices.choices())
