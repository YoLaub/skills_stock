#!/bin/bash
# ─────────────────────────────────────────────
#  Skills & Agents — Claude Code
#  Installateur interactif
#  Usage : curl -s https://raw.githubusercontent.com/YoLaub/skills-agents/main/install.sh | bash
#  Ou en local : bash install.sh
# ─────────────────────────────────────────────

set -e

REPO_OWNER="YoLaub"
REPO_NAME="skills_stock"
REPO_BRANCH="main"
REPO_RAW="https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$REPO_BRANCH"
GH_API="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME"
TARGET=".claude"

# Compteurs globaux (incrémentés par download_file)
INSTALLED=0
SKIPPED=0
REPO_TREE=""  # cache du listing récursif de l'API GitHub

# ── Couleurs ──────────────────────────────────
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"
GREEN="\033[32m"
BLUE="\033[34m"
YELLOW="\033[33m"
RED="\033[31m"
CYAN="\033[36m"

# ── Helpers ───────────────────────────────────
print_header() {
  echo ""
  echo -e "${BOLD}${BLUE}🧠 Skills & Agents — Claude Code${RESET}"
  echo -e "${DIM}Installateur interactif${RESET}"
  echo ""
}

print_step() {
  echo -e "${CYAN}▶ $1${RESET}"
}

print_ok() {
  echo -e "${GREEN}✓${RESET} $1"
}

print_warn() {
  echo -e "${YELLOW}⚠ $1${RESET}"
}

print_error() {
  echo -e "${RED}✗ $1${RESET}"
}

print_divider() {
  echo -e "${DIM}────────────────────────────────────────${RESET}"
}

# ── Vérifications ─────────────────────────────
check_deps() {
  if ! command -v curl &>/dev/null; then
    print_error "curl est requis. Installe-le puis relance le script."
    exit 1
  fi
}

check_claude_code() {
  if ! command -v claude &>/dev/null; then
    print_warn "Claude Code ne semble pas installé sur ce système."
    echo -e "  ${DIM}Les fichiers seront quand même copiés dans .claude/${RESET}"
    echo ""
  fi
}

# ── Catalogue ─────────────────────────────────
# Format : "id|label|type|fichiers..."
# type : agent | skill
# fichiers : chemins relatifs depuis la racine du repo (séparés par ,)

declare -a CATALOGUE=(
  # ── RH Pipeline ───────────────────────────
  "rh-pipeline|Pipeline RH complet (skill orchestrateur)|skill|.claude/skills/rh-pipeline/SKILL.md"
  "cv-analyst|Agent — Analyse CV + score ATS|agent|.claude/agents/rh/cv-analyst.md"
  "cv-designer|Agent — Design HTML A4 du CV|agent|.claude/agents/rh/cv-designer.md"
  "cv-recruiter|Agent — Email recruteur + rapport ATS|agent|.claude/agents/rh/cv-recruiter.md"
  "rh-interviewer|Agent — Entretien motivation (conversationnel)|agent|.claude/agents/rh/rh-interviewer.md"
  "tech-interviewer|Agent — Entretien technique (conversationnel)|agent|.claude/agents/rh/tech-interviewer.md"
  "debrief-agent|Agent — Bilan candidat points forts/faibles|agent|.claude/agents/rh/debrief-agent.md"
  # ── Cert Pipeline ─────────────────────────
  "cert-pipeline|Pipeline Certification complet (skill orchestrateur)|skill|.claude/skills/cert-pipeline/SKILL.md"
  "cert-intake|Agent — Collecte certification + profil candidat|agent|.claude/agents/cert/cert-intake.md"
  "referentiel-loader|Agent — Chargement docs/ ou recherche web officielle|agent|.claude/agents/cert/referentiel-loader.md"
  "gap-analyser|Agent — Croisement profil vs compétences requises|agent|.claude/agents/cert/gap-analyser.md"
  "exam-preparer|Agent — Fiches révision + questions probables|agent|.claude/agents/cert/exam-preparer.md"
  "cert-interviewer|Agent — Simulation entretien jury (conversationnel)|agent|.claude/agents/cert/cert-interviewer.md"
  "cert-debrief|Agent — Bilan candidat + probabilité de validation|agent|.claude/agents/cert/cert-debrief.md"
  # ── Brain Builder ──────────────────────────
  "brain-builder|Skill — Vault Obsidian / mémoire projet structurée|skill|.claude/skills/brain-builder/SKILL.md"
  # ── Skill Optimizer ────────────────────────
  "skill-optimizer|Skill — Optimisation d'un SKILL.md par micro-éditions validées (SkillOpt)|skill|.claude/skills/skill-optimizer/SKILL.md"
  # ── Greenfield TDD + OKF ───────────────────
  "greenfield-tdd-okf|Skill — Workflow greenfield TDD + index OKF (démarrage nouveau projet)|skill|.claude/skills/greenfield-tdd-okf/SKILL.md"
  # ── Presentation Builder ───────────────────
  "presentation-builder|Skill — Construit une présentation (Marp, .pptx/PDF) avec modèle assertion-preuve et porte de contrôle visuelle|skill|.claude/skills/presentation-builder/SKILL.md"
)

# ── Bundles prédéfinis ────────────────────────
declare -A BUNDLES
BUNDLES["tout"]="rh-pipeline cv-analyst cv-designer cv-recruiter rh-interviewer tech-interviewer debrief-agent cert-pipeline cert-intake referentiel-loader gap-analyser exam-preparer cert-interviewer cert-debrief brain-builder skill-optimizer"
BUNDLES["rh"]="rh-pipeline cv-analyst cv-designer cv-recruiter rh-interviewer tech-interviewer debrief-agent"
BUNDLES["cv-only"]="cv-analyst cv-designer cv-recruiter"
BUNDLES["cert"]="cert-pipeline cert-intake referentiel-loader gap-analyser exam-preparer cert-interviewer cert-debrief"
BUNDLES["brain"]="brain-builder"
BUNDLES["optimizer"]="skill-optimizer"
BUNDLES["greenfield"]="greenfield-tdd-okf"
BUNDLES["presentation"]="presentation-builder"

# ── Sélection interactive ─────────────────────
show_catalogue() {
  echo -e "${BOLD}Que veux-tu installer ?${RESET}"
  echo ""
  echo -e "  ${BOLD}[0]${RESET} Tout installer"
  echo -e "  ${BOLD}[b]${RESET} Choisir un bundle"
  echo -e "  ${BOLD}[s]${RESET} Sélection manuelle"
  echo ""
  echo -n "Choix : "
}

show_bundles() {
  echo ""
  echo -e "${BOLD}Bundles disponibles :${RESET}"
  echo ""
  echo -e "  ${BOLD}[1]${RESET} rh      — Pipeline RH complet (skill + 6 agents)"
  echo -e "  ${BOLD}[2]${RESET} cv-only — Agents CV uniquement (analyst + designer + recruiter)"
  echo -e "  ${BOLD}[3]${RESET} cert    — Pipeline Certification complet (skill + 6 agents)"
  echo -e "  ${BOLD}[4]${RESET} brain   — Brain Builder (vault Obsidian / mémoire projet)"
  echo -e "  ${BOLD}[5]${RESET} optimizer — Skill Optimizer (itération sur un SKILL.md)"
  echo -e "  ${BOLD}[6]${RESET} greenfield — Greenfield TDD + OKF (démarrage nouveau projet)"
  echo -e "  ${BOLD}[7]${RESET} presentation — Presentation Builder (slides Marp/pptx/PDF)"
  echo ""
  echo -n "Choix : "
}

show_items() {
  echo ""
  echo -e "${BOLD}Disponible :${RESET}"
  echo ""
  local i=1
  for entry in "${CATALOGUE[@]}"; do
    IFS='|' read -r id label type _ <<< "$entry"
    local type_badge=""
    if [[ "$type" == "skill" ]]; then
      type_badge="${CYAN}[skill] ${RESET}"
    else
      type_badge="${DIM}[agent]${RESET} "
    fi
    printf "  ${BOLD}[%d]${RESET} %b%s\n" "$i" "$type_badge" "$label"
    ((i++))
  done
  echo ""
  echo -e "${DIM}Entrée plusieurs numéros séparés par des espaces : ex. 1 2 3${RESET}"
  echo ""
  echo -n "Sélection : "
}

# ── Téléchargement ────────────────────────────
get_ids_from_selection() {
  local mode="$1"
  local input="$2"
  local selected_ids=()

  if [[ "$mode" == "all" ]]; then
    for entry in "${CATALOGUE[@]}"; do
      IFS='|' read -r id _ <<< "$entry"
      selected_ids+=("$id")
    done

  elif [[ "$mode" == "bundle" ]]; then
    local bundle_key=""
    case "$input" in
      1) bundle_key="rh" ;;
      2) bundle_key="cv-only" ;;
      3) bundle_key="cert" ;;
      4) bundle_key="brain" ;;
      5) bundle_key="optimizer" ;;
      6) bundle_key="greenfield" ;;
      7) bundle_key="presentation" ;;
      *) print_error "Bundle invalide."; exit 1 ;;
    esac
    read -ra selected_ids <<< "${BUNDLES[$bundle_key]}"

  elif [[ "$mode" == "manual" ]]; then
    for num in $input; do
      local idx=$((num - 1))
      if [[ $idx -ge 0 && $idx -lt ${#CATALOGUE[@]} ]]; then
        IFS='|' read -r id _ <<< "${CATALOGUE[$idx]}"
        selected_ids+=("$id")
      else
        print_warn "Numéro $num ignoré (hors catalogue)"
      fi
    done
  fi

  echo "${selected_ids[@]}"
}

# Extrait les chemins des blobs (fichiers) depuis le JSON de l'API git/trees (sur stdin).
# Ordre : jq → PowerShell (Windows/MSYS) → python3 réel → awk.
list_blobs() {
  local json
  json=$(cat)  # lire stdin une seule fois

  if command -v jq &>/dev/null; then
    printf '%s' "$json" | jq -r '.tree[] | select(.type=="blob") | .path'

  elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "$WINDIR" ]] && command -v powershell.exe &>/dev/null; then
    # Windows/Git-Bash : PowerShell natif, Python peut être le Store redirect
    printf '%s' "$json" | powershell.exe -NoProfile -NonInteractive -Command \
      '$in=[Console]::In.ReadToEnd(); ($in|ConvertFrom-Json).tree | Where-Object{$_.type -eq "blob"} | ForEach-Object{$_.path}'

  elif python3 -c "" 2>/dev/null; then
    printf '%s' "$json" | python3 -c 'import sys,json; [print(e["path"]) for e in json.load(sys.stdin).get("tree",[]) if e.get("type")=="blob"]'

  elif python -c "" 2>/dev/null; then
    printf '%s' "$json" | python -c 'import sys,json
for e in json.load(sys.stdin).get("tree",[]):
    if e.get("type")=="blob": print(e["path"])'

  else
    # Dernier recours : awk (JSON compact ou indenté)
    printf '%s' "$json" | awk 'BEGIN{RS="{"} /"type": *"blob"/ {
      if (match($0, /"path": *"[^"]*"/)) {
        s=substr($0,RSTART,RLENGTH); sub(/"path": *"/,"",s); sub(/"$/,"",s); print s
      }
    }'
  fi
}

# Récupère (et met en cache) l'arborescence récursive complète du dépôt en un seul appel API.
fetch_repo_tree() {
  if [[ -z "$REPO_TREE" ]]; then
    REPO_TREE=$(curl -sf \
      -H "Accept: application/vnd.github+json" \
      -H "User-Agent: skills-installer" \
      "$GH_API/git/trees/$REPO_BRANCH?recursive=1") || return 1
  fi
  printf '%s' "$REPO_TREE"
}

# Télécharge un fichier distant (chemin repo) vers un chemin local, avec feedback + comptage.
download_file() {
  local remote_path="$1"
  local local_path="$2"

  mkdir -p "$(dirname "$local_path")"

  if [[ -f "$local_path" ]]; then
    echo -n -e "  ${DIM}(maj)${RESET} $local_path ... "
  else
    echo -n "  $local_path ... "
  fi

  if curl -sf "$REPO_RAW/$remote_path" -o "$local_path" 2>/dev/null; then
    echo -e "${GREEN}✓${RESET}"
    INSTALLED=$((INSTALLED + 1))
  else
    echo -e "${RED}✗ échec${RESET}"
    SKIPPED=$((SKIPPED + 1))
  fi
}

install_ids() {
  local ids=("$@")
  INSTALLED=0
  SKIPPED=0

  local agent_files=()  # fichiers agents (téléchargés tels quels, sous-dossier aplati)
  local skill_dirs=()   # préfixes de dossiers skills (dossier complet via API)

  for id in "${ids[@]}"; do
    for entry in "${CATALOGUE[@]}"; do
      IFS='|' read -r eid _ etype efiles <<< "$entry"
      [[ "$eid" != "$id" ]] && continue
      IFS=',' read -ra files <<< "$efiles"
      for f in "${files[@]}"; do
        if [[ "$f" == .claude/agents/* ]]; then
          agent_files+=("$f")
        elif [[ "$f" == .claude/skills/* ]]; then
          # .claude/skills/<nom>/... → préfixe .claude/skills/<nom>
          local rest="${f#.claude/skills/}"
          skill_dirs+=(".claude/skills/${rest%%/*}")
        fi
      done
    done
  done

  # Dédoublonner les dossiers de skills
  local uniq_dirs=()
  local d u seen
  for d in "${skill_dirs[@]}"; do
    seen=0
    for u in "${uniq_dirs[@]}"; do [[ "$u" == "$d" ]] && seen=1 && break; done
    [[ $seen -eq 0 ]] && uniq_dirs+=("$d")
  done
  skill_dirs=("${uniq_dirs[@]}")

  if [[ ${#agent_files[@]} -eq 0 && ${#skill_dirs[@]} -eq 0 ]]; then
    print_warn "Rien à installer."
    return
  fi

  echo ""
  print_step "Installation dans $TARGET/"
  echo ""

  # ── Agents : fichier unique, sous-dossier de domaine aplati ──
  local f
  for f in "${agent_files[@]}"; do
    download_file "$f" "$TARGET/agents/$(basename "$f")"
  done

  # ── Skills : dossier complet via parcours récursif de l'API GitHub ──
  if [[ ${#skill_dirs[@]} -gt 0 ]]; then
    local tree all_blobs
    tree=$(fetch_repo_tree)
    if [[ -z "$tree" ]]; then
      print_error "Impossible de récupérer l'arborescence du dépôt via l'API GitHub."
      print_warn "Vérifie ta connexion, ou la limite de l'API (60 req/h sans token)."
    else
      # tr -d '\r' : certains python/awk sous Windows émettent des fins de ligne CRLF.
      all_blobs=$(printf '%s' "$tree" | list_blobs | tr -d '\r')
      local dir blob rel found
      for dir in "${skill_dirs[@]}"; do
        found=0
        while IFS= read -r blob; do
          [[ -z "$blob" ]] && continue
          [[ "$blob" == "$dir/"* ]] || continue
          found=1
          # .claude/skills/<nom>/... → $TARGET/skills/<nom>/...
          rel="${blob#.claude/skills/}"
          download_file "$blob" "$TARGET/skills/$rel"
        done <<< "$all_blobs"
        [[ $found -eq 0 ]] && print_warn "Aucun fichier trouvé pour $dir sur $REPO_BRANCH."
      done
    fi
  fi

  echo ""
  print_divider
  echo -e "${GREEN}${BOLD}$INSTALLED fichier(s) installé(s)${RESET}"
  if [[ $SKIPPED -gt 0 ]]; then
    print_warn "$SKIPPED fichier(s) non récupéré(s)"
  fi
}

# ── Post-install ──────────────────────────────
post_install() {
  echo ""
  echo -e "${BOLD}Prochaines étapes :${RESET}"
  echo ""
  echo -e "  1. Ouvre ce projet dans ${BOLD}Claude Code${RESET}"
  echo -e "  2. Les agents et skills sont actifs automatiquement"
  echo -e "  3. Lance un agent : ${DIM}\"Lance l'agent cv-analyst avec ce CV : @mon-cv.pdf\"${RESET}"
  echo -e "  4. Personnalise les fichiers dans ${BOLD}.claude/agents/${RESET} selon ton projet"
  echo ""
  echo -e "${DIM}Documentation : https://github.com/YoLaub/skills-agents${RESET}"
  echo ""
}

# ── Main ──────────────────────────────────────
main() {
  print_header
  check_deps
  check_claude_code

  # Détection si on est dans un projet
  if [[ ! -d ".git" && ! -d "src" && ! -f "package.json" ]]; then
    print_warn "Aucun projet détecté dans le répertoire courant."
    echo -e "  ${DIM}Les fichiers seront installés ici : $(pwd)/.claude/${RESET}"
    echo ""
    echo -n "Continuer quand même ? [o/N] : "
    read -r confirm
    if [[ "$confirm" != "o" && "$confirm" != "O" ]]; then
      echo "Annulé."
      exit 0
    fi
    echo ""
  fi

  show_catalogue
  read -r mode_choice

  local selected_ids=()

  case "$mode_choice" in
    0)
      selected_ids=($(get_ids_from_selection "all" ""))
      ;;
    b|B)
      show_bundles
      read -r bundle_choice
      selected_ids=($(get_ids_from_selection "bundle" "$bundle_choice"))
      ;;
    s|S)
      show_items
      read -r manual_choice
      selected_ids=($(get_ids_from_selection "manual" "$manual_choice"))
      ;;
    *)
      print_error "Choix invalide."
      exit 1
      ;;
  esac

  if [[ ${#selected_ids[@]} -eq 0 ]]; then
    print_warn "Aucun élément sélectionné."
    exit 0
  fi

  echo ""
  echo -e "${BOLD}À installer :${RESET}"
  for id in "${selected_ids[@]}"; do
    for entry in "${CATALOGUE[@]}"; do
      IFS='|' read -r eid label _ <<< "$entry"
      if [[ "$eid" == "$id" ]]; then
        echo -e "  ${DIM}•${RESET} $label"
      fi
    done
  done

  echo ""
  echo -n "Confirmer ? [O/n] : "
  read -r confirm
  if [[ "$confirm" == "n" || "$confirm" == "N" ]]; then
    echo "Annulé."
    exit 0
  fi

  install_ids "${selected_ids[@]}"
  post_install
}

main "$@"
