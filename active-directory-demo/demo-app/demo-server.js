// app.js

import fetch from "node-fetch";
import fs from "fs";
import path from "path";

const BASE_URL = "https://dev.hkube.org/hkube/api-server/api/v1";
const REST_ENDPOINT = "/exec/stored";
const RUN_PIPELINE_URL = `${BASE_URL}${REST_ENDPOINT}`;
const JOB_STATUS_ENDPOINT = "/exec/status";

// Choose which pipeline JSON file to use as body
const PIPELINE_FILES = [
  "pipeline-multi.json",
  "pipeline-single.json"
];

function loadPipelineBody(filename) {
  const filePath = path.join(process.cwd(), filename);
  try {
    const data = fs.readFileSync(filePath, "utf8");
    return JSON.parse(data);
  } catch (err) {
    console.error(`Failed to load pipeline file: ${filename}`);
    throw err;
  }
}

const selectedPipelineFile = PIPELINE_FILES[0]; // 0: multi, 1: single
const body = loadPipelineBody(selectedPipelineFile);
async function main() {
  try {
    // === REST call ===
    console.log(`Running pipeline type ${selectedPipelineFile}...`);
    const response = await fetch(RUN_PIPELINE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const restResult = await response.json();
    console.log("Run response:", restResult);
    const { jobId } = restResult;

    if (!jobId) {
      throw new Error("No jobId returned from pipeline run response.");
    }

    // Poll job status every 1 second
    const statusUrl = `${BASE_URL}${JOB_STATUS_ENDPOINT}/${jobId}`;
    let finished = false;
    console.log(`Polling job status at: ${statusUrl}`);
    while (!finished) {
      try {
        const statusRes = await fetch(statusUrl);
        if (!statusRes.ok) {
          throw new Error(`Status fetch error: ${statusRes.status}`);
        }
        const statusData = await statusRes.json();
        // Display pipeline status and details
        console.log(`Pipeline status: ${statusData.status}`);
        if (statusData.data && statusData.data.details) {
          console.log("Details:", statusData.data.details);
        }
        if (statusData.status === "completed" || statusData.status === "failed") {
          finished = true;
          console.log("Job finished with status:", statusData.status);
          // Fetch and display job results
          const resultsUrl = `${BASE_URL}/exec/results/${jobId}`;
          try {
            const resultsRes = await fetch(resultsUrl);
            if (!resultsRes.ok) {
              throw new Error(`Results fetch error: ${resultsRes.status}`);
            }
            const resultsData = await resultsRes.json();
            // Print the full job results object
            console.log("Job results:", JSON.stringify(resultsData, null, 2));
            // If there is a result array, print it in detail
            if (resultsData.result) {
              console.log("Result array:", JSON.stringify(resultsData.result, null, 2));
            }
          } catch (err) {
            console.error("Error fetching job results:", err);
          }
        } else {
          await new Promise(r => setTimeout(r, 1350));
        }
      } catch (err) {
        console.error("Error fetching job status:", err);
        await new Promise(r => setTimeout(r, 1350));
      }
    }
    
  } catch (err) {
    console.error("Error:", err);
  }
}

main();

