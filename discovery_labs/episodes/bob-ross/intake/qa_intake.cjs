#!/usr/bin/env node
/* Intake integrity checks: no npm packages and no writes. */
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const ROOT=__dirname,episode=path.dirname(ROOT);
const raw=fs.readFileSync(path.join(episode,"data/elements-by-episode.csv"));
const expected="42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf";
assert.equal(crypto.createHash("sha256").update(raw).digest("hex"),expected,"Original source changed");
const metadata=JSON.parse(fs.readFileSync(path.join(ROOT,"metadata.json"),"utf8"));
const graph=JSON.parse(fs.readFileSync(path.join(ROOT,"question_graph.json"),"utf8"));
const rawLines=raw.toString("utf8").trimEnd().split(/\r?\n/);
const sampleLines=fs.readFileSync(path.join(ROOT,"data_sample.csv"),"utf8").trimEnd().split(/\r?\n/);
assert.equal(rawLines.length,404,"403 observations plus header");
assert.equal(rawLines[0].split(",").length,69);
assert.equal(sampleLines.length,13,"12 examples plus header");
assert.equal(metadata.sample.rows,12);
assert.equal(metadata.snapshot.rows,403);
assert.equal(metadata.snapshot.columns,69);
assert.equal(metadata.snapshot.binary_labels,67);
assert.equal(metadata.snapshot.sha256,expected);
assert.equal(sampleLines[0],rawLines[0]);
const original=new Set(rawLines.slice(1));
for(const line of sampleLines.slice(1))assert.ok(original.has(line),"Sample row not found verbatim in original");
assert.equal(new Set(sampleLines.slice(1)).size,12);
assert.equal(graph.arcs.length,12);
assert.equal(new Set(graph.arcs.map(q=>q.id)).size,12);
for(const arc of graph.arcs){
 assert.ok(typeof arc.title==="string"&&arc.title.length>15,arc.id+" title");
 assert.ok(typeof arc.q1==="string"&&arc.q1.length>25,arc.id+" q1");
 assert.ok(Array.isArray(arc.q2)&&arc.q2.length>=2,arc.id+" q2");
 assert.ok(typeof arc.q3==="string"&&arc.q3.length>25,arc.id+" q3");
 assert.ok(arc.method&&arc.adversary&&arc.visual&&arc.external,arc.id+" incomplete");
 assert.ok(!/APROBADA|VALIDADA/.test(arc.status),"Do not assert research approval");
}
for(const file of ["DEEP_RESEARCH_MASTER.md","PLAN_DE_INVESTIGACION.md","VISUAL_SPEC.md",
 "skills/research-question-architect/SKILL.md","prompts/01_BIOGRAFIA_EVENTOS.md",
 "prompts/02_HISTORIA_CONTEXTO.md","prompts/03_CIENCIA_ANTECEDENTES.md",
 "prompts/04_FUENTES_VISUALES_DERECHOS.md","prompts/05_SINTESIS_HIPOTESIS.md"]){
 assert.ok(fs.existsSync(path.join(ROOT,file)),file+" missing");
}
console.log(JSON.stringify({status:"PASS",source_sha256:expected,rows:403,preview_rows:12,
arcs:12,second_order_questions:graph.arcs.reduce((n,q)=>n+q.q2.length,0),
third_order_questions:graph.arcs.length,deep_research_prompts:5,
note:"Integrity only; no Deep Research, inference, rights review or browser QA executed."},null,2));
