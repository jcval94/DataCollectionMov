# Bob Ross Lab — DataCollectionMov MCP + Render Free

A narrowly scoped, authenticated, **offline** MCP pilot. It is *not* a general Python code
execution endpoint. All tools use the original
[Bob Ross classroom dataset](../../examples/bob_ross_clustering/data/manifest.json)
and analysis contract. No API keys or network downloads are required to compare the models.

## What works

- `bob_ross_dataset`: provenance, checksums and feature contract.
- `bob_ross_reference`: committed K-Means reference (clearly marked as precomputed).
- `bob_ross_compare_models(k=4, exclude_guests=True)`: executes three actual algorithms,
  K-Means with 50 initializations, Ward hierarchical and average-linkage Hamming hierarchical.
  All train on the **same 12 human-coded binary features**, k and population.
- `bob_ross_visualizations`: links to committed SVG charts and classroom HTML.
- `bob_ross_storyboard`: six-scene evidence-based educational video outline.

The comparison ranks *eligible* candidates by Euclidean silhouette on the same features,
requiring each group to contain >=5% of the population (at least 10 episodes).
It additionally reports group sizes, within-cluster squared error and measured fit time.
This is **not predictive accuracy**, does not establish the true number of artistic styles,
and does not demonstrate causality. The existing K-Means k=4 choice was imposed by
the four-room museum exercise.

## Connect the Render service you already created

The existing Render template deployment is a **different GitHub repository**. It will
not automatically start serving these tools merely because you created the template.

1. After this PR passes CI and is merged, open Render Dashboard -> your Web Service -> **Settings**.
2. Connect its repository to `jcval94/DataCollectionMov`, branch `main`. If Render
   cannot switch the existing repository, create a new **Free** Web Service from that repo
   (do not delete the old service until the new service passes health checks).
3. Runtime: Python. Build command:
   `pip install -r services/bob_ross_mcp/requirements.txt`
4. Start command: `python services/bob_ross_mcp/server.py`
5. Health check: `/health`. Ensure `MCP_API_TOKEN` exists in **Environment** and is
   a random secret **at least 24 characters**. Use Render's auto-generated value
   if the template already generated one. Never paste tokens in chat or commit them.
6. Configure `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`,
   `MKL_NUM_THREADS=1`. Deploy and wait until the service is **Live**.
7. Browser-safe health URL: `https://<your-service>.onrender.com/health`.
   An authenticated MCP client's endpoint is
   `https://<your-service>.onrender.com/mcp` with
   `Authorization: Bearer <MCP_API_TOKEN>`.

Alternatively, `render.yaml` at the repo root is a **new Blueprint** configured
for the Free plan and with a generated token. It does not modify an existing
Render service. The MCP endpoint needs a client supporting Streamable HTTP and
bearer authentication. ChatGPT mobile support for direct *custom* MCP connections
may be limited by plan/app; do not assume direct access from the phone.

### Mobile fallback via GitHub

After merging this PR, using the **connected GitHub app** in ChatGPT, create an
issue in `jcval94/DataCollectionMov` with the **exact title**:

`Bob Ross: comparar modelos`

Issue body (optional):

```text
k: 4
include_guests: false
```

The owner-only [workflow](../../.github/workflows/bob-ross-on-demand.yml)
runs the same Python comparison on GitHub Actions and adds the result as
a comment on that issue. The analysis is limited to 2 <= k <= 6 and does
not accept scripts, arbitrary file paths or URLs. GitHub Actions executes
the job; Render provides the independently callable MCP endpoint.
ChatGPT may need to read the completed issue in a later message;
an issue creation acknowledgement is not an experiment result.

**Security:** only requests authored by the repository owner with that exact
title trigger the workflow. This is a mobile-compatible bridge, not a claim
that ChatGPT mobile directly connects to custom MCP.

## Offline validation

```bash
python -m pip install -r services/bob_ross_mcp/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python examples/bob_ross_clustering/run.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m unittest discover -s services/bob_ross_mcp/tests -v
```

The tests verify the pinned data, reference, actual model comparison and
input bounds; the repo's previous Bob Ross tests remain unchanged.

## Free-tier limits

Render Free has limited memory and may spin down after inactivity. Do not
run user-authored code, heavy grid searches, concurrent large jobs or long
training there. Results returned by the MCP call are ephemeral. The
GitHub Issue bridge publishes durable summaries and workflow artifacts
that expire after seven days; the comment remains in the issue.
Neither deployment nor end-to-end phone connection is claimed until
the Render service and client have been verified.
