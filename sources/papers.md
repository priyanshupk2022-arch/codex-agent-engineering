# Academic Research & Empirical Benchmarks

This document records peer-reviewed academic research and technical reports forming the methodological foundation for Codex Agent Engineering benchmarks and verification protocols.

## 1. SWE-bench & SWE-agent: Repository-Level Issue Resolution
- **Source Identifier**: `PAPER-SWE-001`
- **Title**: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- **Authors**: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan (Princeton University)
- **Year**: 2024 / ICLR 2024
- **Citation Key**: `jimenez2024swebench`
- **Key Findings & Relevance to CAE**:
  - Evaluates language models on 2,294 real-world software engineering issues from Python repositories.
  - Demonstrates that pass@1 on unit tests without end-to-end regression validation yields high false-positive resolution rates.
  - Found that agents require interactive execution interfaces (bash/shell, test runners, git status inspection) rather than static code prediction to achieve non-trivial success.

## 2. SWE-agent: Agent-Computer Interfaces for Software Engineering
- **Source Identifier**: `PAPER-SWE-002`
- **Title**: SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
- **Authors**: John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan (Princeton NLP)
- **Year**: 2024
- **Citation Key**: `yang2024sweagent`
- **Key Findings & Relevance to CAE**:
  - Designed the Agent-Computer Interface (ACI), proving that tailored tool design (e.g., custom file viewers, search tools with pagination) prevents agent hallucination and context overflow.
  - Direct inspiration for CAE's Skill design and bounded tool output rules.

## 3. Reflexion: Language Agents with Verbal Reinforcement Learning
- **Source Identifier**: `PAPER-REFLEX-001`
- **Title**: Reflexion: Language Agents with Verbal Reinforcement Learning
- **Authors**: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
- **Year**: 2023 / NeurIPS 2023
- **Citation Key**: `shinn2023reflexion`
- **Key Findings & Relevance to CAE**:
  - Introduces dynamic memory and self-reflection loops where agents evaluate test feedback to correct errors iteratively.
  - Formalizes the 4-Tier Test Gate in CAE's debugging and testing workflows.

## 4. ReAct: Synergizing Reasoning and Acting in Language Models
- **Source Identifier**: `PAPER-REACT-001`
- **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
- **Authors**: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao (Princeton & Google Research)
- **Year**: 2023 / ICLR 2023
- **Citation Key**: `yao2023react`
- **Key Findings & Relevance to CAE**:
  - Interleaving reasoning traces ('thought') with task-specific actions ('act') minimizes hallucination in complex tool-use chains.
