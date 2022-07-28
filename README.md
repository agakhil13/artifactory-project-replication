## Script.py will migrates artifactory projects from production to staging environments

### Setting up an environment for script execution:
- Runtime Python 3.x is needed with 'requests' and 'json' package.
- Under the function "main", following variables need to be modified for fetching token:
  - PROD_TOKEN: Admin token from prod environment,
  - PROD_BASE_URL: Prod base url
  - STA_TOKEN: Admin toke from stagin environment.
  - STA_BASE_URL: Staging base url

### Instructions/output to execute the script:
- python3 SCRIPT_NAME.py
