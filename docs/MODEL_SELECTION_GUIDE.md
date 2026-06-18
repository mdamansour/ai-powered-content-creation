# Model Selection Guide

## Overview

The AI Educational Content Creator now supports **dynamic model selection**, automatically fetching available models from Google's API based on your API key. This ensures you always have access to the latest models without manual updates.

## How It Works

The system uses Google's `genai.list_models()` API to:
- ✅ Fetch all available models in real-time
- ✅ Display current capabilities and token limits
- ✅ Show only models you have access to
- ✅ Automatically detect new models as Google releases them

## Available Models

Models are fetched dynamically from Google's API. The exact list depends on your API key's access level. Common models include:

### Flash Models (Fast & Efficient)
- **Best For**: Research, script generation, quick tasks
- **Typical Token Limits**: 8,000-32,000 input tokens
- **Speed**: ⚡ Very Fast
- **Cost**: 💰 Low

**Common Flash Models**:
- `gemini-1.5-flash`
- `gemini-1.5-flash-latest`
- `gemini-1.5-flash-8b`

**Use Cases**:
- Initial topic research
- Script generation
- Quick content iterations
- Real-time feedback

### Pro Models (High Quality)
- **Best For**: Complex analysis, detailed scenarios, comprehensive content
- **Typical Token Limits**: 32,000-128,000 input tokens
- **Speed**: 🐢 Moderate
- **Cost**: 💰💰 Higher

**Common Pro Models**:
- `gemini-1.5-pro`
- `gemini-1.5-pro-latest`
- `gemini-2.0-flash-exp` (experimental)

**Use Cases**:
- Detailed scenario design
- Complex mathematical explanations
- Multi-step problem solving
- Comprehensive content analysis

### Legacy Models
- **Best For**: Stable production environments
- **Note**: May have lower token limits

**Common Legacy Models**:
- `gemini-1.0-pro`
- `gemini-pro`

## Viewing Available Models

To see which models are available with your API key:

1. Go to **Settings → Model Selection**
2. The system will automatically fetch and display all available models
3. Each model shows:
   - Model ID and display name
   - Description and capabilities
   - Input/output token limits
   - Supported generation methods
   - Recommended use cases

## How to Select Models

### 1. In Settings (Default Model)

Navigate to **Settings → Model Selection** to:
- View all available models
- See model capabilities and recommendations
- Set a default model for all tasks

```
Settings → Model Selection → Select Model → Set as Default
```

### 2. Per-Task Selection (Programmatic)

When implementing content generation features, use the `ModelSelector` utility:

```python
from utils.model_selector import ModelSelector

# Get recommended engine for research
engine = ModelSelector.get_engine_for_task("research")

# Use specific model
engine = ModelSelector.get_engine_for_task("scenario", custom_model="gemini-1.5-pro-latest")

# Get model recommendations
recommended = ModelSelector.recommend_model("script")
```

### 3. Dynamic Switching

Switch models during runtime:

```python
from core.ai_engine import AIEngine

engine = AIEngine()

# Switch to Pro for complex task
engine.switch_model("gemini-1.5-pro-latest")
result = await engine.generate_scenario(concept, duration)

# Switch back to Flash for quick task
engine.switch_model("gemini-1.5-flash-latest")
script = await engine.generate_script(scene)
```

## Task-Specific Recommendations

### Research Phase
**Recommended**: Gemini 1.5 Flash
- Fast topic expansion
- Quick concept identification
- Efficient for iterative refinement

### Scenario Design
**Recommended**: Gemini 1.5 Pro
- Complex visualization planning
- Multi-scene coordination
- Detailed animation descriptions

### Script Generation
**Recommended**: Gemini 1.5 Flash
- Quick narration generation
- Good for conversational tone
- Fast iteration cycles

### Complex Analysis
**Recommended**: Gemini 1.5 Pro
- Deep mathematical reasoning
- Multi-step problem solving
- Comprehensive explanations

## Best Practices

### 1. Start Fast, Go Deep
```
Research (Flash) → Validate → Scenario (Pro) → Script (Flash)
```

### 2. Cost Optimization
- Use Flash for drafts and iterations
- Use Pro for final, detailed content
- Monitor token usage

### 3. Quality vs Speed
- **Speed Priority**: Use Flash throughout
- **Quality Priority**: Use Pro for critical sections
- **Balanced**: Flash for research/scripts, Pro for scenarios

### 4. Token Management
- Flash: 8K tokens = ~6,000 words
- Pro: 32K tokens = ~24,000 words
- Plan content accordingly

## Model Selection Workflow

```
┌─────────────────────────────────────────┐
│  1. Configure API Key                   │
│     Settings → API Configuration        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  2. View Available Models               │
│     Settings → Model Selection          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  3. Set Default Model (Optional)        │
│     Choose based on typical use case    │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  4. Use Task-Specific Models            │
│     System auto-recommends per task     │
└─────────────────────────────────────────┘
```

## API Integration

### Checking Available Models (Dynamic)

```python
from core.ai_engine import GeminiModelRegistry
from config.api_keys import APIConfig

# Fetch models dynamically from Google's API
api_key = APIConfig.get_api_key("gemini")
models = GeminiModelRegistry.get_available_models(api_key)

for model in models:
    print(f"{model['name']}: {model['description']}")
    print(f"  Input Tokens: {model['input_token_limit']:,}")
    print(f"  Output Tokens: {model['output_token_limit']:,}")
    print(f"  Best For: {', '.join(model['best_for'])}")
```

### Getting Model Information (Dynamic)

```python
# Fetch specific model info from API
info = GeminiModelRegistry.get_model_info("gemini-1.5-flash-latest", api_key)
if info:
    print(f"Input Tokens: {info['input_token_limit']:,}")
    print(f"Output Tokens: {info['output_token_limit']:,}")
    print(f"Best For: {', '.join(info['best_for'])}")
```

### Model Recommendations (Dynamic)

```python
# Get recommendation based on available models
research_model = GeminiModelRegistry.recommend_model("research", api_key)
scenario_model = GeminiModelRegistry.recommend_model("scenario", api_key)
script_model = GeminiModelRegistry.recommend_model("scripts", api_key)

print(f"Recommended for research: {research_model}")
```

## Troubleshooting

### Model Not Available
**Problem**: Selected model doesn't appear in list
**Solution**:
- Verify API key has access to the model
- Check internet connection
- Refresh the Settings → Model Selection page
- Your API key may not have access to certain experimental models

### Performance Issues
**Problem**: Model responses are slow
**Solution**:
- Switch to Flash model for faster responses
- Reduce max_tokens setting
- Check network connection

### Quality Issues
**Problem**: Generated content lacks detail
**Solution**:
- Switch to Pro model for complex tasks
- Increase temperature setting (0.7-0.9)
- Provide more detailed prompts

### Token Limit Errors
**Problem**: Content exceeds token limit
**Solution**:
- Switch to Pro model (32K tokens)
- Break content into smaller chunks
- Reduce prompt complexity

## Advanced Features

### Custom Model Configuration

Edit `config/settings.py` to customize default model behavior:

```python
class AISettings(BaseModel):
    provider: str = "gemini"
    model: str = "gemini-1.5-flash-latest"  # Default model
    temperature: float = 0.7  # Creativity (0.0-1.0)
    max_tokens: int = 8000  # Response length
```

### Dynamic Model Detection

The system automatically detects:
- ✅ New models as Google releases them
- ✅ Model capabilities (vision, code, etc.)
- ✅ Token limits from API metadata
- ✅ Supported generation methods

No manual updates needed!

## FAQ

**Q: How often are models updated?**
A: Models are fetched in real-time from Google's API, so you always see the latest available models.

**Q: Can I use different models for different projects?**
A: Yes, model selection is per-session. Each project can use different models.

**Q: Does model selection affect saved projects?**
A: No, projects store content, not model choices. You can regenerate with any model.

**Q: Which model is most cost-effective?**
A: Flash models generally offer the best balance of speed, quality, and cost.

**Q: Can I switch models mid-project?**
A: Yes, you can switch models at any stage of content creation.

**Q: Why don't I see certain models?**
A: Model availability depends on your API key's access level. Some experimental models may require special access.

**Q: Are model recommendations mandatory?**
A: No, recommendations are suggestions based on model names and capabilities. You can choose any available model.

## Support

For issues or questions about model selection:
- Check this guide first
- Review TECHNICAL_SPECIFICATION.md
- Open a GitHub issue
- Contact support

---

**Last Updated**: 2026-06-18
**Version**: 0.1.0

Made with ❤️ for educators worldwide