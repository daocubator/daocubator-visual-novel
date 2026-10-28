#!/usr/bin/env bash
# One-shot: fix Cloud Build auto-deploy, rebuild the Ren'Py web build, stage it.
#
#   ./scripts/deploy.sh            setup + build + stage (then you commit & push main)
#   ./scripts/deploy.sh --push     ...and commit + push to main (triggers Cloud Run auto build)
#   ./scripts/deploy.sh --direct   ...build, then deploy straight from this machine (no git)
#   ./scripts/deploy.sh --skip-setup   skip the GCP service-account/trigger fix
#
# Env: RENPY_SDK (default ~/renpy-8.5.0-sdk)
set -euo pipefail

PROJECT="incubation-cloud"
PROJECT_NUMBER="822201629765"
REGION="us-west1"
SERVICE="get-rich-together"
BUILDER_NAME="cloudrun-builder"
BUILDER="$BUILDER_NAME@$PROJECT.iam.gserviceaccount.com"
SDK="${RENPY_SDK:-$HOME/renpy-8.5.0-sdk}"

PUSH=0; DIRECT=0; SETUP=1
for a in "$@"; do
  case "$a" in
    --push) PUSH=1 ;;
    --direct) DIRECT=1 ;;
    --skip-setup) SETUP=0 ;;
    *) echo "Unknown option: $a" >&2; exit 2 ;;
  esac
done

cd "$(dirname "$0")/.."

# ---------------------------------------------------------------- 1. GCP setup
if [ "$SETUP" = 1 ]; then
  command -v gcloud >/dev/null || { echo "gcloud not found (use --skip-setup to skip)" >&2; exit 1; }
  echo "==> GCP: user-managed build service account ($BUILDER)"
  gcloud config set project "$PROJECT" >/dev/null
  gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
    artifactregistry.googleapis.com --project "$PROJECT"

  gcloud iam service-accounts describe "$BUILDER" --project "$PROJECT" >/dev/null 2>&1 \
    || gcloud iam service-accounts create "$BUILDER_NAME" --project "$PROJECT" \
         --display-name "Cloud Run source builder"

  for ROLE in roles/run.admin roles/cloudbuild.builds.builder roles/artifactregistry.writer \
              roles/logging.logWriter roles/storage.objectAdmin; do
    gcloud projects add-iam-policy-binding "$PROJECT" \
      --member "serviceAccount:$BUILDER" --role "$ROLE" --condition=None >/dev/null
  done

  # Builder must be allowed to deploy a revision that runs as the service's runtime SA.
  RUNTIME_SA="$(gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" \
      --format='value(spec.template.spec.serviceAccountName)' 2>/dev/null || true)"
  RUNTIME_SA="${RUNTIME_SA:-$PROJECT_NUMBER-compute@developer.gserviceaccount.com}"
  gcloud iam service-accounts add-iam-policy-binding "$RUNTIME_SA" --project "$PROJECT" \
    --member "serviceAccount:$BUILDER" --role roles/iam.serviceAccountUser >/dev/null

  echo "==> GCP: fixing build trigger service account"
  TMP="$(mktemp -d)"; FIXED=0
  for LOC in "$REGION" global; do
    gcloud builds triggers list --project "$PROJECT" --region "$LOC" --format=json > "$TMP/list.json" 2>/dev/null || continue
    IDS="$(python3 - "$TMP/list.json" "$SERVICE" <<'PY'
import json, sys
for t in json.load(open(sys.argv[1])):
    if sys.argv[2] in json.dumps(t):
        print(t["id"])
PY
)"
    for ID in $IDS; do
      gcloud builds triggers export "$ID" --project "$PROJECT" --region "$LOC" --destination "$TMP/t.yaml"
      python3 scripts/fix_trigger.py "$TMP/t.yaml" "projects/$PROJECT/serviceAccounts/$BUILDER"
      gcloud builds triggers import --project "$PROJECT" --region "$LOC" --source "$TMP/t.yaml"
      echo "    updated trigger $ID ($LOC)"; FIXED=1
    done
    [ "$FIXED" = 1 ] && break
  done
  [ "$FIXED" = 1 ] || echo "    WARNING: no trigger mentioning '$SERVICE' found. In the console set" \
    "Cloud Build > Triggers > <trigger> > Service account = $BUILDER"
  rm -rf "$TMP"
fi

# ---------------------------------------------------------------- 2. Web build
echo "==> Stopping local web server (if running)"
pkill -f serve_web.py 2>/dev/null || true

echo "==> Fresh Ren'Py web build"
[ -x "$SDK/renpy.sh" ] || { echo "Ren'Py SDK not found at $SDK (set RENPY_SDK)" >&2; exit 1; }
rm -rf web-build
"$SDK/renpy.sh" "$SDK/launcher" web_build . --dest ./web-build

for f in web-build/index.html web-build/renpy.wasm web-build/game.zip; do
  [ -f "$f" ] || { echo "Missing $f - web build failed" >&2; exit 1; }
done
if [ -n "$(find web-build -type f -size +95M)" ]; then
  echo "A file in web-build/ exceeds GitHub's 100MB limit:" >&2
  find web-build -type f -size +95M -exec ls -lh {} \; >&2
  exit 1
fi

# ---------------------------------------------------------------- 3. Ship
if [ "$DIRECT" = 1 ]; then
  echo "==> Direct deploy to Cloud Run"
  gcloud run deploy "$SERVICE" --project "$PROJECT" --region "$REGION" \
    --source . --allow-unauthenticated --port 8080
  gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" --format='value(status.url)'
  exit 0
fi

echo "==> Staging deploy files"
git add -f web-build .gitignore .gitattributes scripts/deploy.sh scripts/fix_trigger.py Dockerfile .dockerignore

if [ "$PUSH" = 1 ]; then
  git diff --cached --quiet && { echo "Nothing new to commit."; exit 0; }
  git commit -m "Rebuild web build and fix Cloud Run auto-deploy"
  git push origin main
  echo "==> Pushed. Watch the build: https://console.cloud.google.com/cloud-build/builds;region=$REGION?project=$PROJECT"
else
  echo
  echo "Ready. Now run:"
  echo "  git commit -m 'Rebuild web build and fix Cloud Run auto-deploy' && git push origin main"
fi
echo "Live URL: https://get-rich-together-$PROJECT_NUMBER.$REGION.run.app"
