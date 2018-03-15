class MastermindSchema:
    _schema = {"$schema": "http://json-schema.org/draft-07/schema#", 
    "title": "mastermindSchema",
    "description": "A schema used to validate mastermind.yml translated to JSON",
    "type": "object",
    "properties": {
	"name": { "type": "string" },
	"version": { "type": "string" },
	"description": { "type": "string" },
	"protocol_type": { "type": "string" },
	"ngsi_version": { "type": "integer" },
	"environment_variables": {
	    "type": "array",
	    "items": {
		"type": "object",
		"properties": {
		    "variable": { "type": "string" },
		    "name": { "type": "string" },
		    "description": { "type": "string" },
		    "required": { "type": "boolean" },
		    "managed": { "type": "boolean" },
		    "default": { "type": "string" }
		},
		"minProperties": 6,
		"additionalProperties": False
	    }
	},
	"services": {
	    "type": "array",
	    "items": {
		"type": "object",
		"properties": {
		    "service_type": { "type": "string" },
		    "name": { "type": "string" },
		    "description": { "type": "string" },
		    "required": { "type": "boolean" },
		    "managed": { "type": "boolean" },
		    "retrieve": { "type": "string"},
		    "as": { "type": "string" }
		},
		"minProperties": 7,
		"additionalProperties": False
	    }
	}
    },
    "minProperties": 7,
    "additionalProperties": False
    }                
