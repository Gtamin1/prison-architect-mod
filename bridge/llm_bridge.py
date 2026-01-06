#!/usr/bin/env python3
"""
LLM Bridge for Prison Architect AI Mod

This bridge connects the Prison Architect Lua mod to Ollama (local LLM).
It monitors request files, processes them through Ollama, and writes responses.

Usage:
    python llm_bridge.py [--test] [--model MODEL_NAME]

Options:
    --test          Run in test mode (verify Ollama connection)
    --model NAME    Specify Ollama model (default: llama3)
    --debug         Enable debug logging
"""

import json
import time
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests

# Configuration
DEFAULT_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434"
REQUEST_FILE = "ai_bridge_request.json"
RESPONSE_FILE = "ai_bridge_response.json"
POLL_INTERVAL = 0.5  # seconds
PROCESSING_TIMEOUT = 30  # seconds

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class OllamaBridge:
    """Bridge between Prison Architect mod and Ollama LLM"""

    def __init__(self, model: str = DEFAULT_MODEL, debug: bool = False):
        self.model = model
        self.debug = debug
        self.base_url = OLLAMA_URL
        self.request_path = Path(REQUEST_FILE)
        self.response_path = Path(RESPONSE_FILE)
        self.last_request_time = 0

        if debug:
            logger.setLevel(logging.DEBUG)

        logger.info(f"Initializing Ollama Bridge with model: {model}")

    def check_ollama_status(self) -> bool:
        """Verify Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]

                logger.info(f"Ollama is running. Available models: {model_names}")

                # Check if our model is available
                if not any(self.model in name for name in model_names):
                    logger.warning(f"Model '{self.model}' not found. Available: {model_names}")
                    logger.info(f"Run: ollama pull {self.model}")
                    return False

                return True
            else:
                logger.error(f"Ollama returned status {response.status_code}")
                return False

        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama. Is it running?")
            logger.info("Start Ollama with: ollama serve")
            return False
        except Exception as e:
            logger.error(f"Error checking Ollama status: {e}")
            return False

    def generate_response(self, prompt: str) -> Optional[str]:
        """Send prompt to Ollama and get response"""
        try:
            logger.debug(f"Sending prompt to Ollama (length: {len(prompt)})")

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=PROCESSING_TIMEOUT
            )

            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()

                logger.debug(f"Received response (length: {len(generated_text)})")
                return generated_text
            else:
                logger.error(f"Ollama generation failed: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            return None
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None

    def build_decision_prompt(self, context: Dict[str, Any]) -> str:
        """Build a prompt for NPC decision making"""
        entity = context.get('entity', {})
        nearby = context.get('nearby', [])

        # Build personality description
        personality = entity.get('personality', 'Unknown')
        mood = entity.get('mood', 'neutral')
        entity_type = entity.get('type', 'NPC')

        prompt = f"""You are a {entity_type} in a prison with the personality: {personality}.

CURRENT STATE:
- Mood: {mood}
- Current action: {entity.get('currentAction', 'idle')}

"""

        # Add nearby entities
        if nearby:
            prompt += f"NEARBY ENTITIES ({len(nearby)}):\n"
            for other in nearby[:5]:  # Limit to 5 nearest
                prompt += f"- {other.get('type', 'NPC')} (Personality: {other.get('personality', 'Unknown')}, Distance: {other.get('distance', 0):.1f}m)\n"
            prompt += "\n"

        # Add gang info if applicable
        if entity.get('gang'):
            prompt += f"GANG AFFILIATION: {entity['gang']}\n\n"

        # Add available actions
        prompt += """AVAILABLE ACTIONS:
- wander: Move around randomly
- socialize: Talk to nearby people
- rest: Stand still and observe
- confront: Approach someone aggressively
- flee: Move away from threats
- plan: Think and strategize
- exercise: Use gym equipment
- eat: Go to canteen
- sleep: Rest in cell

Based on your personality and situation, what do you do?
Respond with ONLY the action name and a brief thought (1 sentence).

Format: ACTION: [action] | THOUGHT: [thought]
Example: ACTION: socialize | THOUGHT: I should strengthen my connections with nearby allies.
"""

        return prompt

    def build_conversation_prompt(self, context: Dict[str, Any]) -> str:
        """Build a prompt for NPC conversation"""
        entity = context.get('entity', {})
        target = context.get('target', {})

        personality = entity.get('personality', 'Unknown')
        target_personality = target.get('personality', 'Unknown')

        prompt = f"""You are {personality} talking to {target_personality} in prison.

YOUR PERSONALITY: {personality}
THEIR PERSONALITY: {target_personality}

RELATIONSHIP: {context.get('relationship', 'neutral')}

Generate a short, realistic prison conversation line (1-2 sentences).
Make it authentic to your personality and the prison environment.

Response:"""

        return prompt

    def parse_decision_response(self, response: str) -> Dict[str, str]:
        """Parse LLM response into action and thought"""
        try:
            # Expected format: ACTION: [action] | THOUGHT: [thought]
            if '|' in response:
                parts = response.split('|')
                action_part = parts[0].strip()
                thought_part = parts[1].strip() if len(parts) > 1 else ""

                action = action_part.replace('ACTION:', '').strip().lower()
                thought = thought_part.replace('THOUGHT:', '').strip()

                return {
                    'action': action,
                    'thought': thought
                }
            else:
                # Fallback parsing
                lines = response.strip().split('\n')
                return {
                    'action': lines[0].strip().lower(),
                    'thought': lines[1].strip() if len(lines) > 1 else ""
                }

        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            return {
                'action': 'wander',
                'thought': 'I need to think about this...'
            }

    def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request from the Lua mod"""
        request_type = request_data.get('type', 'decision')
        context = request_data.get('context', {})

        logger.info(f"Processing {request_type} request for entity {context.get('entity', {}).get('id', 'unknown')}")

        if request_type == 'decision':
            prompt = self.build_decision_prompt(context)
        elif request_type == 'conversation':
            prompt = self.build_conversation_prompt(context)
        else:
            logger.warning(f"Unknown request type: {request_type}")
            return {'error': 'Unknown request type'}

        # Generate response
        llm_response = self.generate_response(prompt)

        if llm_response is None:
            return {
                'error': 'LLM generation failed',
                'fallback': {
                    'action': 'wander',
                    'thought': 'System error...'
                }
            }

        # Parse response
        if request_type == 'decision':
            parsed = self.parse_decision_response(llm_response)
            return {
                'success': True,
                'data': parsed,
                'raw': llm_response
            }
        elif request_type == 'conversation':
            return {
                'success': True,
                'data': {
                    'dialogue': llm_response
                },
                'raw': llm_response
            }

    def monitor_requests(self):
        """Main loop: monitor for requests and process them"""
        logger.info("Starting request monitor loop...")
        logger.info(f"Watching for: {self.request_path.absolute()}")

        while True:
            try:
                # Check if request file exists and is new
                if self.request_path.exists():
                    file_mtime = self.request_path.stat().st_mtime

                    if file_mtime > self.last_request_time:
                        self.last_request_time = file_mtime

                        # Read request
                        with open(self.request_path, 'r') as f:
                            request_data = json.load(f)

                        # Process request
                        response_data = self.process_request(request_data)

                        # Write response
                        with open(self.response_path, 'w') as f:
                            json.dump(response_data, f, indent=2)

                        logger.info(f"Response written to {self.response_path}")

                        # Delete request file
                        self.request_path.unlink()

                # Sleep before next check
                time.sleep(POLL_INTERVAL)

            except KeyboardInterrupt:
                logger.info("Shutting down bridge...")
                break
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                time.sleep(POLL_INTERVAL)

    def run_test(self):
        """Test mode: verify everything works"""
        logger.info("=== RUNNING TESTS ===")

        # Test 1: Check Ollama connection
        logger.info("Test 1: Checking Ollama connection...")
        if not self.check_ollama_status():
            logger.error("❌ Ollama connection test FAILED")
            return False
        logger.info("✓ Ollama connection test PASSED")

        # Test 2: Generate a simple response
        logger.info("Test 2: Generating test response...")
        test_prompt = "Say 'Hello from Prison Architect AI!' in one sentence."
        response = self.generate_response(test_prompt)

        if response:
            logger.info(f"✓ Generation test PASSED: {response}")
        else:
            logger.error("❌ Generation test FAILED")
            return False

        # Test 3: Test decision making
        logger.info("Test 3: Testing decision making...")
        test_context = {
            'entity': {
                'id': 1,
                'type': 'Prisoner',
                'personality': 'The Alpha',
                'mood': 'confident',
                'currentAction': 'idle'
            },
            'nearby': [
                {'type': 'Prisoner', 'personality': 'The Follower', 'distance': 5.0}
            ]
        }

        test_request = {
            'type': 'decision',
            'context': test_context
        }

        result = self.process_request(test_request)

        if result.get('success'):
            logger.info(f"✓ Decision test PASSED")
            logger.info(f"  Action: {result['data'].get('action')}")
            logger.info(f"  Thought: {result['data'].get('thought')}")
        else:
            logger.error("❌ Decision test FAILED")
            return False

        logger.info("\n=== ALL TESTS PASSED ===")
        logger.info("The bridge is ready to use!")
        return True


def main():
    parser = argparse.ArgumentParser(description='Prison Architect AI Bridge')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Ollama model to use')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()

    bridge = OllamaBridge(model=args.model, debug=args.debug)

    if args.test:
        # Run tests
        success = bridge.run_test()
        sys.exit(0 if success else 1)
    else:
        # Check Ollama first
        if not bridge.check_ollama_status():
            logger.error("Ollama is not ready. Please start Ollama and try again.")
            sys.exit(1)

        # Start monitoring
        logger.info("Bridge is ready! Waiting for requests from Prison Architect...")
        bridge.monitor_requests()


if __name__ == '__main__':
    main()
