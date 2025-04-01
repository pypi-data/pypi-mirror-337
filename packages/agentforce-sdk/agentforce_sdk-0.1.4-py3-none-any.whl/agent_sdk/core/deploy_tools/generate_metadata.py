"""Metadata generation utilities for Salesforce agent deployment."""

import argparse
import json
import os
import re
import shutil
import zipfile
from xml.sax.saxutils import escape
from typing import Dict, List
import logging

import requests
from simple_salesforce import Salesforce
from .deploy_zipfile import login_to_salesforce

logger = logging.getLogger(__name__)

class MetadataGenerator:
    """Handles generation of Salesforce metadata for agent deployment."""
    
    API_VERSION = "63.0"
    SCHEMA_URLS = {
        "input": "https://cms.salesforce.com/types/lightning__copilotActionInput",
        "output": "https://cms.salesforce.com/types/lightning__copilotActionOutput"
    }
    
    def __init__(self, template_dir: str = 'templates', base_output_dir: str = None):
        """Initialize the metadata generator."""
        self.template_dir = template_dir
        self.base_output_dir = base_output_dir or os.getcwd()
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary output directories."""
        os.makedirs(self.base_output_dir, exist_ok=True)
        for dir_name in ['bots', 'classes', 'genAiFunctions', 'genAiPlugins', 'genAiPlanners']:
            os.makedirs(os.path.join(self.base_output_dir, dir_name), exist_ok=True)
    
    def generate_package_xml(self, version: str = None, metadata_types: List[str] = None) -> None:
        """Generate package.xml file.
        
        Args:
            version (str): API version to use
            metadata_types (List[str]): List of metadata types to include
        """
        if not metadata_types:
            metadata_types = [
                'ApexClass',
                'Bot',
                'BotVersion',
                'GenAiFunction',
                'GenAiPlanner',
                'GenAiPlugin',
                'RemoteSiteSetting'
            ]
        
        version = version or self.API_VERSION
        
        types_xml = ''
        for metadata_type in metadata_types:
            types_xml += f"""    <types>
        <members>*</members>
        <name>{metadata_type}</name>
    </types>
"""
        
        package_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
{types_xml}    <version>{version}</version>
</Package>
"""
        
        with open(os.path.join(self.base_output_dir, "package.xml"), "w", encoding="utf-8") as f:
            f.write(package_xml)
    
    def generate_apex_class(self, class_name: str, content: str) -> None:
        """Generate Apex class files.
        
        Args:
            class_name (str): Name of the Apex class
            content (str): Content of the Apex class
        """
        classes_dir = os.path.join(self.base_output_dir, "classes")
        class_name = self._sanitize_name(class_name)
        # Write class file
        with open(os.path.join(classes_dir, f"{class_name}.cls"), "w", encoding="utf-8") as f:
            f.write(content)
        
        # Write meta file
        meta_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>{self.API_VERSION}</apiVersion>
    <status>Active</status>
</ApexClass>
"""
        with open(os.path.join(classes_dir, f"{class_name}.cls-meta.xml"), "w", encoding="utf-8") as f:
            f.write(meta_xml)
    
    def generate_function_metadata(self, function_data: Dict) -> None:
        """Generate metadata for a GenAI function.
        
        Args:
            function_data (Dict): Function configuration data
        """
        function_name =  self._sanitize_name(function_data['name'])
        function_dir = os.path.join(self.base_output_dir, f"genAiFunctions/{function_name}")
        os.makedirs(function_dir, exist_ok=True)
        
        # Generate function metadata XML
        function_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<GenAiFunction xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>{escape(function_data.get('description', function_name))}</description>
    <invocationTarget>{escape(function_data.get('invocationTarget', function_name))}</invocationTarget>
    <invocationTargetType>{function_data.get('action_type', 'apex').lower()}</invocationTargetType>
    <isConfirmationRequired>false</isConfirmationRequired>
    <masterLabel>{escape(function_name)}</masterLabel>
</GenAiFunction>
"""
        with open(os.path.join(function_dir, f"{function_name}.genAiFunction-meta.xml"), "w", encoding="utf-8") as f:
            f.write(function_xml)
        
        # Generate input/output schemas
        for schema_type in ['input', 'output']:
            schema_dir = os.path.join(function_dir, schema_type)
            os.makedirs(schema_dir, exist_ok=True)
            
            schema = self._create_schema(
                schema_type=schema_type,
                properties=function_data.get(f'{schema_type}s', []),
                is_known_action=function_data.get('is_known_action', False)
            )
            
            with open(os.path.join(schema_dir, "schema.json"), "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=4)
    
    def _create_schema(self, schema_type: str, properties: List[Dict], is_known_action: bool) -> Dict:
        """Create input/output schema for a function.
        
        Args:
            schema_type (str): Type of schema ('input' or 'output')
            properties (List[Dict]): List of property configurations
            is_known_action (bool): Whether this is a known action
            
        Returns:
            Dict: Schema configuration
        """
        schema = {
            "unevaluatedProperties": False,
            "properties": {},
            "lightning:type": "lightning__objectType"
        }
        
        if schema_type == 'input':
            schema["required"] = []
        
        if is_known_action:
            for prop in properties:
                name = prop[f'{schema_type}Name']
                desc = prop[f'{schema_type}_description']
                
                prop_schema = {
                    "title": name,
                    "description": desc,
                    "lightning:type": "lightning__textType",
                    "$ref": "sfdc:propertyType/lightning__textType",
                    "lightning:isPII": False
                }
                
                if schema_type == 'output':
                    prop_schema.update({
                        "copilotAction:isDisplayable": True,
                        "copilotAction:isUsedByPlanner": True
                    })
                else:
                    prop_schema["copilotAction:isUserInput"] = False
                
                schema["properties"][name] = prop_schema
        else:
            # Default schema for unknown actions
            if schema_type == 'input':
                schema["properties"].update({
                    "query": {
                        "title": "query",
                        "description": "Input parameters for the function",
                        "lightning:type": "lightning__textType",
                        "$ref": "sfdc:propertyType/lightning__textType",
                        "lightning:isPII": False,
                        "copilotAction:isUserInput": False
                    },
                    "sample_response": {
                        "title": "sample response",
                        "description": "Example response format",
                        "lightning:type": "lightning__textType",
                        "$ref": "sfdc:propertyType/lightning__textType",
                        "lightning:isPII": False,
                        "copilotAction:isUserInput": False
                    }
                })
                schema["required"] = ["query", "sample_response"]
            else:
                schema["properties"]["generatedOutput"] = {
                    "title": "generatedOutput",
                    "description": "Generated output from the function",
                    "lightning:type": "lightning__textType",
                    "$ref": "sfdc:propertyType/lightning__textType",
                    "lightning:isPII": False,
                    "copilotAction:isDisplayable": True,
                    "copilotAction:isUsedByPlanner": True
                }
        
        return schema
    
    def generate_plugin_metadata(self, topic_data: Dict) -> None:
        """Generate metadata for a GenAI plugin (topic).
        
        Args:
            topic_data (Dict): Topic configuration data
        """
        topic_name = self._sanitize_name(topic_data.get('Topic', topic_data.get('name')))
        
        plugin_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<GenAiPlugin xmlns="http://soap.sforce.com/2006/04/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <description>{escape(topic_data['description'])}</description>
    <developerName>{escape(topic_name)}</developerName>
    <language>en_US</language>
    <masterLabel>{escape(topic_data.get('Topic', topic_data.get('name')))}</masterLabel>
    <pluginType>Topic</pluginType>
    <scope>{escape(topic_data.get('Scope', topic_data.get('scope')))}</scope>
"""
        
        # Add functions
        for action in topic_data.get('actions', []):
            plugin_xml += f"""    <genAiFunctions>
        <functionName>{self._sanitize_name(action['name'])}</functionName>
    </genAiFunctions>
"""
        
        # Add instructions
        for i, instruction in enumerate(topic_data.get('instructions', [])):
            plugin_xml += f"""    <genAiPluginInstructions>
        <description>{escape(instruction)}</description>
        <developerName>Instruction{i + 1}</developerName>
        <language xsi:nil="true"/>
        <masterLabel>Instruction {i + 1}</masterLabel>
    </genAiPluginInstructions>
"""
        
        plugin_xml += "</GenAiPlugin>"
        
        with open(os.path.join(self.base_output_dir, "genAiPlugins", f"{topic_name}.genAiPlugin"), "w", encoding="utf-8") as f:
            f.write(plugin_xml)
    
    def generate_planner_metadata(self, bot_name: str, bot_label: str, bot_description: str, topics: List[str], 
                                version: str = 'v1') -> None:
        """Generate metadata for a GenAI planner.
        
        Args:
            bot_name (str): Name of the bot
            bot_label (str): Label for the bot
            bot_description (str): Description of the bot
            topics (List[str]): List of topic names
            version (str): Version string
        """
        planner_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<GenAiPlanner xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>{escape(bot_description)}</description>
"""
        
        for topic in topics:
            planner_xml += f"""    <genAiPlugins>
        <genAiPluginName>{escape(topic)}</genAiPluginName>
    </genAiPlugins>
"""
        
        planner_xml += f"""    <masterLabel>{escape(bot_label)}</masterLabel>
    <plannerType>AiCopilot__ReAct</plannerType>
</GenAiPlanner>
"""
        
        with open(os.path.join(self.base_output_dir, "genAiPlanners", f"{bot_name}_{version}.genAiPlanner"), "w", encoding="utf-8") as f:
            f.write(planner_xml)
    
    def generate_bot_metadata(self, bot_name: str, bot_label: str, bot_description: str, company_name: str,
                            site_url: str, bot_username: str = None, sample_utterances: List[str] = None,
                            agent_type: str = None, agent_template_type: str = None) -> None:
        """Generate metadata for a bot.
        
        Args:
            bot_name (str): Name of the bot
            bot_label (str): Label for the bot
            bot_description (str): Description of the bot
            company_name (str): Company name
            site_url (str): Site URL
            bot_username (str, optional): Bot username
            sample_utterances (List[str], optional): List of sample utterances
            agent_type (str, optional): Type of agent ('Internal' or 'External')
        """
        with open(os.path.join(self.template_dir, "bots/SampleBot.bot"), "r", encoding="utf-8") as f:
            bot_xml = f.read()
        
        bot_xml = bot_xml.replace("AGENTFORCE_BOT_NAME", escape(bot_name))
        bot_xml = bot_xml.replace("AGENTFORCE_COMPANY_NAME", escape(company_name))
        bot_xml = bot_xml.replace("AGENTFORCE_COMPANY_WEBSITE", escape(site_url))
        bot_xml = bot_xml.replace("AGENTFORCE_DESCRIPTION", escape(bot_description))
        
        # Handle agent type and template type
        is_internal = agent_type and agent_type.lower() == 'internal'
        if is_internal:
            bot_xml = bot_xml.replace("AGENTFORCE_TYPE", 'InternalCopilot')
            bot_xml = bot_xml.replace("AGENTFORCE_TEMPLATE_TYPE", 'Employee')
        else:
            bot_xml = bot_xml.replace("AGENTFORCE_TYPE", 'ExternalCopilot')
            bot_xml = bot_xml.replace("AGENTFORCE_TEMPLATE_TYPE", 'EinsteinServiceAgent')
            
        if agent_template_type is not None:
            bot_xml = bot_xml.replace("AGENTFORCE_TEMPLATE_TYPE", agent_template_type)
        
        if bot_username:
            bot_xml = bot_xml.replace("AGENTFORCE_USER_NAME", f"<botUser>{escape(bot_username)}</botUser>")
        else:
            bot_xml = bot_xml.replace("AGENTFORCE_USER_NAME", '')
        
        if sample_utterances:
            utterances_str = '"' + '"\n- "'.join(sample_utterances) + '"'
            bot_xml = bot_xml.replace("AGENTFORCE_SAMPLE_UTTERANCES", escape(utterances_str))
        else:
            bot_xml = bot_xml.replace("AGENTFORCE_SAMPLE_UTTERANCES", '')
        
        with open(os.path.join(self.base_output_dir, "bots", f"{bot_name}.bot"), "w", encoding="utf-8") as f:
            f.write(bot_xml)
    
    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Sanitize a name for use in Salesforce metadata.
        
        Args:
            name (str): Name to sanitize
            
        Returns:
            str: Sanitized name
        """
        name = name.replace(' ', '_').replace('-', '_').replace('&', 'and')
        return re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_')
    
    def generate_agent_metadata(self, input_json: Dict, site_url: str = '', company_name: str = '',
                              bot_api_name: str = 'TestFlow', bot_username: str = None,
                              username: str = None, password: str = None, domain: str = None,
                              asa_agent: bool = False) -> None:
        """Generate all metadata for an agent.
        
        Args:
            input_json (Dict): Agent configuration
            site_url (str): Site URL
            company_name (str): Company name
            bot_api_name (str): API name for the bot
            bot_username (str, optional): Bot username
            username (str, optional): Salesforce username
            password (str, optional): Salesforce password
            domain (str, optional): Salesforce domain
            asa_agent (bool): Whether this is an ASA agent
        """
        # Generate package.xml
        version = "63.0" 
        bot_api_name = self._sanitize_name(bot_api_name)
        company_name = self._sanitize_name(company_name)
        self.generate_package_xml(version=version)
        
        # Generate Apex classes
        self._generate_apex_classes(bot_api_name, company_name, site_url)
        
        # Process topics and generate metadata
        topics = []
        bot_description = input_json.get('AI_Agent_Description', input_json.get('description', 'Dreamforce 24'))
        sample_utterances = input_json.get('Sample_Utterances', input_json.get('sample_utterances', ['What is Salesforce Agentforce?']))
        agent_type = input_json.get('agent_type', 'External')
        
        input_topics = input_json.get('items', input_json.get('topics', input_json.get('Topics', [])))
        if not isinstance(input_topics, list):
            input_topics = input_topics.get('Topics', input_topics.get('topics', []))
        
        for topic_data in input_topics:
            # Generate plugin metadata
            self.generate_plugin_metadata(topic_data)
            topics.append(self._sanitize_name(topic_data.get('Topic', topic_data.get('name'))))
            
            # Generate function metadata for each action
            for action in topic_data.get('actions', []):
                action['invocationTarget'] = bot_api_name + '_LLMMock'
                self.generate_function_metadata(action)
        
        # Generate planner metadata
        self.generate_planner_metadata(
            bot_name=bot_api_name,
            bot_label=bot_api_name.replace('_', ' '),
            bot_description=bot_description,
            topics=topics
        )
        if agent_type != 'Internal':
            bot_username = verify_asa_user(username, password, domain)
        # Generate bot metadata
        self.generate_bot_metadata(
            bot_name=bot_api_name,
            bot_label=bot_api_name.replace('_', ' '),
            bot_description=bot_description,
            company_name=company_name,
            site_url=site_url,
            bot_username=bot_username,
            sample_utterances=sample_utterances,
            agent_type=agent_type
        )
        
        # Create deployment zip
        self.create_deployment_zip()
    
    def _generate_apex_classes(self, bot_api_name: str, company_name: str, site_url: str) -> None:
        """Generate required Apex classes.
        
        Args:
            bot_api_name (str): API name for the bot
            company_name (str): Company name
            site_url (str): Site URL
        """
        # Generate AtlasRAG class
        with open(os.path.join(self.template_dir, "classes/AtlasRAG.cls"), "r", encoding="utf-8") as f:
            atlas_rag_content = f.read()
        
        atlas_rag_content = atlas_rag_content.replace("<bot-api-name>", bot_api_name)
        atlas_rag_content = atlas_rag_content.replace("<company-name>", re.sub(r'[^A-Za-z0-9\s]', '', company_name))
        atlas_rag_content = atlas_rag_content.replace("<brave_api_key>", os.environ.get("BRAVE_API_KEY", ''))
        atlas_rag_content = atlas_rag_content.replace("<site_url>", site_url)
        atlas_rag_content = atlas_rag_content.replace("<agent_api_name>", bot_api_name)
        
        self.generate_apex_class(f"{bot_api_name}_AtlasRAG", atlas_rag_content)
        
        # Generate LLMMock class
        with open(os.path.join(self.template_dir, "classes/LLMMock.cls"), "r", encoding="utf-8") as f:
            llm_mock_content = f.read()
        
        llm_mock_content = llm_mock_content.replace("BOTAPINAME", bot_api_name)
        llm_mock_content = llm_mock_content.replace("AGENTFORCE_COMPANY_NAME", re.sub(r'[^A-Za-z0-9\s]', '', company_name))
        
        self.generate_apex_class(f"{bot_api_name}_LLMMock", llm_mock_content)
    
    def create_deployment_zip(self) -> str:
        """Create a ZIP file containing all generated metadata.
        
        Returns:
            str: Path to the created ZIP file
        """
        zip_path = f"{self.base_output_dir}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.base_output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.base_output_dir)
                    zipf.write(file_path, arcname)
        return zip_path

def zip_folder(folder_path: str, output_zip: str) -> None:
    """Create a zip file from a folder."""
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

def verify_asa_user(username: str, password: str, domain: str) -> str:
    """Verify or create an ASA user with required permissions."""
    PROFILE = "Einstein Agent User"
    PERM_SETS = ["AgentforceServiceAgentBase", "AgentforceServiceAgentUser"]
    try:
        session_id, instance_url = login_to_salesforce(username, password, domain)
        domain_instance = instance_url.replace("https://", "").split('.')[0]
        asa_user_name = f"agentcreator-asa@{domain_instance}.com"
        
        sf = Salesforce(instance_url=instance_url, session_id=session_id)
        perm_set_ids = [
            sf.query(f"SELECT Id FROM PermissionSet WHERE Name = '{perm_set}' LIMIT 1")['records'][0]['Id']
            for perm_set in PERM_SETS
        ]
        
        user_fetch_query = sf.query(f"SELECT Id, Username FROM User WHERE Username = '{asa_user_name}' LIMIT 1")
        if user_fetch_query['records']:
            asa_user_id = user_fetch_query['records'][0]['Id']
            if _assign_permsets_user(sf, asa_user_id, perm_set_ids):
                return asa_user_name
            return None
        
        profile_query = sf.query(f"SELECT Id FROM Profile WHERE Name = '{PROFILE}'")
        if not profile_query['records']:
            logger.error(f"Profile '{PROFILE}' not found.")
            return None
        
        profile_id = profile_query['records'][0]['Id']
        asa_user = sf.User.create({
            'Username': asa_user_name,
            'Alias': 'acasa',
            'Email': 'noreply@example.com',
            'FirstName': 'AgentCreator ASA',
            'LastName': 'User',
            'ProfileId': profile_id,
            'TimeZoneSidKey': 'America/Los_Angeles',
            'LocaleSidKey': 'en_US',
            'LanguageLocaleKey': 'en_US',
            'EmailEncodingKey': 'UTF-8'
        })
        
        if asa_user and _assign_permsets_user(sf, asa_user['id'], perm_set_ids):
            return asa_user_name
        return None

    except Exception as e:
        logger.error(f"Error creating ASA user: {e}")
        return None

def _assign_permsets_user(sf: Salesforce, user_id: str, perm_set_ids: List[str]) -> bool:
    """Assign permission sets to a user."""
    try:
        assigned_perm_sets_query = sf.query(
            f"SELECT PermissionSetId FROM PermissionSetAssignment WHERE AssigneeId = '{user_id}'"
        )
        assigned_perm_sets = [record['PermissionSetId'] for record in assigned_perm_sets_query['records']]
        
        for perm_set_id in perm_set_ids:
            if perm_set_id not in assigned_perm_sets:
                sf.PermissionSetAssignment.create({
                    'AssigneeId': user_id,
                    'PermissionSetId': perm_set_id
                })
                logger.info(f"Assigned Permission set {perm_set_id} to user.")
        return True
    except Exception as e:
        logger.error(f"Error assigning permission sets: {e}")
        return False

def generate_agent_metadata(
        input_json: Dict,
        base_output_dir: str,
        template_dir: str = 'templates',
        site_url: str = '',
        company_name: str = '',
        bot_api_name: str = 'TestFlow',
        bot_username: str = None,
        username: str = None,
        password: str = None,
        domain: str = None,
        asa_agent: bool = False) -> None:
    """Generate all metadata for an agent."""
    generator = MetadataGenerator(template_dir=template_dir, base_output_dir=base_output_dir)
    generator.generate_agent_metadata(
        input_json=input_json,
        site_url=site_url,
        company_name=company_name,
        bot_api_name=bot_api_name,
        bot_username=bot_username,
        username=username,
        password=password,
        domain=domain,
        asa_agent=asa_agent
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="Path to the input JSON file")
    parser.add_argument("output_dir", help="Path to the output directory")
    parser.add_argument("template_dir", help="Path to the template directory")
    
    args = parser.parse_args()
    
    with open(args.json_file, "r") as f:
        json_data = json.load(f)
    
    generate_agent_metadata(json_data, args.output_dir, args.template_dir)
    logger.info(f"Salesforce metadata generated successfully in: {args.output_dir}")
