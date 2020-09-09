class Section:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"Section: {self.text}"

    def serialize(self):
        return {
            "text": self.text
        }
