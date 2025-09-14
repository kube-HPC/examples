import express from "express";
import fs from "fs";
import path from "path";
import fetch from "node-fetch";

const app = express();
const PORT = 3000;
const BASE_URL = "https://dev.hkube.org/hkube/api-server/api/v1";
const RUN_PIPELINE_ENDPOINT = "/exec/stored";
const JOB_STATUS_ENDPOINT = "/exec/status";
const JOB_RESULTS_ENDPOINT = "/exec/results";
const PIPELINE_FILES = ["pipeline-multi.json", "pipeline-single.json"];
const JOB_GRAPH_PARSED_ENDPOINT = "/graph/parsed";
// Get parsed graph for a job
app.get("/api/graph/:jobId", async (req, res) => {
  try {
    const response = await fetch(`${BASE_URL}${JOB_GRAPH_PARSED_ENDPOINT}/${req.params.jobId}`);
    const result = await response.json();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.use(express.json());
app.use(express.static(path.join(process.cwd(), "public")));

app.get("/api/pipelines", (req, res) => {
  // List available pipeline files
  res.json(PIPELINE_FILES);
});

app.get("/api/pipeline/:name", (req, res) => {
  // Return pipeline file contents
  const filePath = path.join(process.cwd(), req.params.name);
  try {
    const data = fs.readFileSync(filePath, "utf8");
    res.json(JSON.parse(data));
  } catch (err) {
    res.status(404).json({ error: "Pipeline not found" });
  }
});

app.post("/api/run", async (req, res) => {
  // Run pipeline
  const body = req.body;
  try {
    const response = await fetch(`${BASE_URL}${RUN_PIPELINE_ENDPOINT}` , {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const result = await response.json();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get("/api/status/:jobId", async (req, res) => {
  // Get job status
  try {
    const response = await fetch(`${BASE_URL}${JOB_STATUS_ENDPOINT}/${req.params.jobId}`);
    const result = await response.json();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get("/api/results/:jobId", async (req, res) => {
  // Get job results
  try {
    const response = await fetch(`${BASE_URL}${JOB_RESULTS_ENDPOINT}/${req.params.jobId}`);
    const result = await response.json();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
