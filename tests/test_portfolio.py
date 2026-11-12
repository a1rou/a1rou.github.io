import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.projects = {}
        self.current = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if tag == "article" and "project" in classes:
            self.current = "featured" if "project-featured" in classes else "secondary"
            self.projects[self.current] = {"text": [], "links": []}
        if self.current and tag == "a":
            self.projects[self.current]["links"].append(attributes.get("href"))

    def handle_endtag(self, tag):
        if tag == "article":
            self.current = None

    def handle_data(self, data):
        if self.current:
            self.projects[self.current]["text"].append(data.strip())


class PortfolioContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = ProjectParser()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        cls.projects = parser.projects

    def text(self, project):
        return " ".join(self.projects[project]["text"])

    def test_vehicle_project_shows_verified_holdout_metrics_and_split(self):
        text = self.text("secondary")
        for item in ("XGBoost", "ROC-AUC", "0.7532", "Gini", "0.5064", "0.4958", "24 232", "24 414", "24 337"):
            with self.subTest(item=item):
                self.assertIn(item, text)
        self.assertIn("validation", text)
        self.assertIn("test", text)
        self.assertIn("PurchDate", text)

    def test_vehicle_project_explains_hypothetical_product_use(self):
        text = self.text("secondary")
        self.assertIn("закупщик", text.lower())
        self.assertIn("ручн", text.lower())
        self.assertIn("следующ", text.lower())
        self.assertIn("precision", text.lower())

    def test_jewelry_project_explains_own_work_and_authenticity_limit(self):
        text = self.text("featured").lower()
        for item in ("qwen", "json", "тариф", "подлинность", "товаровед", "следующая итерация"):
            with self.subTest(item=item):
                self.assertIn(item, text)
        self.assertIn("не подтверждает", text)

    def test_project_links_stay_available(self):
        featured = self.projects["featured"]["links"]
        secondary = self.projects["secondary"]["links"]
        self.assertIn("https://airouu-hackathon.streamlit.app/", featured)
        self.assertIn("https://github.com/a1rou/hackathon", featured)
        self.assertIn("https://github.com/a1rou/ML5_Decision_trees_School21", secondary)
        self.assertIn("https://github.com/a1rou/ML5_Decision_trees_School21/blob/develop/src/task.ipynb", secondary)


if __name__ == "__main__":
    unittest.main()
