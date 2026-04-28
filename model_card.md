# Model Card: PetFlow

## Overview
PetFlow is a pet care scheduling system that helps users organize tasks, detect scheduling conflicts, and receive simple care suggestions. The system uses rule-based logic and a small dataset of pet care guidelines to support decision-making.

## Intended Use
PetFlow is designed to help pet owners manage daily care routines and stay organized. It is intended for general task planning and should not be used as a replacement for professional veterinary advice.

## Limitations
- The retrieval system relies on a small predefined dataset, so it may not cover all possible pet care situations.
- The scheduler only detects exact time conflicts and does not account for overlapping durations.
- The system assumes user input is mostly accurate beyond basic validation.

## Potential Misuse
Users may rely too heavily on the system for pet care decisions. To reduce this risk, PetFlow provides general guidelines rather than authoritative or medical advice.

## Biases
The system may reflect bias due to its limited dataset of pet care rules. Since the data is manually defined and small in scope, it may not represent all pet types or care practices.

## Testing and Reliability
- Tested task creation with valid and invalid inputs
- Verified conflict detection using overlapping task times
- Tested retrieval system with known and unknown tasks
- Added guardrails to prevent empty inputs and incorrect time formats

Most tests passed successfully, and the system behaved consistently during testing.

## AI Collaboration Reflection

**Helpful use of AI:**
AI was useful in suggesting how to structure the retrieval system and improve conflict explanations. It helped break down the problem into smaller components and made it easier to implement new features.

**Limitations of AI:**
Some AI suggestions added unnecessary complexity or did not fully match the project’s design. I had to adjust and simplify those suggestions to better fit the system.

This process showed that AI can be a helpful tool for generating ideas, but it still requires human judgment to decide what works best.