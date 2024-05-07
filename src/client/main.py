import requests
import time
import json

from config import logger, config

def __make_http_call(url, headers=None) -> dict:
    try:
        response = requests.get(url, headers=headers)
        result = json.loads(response.text)
        result["elapsed"] = str(response.elapsed)
        return result
    except requests.exceptions.RequestException as err:
        logger.error(f"Error making call to {url}: {err}")
        return {"version": "ERROR", "elapsed": "ERROR"}
    except json.JSONDecodeError as err:
        logger.error(f"Error decoding JSON response to dict {url}: {response.text}: {err}")
        return {"version": "ERROR", "elapsed": "ERROR"}

def main() -> None:
    interval = int(config.poll_interval)

    while True:
        with open(config.output_file, "a") as f:
            output = {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) }
            for endpoint in config.endpoints:
                response_data = __make_http_call(url=endpoint["url"], headers=endpoint["headers"])
                output[endpoint["id"]] = {
                    "version": response_data["version"], 
                    "elapsed": response_data["elapsed"]
                }

            logger.info(json.dumps(output))
            f.write(json.dumps(output) + "\n")

            time.sleep(interval)

if __name__ == "__main__":
    main()
