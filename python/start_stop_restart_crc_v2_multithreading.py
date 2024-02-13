import subprocess
import json
import time
from collections import defaultdict
from prettytable import PrettyTable
import datetime
import os
import sys
import argparse
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument("--simulate", action='store_true', help="Simulate script execution")
args = parser.parse_args()

simulate = args.simulate

def process_project(project):
    print(f"Récupère la liste des deployment de {project} et ajout dans le dictionnaire")
    deployments = get_deployments(project)
    project_dict = create_project_dict(project, deployments)
    return project_dict

token1 = "TOKEN"
server1 = "https://api.crc.testing:6443"
project1 = "prj"
MYENV = ["dev"]
MYSON = {"dev": ["x00"]}
lstproj = ["nada"]
lstpod = ["myapp1","app4"]
lstSTATUS = ["test3"]
mod = "stop"
filter_mode = "exclude"
RD_JOBID_NAME = "8888_BOB_"

used_json_status_before_stop = None
nb_scale_desired = None
if nb_scale_desired is not None:
    nb_scale_desired=int(nb_scale_desired)

if mod == "start":
    if used_json_status_before_stop is None and nb_scale_desired is None:
        print("Erreur : Pour le mode 'start', vous devez fournir soit 'used_json_status_before_stop', soit 'nb_scale_desired'.")
        sys.exit(1)
    if used_json_status_before_stop is not None and not os.path.isfile(used_json_status_before_stop):
        print(f"Erreur : Le fichier {used_json_status_before_stop} n'existe pas.")
        sys.exit(1)
    if nb_scale_desired is not None and (not isinstance(nb_scale_desired, int) or nb_scale_desired > 4):
        print("Erreur : 'nb_scale_desired' doit être un entier qui ne dépasse pas 4.")
        sys.exit(1)

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def login_to_openshift(token, server):
    cmd = f'oc login --token={token} --server={server}'
    result = run_command(cmd)
    print("RESULT", result)
    if 'Login failed' in result:
        raise Exception(f'Login failed with error: {result}')
    elif 'Logged into' in result:
        print(f'Successfully logged in {server}')
        openshift_login = result.split(' as ')[-1].split(' ')[0].replace('"',"")
        return openshift_login
    else:
        print("Not logged check your token")
        sys.exit(1)

def get_pods_info(project, appname):
    cmd = f"oc get pods -n {project} -l app={appname} -o json"
    output = run_command(cmd)
    pod_info = json.loads(output)
    pods_info = []
    if pod_info.get('items'):
        for pod in pod_info['items']:
            pod_name = pod['metadata']['name']
            owner_reference = pod['metadata'].get('ownerReferences', [{}])[0].get('name', '')
            pod_details = {
                "podname": pod_name,
                "owner_ref": owner_reference,
                "details": {
                    "READY": "N/A",
                    "STATUS": "N/A",
                    "RESTART": "N/A",
                    "AGE": "N/A"
                }
            }
            if pod.get('status'):
                conditions = pod['status'].get('conditions', [])
                for condition in conditions:
                    if condition['type'] == 'Ready':
                        pod_details['details']['READY'] = condition['status']
                container_statuses = pod['status'].get('containerStatuses', [])
                if container_statuses:
                    container_status = container_statuses[0]
                    state = container_status.get('state', {})
                    status_map = {
                        'running': 'Running',
                        'waiting': 'Waiting',
                        'terminated': 'Terminated',
                        'pending': 'Pending',
                        'succeeded': 'Succeeded',
                        'failed': 'Failed',
                        'unknown': 'Unknown',
                        'crashloopbackoff': 'CrashLoopBackOff',
                        'imagepullbackoff': 'ImagePullBackOff'
                    }
                    pod_details['details']['STATUS'] = next((status_map[key] for key in state if key in status_map), 'N/A')
                    pod_details['details']['RESTART'] = container_status.get('restartCount', 'N/A')
                pod_details['details']['AGE'] = pod['metadata'].get('creationTimestamp', 'N/A')
            pods_info.append(pod_details)

    return pods_info

def get_desired_count(project, appname):
    cmd = f"oc get replicaset -n {project} -l app={appname} -o=jsonpath=" + '{.items[0].metadata.annotations.deployment\.kubernetes\.io/desired-replicas}'
    return run_command(cmd)

def get_deployments(project):
    cmd = f'oc get deployments -n {project}'
    output = run_command(cmd)
    return output.splitlines()

def create_project_dict(project, deployments):
    project_dict = {project: {'deployments': []}}
    for deployment in deployments:
        deployment_info = extract_deployment_info(deployment)
        if deployment_info:
            desired_count = get_desired_count(project, deployment_info['appname'])
            deployment_info['desired_count'] = desired_count
            deployment_info['pods'] = get_pods_info(project, deployment_info['appname'])
            project_dict[project]['deployments'].append(deployment_info)
    return project_dict

def extract_deployment_info(deployment):
    parts = deployment.split()
    if len(parts) == 5 and parts[0] != 'NAME' and any(part.strip() for part in parts):
        return {
            "appname": parts[0],
            "details": {
                "READY": parts[1],
                "UP-TO-DATE": parts[2],
                "AVAILABLE": parts[3],
                "AGE": parts[4]
            }
        }
    else:
        return {}

def generate_project_names(project1, envs, SONs):
    print("Genere les namespaces")
    projectn = []
    for env in envs:
        if env in SONs:
            for son_env in SONs[env]:
                projectn.append(project1 + env + '-' + son_env)
        else:
            print(f' {env} not found')
    return projectn

def filter_prjndict(projndict, proj_list, app_list, status_list, filter_mode):
    prjndict_filtered = {}
    for project, data in projndict.items():
        if filter_mode == "exclude":
            if any(project.startswith(excl) for excl in proj_list):
                continue
        elif filter_mode == "include":
            if not any(project.startswith(incl) for incl in proj_list):
                continue
        deployments_filtered = []
        for deployment in data['deployments']:
            if filter_mode == "exclude":
                if any(deployment['appname'].startswith(excl) for excl in app_list):
                    continue
            elif filter_mode == "include":
                if not any(deployment['appname'].startswith(incl) for incl in app_list):
                    continue
            deployments_filtered.append(deployment)
        if deployments_filtered:
            prjndict_filtered[project] = {'deployments': deployments_filtered}
    return prjndict_filtered

def scale_deployment(project, appname, replicas=0, simulate=False):
    cmd = f'oc scale --replicas={replicas} deployment/{appname} -n {project}'
    if simulate:
        print(f"Simulating: {cmd}")
        return "Simulated scaling"
    else:
        result = run_command(cmd)
        return result

def check_deployment_status(project, appname, desired_count, simulate=False):
    if simulate:
        print(f"Simulating: Checking deployment status for {appname} in {project}")
        return True
    else:
        cmd = f'oc get pods -n {project} -l app={appname} -o json'
        output = run_command(cmd)
        pod_info = json.loads(output)
        available_replicas = len(pod_info['items'])
        if available_replicas > desired_count:
            return False
        return True

def display_deployment_status(project_dict):
    table = PrettyTable()
    table.field_names = ["Project", "Application", "Pod Name", "Status", "Desired Count"]
    for project, data in project_dict.items():
        for deployment in data['deployments']:
            appname = deployment['appname']
            desired_count = deployment['desired_count']
            for pod in deployment['pods']:
                podname = pod['podname']
                status = pod['details']['STATUS']
                table.add_row([project, appname, podname, status, desired_count])
    print(table)
    return table

def export_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
def import_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
def export_to_txt(table, filename):
    with open(filename, 'w') as f:
        f.write(str(table))
def generate_filename(openshift_login,prefix, mode, project, extension):
    date_str = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{RD_JOBID_NAME}_{openshift_login}_{date_str}_{prefix}_{mode}_{project}_fil.{extension}"
    return filename

def manage_deployments(mode1, prjndict_filtered, batch_size=5, used_json_status_before_stop=None, nb_scale_desired=None, filter_mode="exclude",simulate=False, max_replicas=4):
    print(f"Démarrage du mode : {mode1}")
    failed_deployments = []
    prjndict_filtered_before = prjndict_filtered.copy()
    processed_deployments = set()
    desired_count_dict = {}
    if used_json_status_before_stop:
        desired_count_dict = import_from_json(used_json_status_before_stop)
    for project, data in prjndict_filtered.items():
        appname_to_deployments = defaultdict(list)
        for deployment in data['deployments']:
            appname_to_deployments[deployment['appname']].append(deployment)

        for appname, deployments in appname_to_deployments.items():
            deployments = sorted(deployments, key=lambda deployment: int(deployment['desired_count']) > 1 if deployment['desired_count'].isdigit() else 0)
            for i in range(0, len(deployments), batch_size):
                batch = deployments[i:i+batch_size]
                for deployment in batch:
                    if deployment['appname'] in processed_deployments:
                        continue
                    processed_deployments.add(deployment['appname'])

                    print(f"=> Traitement du déploiement applicatif : {deployment['appname']} dans le projet : {project}")
                    desired_count = int(deployment['desired_count']) if deployment['desired_count'].isdigit() else 0
                    if mode1 == "start":
                        for dep in desired_count_dict.get(project, {}).get('deployments', []):
                            if dep['appname'] == deployment['appname']:
                                desired_count = int(dep.get('desired_count', '1'))
                                break
                        if nb_scale_desired is not None:
                            desired_count = min(nb_scale_desired, max_replicas)
                    status = check_deployment_status(project, appname, desired_count if deployment['desired_count'].isdigit() else 0,simulate=simulate)
                    if mode1 == "stop" and status:
                        print(f"Arrêt du déploiement : {deployment['appname']} dans le projet : {project}")
                        scale_deployment(project, appname, 0,simulate=simulate)
                        time.sleep(1)
                    elif mode1 == "start":
                        print(f"Démarrage du déploiement : {deployment['appname']} avec {desired_count} réplicas dans le projet : {project}")
                        result = scale_deployment(project, appname, desired_count,simulate=simulate)
                        if 'error' in result:
                            raise Exception(f"Échec du déploiement avec l'erreur : {result}")
                        time.sleep(1)
                    elif mode1 == "restart":
                        print(f"Redémarrage du déploiement : {deployment['appname']} avec {desired_count} réplicas dans le projet : {project}")
                        if status:
                            result=scale_deployment(project, appname, 0,simulate=simulate)
                            time.sleep(2)
                            print(f"  ==> Retour commande d'arrêt: oc scale --replicas=0 -n {project} output: {result} ")
                        result = scale_deployment(project, appname, desired_count,simulate=simulate)
                        print(f"  ==> Retour commande de démarrage: oc scale --replicas={desired_count} -n {project} output: {result}")
                    else:
                        raise Exception(f'Mode invalide : {mode1}')
                    print("\n")
                    time.sleep(30)
                    deployments = get_deployments(project)
                    project_dict = create_project_dict(project, deployments)
                    prjndict_filtered.update(project_dict)
                    prjndict_filtered = filter_prjndict(prjndict_filtered, lstproj, lstpod, lstSTATUS, filter_mode)
                for deployment in batch:
                    for _ in range(3):
                        status = check_deployment_status(project, appname, desired_count if deployment['desired_count'].isdigit() else 0,simulate=simulate)
                        if status:
                            break
                        time.sleep(20)
                    else:
                        failed_deployments.append(deployment)
                time.sleep(5)
    prjndict_filtered_after = prjndict_filtered
    for deployment in failed_deployments:
        print(f"Échec du démarrage du déploiement : {deployment['appname']}")

    prjndict_filtered_after = prjndict_filtered
    filename = generate_filename(openshift_login,"APRES", mode1, project, "json")
    export_to_json(prjndict_filtered_after, filename)
    print(f"Fichier JSON APRES {mode1} exporté : {os.path.abspath(filename)}")
    table = display_deployment_status(prjndict_filtered_after)
    filename = generate_filename(openshift_login,"APRES", mode1, project, "txt")
    export_to_txt(table, filename)
    print(f"Fichier TXT APRES {mode1} exporté : {os.path.abspath(filename)}")

    if mode1 == "stop":
        print("\nA UTILISER SI BESOIN en MODE START POUR RESTAURER LA VALEUR DU SCALE INITIAL SUITE A L'UTILISATION DU MODE STOP")
        print(f"Chemin vers le fichier JSON AVANT : {filename_before}")

openshift_login=login_to_openshift(token1, server1)
projectn = generate_project_names(project1, MYENV, MYSON)
prjndict = {}
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_project = {executor.submit(process_project, project): project for project in projectn}
    for future in concurrent.futures.as_completed(future_to_project):
        project = future_to_project[future]
        try:
            project_dict = future.result()
            prjndict.update(project_dict)
        except Exception as exc:
            print(f'Le projet {project} a généré une exception: {exc}')

prjndict_filtered = filter_prjndict(prjndict, lstproj, lstpod, lstSTATUS, filter_mode)
output1 = manage_deployments(mode1=mod, prjndict_filtered=prjndict_filtered, batch_size=5, used_json_status_before_stop=used_json_status_before_stop, nb_scale_desired=nb_scale_desired, filter_mode=filter_mode,simulate=simulate)
