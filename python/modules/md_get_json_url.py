#!/usr/bin/python3
#GB-0001 github

import json
import requests
from requests.exceptions import ConnectionError
import socket
import time

def mdgetJson(jsonurl):
    try:
        resp = requests.get(url=jsonurl,timeout=3)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.ConnectionError:
        pass
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return "Error: " + str(e)
    else:
        try:
            resp = requests.get(url=jsonurl,timeout=3)
            resp.raise_for_status()
            data = resp.json()
            print("md", data)
        except request.exceptions.HTTPError as e:
            # Whoops it wasn't a 200
            return "Error: " + str(e)
        except requests.ConnectionError as e:
            resp.status_code = "Connection refused"
            time.sleep(2)
            pass
        except requests.exceptions.RequestException as e:
            pass
        except requests.RequestEception as e:
            resp.status_code = "Error"
            pass
        except requests.Timeout as e:
            resp.status_code = "Time out"
            time.sleep(5)
            pass
        except requests.exceptions.ConnectionError as e:
            pass
        except ConnectionError as e:
            return "Error: " + str(e)
        except (JSONDecodeError, json.JSONDecodeError):
            pass
        except Exception as e:
            return "Error " + str(e)
        except ValueError:
            return "Error: " + str(e)
        except timeout:
            pass
        except MaxRetryError:
            pass