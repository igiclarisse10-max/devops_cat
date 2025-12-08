#!/usr/bin/env bash
# Usage: ./swap-blue-green.sh <namespace> <service-name>
# This script toggles the service selector between blue and green deployments.

NAMESPACE=${1:-default}
SERVICE=${2:-todo-app-service}

CURRENT=$(kubectl -n "$NAMESPACE" get svc "$SERVICE" -o jsonpath='{.spec.selector.active}' 2>/dev/null || echo "")
if [ "$CURRENT" = "blue" ]; then
  NEW=green
else
  NEW=blue
fi

echo "Switching service $SERVICE in namespace $NAMESPACE from '$CURRENT' to '$NEW'"
kubectl -n "$NAMESPACE" patch svc "$SERVICE" -p "{\"spec\":{\"selector\":{\"app\":\"todo-app\",\"active\":\"$NEW\"}}}"

echo "Service updated."
