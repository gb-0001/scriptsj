import requests
import json

# Paramètres de l'API
TOKEN = ""
SERVER = "api.crc.testing:6443"
NAMESPACE = ""
QUOTASNAME = ""

# Seuil d'alerte par défaut
DEFAULT_ALERT_THRESHOLD = 15

# Effectuer la requête à l'API
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}
response = requests.get(f"https://{SERVER}/apis/quota.openshift.io/v1/namespaces/{NAMESPACE}/appliedclusterresourcequotas/{QUOTASNAME}?pretty=true", headers=headers, verify=False)

# Analyser la réponse JSON
data = json.loads(response.text)
print(data)
# Extraire les informations pertinentes
hard_limits = data['status']['total']['hard']
used_limits = data['status']['total']['used']

# Convertir les limites en valeurs numériques pour la comparaison
def convert_limit(limit):
    if limit.endswith('Gi'):
        return float(limit[:-2]) * 1024
    elif limit.endswith('Mi'):
        return float(limit[:-2])
    elif limit.endswith('m'):
        return float(limit[:-1]) / 1000
    else:
        return float(limit)

hard_limits_num = {k: convert_limit(v) for k, v in hard_limits.items()}
used_limits_num = {k: convert_limit(v) for k, v in used_limits.items()}

# Vérifier si les limites sont dépassées
alerts = {}
for resource, hard_limit in hard_limits_num.items():
    used_limit = used_limits_num.get(resource, 0)
    remaining = hard_limit - used_limit
    remaining_percent = (remaining / hard_limit) * 100
    alerts[resource] = remaining_percent < DEFAULT_ALERT_THRESHOLD

# Retourner True si une alerte est déclenchée, False sinon
alert_triggered = any(alerts.values())
print(alert_triggered)
