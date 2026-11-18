/* Bob Ross standalone episode: Node static HTML/data integrity QA (no dependencies). */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const root = __dirname;
const page = fs.readFileSync(path.join(root, "episode.html"), "utf8");
const csv = fs.readFileSync(path.join(root, "data/elements-by-episode.csv"));
const questions = JSON.parse(fs.readFileSync(path.join(root, "questions.json"), "utf8"));
const expected = "42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf";
const digest = crypto.createHash("sha256").update(csv).digest("hex");
assert.equal(digest, expected, "Unexpected dataset hash");
assert.equal(questions.questions.length, 6);
assert.equal(new Set(questions.questions.map(x => x.id)).size, 6);
for (const q of questions.questions) {
  assert.ok(q.question && q.adversary && q.metric, "Incomplete contract: " + q.id);
}
function jsonBlock(id) {
  const match = page.match(new RegExp('<script type="application/json" id="' + id + '">([\\s\\S]*?)<\\/script>'));
  assert.ok(match, "Missing embedded JSON: " + id);
  return JSON.parse(match[1]);
}
const rows = jsonBlock("rows");
const routes = jsonBlock("questions");
assert.equal(rows.length, 403);
assert.equal(routes.length, 6);
assert.equal(rows.filter(x => x.guest === 0).length, 381);
assert.equal(rows.filter(x => x.guest === 1).length, 22);
assert.equal(rows.filter(x => !x.guest && (x.mask & 1) === 0).length, 36);
assert.equal(rows.filter(x => !x.guest && (x.mask & 2) !== 0 && (x.mask & 32) === 0).length, 48);
assert.ok(rows.every(x => Number.isInteger(x.mask) && x.mask >= 0 && x.mask <= 4095));
assert.equal(new Set(rows.map(x => x.id)).size, 403);
const ids = [...page.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
assert.equal(ids.length, new Set(ids).size, "Duplicate element ID");
for (const match of page.matchAll(/byId\("([^"]+)"\)/g)) {
  assert.ok(ids.includes(match[1]), "Missing UI reference: " + match[1]);
}
const script = page.match(/<script>\s*([\s\S]*?)<\/script>\s*<\/body>/);
assert.ok(script, "Missing inline controller");
new vm.Script(script[1], {filename:"episode-inline.js"});
assert.ok(!page.includes("fetch(") && !page.includes("<script src="), "Page must stay offline");
console.log(JSON.stringify({
  status: "PASS",
  checks: ["source-sha256", "six-questions", "403-rows", "guest-split",
           "counterexamples", "embedded-data", "unique-dom-ids",
           "js-syntax", "no-remote-script"],
  note: "Static checks only; this is not a real browser accessibility/visual test."
}, null, 2));
