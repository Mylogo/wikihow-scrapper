from document.section import Section


class Article:
    def __init__(self, title: str):
        self.title = title
        self.sections = []

    def append_section(self, section: Section):
        self.sections.append(section)

    def __str__(self):
        return f"Title: {self.title}\nSection num: {len(self.sections)}"

    def serialize(self):
        return {
            "title": self.title,
            "sections": list(map(lambda section: section.serialize(), self.sections))
        }
