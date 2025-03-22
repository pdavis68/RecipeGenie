import json
import litellm
from typing import Dict, Any, List, Optional

class RecipeGenerator:
    def __init__(self, config: Dict[str, Any]):
        """Initialize the recipe generator with configuration"""
        self.config = config
        self.setup_llm()
    
    def setup_llm(self):
        """Set up the LLM client based on configuration"""
        # Configure LiteLLM with API keys from config
        if 'api_key' in self.config:
            litellm.api_key = self.config['api_key']
        
        # Set default model if specified
        model_name = self.config.get('model', 'gpt-3.5-turbo')
        
        # For Claude models, we need to prefix with 'anthropic/'
        # Handle specific Claude model versions correctly
        if model_name.startswith('claude'):
            # Claude 3.5 Sonnet is the correct model name
            if 'claude-3-7-sonnet' in model_name or 'claude-3.5' in model_name:
                self.model = "anthropic/claude-3-5-sonnet-20240620"
            # Claude 3 Opus
            elif 'claude-3-opus' in model_name:
                self.model = "anthropic/claude-3-opus-20240229"
            # Claude 3 Sonnet
            elif 'claude-3-sonnet' in model_name:
                self.model = "anthropic/claude-3-sonnet-20240229"
            # Claude 3 Haiku
            elif 'claude-3-haiku' in model_name:
                self.model = "anthropic/claude-3-haiku-20240307"
            # Default to Claude 3 Sonnet if unspecified version
            else:
                self.model = "anthropic/claude-3-sonnet-20240229"
        else:
            self.model = model_name
        
        # Set any additional LiteLLM configuration
        if 'litellm_config' in self.config:
            for key, value in self.config['litellm_config'].items():
                setattr(litellm, key, value)
    
    def generate_recipe(self, cuisine: str, centerpiece: str, calories: int, 
                        servings: int, prep_time: int, additional_info: str) -> Dict[str, Any]:
        """Generate a recipe using the configured LLM"""
        # Construct the prompt
        prompt = self._build_prompt(cuisine, centerpiece, calories, servings, prep_time, additional_info)
        
        try:
            # Call the LLM
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2500
            )
        except Exception as e:
            print(f"LiteLLM error with model '{self.model}': {str(e)}")
            raise ValueError(f"Failed to generate recipe with model '{self.model}': {str(e)}")
        
        # Extract and parse the response
        response_text = response.choices[0].message.content
        
        # Find the JSON part of the response
        try:
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                recipe_data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
            
            # Validate the recipe data
            self._validate_recipe_data(recipe_data)
            
            return recipe_data
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse recipe data: {str(e)}")
    
    def _build_prompt(self, cuisine: str, centerpiece: str, calories: int, 
                     servings: int, prep_time: int, additional_info: str) -> str:
        """Build the prompt for the LLM"""
        prompt = """
You are an expert recipe developer. Generate a high-quality recipe in JSON format based on the following parameters:

-   Cuisine: **{cuisine}**
-   Main Ingredient: **{centerpiece}**
-   Maximum Calories per Serving (approx): **{calories}**
-   Number of Servings: **{servings}**
-   Maximum Prep Time: **{prep_time}** minutes
-   Additional Information: **{additional_info}**

The recipe should include:

1.  A title that reflects the cuisine and main ingredient.
2.  A short description of the dish.
3.  A list of ingredients with precise measurements.
4.  Step-by-step cooking instructions that are clear and concise.
5.  Nutritional information, including approximate calories per serving, protein, fats, and carbohydrates.

Ensure the output is **formatted as valid JSON**. Follow this exact structure:

```
{{
  "title": "Example Dish Name",
  "description": "A brief, enticing description of the dish.",
  "cuisine": "{cuisine}",
  "servings": {servings},
  "calories_per_serving": {calories},
  "prep_time_minutes": 20,
  "cook_time_minutes": 30,
  "ingredients": [
    {{"name": "Ingredient 1", "amount": "1 cup"}},
    {{"name": "Ingredient 2", "amount": "2 tbsp"}}
  ],
  "instructions": [
    "Step 1: Detailed cooking instruction.",
    "Step 2: Next step in preparation."
  ],
  "nutrition": {{
    "calories": {calories},
    "protein_g": 0,
    "fat_g": 0,
    "carbohydrates_g": 0
  }}
}}
```

Generate **a realistic and delicious recipe** while maintaining the requested calorie target.
"""
        # Format the prompt with the user's inputs
        return prompt.format(
            cuisine=cuisine,
            centerpiece=centerpiece,
            calories=calories,
            servings=servings,
            prep_time=prep_time,
            additional_info=additional_info
        )
    
    def _validate_recipe_data(self, recipe_data: Dict[str, Any]) -> None:
        """Validate that the recipe data has all required fields"""
        required_fields = [
            "title", "description", "cuisine", "servings", "calories_per_serving",
            "ingredients", "instructions", "nutrition", "prep_time_minutes", "cook_time_minutes"
        ]
        
        for field in required_fields:
            if field not in recipe_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate ingredients
        if not isinstance(recipe_data["ingredients"], list):
            raise ValueError("Ingredients must be a list")
        
        for ingredient in recipe_data["ingredients"]:
            if not isinstance(ingredient, dict) or "name" not in ingredient or "amount" not in ingredient:
                raise ValueError("Each ingredient must have 'name' and 'amount'")
        
        # Validate instructions
        if not isinstance(recipe_data["instructions"], list):
            raise ValueError("Instructions must be a list")
        
        # Validate nutrition
        nutrition = recipe_data["nutrition"]
        required_nutrition = ["calories", "protein_g", "fat_g", "carbohydrates_g"]
        
        for field in required_nutrition:
            if field not in nutrition:
                raise ValueError(f"Missing nutrition field: {field}")
