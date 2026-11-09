<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/hero-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/hero-light.svg" width="100%" alt="Saswat Samal. Software engineer in Bengaluru, India. I build AI agents, backends and cloud infrastructure that hold up in production. Open to remote roles worldwide. Now at Aina, building the AI voice agent. Open source: Lima, Jaeger, NVIDIA Dynamo.">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/saswatsam/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-linkedin-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-linkedin-light.svg" alt="LinkedIn">
    </picture>
  </a>
  <a href="mailto:saswat.sam786@gmail.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-email-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-email-light.svg" alt="Email">
    </picture>
  </a>
  <a href="https://saswatblogs.hashnode.dev/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-blog-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-blog-light.svg" alt="Blog">
    </picture>
  </a>
  <a href="https://x.com/SaswatTwts">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-x-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-x-light.svg" alt="X">
    </picture>
  </a>
  <a href="https://drive.google.com/file/d/1hcg60KqwyXEZT8eU0x7rrYEkEJ4cdWEz/view">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-resume-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/pill-resume-light.svg" alt="Résumé">
    </picture>
  </a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-01-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-01-light.svg" width="100%" alt="01 Impact at Aina">
</picture>

At [Aina](https://aina.co) ($5.5M seed) we build hardware for AI agents. **Dune**, a context-aware 3-key Mac keypad, hit #1 on Product Hunt. **Aina Ring**, a ring with a small screen that shows the one decision your agents need from you, launched in San Francisco and Bangalore in November 2026. I built the ring's voice agent and moved our backend to production AWS.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/metrics-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/metrics-light.svg" width="100%" alt="1,500x faster query: 30 s to 20 ms, it was 23% of production DB time. 2.4 s removed from every voice command. About 95% of prompt tokens hit the prompt cache. 20+ tools the voice agent calls, plus MCP.">
</picture>

<details>
<summary><b>What I built at Aina</b></summary>
<br>

- Built the **AI voice agent for Aina Ring**: LLM tool calling (Claude, OpenAI) over 20+ tools, plus MCP connectors (Notion, Slack, Linear) for home control, Spotify, calendars and notes
- Gave it **long-term memory with RAG**: local embeddings and pgvector (HNSW) search, with prompt caching on ~95% of prompt tokens
- **Migrated the whole backend to production AWS**: RDS Postgres, 9 ECS services, CodeBuild + ECR CI/CD, EventBridge, SQS/SNS and a private VPC
- Rebuilt the **analytics pipeline**: API Gateway → Kinesis → Firehose → S3 (Parquet) → Glue → Athena, with DMS change data capture from Postgres
- Fixed a **WhatsApp outage** that hit at 6 users (thread-pool exhaustion); it now handles 100+ sessions
- Shipped a **Home Assistant plugin** with signed self-updates and auto-rollback, so voice can control any device

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-02-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-02-light.svg" width="100%" alt="02 Journey">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/journey-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/journey-light.svg" width="100%" alt="2020: IIIT Bhubaneswar, B.Tech in Computer Science (2020 to 2024). 2023: UniStack, SDE Intern. 2024: Badho, Full-Stack Developer. Now: Aina, Software Engineer.">
</picture>

<details>
<summary><b>Earlier roles</b></summary>
<br>

**Badho** · Full-Stack Developer · *Oct 2024 – Nov 2025*
- Designed a **workflow orchestration engine** on Temporal (Node.js, PostgreSQL) with a JSON DSL, auto-versioning and multiple queues, built for millions of workflows. Deployments went from days to minutes
- Built **ONDC seller microservices** (search, select, confirm, cancel, fulfillment) with UPI/NEFT settlements
- Ran the services on Docker and Azure with CI/CD, and **Prometheus, Grafana and Loki** for monitoring, alerts and logs

**UniStack** · SDE Intern · *Nov 2023 – Sep 2024*
- Built the backend (Node.js, TypeScript) and the Next.js client for UniStack's payment system
- Built search, confirmation, status, tracking and cancellation for the **ONDC logistics buyer app**, cutting task completion times by 20%

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-03-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-03-light.svg" width="100%" alt="03 Open source">
</picture>

<a href="https://github.com/lima-vm/lima/pull/5675">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-lima-5675-dark.svg">
    <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-lima-5675-light.svg" width="100%" alt="Lima #5675: shell opens the matching guest directory for remapped mounts">
  </picture>
</a>
<a href="https://github.com/lima-vm/lima/pull/5602">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-lima-5602-dark.svg">
    <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-lima-5602-light.svg" width="100%" alt="Lima #5602: keeps the progress line intact while host agent logs stream in">
  </picture>
</a>
<a href="https://github.com/lima-vm/lima/pull/5771">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-lima-5771-dark.svg">
    <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-lima-5771-light.svg" width="100%" alt="Lima #5771: keeps port 22 privileged so non-root users can't fake sshd">
  </picture>
</a>
<a href="https://github.com/jaegertracing/jaeger/pull/9930">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-jaeger-9930-dark.svg">
    <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-jaeger-9930-light.svg" width="100%" alt="Jaeger #9930: retries failed Cassandra name inserts">
  </picture>
</a>
<a href="https://github.com/ai-dynamo/dynamo/pull/16127">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-dynamo-16127-dark.svg">
    <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-dynamo-16127-light.svg" width="100%" alt="NVIDIA Dynamo #16127: deprecates the unused --mm-prompt-template flag">
  </picture>
</a>
<a href="https://github.com/topoteretes/cognee/pull/5674">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-cognee-5674-dark.svg">
    <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/oss-cognee-5674-light.svg" width="100%" alt="cognee #5674: returns 409 instead of 500 for a duplicate role name">
  </picture>
</a>

<p align="right"><sub><a href="https://github.com/search?q=author%3Asaswatsam786+is%3Apr+-user%3Asaswatsam786&type=pullrequests">All my pull requests →</a></sub></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-04-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-04-light.svg" width="100%" alt="04 Selected work">
</picture>

<p align="center">
  <a href="https://github.com/saswatsam786/snapshell">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-snapshell-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-snapshell-light.svg" width="49%" alt="SnapShell: video calls between two terminals, streaming your webcam as ASCII art over WebRTC. Go.">
    </picture>
  </a>
  <a href="https://x.com/SaswatTwts/status/2084023729777221884">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-circle-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-circle-light.svg" width="49%" alt="Circle to Explain: what if your notebook could explain itself? Circle a paragraph, draw ??, and Claude handwrites the answer. Rust and Python.">
    </picture>
  </a>
</p>
<p align="center">
  <a href="https://x.com/SaswatTwts/status/2077896242500391400">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-diary-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-diary-light.svg" width="49%" alt="Enchanted Diary: a handwritten diary on an e-ink tablet, backed by Claude, with a Rust Spotify player. Python and Rust.">
    </picture>
  </a>
  <a href="https://github.com/saswatsam786/telepilot">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-telepilot-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-telepilot-light.svg" width="49%" alt="telepilot: your Claude Code, in your pocket. Text any session from Telegram or iMessage. TypeScript.">
    </picture>
  </a>
</p>
<p align="center">
  <a href="https://github.com/saswatsam786/vessl">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-vessl-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-vessl-light.svg" width="49%" alt="Vessl: a Docker container management CLI in Go.">
    </picture>
  </a>
  <a href="https://x.com/SaswatTwts/status/2040093157006909580">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-button-dark.svg">
      <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/card-button-light.svg" width="49%" alt="Food Button: a key on my Mac that orders dinner, built on Dune.">
    </picture>
  </a>
</p>

<p align="center"><sub>More: <a href="https://github.com/saswatsam786/redis">redis</a>, a Redis-compatible server in Go</sub></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-05-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-05-light.svg" width="100%" alt="05 Toolkit">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/toolkit-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/toolkit-light.svg" width="100%" alt="Languages: Python, Go, TypeScript, Rust, SQL, Bash, C++. AI: LLM agents, tool calling, MCP, RAG, pgvector, prompt caching, Claude, OpenAI. Backend: FastAPI, Celery, SQLAlchemy, Node.js, Temporal, PostgreSQL, Redis, MongoDB. Cloud and ops: AWS (ECS, RDS, Kinesis, Glue, Athena), Azure, Docker, GitHub Actions, Prometheus, Grafana, OpenTelemetry, Linux.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-06-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-06-light.svg" width="100%" alt="06 Recognition">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/recognition-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/recognition-light.svg" width="100%" alt="Winner, Hedera Hashgraph India Web 3.0 Hackathon. Grand Finalist, Smart India Hackathon 2022 and the HarbourX Hackathon. Semi-Finalist, Flipkart Grid 5.0 (2023). Linux Foundation LiFT training scholarship (2022). MLH Prep Fellowship (2022). Microsoft Engage mentee.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-07-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/main/assets/section-07-light.svg" width="100%" alt="07 Activity">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/saswatsam786/saswatsam786/output/github-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/saswatsam786/saswatsam786/output/github-snake.svg" width="100%" alt="A snake eating my GitHub contribution graph">
</picture>

<p align="center"><sub>This profile redraws itself every day from live GitHub data, with <a href="scripts/render.py">one Python script</a>.</sub></p>
