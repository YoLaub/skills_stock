#!/bin/bash
# ─────────────────────────────────────────────
#  Skills & Agents — Claude Code
#  Installateur interactif
#  Usage : curl -s https://raw.githubusercontent.com/YoLaub/skills-agents/main/install.sh | bash
#  Ou en local : bash install.sh
# ─────────────────────────────────────────────

set -e

REPO_RAW="https://raw.githubusercontent.com/YoLaub/skills-agents/main"
TARGET=".claude"

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
  # ── Brain Builder ──────────────────────────
  "brain-builder|Skill — Vault Obsidian / mémoire projet structurée|skill|.claude/skills/brain-builder/SKILL.md"
  # ── Skill Optimizer ────────────────────────
  "skill-optimizer|Skill — Optimisation d'un SKILL.md par micro-éditions validées (SkillOpt)|skill|.claude/skills/skill-optimizer/SKILL.md"
)

# ── Bundles prédéfinis ────────────────────────
declare -A BUNDLES
BUNDLES["tout"]="rh-pipeline cv-analyst cv-designer cv-recruiter rh-interviewer tech-interviewer debrief-agent brain-builder skill-optimizer"
BUNDLES["rh"]="rh-pipeline cv-analyst cv-designer cv-recruiter rh-interviewer tech-interviewer debrief-agent"
BUNDLES["cv-only"]="cv-analyst cv-designer cv-recruiter"
BUNDLES["brain"]="brain-builder"
BUNDLES["optimizer"]="skill-optimizer"

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
  echo -e "  ${BOLD}[3]${RESET} brain   — Brain Builder (vault Obsidian / mémoire projet)"
  echo -e "  ${BOLD}[4]${RESET} optimizer — Skill Optimizer (itération sur un SKILL.md)"
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
      3) bundle_key="brain" ;;
      4) bundle_key="optimizer" ;;
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

install_ids() {
  local ids=("$@")

  # Résoudre les fichiers à télécharger depuis les ids
  declare -A to_download  # chemin_distant -> chemin_local

  for id in "${ids[@]}"; do
    for entry in "${CATALOGUE[@]}"; do
      IFS='|' read -r eid _ etype efiles <<< "$entry"
      if [[ "$eid" == "$id" ]]; then
        IFS=',' read -ra files <<< "$efiles"
        for f in "${files[@]}"; do
          # Déterminer le chemin local dans .claude/
          if [[ "$f" == .claude/agents/* ]]; then
            # .claude/agents/rh/cv-analyst.md → .claude/agents/cv-analyst.md (aplatir le sous-dossier)
            local filename
            filename=$(basename "$f")
            to_download["$f"]="$TARGET/agents/$filename"
          elif [[ "$f" == .claude/skills/* ]]; then
            # .claude/skills/rh-pipeline/SKILL.md → .claude/skills/rh-pipeline/SKILL.md
            local rel="${f#.claude/skills/}"
            to_download["$f"]="$TARGET/skills/$rel"
          fi
        done
      fi
    done
  done

  if [[ ${#to_download[@]} -eq 0 ]]; then
    print_warn "Rien à installer."
    return
  fi

  echo ""
  print_step "Installation dans $TARGET/"
  echo ""

  local installed=0
  local skipped=0

  for remote_path in "${!to_download[@]}"; do
    local local_path="${to_download[$remote_path]}"
    local local_dir
    local_dir=$(dirname "$local_path")

    mkdir -p "$local_dir"

    if [[ -f "$local_path" ]]; then
      echo -n -e "  ${DIM}(existe déjà, mise à jour)${RESET} $local_path ... "
    else
      echo -n "  $local_path ... "
    fi

    if curl -sf "$REPO_RAW/$remote_path" -o "$local_path" 2>/dev/null; then
      echo -e "${GREEN}✓${RESET}"
      ((installed++))
    else
      echo -e "${RED}✗ échec (fichier introuvable sur le dépôt)${RESET}"
      ((skipped++))
    fi
  done

  echo ""
  print_divider
  echo -e "${GREEN}${BOLD}$installed fichier(s) installé(s)${RESET}"
  if [[ $skipped -gt 0 ]]; then
    print_warn "$skipped fichier(s) non récupéré(s)"
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
