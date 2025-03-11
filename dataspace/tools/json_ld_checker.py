from pyld import jsonld
import json

def validate_jsonld(jsonld_data):
    try:
        options = {"expandContext": {}, "documentLoader": "disabled"}

        expanded = jsonld.expand(jsonld_data, options)
        
        if expanded:
            print("Valid JSON-LD")
            print("Expanded:", json.dumps(expanded, indent=2))
            return True
        else:
            print("Invalid JSON-LD")
            return False
    
    except jsonld.JsonLdError as e:
        print(f"Error: {e}")
        return False
    
jsonld_input = {
  "@context": {
    "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
  },
  "@type": "ContractDefinition",
  "@id": "757b0cf4-6b2a-418a-b71a-f701665be884",
  "accessPolicyId": "dpp-usage-policy-example",
  "contractPolicyId": "dpp-usage-policy-example",
  "assetsSelector": 
    {
      "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
      "operator": "=",
      "operandRight": "5f179b28-e6cb-479b-a062-c12ec280993d"
    }
  
}

# Validate JSON-LD
validate_jsonld(jsonld_input)