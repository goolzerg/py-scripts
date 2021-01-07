
## List of command line arguments

Long name | Short | Description                  
--------| -------- | --------                       
--output  | -o | Output file, where variables will be written              
--input  | -i | Input file (JSON), which will be parsed
--root  | -r | Root catalog in vault (engine)
--method   | -m | Method which will be used (GET/PUT)

&nbsp;

## List of mandatory variables

Name | Description | Values   
--------| -------- | --------                       
VAULT_ADDR  | Vault endpoint | ``http://vault:8200``              
VAULT_TOKEN  | Vault token with policy to root catalog (engine) | ``s.kUHgntQIjCIPJPQHdkKACFk3``
SERVICE_NAME  | Service name | ``uploader_service``
ENV_VAULT  | Environment from which variables will be fetched | ``test/stage/prod``

&nbsp;

### GET usage example
```
docker run -v /service_variables.env:/service_variables.env  \
-e VAULT_ADDR=http://vault:8200 -e VAULT_TOKEN=s.3Bl4FHlBd8kAAWY9JbHOnPrA \
-e SERVICE_NAME=uploader_service -e ENV_VAULT=test \
<image_name> --method=get --root=services  --output=/service_variables.env
```
Then we should specify envfile inside docker-compose file
```
web:
  env_file:
    - /service_variables.env
```

Output example:
![GitHub Logo](/vault_get_secret/pic/vault_get.png)

&nbsp;

### PUT usage example

```
docker run -v /service_variables.json:/service_variables.json  \
-e VAULT_ADDR=http://vault:8200 -e VAULT_TOKEN=s.3Bl4FHlBd8kAAWY9JbHOnPrA \
-e SERVICE_NAME=uploader_service -e ENV_VAULT=test \
<image_name> --method=put --root=services  --input=/service_variables.json
```

Output example:
![GitHub Logo](/vault_get_secret/pic/vault_put.png)