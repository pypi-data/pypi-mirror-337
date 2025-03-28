# SynapseGraph

SynapseGraph is a graph-based AI system for dynamic knowledge representation with temporal awareness. It models beliefs, opinions, and their relationships while automatically handling confidence decay, conflict resolution, and uncertainty management.

## 🌟 Vision

SynapseGraph creates a real-time, self-updating knowledge graph that continuously learns, refines, and evolves its understanding over time. It builds a foundation for more human-like reasoning in AI systems by implementing belief formation, opinion synthesis, and dynamic memory management with temporal dimensions. Unlike traditional static knowledge bases, SynapseGraph adapts and evolves based on new information.

## 📑 Table of Contents

-   [Installation](#-installation)
-   [Quick Start](#-quick-start)
-   [Core Concepts](#-core-concepts)
-   [API Reference](#-api-reference)
-   [Contributing](#-contributing)
-   [License](#-license)

## 🌍 Why SynapseGraph?

Traditional knowledge bases are static repositories of information that don't evolve organically or handle uncertainty well. SynapseGraph addresses these limitations by:

-   **Dynamic Knowledge Representation**: Forms and updates beliefs with confidence levels rather than static facts
-   **Temporal Awareness**: Applies time-based decay to model how knowledge relevance changes over time
-   **Uncertainty Handling**: Explicitly models confidence and clarity for all knowledge
-   **Contradiction Resolution**: Detects and manages conflicting information automatically
-   **Opinion Synthesis**: Generates reasoned perspectives based on underlying beliefs

## 🚀 Key Use Cases

SynapseGraph is designed to enhance AI applications requiring sophisticated knowledge management:

1. **Research and Analysis Systems** - Track evolving scientific understanding and conflicting evidence across domains
2. **Decision Support Tools** - Provide nuanced information with confidence measures for business or policy decisions
3. **Content Understanding Engines** - Process multiple information sources with competing narratives and track changes over time
4. **Advanced Conversational Systems** - Build assistants that maintain a coherent and evolving understanding of domains
5. **Educational AI** - Create systems that can represent multiple perspectives on complex topics with appropriate nuance

## 🔑 Features

-   **Dynamic Knowledge Graph**: Store, query, and update interconnected knowledge using Neo4j
-   **Temporal Intelligence**: Automatic confidence decay based on configurable time horizons
-   **Uncertainty Management**: Track confidence and clarity levels for all knowledge
-   **Conflict Detection**: Identify and resolve contradictory information
-   **LLM Integration**: Combine structured knowledge with language model capabilities
-   **Opinion Formation**: Synthesize reasoned perspectives from underlying beliefs
-   **Extensible Architecture**: Modular design enabling custom processing pipelines

## 📦 Installation

### Prerequisites

-   Python 3.8+
-   Neo4j 4.4+ (local or cloud instance)
-   Poetry (recommended for dependency management)
-   OpenAI API key (or other supported LLM provider)

### Setup

1. Install the package:

    ```bash
    pip install synapsegraph-lib
    ```

    For development:

    ```bash
    git clone https://github.com/thienlnam/SynapseGraph.git
    cd SynapseGraph
    poetry install
    ```

2. Set up environment variables (create a `.env` file):

    ```
    NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=your_password
    NEO4J_DATABASE=neo4j

    # LLM Configuration
    OPENAI_API_KEY=your-openai-api-key
    LLM_PROVIDER=openai
    LLM_MODEL=gpt-4o
    LLM_TEMPERATURE=0.7

    # Configuration
    MIN_CONFIDENCE_THRESHOLD=0.3
    OPINION_RESISTANCE_FACTOR=0.8
    CONFIDENCE_DECAY_RATE=0.05
    DEFAULT_SOURCE_TRUST=0.5
    CONTRADICTION_THRESHOLD=0.7
    ```

## 🔄 Quick Start

```python
import os
from dotenv import load_dotenv
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.core.synapse_graph import SynapseGraph
from synapsegraph_lib.ingestion.ingestor import UserInputIngestor, FileIngestor
from synapsegraph_lib.core.config import SourceType

# Load environment variables
load_dotenv()

# Initialize database connection
db = Neo4jConnection(
    uri=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# Initialize SynapseGraph
synapse = SynapseGraph(db)

# Ingest content using an ingestor
ingestor = UserInputIngestor(db)
ingestor.ingest_user_input(
    "Climate change is accelerating, with global temperatures rising significantly in the past decade.",
    user_id="user123",
)

# Query for knowledge about a topic
knowledge = synapse.get_knowledge_by_topic("climate change", limit=10)
for belief in knowledge["beliefs"]:
    print(f"Belief: {belief.statement} (confidence: {belief.confidence:.2f})")

# Search the knowledge graph semantically
search_results = synapse.search_knowledge("global warming impact", limit=5)

# Get a synthesized opinion
opinion = synapse.synthesize_opinion(topic="climate change")
if opinion:
    print(f"Opinion: {opinion.statement}")
    print(f"Stance: {opinion.stance.value}, Confidence: {opinion.confidence:.2f}")

# Check opinion balance (bias detection)
balance = synapse.balance_monitor.analyze_topic_balance(synapse.db, "climate change")
if balance.get("is_biased"):
    print(f"Topic is biased toward {balance['dominant_stance']} stance")

# Detect and resolve conflicts
conflicts = synapse.resolve_conflicts("climate change")
print(f"Resolved {len(conflicts.get('resolutions', []))} conflicts")

# Simulate the passage of time (confidence decay)
decay_results = synapse.apply_temporal_decay(days=90)
print(f"Updated {decay_results.get('updated_beliefs', 0)} beliefs")
```

## 🧪 Running a Test Workflow

### Prerequisites

1. Make sure Neo4j is running and accessible
2. Ensure your `.env` file is configured properly (see [Setup](#-installation))
3. Make sure Poetry is installed

## 🧠 Core Concepts

SynapseGraph implements a multi-layered architecture for knowledge representation:

### Knowledge Components

-   **Beliefs**: Factual statements with confidence and sources
-   **Opinions**: Reasoned perspectives derived from beliefs, with stance and clarity
-   **Entities**: People, organizations, concepts, or other named elements
-   **Events**: Time-bound occurrences with associated beliefs
-   **Sources**: Origins of information with trust metrics

### Key Algorithms

1. **Bayesian-Style Belief Updating**

    - Incrementally updates belief confidence based on new evidence
    - Cross-validates high-impact updates and manages speculative beliefs

2. **Opinion Synthesis**

    - Forms nuanced opinions through structured reasoning
    - Applies domain-specific frameworks and weights beliefs by relevance

3. **Temporal Management**

    - Applies time-based decay to model how knowledge relevance changes
    - Adjusts decay rates based on knowledge domain and time horizon

4. **Conflict Resolution**
    - Detects logical and factual contradictions in the knowledge graph
    - Resolves conflicts through automated methods or human input

## 📊 System Architecture

SynapseGraph consists of these primary modules:

-   **Core**: Base models, database connection, and configuration
-   **Extraction**: Knowledge extraction from text sources
-   **Synthesis**: Opinion formation and reasoning processes
-   **Temporal**: Time-based confidence decay and relevance scoring
-   **Integrity**: Conflict detection and resolution mechanisms
-   **Utilities**: Entity resolution, embedding functions, and helpers

## 🛠️ Development

### Project Structure

```
SynapseGraph/
├── src/
│   ├── core/           # Core models and database connections
│   ├── extraction/     # Knowledge extraction from text
│   ├── synthesis/      # Opinion formation and reasoning
│   ├── temporal/       # Temporal knowledge management
│   ├── integrity/      # Conflict detection and resolution
│   ├── utils/          # Utility functions
│   └── tests/          # Test suite
├── scripts/            # Utility scripts and CLI tools
```

For usage examples and demonstrations, see the CLI documentation in `scripts/cli/README.md`.

### Running Tests

```bash
poetry run pytest
```

Or with coverage:

```bash
poetry run pytest --cov=src
```

## 🔍 Troubleshooting

### Common Issues

-   **Database Connection Problems**: Verify your Neo4j credentials and ensure the database is running
-   **API Key Issues**: Check that your LLM provider API key is correctly set in the environment
-   **Dependencies**: Ensure all required packages are installed in your environment

## 🗺️ Roadmap

1. **Advanced Entity Resolution** - More sophisticated entity disambiguation and merging
2. **Multimodal Knowledge Extraction** - Support for images, audio, and video sources
3. **Active Learning Integration** - Targeted human feedback for high-uncertainty areas
4. **Distributed Graph Support** - Scaling to multiple database instances for larger knowledge graphs
5. **Customizable Epistemological Frameworks** - Domain-specific reasoning approaches
6. **Enhanced Visualization Tools** - Better interfaces for exploring the knowledge graph
7. **Zero-shot Inference Engine** - Reasoning about beliefs without explicit statements

## 🤝 Contributing

Contributions are welcome!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
