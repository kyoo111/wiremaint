"""
Managed Agents Team Setup for AI Daily Report
Agent Team Configuration and Management
"""

import os
import json
import yaml
from typing import Optional
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def load_agent_config(config_path: str = "agents_config.yaml") -> dict:
    """Load agent configuration from YAML file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_agents(config: dict) -> dict:
    """Create all agent instances from configuration."""
    agents_config = config["agents"]
    created_agents = {}

    print("🚀 Creating Agent Team...\n")

    # Create individual agents (without coordinator)
    for agent_name, agent_config in agents_config.items():
        if agent_name == "coordinator":
            continue  # Handle coordinator separately

        print(f"📌 Creating {agent_config['name']}...")

        # Convert tools format
        tools = []
        if "tools" in agent_config:
            for tool in agent_config["tools"]:
                if isinstance(tool, dict):
                    tools.append(tool)
                else:
                    tools.append({"type": tool})

        # Create agent
        agent = client.beta.agents.create(
            name=agent_config["name"],
            model=agent_config["model"],
            system=agent_config["system"],
            tools=tools if tools else [{"type": "agent_toolset_20260401"}],
            description=f"Agent for {agent_name.replace('_', ' ')} task",
        )

        created_agents[agent_name] = agent
        print(f"   ✅ Created: {agent.id}\n")

    return created_agents


def create_coordinator(config: dict, agents: dict) -> dict:
    """Create coordinator agent with multiagent configuration."""
    coordinator_config = config["agents"]["coordinator"]

    print("🎯 Creating Coordinator Agent with Multiagent Setup...\n")

    # Build roster of agents for the coordinator
    roster = []
    for agent_name in coordinator_config["multiagent"]["agents"]:
        if agent_name == "self":
            roster.append({"type": "self"})
        elif agent_name in agents:
            roster.append(agents[agent_name].id)

    # Create coordinator agent
    coordinator = client.beta.agents.create(
        name=coordinator_config["name"],
        model=coordinator_config["model"],
        system=coordinator_config["system"],
        tools=coordinator_config["tools"],
        description="Main orchestrator for AI daily report generation",
        multiagent={
            "type": "coordinator",
            "agents": roster,
        },
    )

    print(f"✅ Coordinator Created: {coordinator.id}\n")
    return {"coordinator": coordinator}


def create_environment(config: dict) -> dict:
    """Create or get environment for the agent team."""
    env_config = config["environment"]

    print("🔧 Setting up Environment...\n")

    environment = client.beta.environments.create(
        name=env_config["name"],
        config=env_config["config"],
    )

    print(f"✅ Environment Created: {environment.id}\n")
    return environment


def save_agent_config(agents: dict, coordinator: dict, environment: dict):
    """Save created agent and environment IDs to a config file."""
    config_data = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "environment_id": environment.id,
        "agents": {
            name: {
                "id": agent.id,
                "version": agent.version,
                "model": agent.model,
            }
            for name, agent in agents.items()
        },
        "coordinator": {
            "id": coordinator["coordinator"].id,
            "version": coordinator["coordinator"].version,
            "model": coordinator["coordinator"].model,
        },
    }

    # Save to JSON
    with open(".agent_team_config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    print("📁 Agent Team Configuration saved to .agent_team_config.json\n")
    return config_data


def setup_agent_team():
    """Complete agent team setup process."""
    print("=" * 60)
    print("AI Daily Report - Agent Team Setup")
    print("=" * 60 + "\n")

    # Load configuration
    config = load_agent_config()

    # Create environment
    environment = create_environment(config)

    # Create individual agents
    agents = create_agents(config)

    # Create coordinator with multiagent setup
    coordinator = create_coordinator(config, agents)

    # Save configuration
    agent_config_data = save_agent_config(agents, coordinator, environment)

    print("=" * 60)
    print("✨ Agent Team Setup Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print(f"   Environment ID: {environment.id}")
    print(f"   Agents Created: {len(agents)}")
    print(f"   Coordinator: {coordinator['coordinator'].id}")
    print("\n💾 Saved to: .agent_team_config.json")

    return agent_config_data


def run_agent_team(task: str, agent_config: Optional[dict] = None) -> str:
    """Run the agent team with a specific task."""
    if agent_config is None:
        # Load saved configuration
        if not os.path.exists(".agent_team_config.json"):
            print("❌ Agent team not configured. Run setup_agent_team() first.")
            return ""

        with open(".agent_team_config.json", "r", encoding="utf-8") as f:
            agent_config = json.load(f)

    environment_id = agent_config["environment_id"]
    coordinator_id = agent_config["coordinator"]["id"]

    print("\n🚀 Running Agent Team...\n")

    # Create session with coordinator agent
    session = client.beta.sessions.create(
        agent={"type": "agent", "id": coordinator_id},
        environment_id=environment_id,
        title=f"AI Report - {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}",
    )

    print(f"📊 Session Created: {session.id}\n")

    # Send task to coordinator
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": task}]}],
    )

    # Stream responses
    print("📝 Agent Team Processing:\n")
    all_responses = []

    with client.beta.sessions.events.stream(session_id=session.id) as stream:
        for event in stream:
            if event.type == "agent.message":
                for block in event.content:
                    if hasattr(block, "text"):
                        print(block.text)
                        all_responses.append(block.text)
            elif event.type == "session.status_idle":
                print("\n✅ Agent Team completed processing")
                break
            elif event.type == "session.status_terminated":
                print("\n⚠️ Session terminated")
                break

    return "\n".join(all_responses)


if __name__ == "__main__":
    # Setup agent team
    agent_config = setup_agent_team()

    # Run agent team with a sample task
    print("\n" + "=" * 60)
    print("Running Sample Task...")
    print("=" * 60)

    task = """
    오늘 AI 일일 리포트를 생성해주세요:
    1. 최신 AI 동향을 수집하여 브리핑을 생성해주세요
    2. 생성된 브리핑의 품질을 검증해주세요
    3. 문제가 있으면 GitHub 이슈로 등록해주세요
    4. 열린 이슈들을 처리해주세요
    5. 프로젝트 문서를 최적화해주세요
    """

    result = run_agent_team(task, agent_config)
