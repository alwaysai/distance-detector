

class InterestItem:
    def __init__(self, width, height, name, labels):
        self.width = width
        self.height = height
        self.name = name
        self.labels = labels

    def get_area(self):
        return self.width * self.height