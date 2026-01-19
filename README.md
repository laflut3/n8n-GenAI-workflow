# GenAI Labs - n8n internship finder

Workflow n8n qui orchestre la recherche d'offres, l'enrichissement par score de ville (MCP), l'extraction LLM, puis l'export Google Sheets et la synthese Discord.

## Workflow n8n (final)
Fichier: `workflow-final.json`

### Etapes du workflow (pas a pas)
1. **Manual Trigger**: demarre l'execution.
2. **Code (matrix)**: genere les couples ville x technologie.
3. **Tavily Search**: recherche une offre par couple.
4. **MCP Client**: recupere le score de ville via `http://mcp:8000/mcp`.
5. **LLM extraction (Gemini)**: force une sortie JSON stricte par offre.
6. **Parse extract**: nettoie et normalise les champs.
7. **LLM summary (Gemini)**: genere un resume FR court par offre.
8. **Merge + Remove duplicates**: fusionne resume + offre, dedoublonne par `source_url`.
9. **If**: separe selon `salary` present ou non.
10. **Google Sheets**: ecrit dans deux onglets (avec/sans salaire).
11. **LLM synthese finale**: produit un rapport global.
12. **Discord**: publie la synthese (tronquee si > 2000 caracteres).

### Champs extraits par offre
- company, 
- job_title, 
- city, 
- country,
- remote_policy, 
- contract_type,
- salary, 
- currency, 
- duration, 
- application_deadline,
- skills[], 
- languages[],
- source_url, 
- source_title,
- city_score,
- summary,

## Prerequis
- Docker + Docker Compose
- Compte n8n
- API keys/credentials:
  - Tavily API
  - Google Gemini (PaLM) API
  - Google Sheets OAuth
  - Discord Webhook

## Demarrage rapide (Docker)
```bash
docker compose up -d
```
- n8n: `http://localhost:5678`
- MCP server: `http://localhost:8000`

## Installation/Execution du serveur MCP (local)
```bash
uv pip install -e .
uv run city-score-mcp
```
Ou:
```bash
uv run python main.py
```

## Configuration n8n
1. Importer `workflow-final.json` dans n8n.
2. Creer les credentials dans n8n:
   - Tavily
   - Google Gemini (PaLM)
   - Google Sheets (OAuth)
   - Discord Webhook
3. Verifier l'URL MCP dans le node **MCP Client**:
   - `http://mcp:8000/mcp` (Docker)
   - ou `http://localhost:8000/mcp` (local)

## Setup Google Sheets (Google Cloud API)
1. Aller sur Google Cloud Console et creer un projet.
2. Activer l'API **Google Sheets** et l'API **Google Drive**.
3. Configurer l'ecran de consentement OAuth.
4. Creer des identifiants OAuth (type \texttt{Desktop App} ou \texttt{Web Application}).
5. Ajouter l'URL de redirection fournie par n8n dans les redirections OAuth.
6. Dans n8n, creer le credential **Google Sheets OAuth2** avec le Client ID/Secret.
7. Autoriser l'acces et verifier la connexion.

## Google Sheets
Deux onglets sont utilises:
- **Results true**: offres avec salaire renseigne
- **result false**: offres sans salaire

Colonnes ecrites:
`company`, `job_title`, `contract_type`, `city`, `country`, `salary`,
`currency`, `duration`, `application_deadline`, `skills`, `languages`,
`source_url`, `source_title`, `city_score`, `summary`, `remote_policy`

## A creer dans Google Sheets (avant execution)
1. Creer un nouveau fichier Google Sheets (ex: `Internships`).
2. Creer deux onglets avec exactement ces noms:
   - `Results true`
   - `result false`
3. Ajouter en ligne 1 les en-tetes de colonnes suivants (dans cet ordre ou mapping manuel identique):
   `company`, `job_title`, `contract_type`, `city`, `country`, `salary`,
   `currency`, `duration`, `application_deadline`, `skills`, `languages`,
   `source_url`, `source_title`, `city_score`, `summary`, `remote_policy`
4. Dans n8n, selectionner ce fichier et ces onglets dans les nodes **save row true** et **save row false**.

## Structure du projet
- `workflow-final.json`: workflow final n8n
- `Dockerfile.mcp`: image du serveur MCP
- `docker-compose.yml`: n8n + MCP
- `main.py`: point d'entree MCP
- `src/genai_labs/`: serveur MCP et scoring
- `docs/`: sources et references
