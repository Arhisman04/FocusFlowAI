from services.ai_service import generate_ai

from services.conversation_engine import (
    detect_conversation_mode
)

from services.tone_engine import (
    get_tone_prompt
)

from services.response_engine import (
    detect_response_length,
    get_response_style
)

from services.personality_engine import (
    get_personality_style
)

from services.memory_engine import (
    summarize_memory,
    get_memory_context
)


def ask_ai(user_input, mode="chat"):

    # Detect conversation behavior
    conversation_mode = detect_conversation_mode(user_input)

    # Detect response sizing
    response_length = detect_response_length(user_input)

    # Generate adaptive tone
    tone_prompt = get_tone_prompt(conversation_mode)

    # Generate personality behavior
    personality_style = get_personality_style(
        conversation_mode
    )

    # Generate adaptive response style
    response_style = get_response_style(
        response_length
    )

    # Inject memory context
    memory_context = get_memory_context()

    # Enhanced input
    enhanced_input = f"""

{memory_context}

Current User Message:
{user_input}
"""

    # =========================
    # STUDY PLAN MODE
    # =========================

    if mode == "plan":

        prompt = f"""
You are FocusFlowAI —
an adaptive AI academic strategist.

You are:
- intelligent
- emotionally aware
- highly adaptive
- practical
- conversational
- human-like

{tone_prompt}

{personality_style}

{response_style}

Student Input:
{enhanced_input}

Generate:

1. Situation Analysis
2. Biggest Problem
3. Recovery Strategy
4. Study Plan
5. Revision Optimization
6. Burnout Prevention

Rules:
- avoid robotic wording
- avoid generic motivation
- prioritize realistic recovery
- optimize marks vs effort
- adapt based on stress and burnout
- sound natural and perceptive
- keep formatting clean
- make the student feel understood
"""

        ai_reply = generate_ai(prompt)

    # =========================
    # NORMAL CHAT MODE
    # =========================

    else:

        prompt = f"""
You are FocusFlowAI.

You are:
- intelligent
- emotionally aware
- adaptive
- conversational
- human-like
- perceptive

You speak like a highly intelligent human mentor.

{tone_prompt}

{personality_style}

{response_style}

Memory Context:
{memory_context}

Student Message:
{user_input}

Rules:
- sound natural
- avoid robotic wording
- avoid repetitive structures
- adapt conversational pacing naturally
- do not overexplain simple messages
- vary sentence structure naturally
- avoid sounding like a productivity article
- speak with warmth and realism
- prioritize clarity and emotional intelligence
- sound emotionally aware but not fake
- talk like a real perceptive human
"""

        ai_reply = generate_ai(prompt)

    # Update memory after reply
    summarize_memory(user_input, ai_reply)

    return ai_reply