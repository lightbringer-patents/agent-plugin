"""Static routing regressions on packaged skills; not model acceptance tests."""

import unittest

from build_release import package_files
from validate_submission import ROOT


class CaptureRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.files = package_files(ROOT, True)

    def text(self, path):
        return self.files[f"skills/{path}"].decode()

    def test_packaged_capture_skill_keeps_three_distinct_paths(self):
        text = self.text("innovation-capture/SKILL.md")
        idea, guided = text.split("- **Lightweight innovation / idea:**", 1)[1].split(
            "- **Invention disclosure through guided capture:**", 1
        )
        guided, direct = guided.split("- **Invention disclosure through direct authoring:**", 1)
        self.assertIn("`create_asset` with `type: innovation`", idea)
        self.assertIn("Do not retrieve the disclosure template", idea)
        self.assertIn("recommend the `invention-capture` journey", guided)
        self.assertIn("only when the journey and required tools are advertised", guided)
        self.assertIn("when the user prefers the current assistant, or the journey is unavailable", direct)
        self.assertIn("`get_innovation_template`", direct)
        self.assertIn("`create_asset` with `type: invention_disclosure`", direct)
        self.assertIn("Follow clear intent without another selection question", text)
        self.assertIn("Saving a disclosure does not request patent preparation", text)

    def test_active_journey_does_not_spawn_a_second_writer(self):
        skill = self.text("innovation-capture/SKILL.md")
        handoff = self.text("innovation-capture/references/capture-handoff.md")
        self.assertIn("Do not run a competing interview, draft or save a second disclosure", skill)
        self.assertIn("Recover an uncertain start or save", skill)
        self.assertIn("before a run starts", handoff)
        self.assertIn("never replay it through another writer", handoff)

    def test_direct_and_preparation_routes_honor_explicit_preference(self):
        direct = self.text("innovation-capture/references/direct-workflow.md")
        preparation = self.text("patent-preparation/SKILL.md")
        self.assertIn("Do not retrieve `get_innovation_template` or apply disclosure readiness criteria", direct)
        self.assertIn("available by user preference even when the journey is advertised", direct)
        self.assertIn("unless the user prefers direct authoring by the current assistant", preparation)
        self.assertIn("when the user prefers it or the journey is unavailable", preparation)

    def test_source_exploration_does_not_promote_all_ideas_to_disclosures(self):
        sources = self.text("innovation-capture/references/source-exploration.md")
        self.assertIn("Saving mined ideas uses `create_asset` with `type: innovation`", sources)
        self.assertIn("applies only to the direct disclosure path", sources)

    def test_old_blanket_template_and_fallback_only_rules_are_absent(self):
        for name, data in self.files.items():
            if name.startswith("skills/") and name.endswith(".md"):
                text = data.decode()
                self.assertNotIn("In the direct-authoring compatibility path, retrieve `get_innovation_template`", text, name)
                self.assertNotIn("Only fall back to the [direct workflow]", text, name)


if __name__ == "__main__":
    unittest.main()
